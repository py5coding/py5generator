import pickle
import textwrap


class DocstringFinder:

    INDENTING = {'class': 8, 'module': 4}

    def __init__(self, docstring_filename):
        with open(docstring_filename, 'rb') as f:
            self._data = pickle.load(f)

    def __getitem__(self, item):
        kind, clsname, methodname = item.split('_', 2)
        try:
            doc = textwrap.indent(
                self._data[(clsname, methodname)],
                prefix=(' ' * DocstringFinder.INDENTING.get(kind, 0))).strip()
            doc += '\n'
            return doc
        except KeyError:
            return 'missing docstring'
