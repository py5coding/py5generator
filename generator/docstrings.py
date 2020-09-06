import re
import json
from io import StringIO
import textwrap
from html.parser import HTMLParser
from pathlib import Path

import xmltodict


PY5_API_EN = Path('py5_docs/Reference/api_en/')


PARAMETERS_TEMPLATE = """

Parameters
----------

{0}"""


METHOD_DOC_TEMPLATE = """
{0}.

Signatures
----------

{1}

Notes
-----

{2}
"""


VARIABLE_DOC_TEMPLATE = """
{0}.

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


def prepare_docstrings(method_signatures_lookup, variable_descriptions):
    docstrings = {}
    for xml_file in sorted(PY5_API_EN.glob('*.xml')):
        key = xml_file.stem
        tuple_key = tuple(key.split('_', maxsplit=1))
        with open(xml_file, 'r') as f:
            data = xmltodict.parse(f.read())
        # TODO: I don't want to remove all html, I want to replace the <b> tags with backticks, for example
        description = remove_html(data['root']['description']).strip()
        item_name = data['root']['name']
        description = '\n'.join([textwrap.fill(d, 80) for d in description.split('\n')])
        first_sentence = re.split(r'\.\s', description, maxsplit=1)[0]
        if item_name.endswith('()'):
            if tuple_key not in method_signatures_lookup:
                print('missing method signatures', tuple_key)
                signatures_variables = 'signatures missing'
            else:
                signatures = []
                variables = set()
                for params, rettype in method_signatures_lookup[tuple_key]:
                    signatures.append(f"{tuple_key[1]}({', '.join(filter(lambda p: p != '/', params))}) -> {rettype}")
                    for p in filter(lambda p: p != '/', params):
                        var_name = p.split(':')[0]
                        if key in variable_descriptions and var_name in variable_descriptions[key]:
                            var_desc = variable_descriptions[key][var_name]
                        else:
                            var_desc = 'missing variable description'
                        variables.add(f'{p} - {var_desc}')

                signatures_variables = '\n'.join(sorted(signatures))
                if variables:
                    signatures_variables += PARAMETERS_TEMPLATE.format('\n'.join(sorted(variables)))
            docstring = METHOD_DOC_TEMPLATE.format(first_sentence, signatures_variables, description)
        else:
            docstring = VARIABLE_DOC_TEMPLATE.format(first_sentence, description)

        docstrings[tuple_key] = docstring

    return docstrings


class DocstringFinder:

    INDENTING = {'class': 8, 'module': 4}

    def __init__(self, method_signatures_lookup, variable_descriptions_filename):
        with open(variable_descriptions_filename, 'r') as f:
            variable_descriptions = json.load(f)
        self._data = prepare_docstrings(method_signatures_lookup, variable_descriptions)

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
