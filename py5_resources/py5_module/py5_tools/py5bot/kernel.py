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
import sys
import ast

from IPython.core.interactiveshell import InteractiveShellABC
from ipykernel.kernelapp import IPKernelApp

from traitlets import Type, Instance, Unicode, List

from ..kernel.kernel import Py5Shell, Py5Kernel
from .. import parsing
from . import py5bot

first_run = True


class Py5BotShell(Py5Shell):

    banner2 = Unicode("Activating py5bot").tag(config=True)

    def run_cell(self, raw_cell, store_history=False, silent=False, shell_futures=True):
        if not raw_cell.strip().startswith('# *** PY5BOT_SETUP_CODE ***'):
            # first check for assignments to or deletions of reserved words
            sketch_ast = ast.parse(raw_cell, mode='exec')
            problems = parsing.check_reserved_words(raw_cell, sketch_ast)
            if problems:
                msg = 'There ' + ('is a problem' if len(problems) == 1 else f'are {len(problems)} problems') + ' with your py5bot code'
                msg += '\n' + '=' * len(msg) + '\n' + '\n'.join(problems)
                print(msg, file=sys.stderr)
                return super(Py5BotShell, self).run_cell(
                    'None', store_history=store_history, silent=silent, shell_futures=shell_futures)

            # TODO: this should use split_setup code
            py5bot_settings = raw_cell.split('\n', maxsplit=1)[0]
            py5bot_setup = '\n'.join(raw_cell.splitlines()[1:])
            py5bot.write_code(py5bot_settings, py5bot_setup)
            raw_cell = py5bot.PY5BOT_CODE

        return super(Py5BotShell, self).run_cell(
            raw_cell, store_history=store_history, silent=silent, shell_futures=shell_futures)

InteractiveShellABC.register(Py5BotShell)


class Py5BotKernel(Py5Kernel):
    shell = Instance('IPython.core.interactiveshell.InteractiveShellABC',
                     allow_none=True)
    shell_class = Type(Py5BotShell)

    implementation = 'py5bot'
    implementation_version = '0.4a3.dev0'


class Py5BotApp(IPKernelApp):
    name = 'py5bot-kernel'

    kernel_class = Type('py5_tools.py5bot.Py5BotKernel',
                        klass='ipykernel.kernelbase.Kernel').tag(config=True)

    exec_lines = List(Unicode(), [
        py5bot.PY5BOT_CODE_INIT
    ]).tag(config=True)
