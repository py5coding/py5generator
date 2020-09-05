from io import StringIO
import textwrap
from html.parser import HTMLParser
from pathlib import Path

import xmltodict


PY5_API_EN = Path('py5_docs/Reference/api_en/')


DOC_TEMPLATE = """
{0}.

Parameters
----------

list params

Notes
-----

{1}
"""


class TagRemover(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = StringIO()

    def handle_data(self, d):
        self.text.write(d)

    def get_data(self):
        return self.text.getvalue()


def remove_html(html):
    tr = TagRemover()
    tr.feed(html)
    return tr.get_data()


def prepare_docstrings():
    docstrings = {}
    for xml_file in PY5_API_EN.glob('*.xml'):
        key = tuple(xml_file.stem.split('_', maxsplit=1))
        with open(xml_file, 'r') as f:
            data = xmltodict.parse(f.read())
            # TODO: I don't want to remove all html, I want to replace the <b> tags with backticks, for example
            description = textwrap.fill(remove_html(data['root']['description']).strip(), 80)
            first_sentence = description.split('. ', maxsplit=1)[0]
            docstring = DOC_TEMPLATE.format(first_sentence, description)
            docstrings[key] = docstring

    return docstrings


class DocstringFinder:

    INDENTING = {'class': 8, 'module': 4}

    def __init__(self):
        self._data = prepare_docstrings()

    def __getitem__(self, item):
        kind, clsname, methodname = item.split('_', 2)
        raw_docstring = 'missing docstring'
        if (clsname, methodname) in self._data:
            raw_docstring = self._data[(clsname, methodname)]
        elif clsname in ['Py5Graphics', 'Py5Image'] and ('Sketch', methodname) in self._data:
            raw_docstring = self._data[('Sketch', methodname)]

        if raw_docstring == 'missing docstring':
            print(raw_docstring, clsname, methodname)

        doc = textwrap.indent(
            raw_docstring,
            prefix=(' ' * DocstringFinder.INDENTING.get(kind, 0))).strip()
        doc += '\n'
        return doc
