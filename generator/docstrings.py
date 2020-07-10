import re
import textwrap
from pathlib import Path


DOCSTRING = re.compile(r'(@@@ DOCSTRING (\w+) @@@)')
DOCSTRING_FILE_HEADER = re.compile(r"^# \w+$", re.UNICODE | re.MULTILINE)


class DocstringDict:

    INDENTING = {'class': 8, 'module': 4}

    def __init__(self, language, docstrings):
        super().__init__()
        self._language = language
        self._docstrings = docstrings

    def __getitem__(self, item):
        try:
            kind, name = item.split('_', 1)
            doc = textwrap.indent(
                self._docstrings[name],
                prefix=(' ' * DocstringDict.INDENTING.get(kind, 0))).strip()
            return doc
        except KeyError:
            return f'missing {self._language} language docstring for {name}'


class DocstringLibrary:

    def __init__(self):
        self._load_docstrings()

    def _load_docstrings(self):
        docstring_dir = Path('py5_resources', 'docstrings')
        self._docstings = {}
        for md_file in docstring_dir.glob('*.md'):
            with open(md_file, 'r') as f:
                md_contents = f.read()
            parsed_md = {k[1:].strip(): v.strip()
                         for k, v in zip(DOCSTRING_FILE_HEADER.findall(md_contents),
                                         DOCSTRING_FILE_HEADER.split(md_contents)[1:])}
            self._docstings[md_file.stem] = parsed_md

    @property
    def languages(self):
        return list(self._docstings.keys())

    def docstring_dict(self, language):
        return DocstringDict(language, self._docstings[language])
