# *****************************************************************************
#
#   Part of the py5generator project; generator of the py5 library
#   Copyright (C) 2020-2023 Jim Schmitz
#
#   This project is free software: you can redistribute it and/or modify it
#   under the terms of the GNU General Public License as published by the
#   Free Software Foundation, either version 3 of the License, or (at your
#   option) any later version.
#
#   This project is distributed in the hope that it will be useful, but
#   WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
#   Public License for more details.
#
#   You should have received a copy of the GNU General Public License along
#   with this program. If not, see <https://www.gnu.org/licenses/>.
#
# *****************************************************************************
import logging
import re
import shlex
import textwrap
from pathlib import Path

from .docfiles import Documentation

logger = logging.getLogger(__name__)

PY5_API_EN = Path('py5_docs/Reference/api_en/')

FIRST_SENTENCE_REGEX = re.compile(r'^.*?\.(?=\s)')
REST_DOC_LINK = re.compile(r'\[\]\([\w_]+\)')

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


MAGIC_DOC_TEMPLATE = """Notes
-----

{0}
"""


def decorator_helper(datum):
    arg_str, *help = datum.split('\n', maxsplit=1)
    return arg_str + f", help={shlex.quote(help[0])}" if help else arg_str


def doclink_to_title_map():
    out = dict()

    for docfile in sorted(PY5_API_EN.glob('*.txt')):
        doc = Documentation(docfile)
        stem = docfile.stem
        name = doc.meta['name']
        item_type = doc.meta['type']
        group = stem.split('_', 1)[0]
        slug = stem.lower()

        if (item_type in ['class', 'pseudoclass'] or
            item_type in ['line magic', 'cell magic'] or
                group in ['Sketch', 'Py5Functions', 'Py5Magics']):
            title = name
        elif group == 'Py5Tools':
            title = f"py5_tools.{name}"
        else:
            title = f"{group}.{name}"

        out[f"[]({slug})"] = f"`{title}`"

    return out


def prepare_mapping(method_signatures_lookup):
    title_map = doclink_to_title_map()
    mapping = {}
    for docfile in sorted(PY5_API_EN.glob('*.txt')):
        key = docfile.stem
        tuple_key = tuple(key.split('_', maxsplit=1))
        doc = Documentation(docfile)
        item_type = doc.meta['type']
        processing_name = doc.meta.get('processing_name')
        description = doc.description.strip()
        for m in REST_DOC_LINK.findall(description):
            description = description.replace(m, title_map[m])
        m = FIRST_SENTENCE_REGEX.match(description)
        first_sentence = m.group() if m else description
        description = '\n'.join([textwrap.fill(d, 80)
                                for d in description.splitlines()])
        first_sentence = textwrap.fill(first_sentence, 80)
        if item_type in ['line magic', 'cell magic']:
            arg_decorators = '\n'.join(
                f'@argument({decorator_helper(d)})' for d in doc.arguments)
            mapping[(tuple_key[0],
                     f'{tuple_key[1]}_arguments')] = arg_decorators
            docstring = MAGIC_DOC_TEMPLATE.format(description)
        elif item_type in ['method', 'function']:
            signatures = doc.signatures
            variables = doc.variables
            if tuple_key not in method_signatures_lookup:
                if not signatures:
                    logger.error(
                        f'missing method signatures in lookup for {tuple_key[0]}.{tuple_key[1]}')
            else:
                found_signatures = set()
                found_variables = set()
                for params, rettype in method_signatures_lookup[tuple_key]:
                    sig = f"{tuple_key[1]}({', '.join(params)}) -> {rettype}"
                    found_signatures.add(sig)
                    if sig not in signatures:
                        logger.warning(
                            f'new signature: {tuple_key[0]}.{tuple_key[1]}, {sig}')
                        signatures.append(sig)
                    for p in [p.replace('*', '') for p in params if p and p not in ['/', '*']]:
                        found_variables.add(p)
                        if p not in variables:
                            logger.warning(
                                f'new variable: {tuple_key[0]}.{tuple_key[1]}, {p}')
                            variables[p] = 'missing variable description'

                # remove no longer used variables and signatures from documentation
                dropped_signatures = set(
                    signatures).difference(found_signatures)
                for dropped_sig in dropped_signatures:
                    logger.warning(
                        f'dropped signature: {tuple_key[0]}.{tuple_key[1]}, {dropped_sig}')
                    signatures.remove(dropped_sig)
                dropped_variables = set(
                    variables.keys()).difference(found_variables)
                for dropped_var in dropped_variables:
                    logger.warning(
                        f'dropped variable: {tuple_key[0]}.{tuple_key[1]}, {dropped_var}')
                    variables.pop(dropped_var)

            extras = ''
            if processing_name:
                extras += f'\n\nUnderlying Processing {item_type}: {doc.meta["pclass"]}.{processing_name}'
            if len(signatures) > 1:
                signatures_txt = '\n'.join(
                    sorted([f' * {s}' for s in signatures]))
                extras += SIGNATURES_TEMPLATE.format(signatures_txt)
            if variables:
                variables_txt = [f'{k}\n    {v}\n'.replace(
                    '\\', '\\\\') for k, v in variables.items()]
                extras += PARAMETERS_TEMPLATE.format(
                    '\n'.join(sorted(variables_txt)))[:-1]
            docstring = METHOD_DOC_TEMPLATE.format(
                first_sentence + extras, description)
        else:
            extras = ''
            if processing_name:
                extras += f'\n\nUnderlying Processing {item_type}: {doc.meta["pclass"]}.{processing_name}'
            docstring = VARIABLE_DOC_TEMPLATE.format(
                first_sentence + extras, description)

        # sort to make everything neat and tidy
        doc.signatures = list(sorted(set(doc.signatures)))
        doc.variables = dict(sorted(doc.variables.items()))

        # write the documentation information back to the original file
        doc.write(PY5_API_EN / docfile.name)

        mapping[tuple_key] = docstring

    return mapping


class TemplateMapping:

    INDENTING = {'class': 8, 'pseudoclass': 0,
                 'module': 4, 'classdoc': 4, 'arguments': 4}

    def __init__(self, method_signatures_lookup):
        self._data = prepare_mapping(method_signatures_lookup)

    def __getitem__(self, item):
        if item.startswith('classdoc'):
            kind, clsname = item.split('_', 1)
            if (clsname,) in self._data:
                raw_value = self._data[(clsname,)]
            else:
                raise RuntimeError(f'missing template mapping: {item}')
        else:
            kind, clsname, methodname = item.split('_', 2)
            if (clsname, methodname) in self._data:
                raw_value = self._data[(clsname, methodname)]
            else:
                raise RuntimeError(f'missing template mapping: {item}')

        value = textwrap.indent(
            raw_value,
            prefix=(' ' * TemplateMapping.INDENTING.get(kind, 0))).strip()
        return value
