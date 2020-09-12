import re
from pathlib import Path

import pandas as pd

from generator.docfiles import Documentation


NEW_TEMPLATE = """@@ meta
name = {0}
category = UNKNOWN
subcategory = UNKNOWN
type = {1}

@@ description
new template no description.

@@ example

"""

PROCESSING_API_EN = Path('/home/jim/Projects/ITP/pythonprocessing/processing-docs/content/api_en/')
PY5_API_EN = Path('py5_docs/Reference/api_en/')

PY5_CLASS_LOOKUP = {
    'PApplet': 'Sketch',
    'PFont': 'Py5Font',
    'PGraphics': 'Py5Graphics',
    'PImage': 'Py5Image',
    'PShader': 'Py5Shader',
    'PShape': 'Py5Shape',
    'PSurface': 'Py5Surface',
}


def snake_case(name):
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name)
    return name.lower()


# read the class datafiles so I know what methods and fields are relevant
class_data_info = dict()
class_resource_data = Path('py5_resources', 'data')
for pclass in PY5_CLASS_LOOKUP.keys():
    filename = 'py5applet.csv' if pclass == 'PApplet' else pclass.lower() + '.csv'
    class_data = pd.read_csv(class_resource_data / filename)
    class_data = class_data.fillna('').set_index('processing_name')
    class_data_info[pclass] = class_data.query("available_in_py5==True")


# go through the class data info and for each relevant method and field
# for each find the xml documentation file or note new files that must be created
xml_files = []
new_xml_files = []
for pclass, class_data in class_data_info.items():
    for processing_name, data in class_data.iterrows():
        item_type = data['type']
        implementation_from_processing = data['implementation_from_processing']
        if item_type in ['static field', 'unknown']:
            # skip, we don't care
            continue
        py5_name = data['py5_name']
        if not implementation_from_processing:
            if pclass == 'PApplet':
                # definitely a new function I need to document
                new_xml_files.append((pclass, py5_name, item_type))
            continue

        # first try the correct documentation filename
        if processing_name:
            if pclass == 'PApplet':
                name = f'{processing_name}.xml'
            else:
                name = f'{pclass}_{processing_name}.xml'
            if processing_name == 'hint':
                xml_file = PROCESSING_API_EN / 'include' / name
            else:
                xml_file = PROCESSING_API_EN / name
            if xml_file.exists():
                # documentation exists, copy
                xml_files.append((xml_file, (pclass, py5_name, processing_name)))
                continue

            # usable documentation might be in a different file because of inheritance
            if pclass in ['PApplet', 'PGraphics', 'PImage']:
                for prefix in ['', 'PGraphics_', 'PImage_']:
                    if processing_name == 'hint':
                        xml_file = PROCESSING_API_EN / 'include' / f'{prefix}{processing_name}.xml'
                    else:
                        xml_file = PROCESSING_API_EN / f'{prefix}{processing_name}.xml'
                    if xml_file.exists():
                        break
            if xml_file.exists():
                # documentation exists, and should have already been copied
                continue

        # new documentation that I must write. skip pgraphics so I don't duplicate work
        if pclass not in ['PGraphics', 'PImage']:
            new_xml_files.append((pclass, py5_name, item_type, processing_name))


# # add a few extras
# for py5_name, processing_name in PY5_SKETCH_EXTRAS:
#     xml_file = PROCESSING_API_EN / f'{processing_name}_var.xml'
#     xml_files.append((xml_file, ('PApplet', py5_name, processing_name)))

# copy the relevant xml files to the py5 directory
for xml_file, file_data in xml_files:
    pclass, py5_name, processing_name = file_data
    doc = Documentation(xml_file)
    # TODO: Pythonize the code examples
    # TODO: add extra metadata such as underlying processing field or method because I want to mention this in the documentation
    doc.write(PY5_API_EN / f'{PY5_CLASS_LOOKUP[pclass]}_{py5_name}.txt')

for new_file_data in new_xml_files:
    pclass, py5_name, item_type, *_ = new_file_data
    with open(PY5_API_EN / f'{PY5_CLASS_LOOKUP[pclass]}_{py5_name}.txt', 'w') as f:
        name = py5_name if item_type == 'dynamic variable' else py5_name + '()'
        f.write(NEW_TEMPLATE.format(name, item_type))

print(f'copied {len(xml_files)} files and created {len(new_xml_files)} new files.')
