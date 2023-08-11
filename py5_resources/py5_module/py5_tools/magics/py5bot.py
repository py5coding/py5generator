# *****************************************************************************
#
#   Part of the py5 library
#   Copyright (C) 2020-2023 Jim Schmitz
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

from IPython.core.magic import Magics, cell_magic, magics_class
from IPython.core.magic_arguments import (argument, kwds, magic_arguments,
                                          parse_argstring)
from IPython.display import display
from py5jupyter.kernels.py5bot.py5bot import Py5BotManager

from .. import split_setup
from ..parsing import check_for_problems
from .util import CellMagicHelpFormatter, filename_check, variable_name_check


@magics_class
class Py5BotMagics(Magics):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._py5bot_mgr = Py5BotManager()

    @magic_arguments()
    @argument(  # DELETE
        """ DELETE
    $arguments_Py5Magics_py5bot_arguments
    """  # DELETE
    )  # DELETE
    @kwds(formatter_class=CellMagicHelpFormatter)
    @cell_magic
    def py5bot(self, line, cell):
        """$class_Py5Magics_py5bot"""
        args = parse_argstring(self.py5bot, line)

        success, result = check_for_problems(cell, "<py5bot>")
        if success:
            py5bot_globals, py5bot_settings, py5bot_setup = result
            if split_setup.count_noncomment_lines(py5bot_settings) == 0:
                py5bot_settings = "size(100, 100, HIDDEN)"
            self._py5bot_mgr.write_code(
                "\n" + py5bot_globals, py5bot_settings, py5bot_setup
            )

            ns = self.shell.user_ns
            exec(self._py5bot_mgr.startup_code + self._py5bot_mgr.run_code, ns)
            png = ns["_PY5BOT_OUTPUT_"]

            if args.filename:
                filename = filename_check(args.filename)
                png.save(filename)
                print(f"PNG file written to {filename}")
            if args.variable:
                if variable_name_check(args.variable):
                    self.shell.user_ns[args.variable] = png
                    print(f"PIL Image assigned to {args.variable}")
                else:
                    print(f"Invalid variable name {args.variable}", file=sys.stderr)

            if png != None:
                display(png)
            del ns["_PY5BOT_OUTPUT_"]
        else:
            print(result, file=sys.stderr)


def load_ipython_extension(ipython):
    ipython.register_magics(Py5BotMagics)
