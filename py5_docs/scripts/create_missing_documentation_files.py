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
from pathlib import Path

import pandas as pd


NEW_TEMPLATE = """@@ meta
name = {0}
type = {1}
{2}
@@ description
The documentation for this field or method has not yet been written. If you know what it does, please help out with a pull request to the relevant file in https://github.com/py5coding/py5generator/tree/master/py5_docs/Reference/api_en/.

"""

PY5_API_EN = Path('py5_docs/Reference/api_en/')

PY5_CLASS_LOOKUP = {
    'Sketch': 'Sketch',
    'PFont': 'Py5Font',
    'PGraphics': 'Py5Graphics',
    'PImage': 'Py5Image',
    'PShader': 'Py5Shader',
    'PShape': 'Py5Shape',
    'PSurface': 'Py5Surface',
    'KeyEvent': 'Py5KeyEvent',
    'MouseEvent': 'Py5MouseEvent',
    'Py5Functions': 'Py5Functions',
    'Py5Tools': 'Py5Tools',
    'Py5Magics': 'Py5Magics',
    'Py5Vector': 'Py5Vector',
}

# read the class datafiles so I know what methods and fields are relevant
class_data_info = dict()
class_resource_data = Path('py5_resources', 'data')
category_lookup_data = dict()
for pclass in PY5_CLASS_LOOKUP.keys():
    filename = pclass.lower() + '.csv'
    class_data = pd.read_csv(class_resource_data / filename)
    class_data = class_data.fillna('').set_index('processing_name')
    class_data_info[pclass] = class_data.query("implementation!='SKIP'")
    if pclass in ['Sketch', 'Py5Functions', 'Py5Tools', 'Py5Magics']:
        category_lookup_data[pclass] = class_data_info[pclass].set_index('py5_name')[['category', 'subcategory']]

# go through the class data info and for each relevant method and field and 
# identify the new files that must be created
new_doc_files = []
for pclass, class_data in class_data_info.items():
    for processing_name, data in class_data.iterrows():
        py5_name = data['py5_name']
        item_type = data['type']
        if item_type in ['static field', 'unknown']:
            continue

        new_docfile = PY5_API_EN / f'{PY5_CLASS_LOOKUP[pclass]}_{py5_name}.txt'
        if new_docfile.exists():
            continue

        new_doc_files.append((pclass, py5_name, item_type, processing_name, new_docfile))

for num, new_file_data in enumerate(new_doc_files):
    pclass, py5_name, item_type, processing_name, new_docfile = new_file_data
    if item_type == 'dynamic variable':
        doc_type = 'field'
        name = py5_name
    elif item_type == 'class':
        doc_type = 'class'
        name = py5_name
    elif item_type == 'function':
        doc_type = 'function'
        name = py5_name + '()'
    elif item_type == 'cell magic':
        doc_type = 'cell magic'
        name = '%%' + py5_name
    elif item_type == 'line magic':
        doc_type = 'line magic'
        name = '%' + py5_name
    else:
        doc_type = 'method'
        name = py5_name + '()'

    print(f"creating {new_docfile}")
    with open(new_docfile, 'w') as f:
        extra = f'pclass = {pclass}\nprocessing_name = {processing_name}\n' if processing_name else ''
        if pclass in category_lookup_data and py5_name in category_lookup_data[pclass].index:
            category = category_lookup_data[pclass].loc[py5_name, 'category'] or 'None'
            subcategory = category_lookup_data[pclass].loc[py5_name, 'subcategory'] or 'None'
            extra += f'category = {category}\nsubcategory = {subcategory}\n'
        f.write(NEW_TEMPLATE.format(name, doc_type, extra))

print(f'created {len(new_doc_files)} new files.')
