import re
from pathlib import Path

import pandas as pd

from generator.docfiles import Documentation


NEW_TEMPLATE = """## meta
name = 
category = 
subcategory = 
type = 

## description


## example
image = 

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


PY5_SKETCH_EXTRAS = [
    # don't do these because I want new files to be created
    # ('get_frame_rate', 'frameRate'),
    # ('is_key_pressed', 'keyPressed'),
    # ('is_mouse_pressed', 'mousePressed'),
]


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
        if item_type in ['static field', 'unknown']:
            # skip, we don't care
            continue
        py5_name = data['py5_name']
        if not processing_name:
            # definitely a new function I need to document
            new_xml_files.append((pclass, py5_name, item_type))
            continue

        # these will be added manually; don't want them added to new_xml_files
        if py5_name in {x[0] for x in PY5_SKETCH_EXTRAS}:
            continue

        # first try the correct documentation filename
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
        if pclass != 'PGraphics':
            new_xml_files.append((pclass, py5_name, item_type, processing_name))


# add a few extras
for py5_name, processing_name in PY5_SKETCH_EXTRAS:
    xml_file = PROCESSING_API_EN / f'{processing_name}_var.xml'
    xml_files.append((xml_file, ('PApplet', py5_name, processing_name)))

# copy the relevant xml files to the py5 directory
for xml_file, file_data in xml_files:
    pclass, py5_name, processing_name = file_data
    doc = Documentation(xml_file)
    doc.write(PY5_API_EN / f'{PY5_CLASS_LOOKUP[pclass]}_{py5_name}.txt')
    # TODO: add extra metadata and Pythonize the code example
    # TODO: should I and can I convert to a different format like yaml or toml? I can't do json
    # TODO: add underlying processing field or method to metadata because I want to mention this in the documentation

for new_file_data in new_xml_files:
    pclass, py5_name, item_type, *_ = new_file_data
    with open(PY5_API_EN / f'{PY5_CLASS_LOOKUP[pclass]}_{py5_name}.txt', 'w') as f:
        name = py5_name if item_type == 'dynamic variable' else py5_name + '()'
        f.write(NEW_TEMPLATE.format(name, item_type))

print(f'copied {len(xml_files)} files and created {len(new_xml_files)} new files.')


# generate docstrings using these xml descriptions with html removed and other info on parameters and signatures taken from other data files
# later, generate processing-like docs using all the xml files by learning from the existing process
# use the xml files to make rst files that I can then use in a nikola website
