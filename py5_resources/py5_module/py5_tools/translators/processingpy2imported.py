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
from pathlib import Path
from io import StringIO
import re
from tokenize import generate_tokens, untokenize, NAME
import autopep8
from typing import Union
import string

from . import util

# TODO: don't forget about the docstrings!

CONSTANT_CHARACTERS = string.ascii_uppercase + string.digits + '_'

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
    'None': 'None',
    'True': 'True',
    'False': 'False',
    'println': 'print',
}


def _snake_case(name):
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


def translate_code(code):
    result = []
    tokens = generate_tokens(StringIO(code).readline)
    for toknum, tokval, _, _, _ in tokens:
        if toknum == NAME:
            result.append((toknum, _snake_case(tokval)))
        else:
            result.append((toknum, tokval))

    return autopep8.fix_code(autopep8.fix_2to3(untokenize(result)), options=dict(aggressive=2))


def translate_file(src: Union[str, Path], dest: Union[str, Path]):
    src = Path(src)
    dest = Path(dest)

    with open(src, 'r') as f:
        new_code = translate_code(f.read())

    if not dest.parent.exists():
        dest.parent.mkdir(parents=True)

    with open(dest, "w") as f:
        f.write(new_code)


def batch_translate_dir(src: Union[str, Path], dest: Union[str, Path], ext='.pyde'):
    util.batch_translate_dir(translate_file, src, dest, ext)
