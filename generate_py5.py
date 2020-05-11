import sys
import re
import argparse
import shutil
import shlex
import autopep8
from pathlib import Path


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
# TEMPLATES
###############################################################################


CLASS_PROPERTY_TEMPLATE = """
    @property
    def {0}(self):
        return self._py5applet.{1}
"""

CLASS_METHOD_TEMPLATE = """
    def {0}(self, *args):
        {1}
        return self._py5applet.{2}(*args)
"""

CLASS_STATIC_FIELD_TEMPLATE = """
    {0} = {1}
"""

CLASS_STATIC_METHOD_TEMPLATE = """
    @classmethod
    def {0}(cls, *args):
        {1}
        return _Py5Applet.{2}(*args)
"""

MODULE_PROPERTY_TEMPLATE = """
{0} = None
del {0}
"""

MODULE_FUNCTION_TEMPLATE = """
def {0}(*args):
    {1}
    return _py5sketch.{0}(*args)
"""

MODULE_STATIC_FUNCTION_TEMPLATE = """
def {0}(*args):
    {1}
    return Sketch.{0}(*args)
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
    'nfs', 'split', 'splitTokens', 'trim', 'debug', 'delay', 'equals',
    # user should use numpy instead
    'min', 'max', 'round', 'map', 'abs', 'pow', 'sqrt', 'ceil', 'floor', 'log',
    'exp', 'sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'atan2', 'degrees',
    'radians', 'sq', 'lerp', 'constrain',
    # public methods that should be skipped
    'runSketch', 'main', 'handleDraw', 'handleSettings', 'usePy5Methods',
    'registerMethod', 'unregisterMethod',
    'showDepthWarning', 'showDepthWarningXYZ', 'showMethodWarning',
    'showVariationWarning', 'showMissingWarning',
    'checkAlpha', 'setSize',
    'getClass',
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
    'autoclass', 'Py5Methods', '_Py5Applet', '_py5sketch', '_py5sketch_used'
}

EXTRA_MODULE_STATIC_FUNCTIONS = {
    'sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'atan2', 'degrees', 'radians',
    'constrain', 'lerp', 'sq'
}

EXTRA_MODULE_FUNCTIONS = {
}

###############################################################################
# UTIL FUNCTIONS
###############################################################################


def snake_case(name):
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name)
    return name.lower()


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

    py5_jar_path = Path('py5jar/dist/py5.jar')
    if not py5_jar_path.exists():
        raise RuntimeError(f'py5 jar not found at {str(py5_jar_path)}')
    import jnius_config
    jnius_config.set_classpath(str(py5_jar_path), str(core_jar_path))
    from jnius import autoclass, JavaStaticMethod, JavaMethod, JavaMultipleMethod, JavaStaticField, JavaField

    Py5Applet = autoclass('py5.core.Py5Applet',
                          include_protected=False, include_private=False)

    methods = set()
    static_methods = set()
    fields = set()
    static_fields = set()

    for k, v in Py5Applet.__dict__.items():
        if isinstance(v, JavaStaticMethod):
            static_methods.add(k)
        elif isinstance(v, (JavaMethod, JavaMultipleMethod)):
            methods.add(k)
        elif isinstance(v, JavaStaticField):
            static_fields.add(k)
        elif isinstance(v, JavaField):
            fields.add(k)

    static_fields -= DEPRECATED
    fields -= DEPRECATED
    methods -= (DEPRECATED | PAPPLET_SKIP_METHODS)
    static_methods -= (DEPRECATED | PAPPLET_SKIP_METHODS)

    # storage for Py5Applet members and the result of the module's __dir__ function.
    class_members = []
    module_members = []
    py5_dir = []

    # code the static constants
    for name in sorted(static_fields):
        if name in PCONSTANT_OVERRIDES:
            module_members.append(f'{name} = {shlex.quote(PCONSTANT_OVERRIDES[name])}\n')
        else:
            val = getattr(Py5Applet, name)
            if isinstance(val, str):
                val = f"'{val}'"
            if name == 'javaVersion':
                val = round(val, 2)
            module_members.append(f'{name} = {val}\n')
            class_members.append(CLASS_STATIC_FIELD_TEMPLATE.format(name, val))
            py5_dir.append(name)

    # code the dynamic variables
    py5_dynamic_vars = []
    for name in sorted(fields):
        snake_name = snake_case(name)
        class_members.append(CLASS_PROPERTY_TEMPLATE.format(snake_name, name))
        module_members.append(MODULE_PROPERTY_TEMPLATE.format(snake_name))
        py5_dynamic_vars.append(snake_name)
        py5_dir.append(snake_name)

    # code the class and instance methods
    for fname in sorted(methods):
        snake_name = snake_case(fname)
        docstring = shlex.quote(f'this is the docstring for {snake_name}')
        class_members.append(CLASS_METHOD_TEMPLATE.format(snake_name, docstring, fname))
        module_members.append(MODULE_FUNCTION_TEMPLATE.format(snake_name, docstring))
        py5_dir.append(snake_name)
    for fname in sorted(static_methods):
        snake_name = snake_case(fname)
        docstring = shlex.quote(f'this is the docstring for {snake_name}')
        class_members.append(CLASS_STATIC_METHOD_TEMPLATE.format(snake_name, docstring, fname))
        module_members.append(MODULE_STATIC_FUNCTION_TEMPLATE.format(snake_name, docstring))
        py5_dir.append(snake_name)

    # add the extra Sketch methods to the module
    for fname in EXTRA_MODULE_STATIC_FUNCTIONS:
        docstring = shlex.quote(f'this is the docstring for {fname}')
        module_members.append(MODULE_STATIC_FUNCTION_TEMPLATE.format(fname, docstring))
        py5_dir.append(fname)
    for fname in EXTRA_MODULE_FUNCTIONS:
        docstring = shlex.quote(f'this is the docstring for {fname}')
        module_members.append(MODULE_FUNCTION_TEMPLATE.format(fname, docstring))
        py5_dir.append(fname)

    class_members_code = ''.join(class_members)
    module_members_code = ''.join(module_members)

    # code the result of the module's __dir__ function and __all__ variable
    py5_dir.extend(EXTRA_DIR_NAMES)
    str_py5_dir = str(sorted(py5_dir, key=lambda x: x.lower()))
    # don't want import * to import the dynamic variables because they cannot be updated
    str_py5_all = str(sorted([x for x in py5_dir if x not in py5_dynamic_vars], key=lambda x: x.lower()))

    # complete the output template
    with open('py5_resources/templates/py5__init__.py', 'r') as f:
        py5_template = f.read()
    py5_code = py5_template.format(class_members_code,
                                   module_members_code,
                                   str_py5_dir,
                                   str_py5_all)
    py5_code = autopep8.fix_code(py5_code, options={'aggressive': 2})

    # build complete py5 module in destination directory
    dest_dir = Path('build')
    print(f'writing py5 in {dest_dir}')
    if dest_dir.exists():
        shutil.rmtree(dest_dir)
    shutil.copytree(Path('py5_resources', 'py5_module_framework'),
                    dest_dir, copy_function=shutil.copy)
    for jar in core_jar_path.parent.glob('*.jar'):
        shutil.copy(jar, dest_dir / 'py5' / 'jars')
    shutil.copy(py5_jar_path, dest_dir / 'py5' / 'jars')
    with open(dest_dir / 'py5' / '__init__.py', 'w') as f:
        f.write(py5_code + '\n')

    print('done!')


def main():
    args = parser.parse_args()
    generate_py5(repo_dir=args.processing_repo_dir,
                 install_dir=args.processing_install_dir)


if __name__ == '__main__':
    main()
