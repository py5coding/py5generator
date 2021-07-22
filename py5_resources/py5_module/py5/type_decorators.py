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
import re
import functools

from jpype.types import JString, JInt


HEX_COLOR_REGEX = re.compile(r'#[0-9A-F]{6}' + chr(36))


def _text_fix_str(f):
    @functools.wraps(f)
    def decorated(self_, *args):
        if isinstance(args[0], str):
            args = [JString(args[0]), *args[1:]]
        return f(self_, *args)

    return decorated


def _ret_str(f):
    @functools.wraps(f)
    def decorated(self_, *args):
        result = f(self_, *args)
        return str(result) if isinstance(result, JString) else result

    return decorated


def _convert_hex_color(indices=[0]):
    def _hex_color(f):
        @functools.wraps(f)
        def decorated(self_, *args):
            args = list(args)
            for i, arg in [(i, args[i]) for i in indices if i < len(args)]:
                if isinstance(arg, str) and HEX_COLOR_REGEX.match(arg.upper()):
                    args[i] = JInt(int("0xFF" + arg[1:], base=16))
                elif isinstance(arg, int) and 0x7FFFFFFF < arg <= 0xFFFFFFFF:
                    args[i] = JInt(arg)
            return f(self_, *args)
        return decorated
    return _hex_color
