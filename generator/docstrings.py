import re
import json
from io import StringIO
import logging
import textwrap
from html.parser import HTMLParser
from pathlib import Path

from .docfiles import Documentation


logger = logging.getLogger(__name__)

PY5_API_EN = Path('py5_docs/Reference/api_en/')

FIRST_SENTENCE_REGEX = re.compile(r'^.*?\.(?=\s)')

PARAMETERS_TEMPLATE = """

Parameters
----------

{0}"""


METHOD_DOC_TEMPLATE = """
{0}

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
    for docfile in sorted(PY5_API_EN.glob('*.txt')):
        key = docfile.stem
        tuple_key = tuple(key.split('_', maxsplit=1))
        doc = Documentation(docfile)
        # TODO: I don't want to remove all html, I want to replace the <b> tags with backticks, for example
        description = remove_html(doc.description).strip()
        item_name = doc.meta['name']
        description = '\n'.join([textwrap.fill(d, 80) for d in description.split('\n')])
        m = FIRST_SENTENCE_REGEX.match(description)
        first_sentence = m .group() if m else description
        if item_name.endswith('()'):
            signatures = doc.signatures
            variables = doc.variables
            if tuple_key not in method_signatures_lookup:
                if not signatures:
                    logger.warning(f'missing method signatures {tuple_key[0]}.{tuple_key[1]}')
                    signatures = ['signatures missing']
            else:
                for params, rettype in method_signatures_lookup[tuple_key]:
                    signatures.append(f"{tuple_key[1]}({', '.join(filter(lambda p: p != '/', params))}) -> {rettype}")
                    for p in filter(lambda p: p != '/', params):
                        if p in variables:
                            continue
                        var_name = p.split(':')[0]
                        if key in variable_descriptions and var_name in variable_descriptions[key]:
                            var_desc = variable_descriptions[key][var_name]
                        else:
                            var_desc = 'missing variable description'
                            logger.warning(f'{var_desc}: {tuple_key[0]}.{tuple_key[1]}, {p}')
                        variables[p] = var_desc

            signatures_variables = '\n'.join(sorted(signatures))
            if variables:
                variables_txt = [f'{k} - {v}' for k, v in variables.items()]
                signatures_variables += PARAMETERS_TEMPLATE.format('\n'.join(sorted(variables_txt)))
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
        elif (clsname, methodname) == ('Py5Graphics', 'mask'):
            raw_docstring = self._data[('Py5Image', methodname)]

        if raw_docstring == 'missing docstring':
            logger.warning(f'{raw_docstring}: {clsname}.{methodname}')

        doc = textwrap.indent(
            raw_docstring,
            prefix=(' ' * DocstringFinder.INDENTING.get(kind, 0))).strip()
        doc += '\n'
        return doc
