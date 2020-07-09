import re
import argparse
import logging
import shutil
import textwrap
from string import Template
import shlex
import autopep8
from pathlib import Path
from functools import lru_cache

import pandas as pd


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
# DOCSTRINGS
###############################################################################


DOCSTRING = re.compile(r'(@@@ DOCSTRING (\w+) @@@)')
DOCSTRING_FILE_HEADER = re.compile(r"^# \w+$", re.UNICODE | re.MULTILINE)


class DocstringDict:

    INDENTING = {'class': 8, 'module': 4}

    def __init__(self, language, docstrings):
        super().__init__()
        self._language = language
        self._docstrings = docstrings

    def __getitem__(self, item):
        try:
            kind, name = item.split('_', 1)
            doc = textwrap.indent(
                self._docstrings[name],
                prefix=(' ' * DocstringDict.INDENTING.get(kind, 0))).strip()
            return doc
        except KeyError:
            return f'missing {self._language} language docstring for {name}'


class DocstringLibrary:

    def __init__(self):
        self._load_docstrings()

    def _load_docstrings(self):
        docstring_dir = Path('py5_resources', 'docstrings')
        self._docstings = {}
        for md_file in docstring_dir.glob('*.md'):
            with open(md_file, 'r') as f:
                md_contents = f.read()
            parsed_md = {k[1:].strip(): v.strip()
                         for k, v in zip(DOCSTRING_FILE_HEADER.findall(md_contents),
                                         DOCSTRING_FILE_HEADER.split(md_contents)[1:])}
            self._docstings[md_file.stem] = parsed_md

    @property
    def languages(self):
        return list(self._docstings.keys())

    def docstring_dict(self, language):
        return DocstringDict(language, self._docstings[language])


###############################################################################
# TEMPLATES
###############################################################################


METHOD_REGEX = re.compile(r'(@\w+)?\s*def (.*?)\((cls|self),?\s*(.*?)\)\s*-?>?\s*(.*?):$', re.MULTILINE | re.DOTALL)
TYPEHINT_COMMA_REGEX = re.compile(r'(\[[\w\s,]+\])')

CLASS_STATIC_FIELD_TEMPLATE = """
    {0} = {1}"""

CLASS_PROPERTY_TEMPLATE = """
    def _get_{0}(self) -> {1}:
        \"\"\"$class_{0}\"\"\"
        return self._py5applet.{2}
    {0}: {1} = property(fget=_get_{0})
"""

CLASS_METHOD_TYPEHINT_TEMPLATE = """
    @overload
    def {0}({1}) -> {2}:
        \"\"\"$class_{0}\"\"\"
        pass
"""

CLASS_METHOD_TEMPLATE = """
    {4}
    def {0}({1}, *args):
        \"\"\"$class_{0}\"\"\"
        try:
            return {2}.{3}(*args)
        except Exception as e:
            raise Py5Exception(e.__class__.__name__, str(e), '{0}', args)
"""

CLASS_METHOD_TEMPLATE_WITH_TYPEHINTS = """
    {4}
    def {0}({1}) -> {5}:
        \"\"\"$class_{0}\"\"\"
        try:
            return {2}.{3}({6})
        except Exception as e:
            raise Py5Exception(e.__class__.__name__, str(e), '{0}', [{6}])
"""

MODULE_STATIC_FIELD_TEMPLATE = """
{0} = {1}"""

MODULE_PROPERTY_TEMPLATE = """
{0}: {1} = None"""

MODULE_PROPERTY_PRE_RUN_TEMPLATE = """
        global {0}
        del {0}"""

MODULE_FUNCTION_TYPEHINT_TEMPLATE = """
@overload
def {0}({1}) -> {2}:
    \"\"\"$module_{0}\"\"\"
    pass
"""

MODULE_FUNCTION_TEMPLATE = """
def {0}(*args):
    \"\"\"$module_{0}\"\"\"
    return {1}.{0}(*args)
"""

MODULE_FUNCTION_TEMPLATE_WITH_TYPEHINTS = """
def {0}({1}) -> {3}:
    \"\"\"$module_{0}\"\"\"
    return {2}.{0}({4})
"""


###############################################################################
# REFERENCE AND LOOKUPS
###############################################################################


PAPPLET_SKIP_PARAM_TYPES = {
    'processing/core/PMatrix3D', 'processing/core/PMatrix2D',
    'processing/core/PMatrix', 'java/io/File'
}

PCONSTANT_OVERRIDES = {
    'WHITESPACE': r' \t\n\r\x0c\xa0',
    'ESC': r'\x1b',
    'RETURN': r'\r',
    'ENTER': r'\n',
    'DELETE': r'\x7f',
    'BACKSPACE': r'\x08',
    'TAB': r'\t'
}

EXTRA_DIR_NAMES = {
    'run_sketch', 'get_py5applet', 'reset_py5', 'exit_sketch',
    'autoclass', 'Py5Methods', '_Py5Applet', '_py5sketch', '_py5sketch_used',
    'prune_tracebacks', 'set_stackprinter_style', 'create_font_file'
}

JTYPE_CONVERSIONS = {
    'boolean': 'bool',
    'char': 'chr',
    'long': 'int',
    'java/lang/String': 'str',
    'java/lang/Object': 'Any',
    'processing/opengl/PShader': 'Py5Shader',
    'processing/core/PFont': 'Py5Font'
}


###############################################################################
# UTIL FUNCTIONS
###############################################################################


class CodeBuilder:

    def __init__(self, method_parameter_names_data, py5_names, py5_decorators,
                 class_members, module_members, py5_dir):
        self.method_parameter_names_data = method_parameter_names_data
        self.py5_names = py5_names
        self.py5_decorators = py5_decorators
        self.class_members = class_members
        self.module_members = module_members
        self.py5_dir = py5_dir

    def snake_case(self, name):
        name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name)
        return name.lower()

    @lru_cache(128)
    def convert_type(self, jtype: str) -> str:
        if jtype == 'void':
            return 'None'

        isarray = jtype.endswith('[]')
        jtype = jtype[:-2] if isarray else jtype
        out = JTYPE_CONVERSIONS.get(jtype, jtype.split('/')[-1])

        return f'List[{out}]' if isarray else out

    def param_annotation(self, varname: str, jtype: str) -> str:
        if jtype.endswith('...'):
            jtype = jtype[:-3]
            varname = '*' + varname

        return f'{varname}: {self.convert_type(jtype)}'

    def make_param_rettype_strs(self, fname, first_param, params, rettype):
        try:
            parameter_name_key = ','.join([p.split('/')[-1].replace('...', '[]') for p in params])
            parameter_names, _ = self.method_parameter_names_data['PApplet'][fname][parameter_name_key]
            parameter_names = [self.snake_case(p) for p in parameter_names.split(',')]
            paramstrs = [first_param] + [self.param_annotation(pn, p) for pn, p in zip(parameter_names, params)]
        except Exception:
            logger.warning(f'missing parameter names for {fname} {params}')
            paramstrs = [first_param] + [self.param_annotation(f'arg{i}', p) for i, p in enumerate(params)]
        rettypestr = self.convert_type(rettype)

        return paramstrs, rettypestr

    def code_methods(self, methods, static):
        for fname, method in sorted(methods, key=lambda x: x[0]):
            snake_name = self.py5_names[fname]
            if static:
                first_param, classobj, moduleobj, decorator = 'cls', '_Py5Applet', 'Sketch', '@classmethod'
            else:
                first_param, classobj, moduleobj, decorator = 'self', 'self._py5applet', '_py5sketch', self.py5_decorators[snake_name]
            # if there is only one method signature, create the real method with typehints
            if len(method.signatures()) == 1:
                params, rettype = method.signatures()[0]
                if PAPPLET_SKIP_PARAM_TYPES.intersection(params) or rettype in PAPPLET_SKIP_PARAM_TYPES:
                    continue
                paramstrs, rettypestr = self.make_param_rettype_strs(fname, first_param, params, rettype)
                # create the class and module code
                self.class_members.append(CLASS_METHOD_TEMPLATE_WITH_TYPEHINTS.format(
                    snake_name, ', '.join(paramstrs), classobj, fname, decorator, rettypestr,
                    ', '.join([p.split(':')[0] for p in paramstrs[1:]])))
                self.module_members.append(MODULE_FUNCTION_TEMPLATE_WITH_TYPEHINTS.format(
                    snake_name, ', '.join(paramstrs[1:]), moduleobj, rettypestr,
                    ', '.join([p.split(':')[0] for p in paramstrs[1:]])))
            else:
                # loop through the method signatures and create the typehint methods
                skipped_all = True
                for params, rettype in sorted(method.signatures(), key=lambda x: len(x[0])):
                    if PAPPLET_SKIP_PARAM_TYPES.intersection(params) or rettype in PAPPLET_SKIP_PARAM_TYPES:
                        continue
                    skipped_all = False
                    paramstrs, rettypestr = self.make_param_rettype_strs(fname, first_param, params, rettype)
                    # create the class and module typehints
                    self.class_members.append(CLASS_METHOD_TYPEHINT_TEMPLATE.format(snake_name, ', '.join(paramstrs), rettypestr))
                    self.module_members.append(MODULE_FUNCTION_TYPEHINT_TEMPLATE.format(snake_name, ', '.join(paramstrs[1:]), rettypestr))
                if skipped_all:
                    continue
                # now construct the real methods
                self.class_members.append(CLASS_METHOD_TEMPLATE.format(snake_name, first_param, classobj, fname, decorator))
                self.module_members.append(MODULE_FUNCTION_TEMPLATE.format(snake_name, moduleobj))
            self.py5_dir.append(snake_name)


class CodeCopier:

    def __init__(self, format_params, docstring_dict):
        self.format_params = format_params
        self.docstring_dict = docstring_dict

    def __call__(self, src, dest, *, follow_symlinks=True):
        logger.info(f'copying {src} to {dest}')

        with open(src, 'r') as f:
            content = f.read()

        if content.find('*** FORMAT PARAMS ***') > 0:
            content = re.sub(r'^.*DELETE$', '',
                             content.format(**self.format_params),
                             flags=re.MULTILINE | re.UNICODE)
        content = Template(content).substitute(self.docstring_dict)
        content = autopep8.fix_code(content, options={'aggressive': 2})

        with open(dest, 'w') as f:
            f.write(content)

        return dest


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
    py5_decorators = py5applet_data.set_index('py5_name')['decorator']

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

    # storage for Py5Applet members and the result of the module's __dir__ function.
    class_members = []
    module_members = []
    run_sketch_pre_run_steps = []
    py5_dir = []

    logger.info('coding static constants')
    for name in sorted(static_fields):
        if name in PCONSTANT_OVERRIDES:
            module_members.append(f'\n{name} = {shlex.quote(PCONSTANT_OVERRIDES[name])}')
        else:
            val = getattr(Py5Applet, name)
            if isinstance(val, str):
                val = f"'{val}'"
            if name == 'javaVersion':
                val = round(val, 2)
            module_members.append(MODULE_STATIC_FIELD_TEMPLATE.format(name, val))
            class_members.append(CLASS_STATIC_FIELD_TEMPLATE.format(name, val))
            py5_dir.append(name)

    logger.info('coding dynamic variables')
    py5_dynamic_vars = []
    for name in sorted(fields):
        snake_name = py5_names[name]
        var_type = (
            {'args': 'List[str]', 'g': 'PGraphics', 'recorder': 'PGraphics', 'pixels': 'List[int]'}
        ).get(name, type(getattr(py5applet, name)).__name__)
        class_members.append(CLASS_PROPERTY_TEMPLATE.format(snake_name, var_type, name))
        module_members.append(MODULE_PROPERTY_TEMPLATE.format(snake_name, var_type))
        run_sketch_pre_run_steps.append(MODULE_PROPERTY_PRE_RUN_TEMPLATE.format(snake_name))
        py5_dynamic_vars.append(snake_name)
        py5_dir.append(snake_name)

    logger.info('coding class methods')
    code_builder = CodeBuilder(method_parameter_names_data, py5_names, py5_decorators,
                               class_members, module_members, py5_dir)
    code_builder.code_methods(methods, False)
    code_builder.code_methods(static_methods, True)

    # add the methods in the mixin classes as functions in the __init__.py module
    mixin_dir = Path('py5_resources', 'py5_module', 'py5', 'mixins')
    for filename in mixin_dir.glob('*.py'):
        if filename.stem == '__init__':
            continue
        with open(filename) as f:
            code = f.read()
            code = code.split('*** BEGIN METHODS ***')[1].strip()

        module_members.append(f'\n{"#" * 78}\n# module functions from {filename.name}\n{"#" * 78}\n')
        for decorator, fname, arg0, args, rettypestr in METHOD_REGEX.findall(code):
            if fname.startswith('_'):
                continue
            elif decorator == '@overload':
                module_members.append(MODULE_FUNCTION_TYPEHINT_TEMPLATE.format(fname, args, rettypestr))
            else:
                moduleobj = 'Sketch' if arg0 == 'cls' else '_py5sketch'
                paramlist = []
                for arg in TYPEHINT_COMMA_REGEX.sub('', args).split(','):
                    paramname = arg.split(':')[0].strip()
                    if '=' in arg:
                        paramlist.append(f'{paramname}={paramname}')
                    else:
                        paramlist.append(paramname)

                params = ', '.join(paramlist)
                module_members.append(MODULE_FUNCTION_TEMPLATE_WITH_TYPEHINTS.format(
                    fname, args, moduleobj, rettypestr, params))
                py5_dir.append(fname)

    class_members_code = ''.join(class_members)
    module_members_code = ''.join(module_members)
    run_sketch_pre_run_code = ''.join(run_sketch_pre_run_steps)

    # code the result of the module's __dir__ function and __all__ variable
    py5_dir.extend(EXTRA_DIR_NAMES)
    str_py5_dir = str(sorted(py5_dir, key=lambda x: x.lower()))
    # don't want import * to import the dynamic variables because they cannot be updated
    str_py5_all = str(sorted([x for x in py5_dir if x not in py5_dynamic_vars], key=lambda x: x.lower()))

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
