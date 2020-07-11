import argparse
import logging
import shutil
from pathlib import Path

import pandas as pd

from generator import CodeBuilder, DocstringLibrary, CodeCopier
from generator import reference as ref


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

    method_parameter_names_data = dict()
    with open(method_parameter_names_data_file, 'r') as f:
        for line in f.readlines():
            c, f, types, params, rettype = line.split('|')
            if c not in method_parameter_names_data: method_parameter_names_data[c] = dict()
            if f not in method_parameter_names_data[c]: method_parameter_names_data[c][f] = dict()
            if types in method_parameter_names_data[c][f]: raise RuntimeError('assumption violated')
            method_parameter_names_data[c][f][types] = (params, rettype)

    logger.info('examining Java classes')
    Py5Applet = autoclass('py5.core.Py5Applet',
                          include_protected=False, include_private=False)
    py5applet = Py5Applet()

    logger.info('loading datafile to identify included methods and fields')
    py5applet_data = pd.read_csv(Path('py5_resources', 'data', 'py5applet.csv')).fillna('')
    py5_names = py5applet_data.set_index('processing_name')['py5_name']
    py5_decorators = py5applet_data.set_index('processing_name')['decorator']
    py5_special_kwargs = py5applet_data.set_index('processing_name')['special_kwargs']

    all_fields_and_methods = set(py5applet_data['processing_name'])
    included_py5applet_data = py5applet_data.query("implementation_from_processing==True and processing_name != ''")
    included_methods = set(included_py5applet_data.query("type=='method'")['processing_name'])
    included_static_methods = set(included_py5applet_data.query("type=='static method'")['processing_name'])
    included_fields = set(included_py5applet_data.query("type=='dynamic variable'")['processing_name'])
    included_static_fields = set(included_py5applet_data.query("type=='static field'")['processing_name'])

    methods = set()
    static_methods = set()
    fields = set()
    static_fields = set()

    for k, v in Py5Applet.__dict__.items():
        if isinstance(v, JavaStaticMethod) and k in included_static_methods:
            static_methods.add((k, v))
        elif isinstance(v, (JavaMethod, JavaMultipleMethod)) and k in included_methods:
            methods.add((k, v))
        elif isinstance(v, JavaStaticField) and k in included_static_fields:
            static_fields.add(k)
        elif isinstance(v, JavaField) and k in included_fields:
            fields.add(k)
        if k not in all_fields_and_methods and not k.startswith('_'):
            logger.warning(f'detected previously unknown {type(v).__name__} {k}')

    code_builder = CodeBuilder(method_parameter_names_data,
                               py5_names, py5_decorators, py5_special_kwargs)

    logger.info('coding static constants')
    code_builder.code_static_constants(static_fields, Py5Applet)

    logger.info('coding dynamic variables')
    py5_dynamic_vars, run_sketch_pre_run_steps = code_builder.code_dynamic_variables(
        fields, py5applet)

    logger.info('coding class methods')
    code_builder.code_methods(methods, False)
    code_builder.code_methods(static_methods, True)

    # add the methods in the mixin classes as functions in the __init__.py module
    mixin_dir = Path('py5_resources', 'py5_module', 'py5', 'mixins')
    for filename in mixin_dir.glob('*.py'):
        if filename.stem == '__init__':
            continue
        code_builder.code_mixin(filename)

    class_members_code = ''.join(code_builder.class_members)
    module_members_code = ''.join(code_builder.module_members)
    run_sketch_pre_run_code = ''.join(run_sketch_pre_run_steps)

    # code the result of the module's __dir__ function and __all__ variable
    code_builder.py5_dir.extend(ref.EXTRA_DIR_NAMES)
    str_py5_dir = str(sorted(code_builder.py5_dir, key=lambda x: x.lower()))
    # don't want import * to import the dynamic variables because they cannot be updated
    str_py5_all = str(sorted([x for x in code_builder.py5_dir if x not in py5_dynamic_vars], key=lambda x: x.lower()))

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
