# *****************************************************************************
#
#   Part of the py5generator project; generator of the py5 library
#   Copyright (C) 2020-2021 Jim Schmitz
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
import re
from pathlib import Path

import xmltodict


DOC_REGEX = re.compile(r'(?<=@@ )(\w+)\s(.*?)(?=@@|$)', re.DOTALL)
META_REGEX = re.compile(r'(\w*)\s*=\s*(.*)')
CODE_REGEX = re.compile(r'image\s*=\s*([\w\d\.]+)\s+(.*)', re.DOTALL)


class Documentation:

    def __init__(self, filename=None):
        self.meta = {}
        self.examples = []
        self.signatures = []
        self.variables = {}
        self.arguments = []
        self.description = ''
        if filename:
            if not isinstance(filename, Path):
                filename = Path(filename)
            with open(filename, 'r') as f:
                content = f.read()
            if filename.suffix == '.txt':
                self.meta, self.signatures, self.variables, self.arguments, self.examples, self.description = self._from_txt(content)
            elif filename.suffix == '.xml':
                self.meta, self.examples, self.description = self._from_xml(content)
            else:
                raise RuntimeError(f'unable to read {filename}')

    def write(self, filename):
        filename = Path(filename)
        if not filename.parent.exists():
            filename.parent.mkdir(parents=True)
        with open(filename, 'w') as f:
            f.write('@@ meta\n')
            f.write('\n'.join(f'{m[0]} = {m[1]}' for m in self.meta.items()) + '\n')
            if self.signatures:
                f.write('\n@@ signatures\n')
                for signature in sorted(self.signatures):
                    f.write(f'{signature}\n')
            if self.variables:
                f.write('\n@@ variables\n')
                for var, desc in sorted(self.variables.items()):
                    f.write(f'{var} - {desc}\n')
            if self.arguments:
                f.write('\n@@ arguments\n')
                for argument in self.arguments:
                    f.write(f'{argument}\n')
            f.write('\n@@ description\n')
            f.write(f'{self.description}\n')
            for image, code in self.examples:
                f.write('\n@@ example\n')
                if image:
                    f.write(f'image = {image}\n\n')
                f.write(f'{code}\n')

    def _from_xml(self, content):
        xml = xmltodict.parse(content)['root']
        meta = {}
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
        # clean up the type metadata
        if meta['name'].endswith('()'):
            meta['type'] = 'method'
        elif meta['name'][0].isupper():
            meta['type'] = 'class'
        else:
            meta['type'] = 'field'
        return meta, examples, description

    def _from_txt(self, text):
        meta = {}
        signatures = []
        variables = {}
        arguments = []
        examples = []
        description = ''
        for kind, content in DOC_REGEX.findall(text):
            if kind == 'meta':
                meta = dict(META_REGEX.findall(content))
            elif kind == 'signatures':
                signatures.extend(content.strip().split('\n'))
            elif kind == 'variables':
                var_desc = [var.split('-', 1) for var in content.strip().split('\n')]
                variables.update({k.strip(): v.strip() for k, v in var_desc})
            elif kind == 'arguments':
                arguments.extend(content.strip().split('\n'))
            elif kind == 'example':
                if m := CODE_REGEX.match(content.strip()):
                    examples.append(m.groups())
                else:
                    examples.append((None, content.strip()))
            elif kind == 'description':
                description = content.strip()
        return meta, signatures, variables, arguments, examples, description
