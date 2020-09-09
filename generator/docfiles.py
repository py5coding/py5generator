import re
from pathlib import Path

import xmltodict


DOC_REGEX = re.compile(r'(?<=## )(\w+)\s(.*?)(?=##|$)', re.DOTALL)
META_REGEX = re.compile(r'(\w*)\s*=\s*(.*)')
CODE_REGEX = re.compile(r'image\s*=\s*([\w\d\.]+)\s+(.*)', re.DOTALL)


class Documentation:

    def __init__(self, filename=None):
        self.meta = {}
        self.examples = []
        self.description = ''
        if filename:
            if not isinstance(filename, Path):
                filename = Path(filename)
            with open(filename, 'r') as f:
                content = f.read()
            if filename.suffix == '.txt':
                self.meta, self.examples, self.description = self._from_txt(content)
            elif filename.suffix == '.xml':
                self.meta, self.examples, self.description = self._from_xml(content)
            else:
                raise RuntimeError(f'unable to read {filename}')

    def write(self, filename):
        with open(filename, 'w') as f:
            f.write('## meta\n')
            f.write('\n'.join(f'{m[0]} = {m[1]}' for m in self.meta.items()))
            f.write('\n\n## description\n')
            f.write(f'{self.description}\n')
            for image, code in self.examples:
                f.write('\n## example\n')
                if image:
                    f.write(f'image = {image}\n\n')
                f.write(f'{code}\n')

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
