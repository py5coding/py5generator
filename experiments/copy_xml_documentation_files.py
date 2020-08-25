import re
import json
from pathlib import Path
from collections import defaultdict

import pandas as pd

import xmltodict


API_EN_DIR = Path('/home/jim/Projects/ITP/pythonprocessing/processing-docs/content/api_en/')


PY5_CLASS_LOOKUP = {
    'PApplet': 'Sketch',
    'PFont': 'Py5Font',
    'PGraphics': 'Py5Graphics',
    'PImage': 'Py5Image',
    'PShader': 'Py5Shader',
    'PShape': 'Py5Shape',
    'PSurface': 'Py5Surface',
}


# read the class datafiles
class_data_info = dict()
class_resource_data = Path('py5_resources', 'data')
for pclass in PY5_CLASS_LOOKUP.keys():
    filename = 'py5applet.csv' if pclass == 'PApplet' else pclass.lower() + '.csv'
    class_data = pd.read_csv(class_resource_data / filename).fillna('').set_index('processing_name')
    class_data_info[pclass] = class_data.query("available_in_py5==True")

count = 0
for pclass, class_data in class_data_info.items():
    for processing_name, data in class_data.iterrows():
        if data['type'] in ['static field', 'unknown']:
            # skip, we don't care
            continue
        py5_name = data['py5_name']
        if not processing_name:
            # definitely a new function I need to document
            count += 1
            print(pclass, py5_name, '*** NONE***')
            continue

        # first try this
        # what about the hint file? it is in PGraphics and PApplet
        xml_file = API_EN_DIR / (f'{processing_name}.xml' if pclass == 'PApplet' else f'{pclass}_{processing_name}.xml')
        if xml_file.exists():
            # documentation exists, copy
            continue

        # might be in a different file
        if pclass in ['PApplet', 'PGraphics', 'PImage']:
            for prefix in ['', 'PGraphics_', 'PImage_']:
                if processing_name == 'hint':
                    xml_file = API_EN_DIR / 'include' / f'{prefix}{processing_name}.xml'
                else:
                    xml_file = API_EN_DIR / f'{prefix}{processing_name}.xml'
                if xml_file.exists():
                    break
        if xml_file.exists():
            # documentation exists, copy
            continue

        # new documentation
        count += 1
        print(pclass, py5_name, processing_name)


# go through class_data_info and copy the relevant xml files from api_en
# when copying I should edit the example code
# if the file does not exist, create a blank file to be edited later

# generate docstrings using these xml descriptions with html removed and other info on parameters and signatures taken from other data files
# later, generate processing-like docs using all the xml files using the existing process

"""
https://github.com/jdf
https://github.com/jdf/processing-py-site/blob/master/Reference/api_en/green.xml
https://py.processing.org/reference/

https://github.com/processing/
https://github.com/processing/processing-docs/tree/master/content/api_en
https://processing.org/reference/createShape_.html
"""
