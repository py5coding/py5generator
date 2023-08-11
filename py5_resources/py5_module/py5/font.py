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
from typing import overload  # noqa

import jpype
from jpype import JArray, JException, JString  # noqa

from . import spelling
from .decorators import _ret_str  # noqa
from .shape import Py5Shape, _return_py5shape  # noqa

py5font_class_members_code = None  # DELETE


def _return_py5font(f):
    @functools.wraps(f)
    def decorated(self_, *args):
        return Py5Font(f(self_, *args))

    return decorated


def _load_py5font(f):
    @functools.wraps(f)
    def decorated(self_, *args):
        # TODO: for load_font this prints a Java exception to strerr if the file cannot be found or read
        try:
            ret = f(self_, *args)
        except JException as e:
            msg = e.message()
        else:
            if ret is None:
                msg = "font file is missing or inaccessible."
            else:
                return Py5Font(ret)
        raise RuntimeError(
            "cannot load font file " + str(args[0]) + ". error message: " + msg
        )

    return decorated


def _return_list_str(f):
    @functools.wraps(f)
    def decorated(cls_, *args):
        return [str(x) for x in f(cls_, *args) or []]

    return decorated


class Py5Font:
    """$classdoc_Py5Font"""

    _cls = jpype.JClass("processing.core.PFont")
    CHARSET = _cls.CHARSET

    _py5_object_cache = weakref.WeakSet()

    def __new__(cls, pfont):
        for o in cls._py5_object_cache:
            if pfont == o._instance:
                return o
        else:
            o = object.__new__(Py5Font)
            o._instance = pfont
            cls._py5_object_cache.add(o)
            return o

    def __str__(self) -> str:
        return (
            "Py5Font(font_name='"
            + self.get_name()
            + "', font_size="
            + str(self.get_size())
            + ")"
        )

    def __repr__(self) -> str:
        return self.__str__()

    def __getattr__(self, name):
        raise AttributeError(spelling.error_msg("Py5Font", name, self))


{py5font_class_members_code}
