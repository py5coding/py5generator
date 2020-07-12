import argparse
import logging
import shutil
from pathlib import Path

import pandas as pd

from generator import CodeBuilder, DocstringLibrary, CodeCopier
from generator import reference as ref
from generator import templates as templ


logging.basicConfig(format="%(asctime)s | %(levelname)s | %(message)s", level=logging.INFO)

logger = logging.getLogger(__name__)

###############################################################################
# ARGUMENT PARSING
###############################################################################


parser = argparse.ArgumentParser(description="Generate py5 library using processing jars",
                                 epilog="this is the epilog")
parser.add_argument('-r', '--repo', action='store', dest='processing_repo_dir',
                    help='location of processing code (github repository)')
parser.add_argument('-p', '--param', action='store', dest='method_parameter_names_data_file',
                    help='location of method parameter names data file created by Py5Doclet')


###############################################################################
# MAIN
###############################################################################


def generate_py5(repo_dir, method_parameter_names_data_file):
    """Generate an installable py5 library using processing jars
    """
    repo_dir = Path(repo_dir)

    logger.info('generating py5 library...')
    core_jars = list(repo_dir.glob('**/core.jar'))
    if len(core_jars) != 1:
        if core_jars:
            msg = f'more than one core.jar found in {repo_dir}'
        else:
            msg = f'core.jar not found in {repo_dir}'
        logger.critical(msg)
        raise RuntimeError(msg)
    core_jar_path = core_jars[0]

    py5_jar_path = Path('py5_jar', 'dist', 'py5.jar')
    if not py5_jar_path.exists():
        msg = f'py5 jar not found at {str(py5_jar_path)}'
        logger.critical(msg)
        raise RuntimeError(msg)
    import jnius_config
    jnius_config.set_classpath(str(py5_jar_path), str(core_jar_path))
    from jnius import autoclass, JavaStaticMethod, JavaMethod, JavaMultipleMethod, JavaStaticField, JavaField

    class_method_parameter_names_data = dict()
    with open(method_parameter_names_data_file, 'r') as f:
        for line in f.readlines():
            c, f, types, params, rettype = line.split('|')
            if c not in class_method_parameter_names_data: class_method_parameter_names_data[c] = dict()
            if f not in class_method_parameter_names_data[c]: class_method_parameter_names_data[c][f] = dict()
            if types in class_method_parameter_names_data[c][f]: raise RuntimeError('assumption violated')
            class_method_parameter_names_data[c][f][types] = (params, rettype)

    logger.info('examining Java classes')
    Py5Applet = autoclass('py5.core.Py5Applet',
                          include_protected=False, include_private=False)
    py5applet = Py5Applet()

    logger.info('loading datafile to identify included methods and fields')
    py5applet_data = pd.read_csv(Path('py5_resources', 'data', 'py5applet.csv')).fillna('').set_index('processing_name')

    all_fields_and_methods = set(py5applet_data.index)
    included_fields_namd_methods = set(py5applet_data.query("implementation_from_processing==True").index)

    code_builder = CodeBuilder(class_method_parameter_names_data['PApplet'], py5applet_data)

    ordering = {JavaStaticField: 0, JavaField: 1}
    for k, v in sorted(Py5Applet.__dict__.items(), key=lambda x: (ordering.get(type(x[1]), 2), x[0])):
        if isinstance(v, JavaStaticMethod) and k in included_fields_namd_methods:
            code_builder.code_method(k, v, True)
        elif isinstance(v, (JavaMethod, JavaMultipleMethod)) and k in included_fields_namd_methods:
            code_builder.code_method(k, v, False)
        elif isinstance(v, JavaStaticField) and k in included_fields_namd_methods:
            code_builder.code_static_constant(k, getattr(Py5Applet, k))
        elif isinstance(v, JavaField) and k in included_fields_namd_methods:
            code_builder.code_dynamic_variable(k, type(getattr(py5applet, k)).__name__)
        if k not in all_fields_and_methods and not k.startswith('_'):
            logger.warning(f'detected previously unknown {type(v).__name__} {k}')

    # add the methods in the mixin classes as functions in the __init__.py module
    mixin_dir = Path('py5_resources', 'py5_module', 'py5', 'mixins')
    for filename in mixin_dir.glob('*.py'):
        if filename.stem == '__init__':
            continue
        code_builder.code_mixin(filename)

    run_sketch_pre_run_steps = [
        templ.MODULE_PROPERTY_PRE_RUN_TEMPLATE.format(n) for n in sorted(code_builder.dynamic_variable_names)
    ]

    class_members_code = ''.join(code_builder.class_members)
    module_members_code = ''.join(code_builder.module_members)
    run_sketch_pre_run_code = ''.join(run_sketch_pre_run_steps)

    # code the result of the module's __dir__ function and __all__ variable
    py5_dir_names = code_builder.all_names | ref.EXTRA_DIR_NAMES
    # code_builder.py5_dir.extend(ref.EXTRA_DIR_NAMES)
    str_py5_dir = str(sorted(py5_dir_names, key=lambda x: x.lower()))
    # don't want import * to import the dynamic variables because they cannot be updated
    str_py5_all = str(sorted([x for x in py5_dir_names if x not in code_builder.dynamic_variable_names], key=lambda x: x.lower()))

    format_params = dict(class_members_code=class_members_code,
                         module_members_code=module_members_code,
                         run_sketch_pre_run_code=run_sketch_pre_run_code,
                         str_py5_dir=str_py5_dir,
                         str_py5_all=str_py5_all)
    docstring_library = DocstringLibrary()
    # build complete py5 module in destination directory
    dest_dir = Path('build')
    logger.info(f'building py5 in {dest_dir}')
    if dest_dir.exists():
        shutil.rmtree(dest_dir)
    for language in ['en']:  # docstring_library.languages:
        docstrings = docstring_library.docstring_dict(language)
        copier = CodeCopier(format_params, docstrings)
        if dest_dir.exists():
            shutil.rmtree(dest_dir)
        # TODO: does this work in WSL? if so, wrap in try-catch block for only that exception type
        shutil.copytree(Path('py5_resources', 'py5_module'), dest_dir, copy_function=copier)
        for jar in core_jar_path.parent.glob('*.jar'):
            shutil.copy(jar, dest_dir / 'py5' / 'jars')
        shutil.copy(py5_jar_path, dest_dir / 'py5' / 'jars')

    dest_dir.touch()

    logger.info('done!')


def main():
    args = parser.parse_args()
    generate_py5(repo_dir=args.processing_repo_dir,
                 method_parameter_names_data_file=args.method_parameter_names_data_file)


if __name__ == '__main__':
    main()
