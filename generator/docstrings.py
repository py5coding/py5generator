from io import StringIO
import textwrap
from html.parser import HTMLParser
from pathlib import Path

import xmltodict


PY5_API_EN = Path('py5_docs/Reference/api_en/')


METHOD_DOC_TEMPLATE = """
{0}.

Signatures
----------

{1}

Notes
-----

{2}
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


def prepare_docstrings(method_signatures_lookup):
    docstrings = {}
    # TODO: how does this work for frameRate the variable and frameRate the method? they are two different things but only there is only one file
    for xml_file in sorted(PY5_API_EN.glob('*.xml')):
        key = tuple(xml_file.stem.split('_', maxsplit=1))
        with open(xml_file, 'r') as f:
            data = xmltodict.parse(f.read())
        # TODO: I don't want to remove all html, I want to replace the <b> tags with backticks, for example
        description = remove_html(data['root']['description']).strip()
        description = '\n'.join([textwrap.fill(d, 80) for d in description.split('\n')])
        first_sentence = description.split('. ', maxsplit=1)[0]
        if key not in method_signatures_lookup:
            print('missing', key)
            method_signatures = 'signatures missing'
        else:
            signatures = []
            for params, rettype in method_signatures_lookup[key]:
                signatures.append(f"{key[1]}({', '.join(filter(lambda p: p != '/', params))}) -> {rettype}")
            method_signatures = '\n'.join(sorted(signatures))
        docstring = METHOD_DOC_TEMPLATE.format(first_sentence, method_signatures, description)
        docstrings[key] = docstring

    return docstrings


class DocstringFinder:

    INDENTING = {'class': 8, 'module': 4}

    def __init__(self, method_signatures_lookup):
        self._data = prepare_docstrings(method_signatures_lookup)

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
