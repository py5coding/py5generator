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
# *** FORMAT PARAMS ***
import functools
from typing import overload, Any  # noqa
import weakref

from .image import Py5Image  # noqa
from . import spelling


py5surface_class_members_code = None  # DELETE


def _return_py5surface(f):
    @functools.wraps(f)
    def decorated(self_, *args):
        return Py5Surface(f(self_, *args))
    return decorated


class Py5Surface:
    """$classdoc_Py5Surface
    """
    _py5_object_cache = weakref.WeakSet()

    def __new__(cls, psurface):
        for o in cls._py5_object_cache:
            if psurface == o._instance:
                return o
        else:
            o = object.__new__(Py5Surface)
            o._instance = psurface
            cls._py5_object_cache.add(o)
            return o

    def __str__(self) -> str:
        return f"Py5Surface(id=" + str(id(self)) + ")"

    def __repr__(self) -> str:
        return self.__str__()

    def __getattr__(self, name):
        msg = 'Py5Surface objects have no fields or methods named "' + name + '"'
        if (suggestions := spelling.suggestions(name, set(dir(self)))):
            msg += '. Did you mean ' + suggestions + '?'
        raise AttributeError(msg)

{py5surface_class_members_code}
