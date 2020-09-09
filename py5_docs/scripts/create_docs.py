import re
import json
from pathlib import Path
from collections import defaultdict

import pandas as pd

import xmltodict


CODE_REGEX = re.compile(r'(`[^`]*`)')

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


class DocData:

    def __init__(self):
        self.vars = dict()
        self.see_also = []

    def _text_cleanup(self, text):
        for c in CODE_REGEX.findall(text):
            new_c = snake_case(c)
            new_c = re.sub(r';\s*', '\n', new_c)
            new_c = new_c.replace(',', '')
            text = text.replace(c, new_c)
        # fix the backticks
        text = text.replace('`', '``')
        text = re.sub('`{3,}', '``', text)
        for pname, py5name in PY5_CLASS_LOOKUP.items():
            text = text.replace(pname, py5name)
            # this second fixes what the snake_function does to code
            text = text.replace(snake_case(pname), py5name)
        return text

    def report_param(self, varname, vardesc):
        self.vars[varname] = vardesc

    def report_see_also(self, classname, call):
        self.see_also.append((classname, self._text_cleanup(call)))

    def get_see(self, docdata):
        out = []
        for classname, call in self.see_also:
            see = f'{classname}.{call}'
            key = (classname, call.split('(', 1)[0])
            if key in docdata:
                see += ' : ' + docdata[key].first
            out.append(see)
        return '\n\n'.join(out)


# load the javadocs information
filename = 'py5_docs/docfiles/javadocs.xml'
with open(filename, 'r') as f:
    root = xmltodict.parse(f.read())

# read the class datafiles
class_data_info = dict()
class_resource_data = Path('py5_resources', 'data')
for pclass in PY5_CLASS_LOOKUP.keys():
    filename = 'py5applet.csv' if pclass == 'PApplet' else pclass.lower() + '.csv'
    class_data = pd.read_csv(class_resource_data / filename).fillna('').set_index('processing_name')
    class_data_info[pclass] = class_data.query("implementation_from_processing==True")['py5_name']

# where the documentation data will be organized and stored
docdata = defaultdict(DocData)

for commenttree in root['commenttrees']['commenttree']:
    pclass = commenttree['@class'].split('.')[-1]
    # only generate comments for classes and methods that are actually used
    if pclass not in PY5_CLASS_LOOKUP.keys():
        continue
    if commenttree['@name'] in class_data_info[pclass]:
        py5name = class_data_info[pclass][commenttree['@name']]
    else:
        continue

    py5class = PY5_CLASS_LOOKUP[pclass]
    kind = commenttree['@kind']

    fdata = docdata[(py5class, kind, py5name)]

    blocktags = commenttree['blocktags']
    if blocktags:
        tags = blocktags['blocktag']
        if isinstance(tags, str):
            tags = [tags]
        for tag in [t[7:] for t in tags if t.startswith('@param ')]:
            tokens = tag.split(' ', 1)
            if len(tokens) == 2:
                fdata.report_param(*tokens)
        for tag in [t[5:] for t in tags if t.startswith('@see ')]:
            tokens = tag.split('#', 1)
            if len(tokens) == 2:
                fdata.report_see_also(PY5_CLASS_LOOKUP.get(tokens[0], py5class), tokens[1])


variable_descriptions = defaultdict(dict)
docstrings = []
for (py5class, kind, py5name), fdata in sorted(docdata.items()):
    for var, desc in fdata.vars.items():
        variable_descriptions[f'{py5class}_{py5name}'][snake_case(var)] = desc

with open('/tmp/variable_descriptions.json', 'w') as f:
    json.dump(variable_descriptions, f, indent=2)
