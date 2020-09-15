import re
import json
import logging
import textwrap
from pathlib import Path

from .docfiles import Documentation


logger = logging.getLogger(__name__)

PY5_API_EN = Path('py5_docs/Reference/api_en/')

FIRST_SENTENCE_REGEX = re.compile(r'^.*?\.(?=\s)')

PARAMETERS_TEMPLATE = """

Parameters
----------

{0}"""


SIGNATURES_TEMPLATE = """

Methods
-------

You can use any of the following signatures:

{0}"""


METHOD_DOC_TEMPLATE = """{0}

Notes
-----

{1}
"""


VARIABLE_DOC_TEMPLATE = """
{0}

Notes
-----

{1}
"""


def prepare_docstrings(method_signatures_lookup, variable_descriptions):
    docstrings = {}
    for docfile in sorted(PY5_API_EN.glob('*.txt')):
        key = docfile.stem
        tuple_key = tuple(key.split('_', maxsplit=1))
        doc = Documentation(docfile)
        item_name = doc.meta['name']
        description = doc.description.strip()
        m = FIRST_SENTENCE_REGEX.match(description)
        first_sentence = m.group() if m else description
        description = '\n'.join([textwrap.fill(d, 80) for d in description.split('\n')])
        first_sentence = textwrap.fill(first_sentence, 80)
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

            # TODO: write the documentation information back to the same file? or a different one?
            doc.write(Path('/tmp/docfiles/') / docfile.name)

            extras = ''
            if len(signatures) > 1:
                signatures_txt = '\n'.join(sorted([f' * {s}' for s in signatures]))
                extras = SIGNATURES_TEMPLATE.format(signatures_txt)
            if variables:
                variables_txt = [f'{k}\n    {v}\n' for k, v in variables.items()]
                extras += PARAMETERS_TEMPLATE.format('\n'.join(sorted(variables_txt)))[:-1]
            docstring = METHOD_DOC_TEMPLATE.format(first_sentence + extras, description)
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
