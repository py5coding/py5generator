import sys
import re
import argparse
import shutil
import shlex
from pathlib import Path


###############################################################################
# ARGUMENT PARSING
###############################################################################


parser = argparse.ArgumentParser(description="Generate py5 library using processing jars",
                                 epilog="this is the epilog")


parser.add_argument(action='store', dest='py5_destination_dir', default='.',
                    help='location to write generated py5 library')
parser.add_argument('-x', '--exist_ok', action='store_true',
                    dest='dest_exist_ok', default=False,
                    help='ok to replace py5 directory in py5_destination_dir')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-r', '--repo', action='store', dest='processing_repo_dir',
                   help='location of processing code (github repository)')
group.add_argument('-p', '--pde', action='store', dest='processing_install_dir',
                   help='location of installed processing application (PDE)')


###############################################################################
# TEMPLATES
###############################################################################


METHOD_TEMPLATE = """
def {0}(*args):
    return _papplet.{1}(*args)"""

STATIC_METHOD_TEMPLATE = """
def {0}(*args):
    return Py5Applet.{1}(*args)"""

DYNAMIC_VAR_TEMPLATE = """
    global {0}
    {0} = _papplet.{1}"""


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
    'radians', 'sq',
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


def generate_py5(dest_dir, dest_exist_ok=False, repo_dir=None, install_dir=None):
    """Generate an installable py5 library using processing jars
    """
    dest_dir = Path(dest_dir)
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

    import jnius_config
    # TODO: add a helpful error message if py5.jar does not exist
    jnius_config.set_classpath('py5jar/dist/py5.jar', str(core_jar_path))
    from jnius import autoclass
    from jnius import JavaStaticMethod, JavaMethod, JavaMultipleMethod, JavaStaticField, JavaField

    Py5Applet = autoclass('py5.core.Py5Applet',
                          include_protected=False, include_private=False)

    # TODO: simplify below code by splitting out static methods
    methods = set()
    fields = set()
    static_fields = set()

    for k, v in Py5Applet.__dict__.items():
        if isinstance(v, (JavaStaticMethod, JavaMethod, JavaMultipleMethod)):
            methods.add(k)
        elif isinstance(v, JavaStaticField):
            static_fields.add(k)
        elif isinstance(v, JavaField):
            fields.add(k)

    # code the static constants
    py5_constants = []
    for name in sorted(static_fields):
        if name in DEPRECATED:
            continue
        if name in PCONSTANT_OVERRIDES:
            py5_constants.append(f'{name} = {shlex.quote(PCONSTANT_OVERRIDES[name])}')
        else:
            val = getattr(Py5Applet, name)
            if isinstance(val, str):
                val = f"'{val}'"
            if name == 'javaVersion':
                val = round(val, 2)
            py5_constants.append(f'{name} = {val}')
    py5_constants_code = '\n'.join(py5_constants)

    # code the dynamic variables
    init_vars = []
    update_vars = []
    for name in sorted(fields):
        if name in DEPRECATED:
            continue
        snake_name = snake_case(name)
        init_vars.append(f'{snake_name} = None')
        update_vars.append(DYNAMIC_VAR_TEMPLATE.format(snake_name, name))
    py5_init_dynamic_var_code = '\n'.join(init_vars)
    py5_update_dynamic_var_code = ''.join(update_vars)[5:]

    # code the class and instance methods
    py5_functions = []
    for fname in sorted(methods):
        if fname in DEPRECATED or fname in PAPPLET_SKIP_METHODS:
            continue
        if isinstance(getattr(Py5Applet, fname), JavaStaticMethod):
            py5_functions.append(STATIC_METHOD_TEMPLATE.format(snake_case(fname), fname))
        else:
            py5_functions.append(METHOD_TEMPLATE.format(snake_case(fname), fname))
    py5_functions_code = '\n\n'.join(py5_functions)

    # complete the output template
    with open('py5_resources/templates/py5__init__.py', 'r') as f:
        py5_template = f.read()
    py5_code = py5_template.format(py5_constants_code,
                                   py5_init_dynamic_var_code,
                                   py5_update_dynamic_var_code,
                                   py5_functions_code)

    # build complete py5 module in destination directory
    # first validate the output directory
    print(f'writing py5 in {dest_dir}')
    if dest_dir.exists():
        if not dest_dir.is_dir():
            print(f'output destination {dest_dir} is not a directory.', file=sys.stderr)
            return
    else:
        dest_dir.mkdir(parents=True)
    output_dir = dest_dir / 'py5'
    if output_dir.exists():
        if dest_exist_ok:
            shutil.rmtree(output_dir)
        else:
            print(f'output destination {output_dir} already exists.', file=sys.stderr)
            return

    base_path = Path(__file__).absolute().parent
    shutil.copytree(base_path / 'py5_resources' / 'py5_module_framework' / '',
                    output_dir)
    for jar in core_jar_path.parent.glob('*.jar'):
        shutil.copy(jar, output_dir / 'py5' / 'jars')
    shutil.copy('py5jar/dist/py5.jar', output_dir / 'py5' / 'jars')
    with open(output_dir / 'py5' / '__init__.py', 'w') as f:
        f.write(py5_code)

    print('done!')


def main():
    args = parser.parse_args()
    generate_py5(args.py5_destination_dir,
                 dest_exist_ok=args.dest_exist_ok,
                 repo_dir=args.processing_repo_dir,
                 install_dir=args.processing_install_dir)


if __name__ == '__main__':
    main()
