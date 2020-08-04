import tempfile
import textwrap
import builtins


_CODE_TEMPLATE = """
def settings():
    size({0}, {1}, SVG, "{2}")


def setup():
{3}

    exit_sketch()
"""


_CODE_FRAMEWORK = """
import py5

with open('{0}', 'r') as f:
    eval(compile(f.read(), '{0}', 'exec'))

py5.run_sketch(block=True)
"""

# TODO: this is the same as in run.py
class Py5Namespace(dict):

    def __init__(self, py5, user_ns=None, suppress_warnings=False):
        super().__init__()
        self._py5 = py5
        self._warned = {'__doc__'}
        self._user_ns = user_ns if user_ns else {}
        self._suppress_warnings = suppress_warnings

    def _kind(self, thing):
        if isinstance(thing, type):
            return 'class'
        elif callable(thing):
            return 'function'
        else:
            return 'variable'

    def _issue_warning(self, key, what, exiting_thing, new_thing):
        existing_kind = self._kind(exiting_thing)
        new_kind = self._kind(new_thing)
        same = 'another' if existing_kind == new_kind else 'a'
        print(f'your sketch code has replaced {what} {key} {existing_kind} with {same} {new_kind}, which may cause problems.')
        self._warned.add(key)

    def __setitem__(self, key, value):
        if hasattr(self._py5, key) and key not in self._warned:
            self._issue_warning(key, 'py5', getattr(self._py5, key), value)
        if hasattr(builtins, key) and key not in self._warned:
            self._issue_warning(key, 'builtin', getattr(builtins, key), value)

        return super().__setitem__(key, value)

    def __getitem__(self, item):
        try:
            return super().__getitem__(item)
        except KeyError:
            if (not self._suppress_warnings and item not in self._warned
                    and item in self._user_ns and item in dir(self._py5)):
                print(f'WARNING: py5 name conflict detected with "{item}"')
                self._warned.add(item)
            if item in dir(self._py5):
                return getattr(self._py5, item)
            elif hasattr(builtins, item):
                return getattr(builtins, item)
            elif item in self._user_ns:
                return self._user_ns[item]
            else:
                raise KeyError(f'{item} not found')


def draw_svg(code, width, height, user_ns=None, suppress_warnings=False):
    temp_py = tempfile.NamedTemporaryFile(suffix='.py')
    temp_svg = tempfile.NamedTemporaryFile(suffix='.svg')

    with open(temp_py.name, 'w') as f:
        code = _CODE_TEMPLATE.format(width, height, temp_svg.name,
                                     textwrap.indent(code, ' ' * 4))
        f.write(code)

    import py5
    if py5._py5sketch_used:
        py5.reset_py5()
    py5_ns = Py5Namespace(py5, user_ns=user_ns, suppress_warnings=suppress_warnings)
    exec(_CODE_FRAMEWORK.format(temp_py.name), py5_ns)

    temp_py.close()

    with open(temp_svg.name, 'r') as f:
        svg_code = f.read()

    temp_svg.close()
    return svg_code


__all__ = ['draw_svg']
