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
"""
This code was used once to programmatically adjust the documentation files. I
wanted to add links between all reference docs and to put all constants in
fixed width fonts.

The links will need to be adjusted for things like Py5Image.width, which will
try to link to Sketch.width. They will need to be manually adjusted to the
Py5Image version. There will also be other minor issues.
"""
import re
from pathlib import Path

from generator.docfiles import Documentation


PY5_API_EN = Path('py5_docs/Reference/api_en/')
PY5_REFERENCE = re.compile(r'``[a-z_]+[\(\)\[\]]*``')
PY5_ALL_UPPER_CASE = re.compile(r'\s[A-Z_][A-Z_0-9]+[\s,]')

slug_lookup = dict()
for docfile in sorted(PY5_API_EN.glob('*.txt')):
    doc = Documentation(docfile)
    name = doc.meta['name']
    stem = docfile.stem
    if stem == 'Sketch':
        continue
    group = stem.split('_', 1)[0]
    if group in ['Sketch', 'Py5Functions', 'Py5Tools', 'Py5Magics']:
        slug = stem[len(group)+1:].lower()
    else:
        slug = stem.lower()
    slug_lookup[name] = f':doc:`{slug}`'


for docfile in sorted(PY5_API_EN.glob('*.txt')):
    print('=' * 60)
    print(docfile)
    print('-' * 20)

    doc = Documentation(docfile)
    desc = doc.description

    print(desc)

    print('-' * 20)

    for ref in set(PY5_REFERENCE.findall(doc.description)):
        key = ref[2:-2]
        if key == doc.meta['name']:
            continue
        if key not in slug_lookup:
            continue
        print(ref, ':', slug_lookup[key])
        desc = desc.replace(ref, slug_lookup[key])

    print('-' * 20)

    for ref in set(PY5_ALL_UPPER_CASE.findall(doc.description)):
        replacement = f'{ref[0]}``{ref[1:-1]}``{ref[-1]}'
        print(f'[{ref}]', ':', f'[{replacement}]')
        desc = desc.replace(ref, replacement)

    print('-' * 20)
    print(desc)
    doc.description = desc
    # doc.write(docfile)
