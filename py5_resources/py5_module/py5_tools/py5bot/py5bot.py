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
import ast
import re

import stackprinter

from .. import parsing
from .. import split_setup


PY5BOT_CODE_STARTUP = """
import time as _PY5BOT_time
import ast as _PY5BOT_ast
import functools

import py5_tools
py5_tools.set_imported_mode(True)
import py5_tools.parsing as _PY5BOT_parsing
from py5 import *


def _change_renderer(f):
    @functools.wraps(f)
    def decorated(*args):
        if len(args) == 2:
            args = *args, HIDDEN
        f(*args)
    return decorated

size = _change_renderer(size)

del _change_renderer
del functools
"""


PY5BOT_CODE = """
_PY5BOT_OUTPUT_ = None


def settings():
    with open('{0}', 'r') as f:
        exec(
            compile(
                _PY5BOT_parsing.transform_py5_code(
                    _PY5BOT_ast.parse(f.read(), filename='{0}', mode='exec'),
                ),
                filename='{0}',
                mode='exec'
            )
        )


def setup():
    global _PY5BOT_OUTPUT_

    with open('{1}', 'r') as f:
        exec(
            compile(
                _PY5BOT_parsing.transform_py5_code(
                    _PY5BOT_ast.parse(f.read(), filename='{1}', mode='exec'),
                ),
                filename='{1}',
                mode='exec'
            )
        )

    from PIL import Image
    load_np_pixels()
    arr = np_pixels()[:, :, 1:]
    _PY5BOT_OUTPUT_ = Image.fromarray(arr)

    exit_sketch()


run_sketch()

while not is_dead:
    _PY5BOT_time.sleep(0.05)
if is_dead_from_error:
    exit_sketch()

_PY5BOT_OUTPUT_
"""


def check_for_problems(code):
    # does the code parse? if not, return an error message
    try:
        sketch_ast = None
        sketch_ast = ast.parse(code, filename="py5bot.py", mode='exec')
    except Exception as e:
        msg = stackprinter.format(e)
        m = re.search(r'^SyntaxError:', msg, flags=re.MULTILINE)
        if m:
            msg = msg[m.start(0):]
        msg = 'There is a problem with your code:\n' + msg
        return False, msg

    # check for assignments to or deletions of reserved words
    problems = parsing.check_reserved_words(code, sketch_ast)
    if problems:
        msg = 'There ' + ('is a problem' if len(problems) == 1 else f'are {len(problems)} problems') + ' with your code.\n'
        msg += '=' * len(msg) + '\n' + '\n'.join(problems)
        return False, msg

    cutoff = split_setup.find_cutoff(code, 'imported')
    py5bot_settings = '\n'.join(code.splitlines()[:cutoff])
    py5bot_setup = '\n'.join(code.splitlines()[cutoff:])

    # check for calls to size, etc, that were not at the beginning of the code
    problems = split_setup.check_for_special_functions(py5bot_setup, 'imported')
    if problems:
        msg = 'There ' + ('is a problem' if len(problems) == 1 else f'are {len(problems)} problems') + ' with your code.\n'
        msg += 'The function ' + ('call' if len(problems) == 1 else 'calls') + ' to '
        problems = [f'{name} (on line {i + 1})' for i, name in problems]
        if len(problems) == 1:
            msg += problems[0]
        elif len(problems) == 2:
            msg += f'{problems[0]} and {problems[1]}'
        else:
            msg += ', and '.join(', '.join(problems).rsplit(', ', maxsplit=1))
        msg += ' must be moved to the beginning of your code, before any other code.'
        return False, msg

    return True, (py5bot_settings, py5bot_setup)


class Py5BotManager:

    def __init__(self):
        tempdir = Path(tempfile.TemporaryDirectory().name)
        tempdir.mkdir(parents=True, exist_ok=True)
        self.settings_filename = tempdir / '_PY5_STATIC_SETTINGS_CODE_.py'
        self.setup_filename = tempdir / '_PY5_STATIC_SETUP_CODE_.py'
        self.startup_code = PY5BOT_CODE_STARTUP
        self.run_code = PY5BOT_CODE.format(self.settings_filename, self.setup_filename)

    def write_code(self, settings_code, setup_code):
        with open(self.settings_filename, 'w') as f:
            f.write(settings_code)

        with open(self.setup_filename, 'w') as f:
            f.write(setup_code)
