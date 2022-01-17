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
# *** FORMAT PARAMS ***
import functools
from typing import overload, Any  # noqa

from .image import Py5Image  # noqa


py5surface_class_members_code = None  # DELETE


def _return_py5surface(f):
    @functools.wraps(f)
    def decorated(self_, *args):
        return Py5Surface(f(self_, *args), getattr(self_, '_pimage_cache', None))
    return decorated


class Py5Surface:
    """$classdoc_Py5Surface
    """

    def __init__(self, psurface, pimage_cache):
        self._instance = psurface
        self._pimage_cache = pimage_cache


{py5surface_class_members_code}
