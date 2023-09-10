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
from jpype import JClass, JInt

_Py5ColorHelper = JClass("py5.core.Py5ColorHelper")


class Py5Color(int):
    def __new__(cls, val, *, creator):
        color = super().__new__(cls, val)
        color._creator = creator
        return color

    def __repr__(self):
        return str(_Py5ColorHelper.repr(self._creator._instance, JInt(self)))

    def __str__(self):
        return self.__repr__()

    def to_hex(self):
        return str(_Py5ColorHelper.toHex(JInt(self)))
