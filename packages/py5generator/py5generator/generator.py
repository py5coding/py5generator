import string
import pkgutil
import shlex

import jnius_config
jnius_config.set_classpath('.', '/home/jim/Projects/git/processing/core/library/*')
from jnius import autoclass  # noqa
from jnius import JavaMethod, JavaMultipleMethod, JavaStaticMethod  # noqa

PythonPApplet = autoclass('processing.core.PythonPApplet')
PConstants = autoclass('processing.core.PConstants')

_papplet = PythonPApplet()

pappletSkipMethods = {
    'print', 'exec', 'draw', 'setup', 'exit',
    'handleDrawPt1', 'handleDrawPt2', 'handleDrawPt3',
    'handleSettingsPt1', 'handleSettingsPt2',
}

pconstantOverrides = {
    'WHITESPACE': r' \t\n\r\x0c\xa0',
    'ESC': r'\x1b',
    'RETURN': r'\r',
    'ENTER': r'\n',
    'DELETE': r'\x7f',
    'BACKSPACE': r'\x08',
    'TAB': r'\t'
}

pappletStaticVariables = {
    'javaPlatform', 'javaVersion', 'javaVersionName', 'platform', 'platformNames', 'useNativeSelect'
}


def generate_py5():
    py5_template = pkgutil.get_data('py5generator', 'templates/py5_init_template.py').decode('utf-8')

    py5_constants = []
    for name in filter(lambda x: x[0] in string.ascii_uppercase, dir(PConstants)):
        # TODO: can I combine this with a ChainDict?
        if name in pconstantOverrides:
            py5_constants.append(f'{name} = {shlex.quote(pconstantOverrides[name])}')
        else:
            val = getattr(PConstants, name)
            if isinstance(val, str):
                val = f"'{val}'"
            py5_constants.append(f'{name} = {val}')

    for name in pappletStaticVariables:
        val = getattr(PythonPApplet, name)
        if isinstance(val, str):
            val = f"'{val}'"
        elif name == 'javaVersion':  # necessary hack
            val = round(val, 1)
        py5_constants.append(f'{name} = {val}')

    py5_functions = []
    for fname in filter(lambda x: x[0] in string.ascii_lowercase, dir(_papplet)):
        if fname in pappletSkipMethods or fname in pappletStaticVariables or '$' in fname:
            continue

        if not isinstance(getattr(_papplet, fname), (JavaMethod, JavaStaticMethod, JavaMultipleMethod)):
            print('skipping', fname, type(getattr(_papplet, fname)))
            continue

        if isinstance(getattr(_papplet, fname), JavaStaticMethod):
            py5_functions.append(f"def {fname}(*args):\n    return PythonPApplet.{fname}(*args)\n")
        else:
            py5_functions.append(f"def {fname}(*args):\n    return _papplet.{fname}(*args)\n")

    py5_code = py5_template.format('\n'.join(py5_constants),
                                   '\n\n'.join(py5_functions))

    with open('/tmp/__init__.py', 'w') as f:
        f.write(py5_code)
