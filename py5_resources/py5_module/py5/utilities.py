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
import jpype

from . import spelling


class Py5Utilities:
    """TODO: there should there be a classdoc_Py5Utilities
    """
    def __init__(self, sketch):
        self._instance = jpype.JClass('py5utils.Py5Utilities')(sketch)
        self._dir = list(set(dir(self._instance)) - set('equals getClass hashCode notify notifyAll wait toString'.split()))

    def __str__(self) -> str:
        return f"Py5Utilities()"

    def __repr__(self) -> str:
        return self.__str__()

    def __dir__(self):
        return self._dir

    def __getattr__(self, name):
        if hasattr(self._instance, name):
            return getattr(self._instance, name)
        else:
            raise AttributeError(spelling.error_msg('Py5Utilities', name, self._instance))
