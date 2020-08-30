import builtins
from collections.abc import MutableMapping


class Py5Namespace(MutableMapping, dict):

    """
    Variable Namespace used for pde mode py5 execution.

    This inherits from both MutableMapping and dict because `exec` requires
    the globals param to be a `dict` type. The MutableMapping implementation
    should take precedence over all of the method calls.
    """

    def __init__(self, py5):
        super(Py5Namespace, self).__init__()
        self._py5 = py5
        self._ns = dict()

    def __getitem__(self, item):
        try:
            return self._ns[item]
        except KeyError:
            if item in dir(self._py5):
                return getattr(self._py5, item)
            elif hasattr(builtins, item):
                return getattr(builtins, item)
            else:
                raise KeyError(f'{item} not found')

    def __setitem__(self, key, value):
        self._ns[key] = value

    def __delitem__(self, key):
        del self._ns[key]

    def __iter__(self):
        for k in self._ns.keys():
            yield k
        for k in dir(self._py5):
            yield k
        for k in dir(builtins):
            yield k

    def __len__(self):
        return len(self._ns) + len(dir(self._py5)) + len(dir(builtins))
