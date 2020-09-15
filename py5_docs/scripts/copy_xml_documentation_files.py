import re
from pathlib import Path
from io import StringIO
import string
import shlex
from html.parser import HTMLParser

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

SNAKE_CASE_OVERRIDE = {
    'null': 'None',
    'true': 'True',
    'false': 'False',
}

CONSTANT_CHARACTERS = string.ascii_uppercase + string.digits + '_'


def snake_case(name):
    if all([c in CONSTANT_CHARACTERS for c in list(name)]):
        return name
    if re.match(r'0x[\da-fA-F]{2,}', name):
        return name
    elif (stem := name.replace('()', '')) in PY5_CLASS_LOOKUP:
        return name.replace(stem, PY5_CLASS_LOOKUP[stem])
    elif name in SNAKE_CASE_OVERRIDE:
        return SNAKE_CASE_OVERRIDE[name]
    else:
        name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name)
        return name.lower()


def convert_to_python(code):
    code = code.replace('println', 'print')
    code = code.replace('//', '#')

    # convert function declarations
    code = re.sub(r'void\s+(\w+)\(([\w\s]*)\)\s*{', r'def \1(\2):', code)

    # convert if statements
    code = re.sub(r'if\s+\((.+?)\)\s*{', r'if \1:', code)
    code = code.replace('} else if', 'elif')
    code = code.replace('} else {', 'else:')

    # convert for loops to range iteration
    for m in re.finditer(r'for \(\w+\s+(\w+)\s*=\s*(\d+); \1\s*([<=>]+)\s*([^;]+);\s*\1\s*([^\)]*)\)\s*{', code):
        end = m.group(4) + ('' if m.group(3) == '<' else ' + 1')
        step = '' if (step := m.group(5)) == '++' else f",{step.split('=')[1]}"
        code = code.replace(m.group(), f'for {m.group(1)} = range({m.group(2)}, {end}{step}):')

    # convert variable declarations
    # this converts declarations with assignments
    for m in re.finditer(r'^(\s*)([\w\[\]]+) +(\w+)\s*=', code, flags=re.MULTILINE):
        if m.group(2) in {'for', 'if'}:
            continue
        else:
            code = code.replace(m.group(), f'{m.group(1)}{m.group(3)} =')

    # this removes declarations without assignments but adds global statement to setup if it is present
    global_vars = []
    for m in re.finditer(r'^[\w\[\]]+ +([\w #\d;]+)$', code, flags=re.MULTILINE):
        global_vars.append(m.group(1))
        code = code.replace(m.group(), '')

    if global_vars:
        replacement = '\n'.join([f'  global {g}' for g in global_vars])
        code = code.replace('def setup():', f'def setup():\n{replacement}')

    # convert x.length to len(x)
    code = re.sub(r'([\w\.]+)\.length', r'len(\1)', code)

    # get rid of the closing braces
    code = re.sub(r'^\s*}', '', code, flags=re.MULTILINE)

    # indenting spacing == 4
    code = re.sub(r'^( +)(?!$)', r'\1\1', code, flags=re.MULTILINE)

    # because of course ;)
    code = code.replace(';', '')

    return code


def adjust_code(code):
    if code == '#':
        return code
    code = re.sub(r'#(?=[\da-fA-F]{2,})', '0x', code)
    tokens = shlex.shlex(code)
    tokens.whitespace = ''
    new_code = StringIO()
    for token in tokens:
        if token[0] in {'"'}:
            new_code.write(token)
        else:
            new_code.write(snake_case(token))

    code = new_code.getvalue()
    code = convert_to_python(code)

    return code


class TagRemover(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = StringIO()
        self._in_code_block = False
        self._tag_list = set()

    def handle_starttag(self, tag, attrs):
        if tag in {'b', 'tt', 'strong', 'pre'}:
            self.text.write('``')
            self._in_code_block = True
        elif tag in {'i', 'em'}:
            self.text.write('*')
        elif tag in {'a', 'br'}:
            pass
        else:
            self._tag_list.add(tag)

    def handle_endtag(self, tag):
        # documentation erroniously uses </s> to end some <b> tags
        if tag in {'b', 's', 'tt', 'strong', 'pre'}:
            self.text.write('``')
            self._in_code_block = False
        elif tag in {'i', 'em'}:
            self.text.write('*')
        elif tag in {'br', 'a'}:
            pass
        else:
            self._tag_list.add(tag)

    def handle_data(self, d):
        if self._in_code_block:
            self.text.write(adjust_code(d))
        else:
            self.text.write(d)

    def get_data(self):
        if self._tag_list:
            print(self._tag_list)
        return self.text.getvalue()


def remove_html(html):
    # remove html tags and do some conversions
    tr = TagRemover()
    tr.feed(html)
    text = tr.get_data()
    # find text that looks like a function reference
    while m := re.search(r'(?<!`)(\w+\(\))(?!`)', text):
        text = text[:m.start()] + f'``{snake_case(m.group())}``' + text[m.end():]

    return text


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


# copy the relevant xml files to the py5 directory
for xml_file, file_data in xml_files:
    pclass, py5_name, processing_name = file_data
    doc = Documentation(xml_file)
    doc.description = remove_html(doc.description)
    doc.meta['processing_name'] = processing_name
    doc.meta['name'] = doc.meta['name'].replace(processing_name, py5_name)
    new_examples = []
    for image_name, code in doc.examples:
        new_examples.append((image_name, adjust_code(code)))
    doc.examples = new_examples
    doc.write(PY5_API_EN / f'{PY5_CLASS_LOOKUP[pclass]}_{py5_name}.txt')

for new_file_data in new_xml_files:
    pclass, py5_name, item_type, *_ = new_file_data
    with open(PY5_API_EN / f'{PY5_CLASS_LOOKUP[pclass]}_{py5_name}.txt', 'w') as f:
        name = py5_name if item_type == 'dynamic variable' else py5_name + '()'
        f.write(NEW_TEMPLATE.format(name, item_type))

print(f'copied {len(xml_files)} files and created {len(new_xml_files)} new files.')
