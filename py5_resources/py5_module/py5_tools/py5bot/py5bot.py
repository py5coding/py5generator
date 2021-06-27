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
from pathlib import Path
import tempfile

# TODO: don't pop open a window for JAVA2D renderer, use HIDDEN renderer instead
# TODO: proper error messages for both syntax / parsing errors and runtime py5 errors
# TODO: use split_setup in py5bot shell


PY5BOT_CODE_INIT = """
# *** PY5BOT_CODE_BYPASS ***

import time as _PY5BOT_time
import ast as _PY5BOT_ast

import py5_tools
py5_tools.set_imported_mode(True)
from py5 import *


_PY5BOT_OUTPUT_ = None


def settings():
    exec(compile(py5_tools.parsing.transform_py5_code(_PY5BOT_SETTINGS_AST_), filename='{0}', mode='exec'))


def setup():
    global _PY5BOT_OUTPUT_
    _PY5BOT_OUTPUT_ = None

    exec(compile(py5_tools.parsing.transform_py5_code(_PY5BOT_SETUP_AST_), filename='{1}', mode='exec'))

    from PIL import Image
    load_np_pixels()
    arr = np_pixels()[:, :, 1:]
    _PY5BOT_OUTPUT_ = Image.fromarray(arr)

    exit_sketch()
"""


PY5BOT_CODE = """
with open('{0}', 'r') as f:
    _PY5BOT_SETTINGS_AST_ = _PY5BOT_ast.parse(f.read(), filename='{0}', mode='exec')

with open('{1}', 'r') as f:
    _PY5BOT_SETUP_AST_ = _PY5BOT_ast.parse(f.read(), filename='{1}', mode='exec')

run_sketch()

while not is_dead:
    _PY5BOT_time.sleep(0.05)
if is_dead_from_error:
    exit_sketch()

_PY5BOT_OUTPUT_
"""


class Py5BotManager:

    def __init__(self):
        tempdir = Path(tempfile.TemporaryDirectory().name)
        tempdir.mkdir(parents=True, exist_ok=True)
        self.settings_filename = tempdir / 'py5bot_settings_code.py'
        self.setup_filename = tempdir / 'py5bot_setup_code.py'
        self.init_code = PY5BOT_CODE_INIT.format(self.settings_filename, self.setup_filename)
        self.run_cell_code = PY5BOT_CODE.format(self.settings_filename, self.setup_filename)
        self.initialized = False

    def write_code(self, settings_code, setup_code):
        with open(self.settings_filename, 'w') as f:
            f.write(settings_code)

        with open(self.setup_filename, 'w') as f:
            f.write(setup_code)
