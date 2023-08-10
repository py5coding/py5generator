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
from __future__ import annotations

import functools
import weakref
from typing import Union, overload  # noqa

from . import spelling
from .base import Py5Base
from .mixins import PixelPy5ImageMixin

py5image_class_members_code = None  # DELETE


def _return_py5image(f):
    @functools.wraps(f)
    def decorated(self_, *args):
        ret = f(self_, *args)
        if ret is None or isinstance(ret, int):
            return ret
        else:
            return Py5Image(ret)
    return decorated


class Py5Image(PixelPy5ImageMixin, Py5Base):
    """$classdoc_Py5Image
    """
    _py5_object_cache = weakref.WeakSet()

    def __new__(cls, pimage):
        for o in cls._py5_object_cache:
            if pimage == o._instance:
                return o
        else:
            o = object.__new__(Py5Image)
            cls._py5_object_cache.add(o)
            return o

    def __init__(self, pimage):
        if pimage == getattr(self, '_instance', None):
            # this is a cached Py5Image object, don't re-run __init__()
            return

        self._instance = pimage
        super().__init__(instance=pimage)

    def __str__(self) -> str:
        return f"Py5Image(width=" + str(self._get_width()) + ", height=" + str(self._get_height()) + ")"

    def __repr__(self) -> str:
        return self.__str__()

    def __getattr__(self, name):
        raise AttributeError(spelling.error_msg('Py5Image', name, self))


{py5image_class_members_code}
