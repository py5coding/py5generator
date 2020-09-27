# import py5_tools.namespace
# import py5

# ns = py5_tools.namespace.Py5Namespace(py5)

# https://github.com/python/cpython/blob/master/Lib/collections/__init__.py

# https://stackoverflow.com/questions/41747211/passing-a-weakvaluedictionary-namespace-to-exec

from collections.abc import MutableMapping


class TestNamespace_(MutableMapping):

    def __init__(self):
        super(TestNamespace_, self).__init__()
        self._ns = dict()

    def __getitem__(self, item):
        print('getting', item)
        return self._ns[item]

    def __setitem__(self, key, value):
        print('setting', key, value)
        self._ns[key] = value

    def __delitem__(self, key):
        del self._ns[key]

    def __iter__(self):
        for k in self._ns.keys():
            yield k

    def __len__(self):
        return len(self._ns)

    def __contains__(self, key):
        print('contains', key)
        return key in self._ns

    def get(self, key, default=None):
        print('get', key)
        if self.__contains__(key):
            return self.__getitem__(self)
        else:
            return default

    def update(self, E, **F):
        print('in update')

    def keys():
        print('keys')

    def values():
        print('values')

    def __or__(self, other):
        raise RuntimeError('or')

    def __ror__(self, other):
        raise RuntimeError('ror')

    def __ior__(self, other):
        raise RuntimeError('ior')

    def __copy__(self):
        raise RuntimeError('copy')

    def copy(self):
        raise RuntimeError('copy2')


TestNamespace = type('TestNamespace', (TestNamespace_, dict), {})

ns = TestNamespace()

code = """
print('running')
foo1 = 10
print(foo1)
foo2 = 20
print(foo2)

def f1():
    global foo2
    foo2 = 200

f1()

print(foo2)
"""

exec(code, ns)
