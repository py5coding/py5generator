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
import shlex
import autopep8
from typing import Union
import string

from . import util

# TODO: don't forget about the docstrings!
# TODO: refactor this, only translate_token is specific to this task, move rest to util

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


def translate_token(token):
    if all([c in CONSTANT_CHARACTERS for c in list(token)]):
        return token
    if re.match(r'0x[\da-fA-F]{2,}', token):
        return token
    elif (stem := token.replace('()', '')) in PY5_CLASS_LOOKUP:
        return token.replace(stem, PY5_CLASS_LOOKUP[stem])
    elif token in SNAKE_CASE_OVERRIDE:
        return SNAKE_CASE_OVERRIDE[token]
    else:
        token = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', token)
        token = re.sub('([a-z0-9])([A-Z])', r'\1_\2', token)
        return token.lower()


def translate_code(code):
    tokens = shlex.shlex(code)
    tokens.whitespace = ''
    tokens.wordchars += '.'
    tokens.commenters = ''
    tokens.quotes = ''

    out = StringIO()
    in_comment = False
    in_quote = None
    for token in tokens:
        if token in ["'", '"'] and not in_comment:
            if not in_quote:
                in_quote = token
            elif in_quote and token == in_quote:
                in_quote = None
        elif token == '#':
            in_comment = True
        elif token == '\n':
            in_comment = False
            in_quote = None
        elif not (in_comment or in_quote):
            token = translate_token(token)

        out.write(token)

    return autopep8.fix_code(out.getvalue(), options=dict(aggressive=2))


def translate_file(src: Union[str, Path], dest: Union[str, Path]):
    src = Path(src)
    dest = Path(dest)

    with open(src, 'r') as f:
        new_code = translate_code(f.read())

    if not dest.parent.exists():
        dest.parent.mkdir(parents=True)

    with open(dest, "w") as f:
        f.write(new_code)


def translate_dir(src: Union[str, Path], dest: Union[str, Path], ext='.pyde'):
    util.batch_translate_dir(translate_file, src, dest, ext)


__ALL__ = ['translate_token', 'translate_code', 'translate_file', 'translate_dir']

def __dir__():
    return __ALL__
