import re
import textwrap


DOCSTRING_FILE_HEADER = re.compile(r"^# \w+$", re.UNICODE | re.MULTILINE)


class DocstringDict:

    INDENTING = {'class': 8, 'module': 4}

    def __init__(self, filename):
        super().__init__()
        self._docstrings = self._load_docstrings(filename)

    def _load_docstrings(self, filename):
        with open(filename, 'r') as f:
            md_contents = f.read()
        return {k[1:].strip(): v.strip()
                for k, v in zip(DOCSTRING_FILE_HEADER.findall(md_contents),
                                DOCSTRING_FILE_HEADER.split(md_contents)[1:])}

    def __getitem__(self, item):
        try:
            dockey, params = item.split('|')
            kind, name = dockey.split('_', 1)
            # TODO: replace var description with real description from json file I make in create_docs.py
            paramtext = '\n\n'.join([f'{p}\n    var description' for p in params.replace(
                ':', ': ').split('+')]) if params else ''
            doc = textwrap.indent(
                self._docstrings[name].replace('PARAMTEXT', paramtext),
                prefix=(' ' * DocstringDict.INDENTING.get(kind, 0))).strip()
            doc += '\n'
            return doc
        except KeyError:
            return 'missing docstring'
