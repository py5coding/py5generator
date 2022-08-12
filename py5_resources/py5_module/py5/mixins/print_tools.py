# *****************************************************************************
#
#   Part of the py5 library
#   Copyright (C) 2020-2022 Jim Schmitz
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

from typing import Any


class PrintlnStream:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._println_stream = None

    def _init_println_stream(self):
        self._println_stream.init()

    # *** BEGIN METHODS ***

    def set_println_stream(self, println_stream: Any) -> None:
        """$class_Sketch_set_println_stream"""
        self._println_stream = println_stream

    def println(self, *args, sep: str = ' ', end: str = '\n', stderr: bool = False) -> None:
        """$class_Sketch_println"""
        msg = sep.join(str(x) for x in args)
        if self._println_stream is None:
            print(msg, end=end, file=sys.stderr if stderr else sys.stdout)
        else:
            self._println_stream.print(msg, end=end, stderr=stderr)
