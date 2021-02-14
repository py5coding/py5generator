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


def convert_to_module_mode2(code):
    """convert functionless example code to something with a settings and a setup
    """
    lines = code.splitlines()
    has_functions = any(code.find(f'def {f}():') >= 0 for f in ['settings', 'setup', 'draw'])

    if has_functions:
        # skip calls for the default size
        new_code = '\n'.join(l for l in lines if l.find('py5.size(100, 100)') == -1)

        return new_code
    else:
        settings_lines = []
        setup_lines = []
        # calls to settings, pixel_density, smooth, etc. need to go to settings
        for line in lines:
            if any(line.find(f'py5.{f}') >= 0 for f in ['size', 'full_screen', 'no_smooth', 'smooth', 'pixel_density']):
                # skip calls for the default size
                if line.find('py5.size(100, 100)') >= 0:
                    continue
                settings_lines.append(line)
            else:
                setup_lines.append(line)

        out = StringIO()

        def write_indented_function(fname, code_lines):
            out.write(f"def {fname}():\n")
            out.writelines(f'    {l}\n' for l in code_lines)
            out.write('\n\n')

        if settings_lines:
            write_indented_function('settings', settings_lines)

        if setup_lines:
            write_indented_function('setup', setup_lines)

        return out.getvalue().strip()


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
        new_code = convert_to_module_mode2(code)
        new_examples.append((image, new_code))

        # check for parsing errors and other problems
        try:
            # try parsing the new code, since that will catch errors
            ast.parse(new_code)

            # use autopep8 to make output look good
            new_code = autopep8.fix_code(new_code, options={'aggressive': 2})
        except SyntaxError as e:
            problem_files += 1
            print('=' * 100)
            print(f'errors in file {docfile}')
            print('-' * 20)
            print(new_code)
            print('-' * 20)
            print(e)

    doc.examples = new_examples
    doc.write(docfile)

print('=' * 40)
print(f'there are {problem_files} files that need attention.')
