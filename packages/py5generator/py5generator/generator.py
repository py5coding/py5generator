import pkgutil
from io import StringIO
import string

import jnius_config
jnius_config.set_classpath('.', '/home/jim/Projects/git/processing/core/library/*')
from jnius import autoclass  # noqa

PythonPApplet = autoclass('processing.core.PythonPApplet')
PConstants = autoclass('processing.core.PConstants')

_papplet = PythonPApplet()

pconstantOverrides = {
    'WHITESPACE': r"' \t\n\r\x0c\xa0'",
    'ESC': r"'\x1b'",
    'RETURN': r"'\r'",
    'ENTER': r"'\n'",
    'DELETE': r"'\x7f'",
    'BACKSPACE': r"'\x08'",
    'TAB': r"'\t'"
}


def generate_py5():
    py5_template = pkgutil.get_data('py5generator', 'templates/py5_init_template.py').decode('utf-8')

    py5_constants = StringIO()
    for name in filter(lambda x: x[0] in string.ascii_uppercase, dir(PConstants)):
        # TODO: can I combine this with a ChainDict?
        if name in pconstantOverrides:
            py5_constants.write(f'{name} = {pconstantOverrides[name]}\n')
        else:
            val = getattr(PConstants, name)
            if isinstance(val, str):
                val = f"'{val}'"
            py5_constants.write(f'{name} = {val}\n')

    py5_functions = StringIO()
    for fname in filter(lambda x: x[0] in string.ascii_lowercase, dir(_papplet)):
        # TODO: what about exit?
        if fname in ['print', 'exec', 'draw', 'setup'] or '$' in fname:
            continue
        # TODO: use export decorator
        # https://stackoverflow.com/questions/44834/can-someone-explain-all-in-python

        # TODO: only do this for types jnius.JavaMultipleMethod or regular method
        # I want to skip over things like mouseX and mouseY
        code = f"def {fname}(*args):\n    return _papplet.{fname}(*args)\n\n\n"
        py5_functions.write(code)

    py5_code = py5_template.format(py5_constants.getvalue(),
                                   py5_functions.getvalue())

    with open('/tmp/__init__.py', 'w') as f:
        f.write(py5_code)
