# *****************************************************************************
#
#   Part of the py5 library
#   Copyright (C) 2020-2021 Jim Schmitz
#
#   This library is free software: you can redistribute it and/or modify it
#   under the terms of the GNU Lesser General Public License as published by
#   the Free Software Foundation, either version 2.1 of the License, or (at
#   your option) any later version.
#
#   This library is distributed in the hope that it will be useful, but
#   WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser
#   General Public License for more details.
#
#   You should have received a copy of the GNU Lesser General Public License
#   along with this library. If not, see <https://www.gnu.org/licenses/>.
#
# *****************************************************************************

# TODO: don't pop open a window for JAVA2D renderer, use HIDDEN renderer instead
# TODO: proper error messages for both syntax / parsing errors and runtime py5 errors
# TODO: use split_setup in py5bot shell
# TODO: use tempfile to get a tempdirectory. "/tmp/" won't work on Windows


_PY5BOT_SETTINGS_FILENAME_ = '/tmp/py5bot_settings_code.py'
_PY5BOT_SETUP_FILENAME_ = '/tmp/py5bot_setup_code.py'

PY5BOT_CODE_INIT = """
# *** PY5BOT_CODE_BYPASS ***

import time as _PY5BOT_time
import ast as _PY5BOT_ast

import py5_tools
py5_tools.set_imported_mode(True)
from py5 import *

_PY5BOT_SETTINGS_FILENAME_ = '{0}'
_PY5BOT_SETUP_FILENAME_ = '{1}'


def settings():
    exec(compile(py5_tools.parsing.transform_py5_code(_PY5BOT_SETTINGS_AST_), filename=_PY5BOT_SETTINGS_FILENAME_, mode='exec'))


def setup():
    global _PY5BOT_OUTPUT_
    _PY5BOT_OUTPUT_ = None

    exec(compile(py5_tools.parsing.transform_py5_code(_PY5BOT_SETUP_AST_), filename=_PY5BOT_SETUP_FILENAME_, mode='exec'))

    from PIL import Image
    load_np_pixels()
    arr = np_pixels()[:, :, 1:]
    _PY5BOT_OUTPUT_ = Image.fromarray(arr)

    exit_sketch()
""".format(_PY5BOT_SETTINGS_FILENAME_, _PY5BOT_SETUP_FILENAME_)


PY5BOT_CODE = """
with open(_PY5BOT_SETTINGS_FILENAME_, 'r') as f:
    _PY5BOT_SETTINGS_AST_ = _PY5BOT_ast.parse(f.read(), filename=_PY5BOT_SETTINGS_FILENAME_, mode='exec')

with open(_PY5BOT_SETUP_FILENAME_, 'r') as f:
    _PY5BOT_SETUP_AST_ = _PY5BOT_ast.parse(f.read(), filename=_PY5BOT_SETUP_FILENAME_, mode='exec')

run_sketch()

while not is_dead:
    _PY5BOT_time.sleep(0.05)
if is_dead_from_error:
    exit_sketch()

_PY5BOT_OUTPUT_
"""


def write_code(settings_code, setup_code):
    with open(_PY5BOT_SETTINGS_FILENAME_, 'w') as f:
        f.write(settings_code)

    with open(_PY5BOT_SETUP_FILENAME_, 'w') as f:
        f.write(setup_code)
