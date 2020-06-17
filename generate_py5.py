import sys
import re
import argparse
import shutil
import textwrap
from string import Template
import shlex
import autopep8
from pathlib import Path
from functools import lru_cache


###############################################################################
# ARGUMENT PARSING
###############################################################################


parser = argparse.ArgumentParser(description="Generate py5 library using processing jars",
                                 epilog="this is the epilog")
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-r', '--repo', action='store', dest='processing_repo_dir',
                   help='location of processing code (github repository)')
group.add_argument('-p', '--pde', action='store', dest='processing_install_dir',
                   help='location of installed processing application (PDE)')


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
    def {0}({1}, *args, **kwargs):
        \"\"\"$class_{0}\"\"\"
        try:
            return {2}.{3}(*args, **kwargs)
        except Exception as e:
            raise Py5Exception(e.__class__.__name__, str(e), '{0}', args, kwargs)
"""

CLASS_METHOD_TEMPLATE_WITH_TYPEHINTS = """
    {4}
    def {0}({1}) -> {5}:
        \"\"\"$class_{0}\"\"\"
        try:
            return {2}.{3}({6})
        except Exception as e:
            raise Py5Exception(e.__class__.__name__, str(e), '{0}', args, kwargs)
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
def {0}(*args, **kwargs):
    \"\"\"$module_{0}\"\"\"
    return {1}.{0}(*args, **kwargs)
"""

MODULE_FUNCTION_TEMPLATE_WITH_TYPEHINTS = """
def {0}({1}) -> {3}:
    \"\"\"$module_{0}\"\"\"
    return {2}.{0}({4})
"""


###############################################################################
# REFERENCE AND LOOKUPS
###############################################################################


PAPPLET_SKIP_METHODS = {
    # main sketch methods
    'settings', 'setup', 'draw',
    # key and mouse events
    'keyPressed', 'keyTyped', 'keyReleased',
    'mouseClicked', 'mouseDragged', 'mouseMoved', 'mouseEntered',
    'mouseExited', 'mousePressed', 'mouseReleased', 'mouseWheel',
    # exit method
    'exitActual',
    # builtin python functions
    'print', 'exec', 'exit', 'str', 'set', 'map', 'sort',
    # user should use Python instead
    'append', 'arrayCopy', 'arraycopy', 'concat', 'expand', 'reverse', 'shorten',
    'splice', 'subset', 'binary', 'boolean', 'byte', 'char', 'float', 'hex',
    'int', 'unbinary', 'unhex', 'join', 'match', 'matchAll', 'nf', 'nfc', 'nfp',
    'nfs', 'split', 'splitTokens', 'trim', 'debug', 'delay', 'equals', 'println',
    'printArray',
    # user should use numpy instead
    'min', 'max', 'round', 'map', 'abs', 'pow', 'sqrt', 'ceil', 'floor', 'log',
    'exp', 'sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'atan2', 'degrees',
    'radians', 'sq', 'lerp', 'constrain', 'norm', 'mag', 'dist',
    # public methods that should be skipped
    'runSketch', 'main', 'handleDraw', 'handleSettings', 'usePy5Methods',
    'registerMethod', 'unregisterMethod',
    'showDepthWarning', 'showDepthWarningXYZ', 'showMethodWarning',
    'showVariationWarning', 'showMissingWarning',
    'checkAlpha', 'setSize', 'die',
    # methods that are missing documentation that are not a part of the framework
    'attrib', 'attribColor', 'attribNormal', 'attribPosition', 'beginPGL', 'endPGL',
    'exitCalled', 'flush', 'focusGained', 'focusLost', 'frameMoved', 'frameResized',
    'isKeyPressed', 'isLooping', 'orientation', 'sketchDisplay', 'sketchFullScreen',
    'sketchHeight', 'sketchOutputPath' 'sketchPath', 'sketchPixelDensity', 'sketchRenderer',
    'sketchSmooth', 'sketchSmooth', 'sketchWidth', 'sketchWindowColor', 'blendColor',
    # files methods that should be done in Python
    'createInput', 'createInputRaw', 'createOutput', 'createPath', 'createReader',
    'createWriter', 'dataFile', 'dataPath', 'link', 'listFiles', 'listPaths',
    'loadJSONArray', 'loadJSONObject', 'parseJSONArray', 'parseJSONObject',
    'saveJSONArray', 'saveJSONObject',
    'loadBytes', 'saveBytes', 'loadXML', 'parseXML', 'saveXML', 'launch',
    'loadStrings', 'saveStrings', 'loadTable', 'saveTable', 'saveStream',
    'saveFile', 'savePath', 'checkExtension', 'getExtension', 'desktopFile',
    'desktopPath', 'shell', 'urlDecode', 'urlEncode', 'sketchFile', 'sketchOutputStream',
    # parsing methods that should be done in Python
    'parseBoolean', 'parseByte', 'parseChar', 'parseInt', 'parseFloat',
    # internal methods
    'postEvent', 'style', 'hideMenuBar', 'saveViaImageIO',
    'getClass', 'hashCode', 'wait', 'notify', 'notifyAll', 'toString',
    'setAndUpdatePixels', 'loadAndGetPixels'
}

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

DEPRECATED = {
    'firstMouse', 'mouseEvent', 'keyEvent', 'MACOSX'
}

EXTRA_DIR_NAMES = {
    'run_sketch', 'get_py5applet', 'reset_py5', 'exit_sketch',
    'autoclass', 'Py5Methods', '_Py5Applet', '_py5sketch', '_py5sketch_used',
    '_prune_tracebacks'
}

EXTRA_MODULE_STATIC_FUNCTIONS = {
    'sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'atan2', 'degrees', 'radians',
    'constrain', 'lerp', 'sq', 'mag', 'dist', 'norm',
    'load_json', 'save_json', 'parse_json'
}

EXTRA_MODULE_FUNCTIONS = {
    'exit_sketch', 'get_py5applet', 'hot_reload_draw',
    'profile_functions', 'profile_draw', 'print_line_profiler_stats'
}

###############################################################################
# UTIL FUNCTIONS
###############################################################################


def snake_case(name):
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name)
    return name.lower()


@lru_cache(128)
def convert_type(jtype: str) -> str:
    if jtype == 'void':
        return 'None'

    isarray = jtype.endswith('[]')
    jtype = jtype[:-2] if isarray else jtype

    if jtype == 'boolean':
        out = 'bool'
    elif jtype == 'char':
        out = 'chr'
    elif jtype == 'long':
        out = 'int'
    elif jtype == 'java/lang/String':
        out = 'str'
    elif jtype == 'java/lang/Object':
        out = 'Any'
    else:
        tokens = jtype.split('/')
        out = tokens[-1]

    return f'List[{out}]' if isarray else out


def param_annotation(varname: str, jtype: str) -> str:
    if jtype.endswith('...'):
        jtype = jtype[:-3]
        varname = '*' + varname

    return f'{varname}: {convert_type(jtype)}'

###############################################################################
# MAIN
###############################################################################


def generate_py5(repo_dir=None, install_dir=None):
    """Generate an installable py5 library using processing jars
    """
    repo_dir = repo_dir and Path(repo_dir)
    install_dir = install_dir and Path(install_dir)

    print(f'generating py5 library...')
    search_dir = repo_dir or install_dir
    core_jars = list(search_dir.glob('**/core.jar'))
    if len(core_jars) != 1:
        if core_jars:
            print(
                f'more than one core.jar found in {search_dir}', file=sys.stderr)
        else:
            print(f'core.jar not found in {search_dir}', file=sys.stderr)
        return
    core_jar_path = core_jars[0]

    py5_jar_path = Path('py5jar', 'dist', 'py5.jar')
    if not py5_jar_path.exists():
        raise RuntimeError(f'py5 jar not found at {str(py5_jar_path)}')
    import jnius_config
    jnius_config.set_classpath(str(py5_jar_path), str(core_jar_path))
    from jnius import autoclass, JavaStaticMethod, JavaMethod, JavaMultipleMethod, JavaStaticField, JavaField

    method_parameter_names_data = dict()
    with open('/tmp/params.psv', 'r') as f:
        for line in f.readlines():
            c, f, types, params, rettype = line.split('|')
            if c not in method_parameter_names_data: method_parameter_names_data[c] = dict()
            if f not in method_parameter_names_data[c]: method_parameter_names_data[c][f] = dict()
            if types in method_parameter_names_data[c][f]: raise RuntimeError('assumption violated')
            method_parameter_names_data[c][f][types] = (params, rettype)

    print('examining Java classes')
    Py5Applet = autoclass('py5.core.Py5Applet',
                          include_protected=False, include_private=False)
    py5applet = Py5Applet()

    methods = set()
    static_methods = set()
    fields = set()
    static_fields = set()

    for k, v in Py5Applet.__dict__.items():
        if isinstance(v, JavaStaticMethod) and k not in (DEPRECATED | PAPPLET_SKIP_METHODS):
            static_methods.add((k, v))
        elif isinstance(v, (JavaMethod, JavaMultipleMethod)) and k not in (DEPRECATED | PAPPLET_SKIP_METHODS):
            methods.add((k, v))
        elif isinstance(v, JavaStaticField) and k not in DEPRECATED:
            static_fields.add(k)
        elif isinstance(v, JavaField) and k not in DEPRECATED:
            fields.add(k)

    # storage for Py5Applet members and the result of the module's __dir__ function.
    class_members = []
    module_members = []
    run_sketch_pre_run_steps = []
    py5_dir = []

    # code the static constants
    print('coding static constants')
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

    # code the dynamic variables
    print('coding dynamic variables')
    py5_dynamic_vars = []
    for name in sorted(fields):
        snake_name = snake_case(name)
        var_type = (
            {'args': 'List[str]', 'g': 'PGraphics', 'recorder': 'PGraphics', 'pixels': 'List[int]'}
        ).get(name, type(getattr(py5applet, name)).__name__)
        class_members.append(CLASS_PROPERTY_TEMPLATE.format(snake_name, var_type, name))
        module_members.append(MODULE_PROPERTY_TEMPLATE.format(snake_name, var_type))
        run_sketch_pre_run_steps.append(MODULE_PROPERTY_PRE_RUN_TEMPLATE.format(snake_name))
        py5_dynamic_vars.append(snake_name)
        py5_dir.append(snake_name)

    # code the class and instance methods
    def code_methods(methods, static):
        for fname, method in sorted(methods, key=lambda x: x[0]):
            snake_name = snake_case(fname)
            if static:
                first_param, classobj, moduleobj, decorator = 'cls', '_Py5Applet', 'Sketch', '@classmethod'
            else:
                first_param, classobj, moduleobj, decorator = 'self', 'self._py5applet', '_py5sketch', ''
            # first, construct the typehint code
            if len(method.signatures()) == 1:
                params, rettype = method.signatures()[0]
                if PAPPLET_SKIP_PARAM_TYPES.intersection(params) or rettype in PAPPLET_SKIP_PARAM_TYPES:
                    continue
                try:
                    parameter_names, _ = method_parameter_names_data['PApplet'][fname][','.join([p.split('/')[-1] for p in params])]
                    parameter_names = [snake_case(p) for p in parameter_names.split(',')]
                    paramstrs = [first_param] + [param_annotation(pn, p) for pn, p in zip(parameter_names, params)]
                except Exception:
                    print('* problem finding parameter names for', fname, params)
                    paramstrs = [first_param] + [param_annotation(f'arg{i}', p) for i, p in enumerate(params)]
                rettypestr = convert_type(rettype)
                class_members.append(CLASS_METHOD_TEMPLATE_WITH_TYPEHINTS.format(
                    snake_name, ', '.join(paramstrs), classobj, fname, decorator, rettypestr, ', '.join([p.split(':')[0] for p in paramstrs[1:]])))
                module_members.append(MODULE_FUNCTION_TEMPLATE_WITH_TYPEHINTS.format(
                    snake_name, ', '.join(paramstrs[1:]), moduleobj, rettypestr, ', '.join([p.split(':')[0] for p in paramstrs[1:]])))
            else:
                for params, rettype in sorted(method.signatures(), key=lambda x: len(x[0])):
                    if PAPPLET_SKIP_PARAM_TYPES.intersection(params) or rettype in PAPPLET_SKIP_PARAM_TYPES:
                        continue
                    try:
                        parameter_names, _ = method_parameter_names_data['PApplet'][fname][','.join([p.split('/')[-1] for p in params])]
                        parameter_names = [snake_case(p) for p in parameter_names.split(',')]
                        paramstrs = [first_param] + [param_annotation(pn, p) for pn, p in zip(parameter_names, params)]
                    except Exception:
                        print('** problem finding parameter names for', fname, params)
                        paramstrs = [first_param] + [param_annotation(f'arg{i}', p) for i, p in enumerate(params)]
                    rettypestr = convert_type(rettype)
                    class_members.append(CLASS_METHOD_TYPEHINT_TEMPLATE.format(
                        snake_name, ', '.join(paramstrs), rettypestr))
                    module_members.append(MODULE_FUNCTION_TYPEHINT_TEMPLATE.format(
                        snake_name, ', '.join(paramstrs[1:]), rettypestr))
                # now construct the real methods
                class_members.append(CLASS_METHOD_TEMPLATE.format(snake_name, first_param, classobj, fname, decorator))
                module_members.append(MODULE_FUNCTION_TEMPLATE.format(snake_name, moduleobj))
            py5_dir.append(snake_name)

    print('coding class methods')
    code_methods(methods, False)
    code_methods(static_methods, True)

    # add the extra Sketch methods to the module
    print('coding extra module functions')
    for fname in EXTRA_MODULE_FUNCTIONS:
        module_members.append(MODULE_FUNCTION_TEMPLATE.format(fname, '_py5sketch'))
        py5_dir.append(fname)
    for fname in EXTRA_MODULE_STATIC_FUNCTIONS:
        module_members.append(MODULE_FUNCTION_TEMPLATE.format(fname, 'Sketch'))
        py5_dir.append(fname)

    class_members_code = ''.join(class_members)
    module_members_code = ''.join(module_members)
    run_sketch_pre_run_code = ''.join(run_sketch_pre_run_steps)

    # code the result of the module's __dir__ function and __all__ variable
    py5_dir.extend(EXTRA_DIR_NAMES)
    str_py5_dir = str(sorted(py5_dir, key=lambda x: x.lower()))
    # don't want import * to import the dynamic variables because they cannot be updated
    str_py5_all = str(sorted([x for x in py5_dir if x not in py5_dynamic_vars], key=lambda x: x.lower()))

    # complete the output template
    print('arranging code')
    with open(Path('py5_resources', 'templates', 'py5__init__.py'), 'r') as f:
        py5_template = f.read()
        py5_docstring_template = Template(
            re.sub(r'^.*DELETE$', '',
                   py5_template.format(class_members_code=class_members_code,
                                       module_members_code=module_members_code,
                                       run_sketch_pre_run_code=run_sketch_pre_run_code,
                                       str_py5_dir=str_py5_dir,
                                       str_py5_all=str_py5_all),
                   flags=re.MULTILINE | re.UNICODE))

    # build complete py5 module in destination directory
    dest_dir = Path('build')
    print(f'building py5 in {dest_dir}')
    if dest_dir.exists():
        shutil.rmtree(dest_dir)
    try:
        shutil.copytree(Path('py5_resources', 'py5_module_framework'),
                        dest_dir, copy_function=shutil.copy)
    except Exception:
        # ignore WSL error
        pass
    for jar in core_jar_path.parent.glob('*.jar'):
        shutil.copy(jar, dest_dir / 'py5' / 'jars')
    shutil.copy(py5_jar_path, dest_dir / 'py5' / 'jars')

    # add the docstrings and write out the different languages
    docstring_library = DocstringLibrary()
    for language in ['en']:  # docstring_library.languages:
        print(f'adding docstrings for language {language}')
        py5_code_w_docs = py5_docstring_template.substitute(docstring_library.docstring_dict(language))
        print(f'format code for {language}')
        py5_code_w_docs = autopep8.fix_code(py5_code_w_docs, options={'aggressive': 2})

        print(f'writing {language} file')
        with open(dest_dir / 'py5' / f'{language}.py', 'w') as f:
            f.write(py5_code_w_docs + '\n')
        if language == 'en':
            with open(dest_dir / 'py5' / '__init__.py', 'w') as f:
                f.write(py5_code_w_docs + '\n')

    print('done!')


def main():
    args = parser.parse_args()
    generate_py5(repo_dir=args.processing_repo_dir,
                 install_dir=args.processing_install_dir)


if __name__ == '__main__':
    main()
