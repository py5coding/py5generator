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
"""
This code is no longer used but might be pillaged one day to help convert code
to something usable by py5.

This code was used once to convert the example code to module mode code.
"""
import ast
import shlex
import autopep8
from io import StringIO
from pathlib import Path

from generator.docfiles import Documentation
import py5.reference as ref
from py5_tools import parsing


PY5_API_EN = Path('py5_docs/Reference/api_en/')


def convert_to_module_mode(code):
    """convert imported mode code to module mode code.

    not guaranteed to work for all inputs. will not properly handle
    multi-line strings. still, it works better than what I came up
    with using tokenize.
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


py5_reserved_word_errors = 0
ast_syntax_errors = 0
problem_files = 0
for docfile in sorted(PY5_API_EN.glob('*.txt')):
    doc = Documentation(docfile)

    # skip these because I know I wrote them correctly in module mode
    if doc.meta['type'] in ['function', 'line magic', 'cell magic']:
        print(f'skipping {docfile}')
        continue

    # convert and evaluate each example
    new_examples = []
    for image, code in doc.examples:
        new_code = convert_to_module_mode(code)
        new_examples.append((image, new_code))

        # check for parsing errors and other problems
        py5_errors = []
        parsing_errors = []
        try:
            # parse and check the original code, which is in imported mode
            problems = parsing.check_reserved_words(ast.parse(code))
            if problems:
                py5_reserved_word_errors += 1
                py5_errors.extend([p.message(code) for p in problems])

            # also try parsing the new code, since that will catch more errors
            ast.parse(new_code)

            # use autopep8 to make output look good
            new_code = autopep8.fix_code(new_code, options={'aggressive': 2})
        except SyntaxError as e:
            ast_syntax_errors += 1
            parsing_errors.append(str(e))

        if py5_errors or parsing_errors:
            problem_files += 1
            print('=' * 100)
            print(f'errors in file {docfile}')
            print('-' * 20)
            print(new_code)
            for s in [*py5_errors, *parsing_errors]:
                print('-' * 20)
                print(s)

    doc.examples = new_examples
    doc.write(docfile)

print('=' * 40)
print(f'there were {ast_syntax_errors} parsing errors.')
print(f'there were {py5_reserved_word_errors} py5 reserved word errors.')
print(f'there are {problem_files} files that need attention.')
