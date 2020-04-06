"""
Py5 Generator Code
"""
import string
import re
import pkgutil
import shlex


###############################################################################
# PYJNIUS SETUP
###############################################################################


import jnius_config
jnius_config.set_classpath('.', '/home/jim/Projects/git/processing/core/library/*')
from jnius import autoclass  # noqa
from jnius import JavaMethod, JavaMultipleMethod, JavaStaticMethod  # noqa

PythonPApplet = autoclass('processing.core.PythonPApplet')
PConstants = autoclass('processing.core.PConstants')

_papplet = PythonPApplet()


###############################################################################
# TEMPLATES
###############################################################################


METHOD_TEMPLATE = """
def {0}(*args):
    return _papplet.{1}(*args)"""

STATIC_METHOD_TEMPLATE = """
def {0}(*args):
    return PythonPApplet.{1}(*args)"""

DYNAMIC_VAR_TEMPLATE = """
    global {0}
    {0} = _papplet.{1}"""


###############################################################################
# REFERENCE AND LOOKUPS
###############################################################################


PAPPLET_SKIP_METHODS = {
    'print', 'exec', 'draw', 'setup', 'exit',
    'min', 'max', 'round', 'map', 'abs', 'pow',
    'runSketch',
    'handleDrawPt1', 'handleDrawPt2', 'handleDrawPt3',
    'handleSettingsPt1', 'handleSettingsPt2',
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

PAPPLET_STATIC_VARIABLES = {
    'javaPlatform', 'javaVersion', 'javaVersionName', 'platform', 'platformNames', 'useNativeSelect'
}

PAPPLET_DYNAMIC_VARIABLES = {
    'frameRate',
    'frameCount',
    # 'width', 'height',
    # 'pmouseX', 'pmouseY',
    'mouseX', 'mouseY',
    # 'pixels'
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


def generate_py5():
    """Generate the Py5 library
    """
    # read the output template
    py5_template = pkgutil.get_data('py5generator', 'templates/py5_init_template.py').decode('utf-8')

    # identify and code the static constants
    py5_constants = []
    for name in filter(lambda x: x[0] in string.ascii_uppercase, dir(PConstants)):
        # TODO: can I combine this with a ChainDict?
        if name in PCONSTANT_OVERRIDES:
            py5_constants.append(f'{name} = {shlex.quote(PCONSTANT_OVERRIDES[name])}')
        else:
            val = getattr(PConstants, name)
            if isinstance(val, str):
                val = f"'{val}'"
            py5_constants.append(f'{name} = {val}')
    py5_constants_code = '\n'.join(py5_constants)

    for name in PAPPLET_STATIC_VARIABLES:
        val = getattr(PythonPApplet, name)
        if isinstance(val, str):
            val = f"'{val}'"
        elif name == 'javaVersion':  # necessary hack
            val = round(val, 1)
        py5_constants.append(f'{name} = {val}')

    # identify and code the dynamic variables
    init_vars = []
    update_vars = []
    for name in PAPPLET_DYNAMIC_VARIABLES:
        snake_name = snake_case(name)
        init_vars.append(f'{snake_name} = None')
        update_vars.append(DYNAMIC_VAR_TEMPLATE.format(snake_name, name))
    py5_init_dynamic_var_code = '\n'.join(init_vars)
    py5_update_dynamic_var_code = ''.join(update_vars)[5:]

    # identify and code the class and instance methods
    py5_functions = []
    for fname in filter(lambda x: x[0] in string.ascii_lowercase, dir(_papplet)):
        if fname in PAPPLET_SKIP_METHODS or fname in PAPPLET_STATIC_VARIABLES or '$' in fname:
            continue

        if not isinstance(getattr(_papplet, fname), (JavaMethod, JavaStaticMethod, JavaMultipleMethod)):
            print('skipping', fname, type(getattr(_papplet, fname)))
            continue

        if isinstance(getattr(_papplet, fname), JavaStaticMethod):
            py5_functions.append(STATIC_METHOD_TEMPLATE.format(snake_case(fname), fname))
        else:
            py5_functions.append(METHOD_TEMPLATE.format(snake_case(fname), fname))
    py5_functions_code = '\n\n'.join(py5_functions)

    py5_code = py5_template.format(py5_constants_code,
                                   py5_init_dynamic_var_code,
                                   py5_update_dynamic_var_code,
                                   py5_functions_code)

    with open('/tmp/__init__.py', 'w') as f:
        f.write(py5_code)
