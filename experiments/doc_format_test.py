import re
from pathlib import Path

import xmltodict


test_text = """## meta
name = noise()
category =Math
subcategory= Random
type=method

## description
this is awesome

so is this

## example
image = foo.jpg

foo = 10 # asdf
py5.size(10, 20)
py5.rect(1, 2, 3, 4)

## example

bar = 10 # asdf
py5.size(100, 200)
py5.rect(1, 2, 3, 4)
"""

DOC_REGEX = re.compile(r'(?<=## )(\w+)\s(.*?)(?=##|$)', re.DOTALL)
META_REGEX = re.compile(r'(\w*)\s?=\s?(.*)')
CODE_REGEX = re.compile(r'image\s?=\s?([\w\d\.]+)\s+(.*)', re.DOTALL)


class Documentation:

    def __init__(self, filename):
        if not isinstance(filename, Path):
            filename = Path(filename)
        with open(filename, 'r') as f:
            content = f.read()
        if filename.suffix == '.txt':
            self.meta, self.examples, self.description = self._from_txt(content)
        elif filename.suffix == '.xml':
            self.meta, self.examples, self.description = self._from_xml(content)

    def _from_xml(self, content):
        xml = xmltodict.parse(content)['root']
        meta = dict()
        examples = []
        description = ''
        for key in xml.keys():
            if key == 'description':
                description = xml['description']
            elif key == 'example':
                example = xml['example']
                if isinstance(example, list):
                    examples = [(x.get('image'), x['code']) for x in example]
                else:
                    examples = [(example.get('image'), example['code'])]
            else:
                meta[key] = xml[key]
        return meta, examples, description

    def _from_txt(self, text):
        meta = dict()
        examples = []
        description = ''
        for kind, content in DOC_REGEX.findall(text):
            if kind == 'meta':
                meta = dict(META_REGEX.findall(content))
            elif kind == 'example':
                if m := CODE_REGEX.match(content.strip()):
                    examples.append(m.groups())
                else:
                    examples.append((None, content.strip()))
            elif kind == 'description':
                description = content.strip()
        return meta, examples, description


filename1 = 'py5_docs/Reference/api_en/Sketch_tint.xml'
filename2 = 'py5_docs/Reference/api_en/Sketch_bezier_detail.xml'
doc1 = Documentation(filename1)
doc2 = Documentation(filename2)

filename3 = '/tmp/test_text.txt'
with open(filename3, 'w') as f:
    f.write(test_text)
doc3 = Documentation(filename3)

for filename in Path('py5_docs/Reference/api_en/').glob('*.xml'):
    Documentation(filename)
