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
from pathlib import Path
import re


from generator.docfiles import Documentation


PY5_API_EN = Path('py5_docs/Reference/api_en/')


LINK_REGEX = re.compile(r':doc:`(\w+)`')


for docfile in sorted(PY5_API_EN.glob('*.txt')):
# for docfile in list(sorted(PY5_API_EN.glob('*.txt')))[:10]:
    doc = Documentation(docfile)
    desc = doc.description

    # there's only one file (Py5Shape_set_visible.txt) that contains a variable
    # description with rest. Adjust it manually
    for _, var_desc in sorted(doc.variables.items()):
        if var_desc.find(':doc:') >= 0 or var_desc.find('`') >= 0 or var_desc.find('*') >= 0:
            print(docfile, var_desc)

    # convert ``x = 42`` to `x = 42`
    desc = desc.replace('``', '`')

    # convert :doc:`sketch_screen_y` to [](sketch_screen_y)
    desc = LINK_REGEX.sub(r'[](\1)', desc)

    doc.description = desc
    doc.write(docfile)
