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
import re

from IPython.core.interactiveshell import InteractiveShellABC
from ipykernel.kernelapp import IPKernelApp

from traitlets import Type, Instance, Unicode, List

import stackprinter

from ..kernel.kernel import Py5Shell, Py5Kernel
from .. import parsing
from .. import split_setup
from . import py5bot

first_run = True


class Py5BotShell(Py5Shell):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._py5bot_mgr = py5bot.Py5BotManager()

    banner2 = Unicode("Activating py5bot").tag(config=True)

    def run_cell(self, raw_cell, store_history=False, silent=False, shell_futures=True):
        # check for special code that should bypass py5bot processing
        if raw_cell.strip().startswith('# *** PY5BOT_CODE_BYPASS ***'):
            return super(Py5BotShell, self).run_cell(
                raw_cell, store_history=store_history, silent=silent, shell_futures=shell_futures)

        # does the code parse? if not, display an error message
        try:
            sketch_ast = None
            sketch_ast = ast.parse(raw_cell, filename="py5bot.py", mode='exec')
        except Exception as e:
            msg = stackprinter.format(e)
            m = re.search(r'^SyntaxError:', msg, flags=re.MULTILINE)
            if m:
                msg = msg[m.start(0):]
            msg = 'py5bot encountered an error in your code:\n' + msg
            print(msg, file=sys.stderr)

            return super(Py5BotShell, self).run_cell(
                'None', store_history=False, silent=silent, shell_futures=shell_futures)

        # check for assignments to or deletions of reserved words
        problems = parsing.check_reserved_words(raw_cell, sketch_ast)
        if problems:
            msg = 'There ' + ('is a problem' if len(problems) == 1 else f'are {len(problems)} problems') + ' with your py5bot code.\n'
            msg += '=' * len(msg) + '\n' + '\n'.join(problems)
            print(msg, file=sys.stderr)
            return super(Py5BotShell, self).run_cell(
                'None', store_history=False, silent=silent, shell_futures=shell_futures)

        cutoff = split_setup.find_cutoff(raw_cell, 'imported')
        py5bot_settings = '\n'.join(raw_cell.splitlines()[:cutoff])
        py5bot_setup = '\n'.join(raw_cell.splitlines()[cutoff:])

        problems = split_setup.check_for_special_functions(py5bot_setup, 'imported')
        if problems:
            msg = 'There ' + ('is a problem' if len(problems) == 1 else f'are {len(problems)} problems') + ' with your py5bot code.\n'
            msg += 'The function ' + ('call' if len(problems) == 1 else 'calls') + ' to '
            problems = [f'{name} (on line {i})' for i, name in problems]
            if len(problems) == 1:
                msg += problems[0]
            elif len(problems) == 2:
                msg += f'{problems[0]} and {problems[1]}'
            else:
                msg += ', and '.join(', '.join(problems).rsplit(', ', maxsplit=1))
            msg += ' must be moved to the top of the code cell, before any other code.'
            print(msg, file=sys.stderr)
            return super(Py5BotShell, self).run_cell(
                'None', store_history=False, silent=silent, shell_futures=shell_futures)


        if split_setup.count_noncomment_lines(py5bot_settings) == 0:
            py5bot_settings = 'size(100, 100, HIDDEN)'
        self._py5bot_mgr.write_code(py5bot_settings, py5bot_setup)

        return super(Py5BotShell, self).run_cell(
            self._py5bot_mgr.run_cell_code, store_history=store_history, silent=silent, shell_futures=shell_futures)

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
        '# *** PY5BOT_CODE_BYPASS ***\n' + py5bot.PY5BOT_CODE_STARTUP
    ]).tag(config=True)
