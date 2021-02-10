# *****************************************************************************
#
#   Part of the py5generator project; generator of the py5 library
#   Copyright (C) 2020-2021 Jim Schmitz
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
import ast
import shlex
from io import StringIO
from pathlib import Path

from generator.docfiles import Documentation
import py5.reference as ref

PY5_API_EN = Path('py5_docs/Reference/api_en/')


def convert_to_module_mode(code):
    """convert imported mode code to module mode code.

    not guaranteed to work for all inputs. will not properly handle
    multi-line strings.
    """
    tokens = shlex.shlex(code)
    tokens.whitespace = ''
    tokens.wordchars += '.'
    tokens.commenters = ''
    tokens.quotes = ''

    out = StringIO()
    in_comment = False
    in_quote = None
    for token in tokens:
        if token in ["'", '"'] and not in_comment:
            if not in_quote:
                in_quote = token
            elif in_quote and token == in_quote:
                in_quote = None
        elif token == '#':
            in_comment = True
        elif token == '\n':
            in_comment = False
            in_quote = None
        elif token in ref.PY5_DIR_STR and not (in_comment or in_quote):
            token = 'py5.' + token
        out.write(token)

    return out.getvalue()


parsing_errors = 0
for docfile in sorted(PY5_API_EN.glob('*.txt')):
    doc = Documentation(docfile)

    if doc.meta['type'] in ['function', 'magic']:
        # skip these because I know I wrote them in module mode
        print(f'skipping {docfile}')
        continue

    new_examples = []
    for image, code in doc.examples:
        new_code = convert_to_module_mode(code)
        new_examples.append((image, new_code))

        # quick check for parsing errors
        try:
            ast.parse(new_code)
        except Exception as e:
            parsing_errors += 1
            print('=' * 40)
            print(f'parsing error in file {docfile}')
            print('-' * 20)
            print(new_code)
            print('-' * 20)
            print(e)

    doc.examples = new_examples
    doc.write(docfile)

print(f'there were {parsing_errors} parsing errors.')
