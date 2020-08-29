import builtins


# TODO: maybe move this back to py5_tools?
# TODO: use MutableMapping https://docs.python.org/3/library/collections.abc.html instead


class Py5Namespace(dict):

    def __init__(self, py5, user_ns=None):
        super().__init__()
        self._py5 = py5
        self._user_ns = user_ns or dict()

    def __setitem__(self, key, value):
        return super().__setitem__(key, value)

    def __getitem__(self, item):
        try:
            return super().__getitem__(item)
        except KeyError:
            if item in dir(self._py5):
                return getattr(self._py5, item)
            elif hasattr(builtins, item):
                return getattr(builtins, item)
            elif item in self._user_ns:
                return self._user_ns[item]
            else:
                raise KeyError(f'{item} not found')
