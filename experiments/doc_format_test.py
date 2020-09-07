import re
from pathlib import Path

import xmltodict


test_text = """## meta
name = noise()
category = Math
subcategory = Random
type = method

## description
this is awesome

so is this

## example
image = foo.jpg

foo = 10 # asdf
py5.size(10, 20)
py5.rect(1, 2, 3, 4)
"""

DOC_REGEX = re.compile(r'(?<=## )(\w+)\s(.*?)(?=##|$)', re.DOTALL)
META_REGEX = re.compile(r'(\w*) = (.*)')
CODE_REGEX = re.compile(r'image = ([\w\d\.]+)\s+(.*)', re.DOTALL)


class Documentation:

    def __init__(self, filename):
        if not isinstance(filename, Path):
            filename = Path(filename)
        if filename.suffix == '.txt':
            self.meta, self.examples, self.description = self._from_txt_file(filename)
        elif filename.suffix == '.xml':
            self.meta, self.examples, self.description = self._from_xml_file(filename)

    def _from_xml_file(self, filename):
        with open(filename, 'r') as f:
            content = xmltodict.parse(f.read())['root']
        meta = dict()
        examples = []
        description = ''
        for key in content.keys():
            if key == 'description':
                description = content['description']
            elif key == 'example':
                example = content['example']
                if isinstance(example, list):
                    examples = [(x.get('image'), x['code']) for x in example]
                else:
                    examples = [(example.get('image'), example['code'])]
            else:
                meta[key] = content[key]
        return meta, examples, description

    def _from_txt_file(self, filename):
        with open(filename, 'r') as f:
            text = f.read()
        meta = dict()
        examples = []
        description = ''
        for kind, content in DOC_REGEX.findall(text):
            if kind == 'meta':
                meta = dict(META_REGEX.findall(content))
            elif kind == 'example':
                # TODO: this is wrong, there might not be an image
                examples.append(CODE_REGEX.match(content.strip()).groups())
            elif kind == 'description':
                description = content.strip()
        return meta, examples, description


filename1 = 'py5_docs/Reference/api_en/Sketch_tint.xml'
filename2 = 'py5_docs/Reference/api_en/Sketch_bezier_detail.xml'
doc1 = Documentation(filename1)
doc2 = Documentation(filename2)

for filename in Path('py5_docs/Reference/api_en/').glob('*.xml'):
    Documentation(filename)
