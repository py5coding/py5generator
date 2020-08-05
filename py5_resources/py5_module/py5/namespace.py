import builtins


# TODO: maybe move this back to py5_tools?


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
        if not self._suppress_warnings:
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
