# *****************************************************************************
#
#   Part of the py5generator project; generator of the py5 library
#   Copyright (C) 2020-2022 Jim Schmitz
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
This code is no longer used but might be pillaged one day to help work with
the documentation example code.

This code was used once to combine the settings and setup functions in the
example code when the code change was made to allow calls to size() in the
user's setup() function.
"""
import re
import autopep8
from pathlib import Path

from generator.docfiles import Documentation


PY5_API_EN = Path('py5_docs/Reference/api_en/')


SETUP_CODE_REGEX = re.compile(r'^def setup\(\):.*?(?=^\w|\Z)', flags=re.MULTILINE | re.DOTALL)
SETTINGS_CODE_REGEX = re.compile(r'^def settings\(\):.*?(?=^\w|\Z)', flags=re.MULTILINE | re.DOTALL)


problem_files = 0
for docfile in sorted(PY5_API_EN.glob('*.txt')):
    doc = Documentation(docfile)

    new_examples = []

    for image, code in doc.examples:
        has_setup = SETUP_CODE_REGEX.search(code)
        has_settings = SETTINGS_CODE_REGEX.search(code)

        if has_setup and has_settings:
            settings_code = has_settings.group().strip()
            setup_code = has_setup.group().strip()
            settings_lines = settings_code.split('\n')
            setup_lines = setup_code.split('\n')

            new_setup = '\n'.join([setup_lines[0], *settings_lines[1:], *setup_lines[1:]])

            new_code = code.replace(setup_code, '').replace(settings_code, new_setup)
            new_code = autopep8.fix_code(new_code, options=dict(aggressive=2)).strip()

            new_examples.append((image, new_code))

            print('*' * 40)
            print(new_code)

        elif has_settings:
            new_code = code.replace('def settings()', 'def setup()').strip()

            new_examples.append((image, new_code))

            print('*' * 40)
            print(new_code)
        else:
            new_examples.append((image, code.strip()))

    doc.examples = new_examples
    doc.write(docfile)
