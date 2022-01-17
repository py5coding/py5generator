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
import re
from pathlib import Path


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
            if filename.suffix == '.txt':
                with open(filename, 'r') as f:
                    self.parse(f.read())
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
                f.write('\n\n'.join(self.arguments) + '\n')
            f.write('\n@@ description\n')
            f.write(f'{self.description}\n')
            for image, code in self.examples:
                f.write('\n@@ example\n')
                if image:
                    f.write(f'image = {image}\n\n')
                f.write(f'{code}\n')

    def parse(self, text):
        for kind, content in DOC_REGEX.findall(text):
            if kind == 'meta':
                self.meta = dict(META_REGEX.findall(content))
            elif kind == 'signatures':
                self.signatures.extend(content.strip().splitlines())
            elif kind == 'variables':
                var_desc = [var.split('-', 1) for var in content.strip().splitlines()]
                self.variables.update({k.strip(): v.strip() for k, v in var_desc})
            elif kind == 'arguments':
                self.arguments.extend(content.strip().split('\n\n'))
            elif kind == 'example':
                if m := CODE_REGEX.match(content.strip()):
                    self.examples.append(m.groups())
                else:
                    self.examples.append((None, content.strip()))
            elif kind == 'description':
                self.description = content.strip()
