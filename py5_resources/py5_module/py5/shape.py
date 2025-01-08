# *****************************************************************************
#
#   Part of the py5 library
#   Copyright (C) 2020-2025 Jim Schmitz
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
import types
import weakref
from pathlib import Path
from typing import Sequence, overload  # noqa

import numpy as np
import numpy.typing as npt  # noqa
from jpype import JClass, JException
from jpype.types import JBoolean, JFloat, JInt

from . import spelling
from .decorators import (
    _context_wrapper,
    _convert_hex_color,
    _convert_hex_color2,
    _ret_str,
    _return_color,
)
from .pmath import _get_pvector_wrapper  # noqa

py5shape_class_members_code = None  # DELETE


def _return_list_py5shapes(f):
    @functools.wraps(f)
    def decorated(self_, *args):
        try:
            return [Py5Shape(s) for s in f(self_, *args)]
        except Exception as e:
            return []

    return decorated


def _return_py5shape(f):
    @functools.wraps(f)
    def decorated(self_, *args):
        result = f(self_, *args)
        if result:
            return Py5Shape(result)

    return decorated


def _py5shape_type_fixer(f):
    @functools.wraps(f)
    def decorated(self_, *args):
        def fix_type(arg):
            if isinstance(arg, bool):
                return JBoolean(arg)
            elif isinstance(arg, (int, np.integer)):
                return JInt(arg)
            elif isinstance(arg, float):
                return JFloat(arg)
            else:
                return arg

        args = [fix_type(a) for a in args]
        return f(self_, *args)

    return decorated


def _load_py5shape(f):
    @functools.wraps(f)
    def decorated(self_, *args):
        msg, pshape = "", None

        try:
            if (pshape := f(self_, *args)) is None:
                msg = "Processing unable to read shape file"
        except Exception as e:
            msg = e.message()
            if msg == "None":
                msg = "shape file cannot be found"

        if pshape is None:
            raise RuntimeError(
                "cannot load shape " + str(args[0]) + ". error message: " + msg
            )
        else:
            return Py5Shape(pshape)

    return decorated


def _return_numpy_array(f):
    @functools.wraps(f)
    def decorated(self_, *args):
        result = f(self_, *args)
        return np.array(result) if result is not None else None

    return decorated


_Py5ShapeHelper = JClass("py5.core.Py5ShapeHelper")


class Py5Shape:
    """$classdoc_Py5Shape"""

    _py5_object_cache = weakref.WeakSet()

    def __new__(cls, pshape):
        for o in cls._py5_object_cache:
            if pshape == o._instance:
                return o
        else:
            o = object.__new__(Py5Shape)
            o._instance = pshape
            cls._py5_object_cache.add(o)
            return o

    def __str__(self):
        name = "'" + self.get_name() + "'" if self.get_name() else str(None)
        return f"Py5Shape(name=" + name + ")"

    def __repr__(self):
        return self.__str__()

    def __getattr__(self, name):
        raise AttributeError(spelling.error_msg("Py5Shape", name, self))

    # *** BEGIN METHODS ***

    def _get_width(self) -> float:  # @decorator
        """$class_Py5Shape_width"""
        return self._instance.getWidth()

    width: float = property(fget=_get_width, doc="""$class_Py5Shape_width""")

    def _get_height(self) -> float:  # @decorator
        """$class_Py5Shape_height"""
        return self._instance.getHeight()

    height: float = property(fget=_get_height, doc="""$class_Py5Shape_height""")

    def _get_depth(self) -> float:  # @decorator
        """$class_Py5Shape_depth"""
        return self._instance.getDepth()

    depth: float = property(fget=_get_depth, doc="""$class_Py5Shape_depth""")

    def set_strokes(self, strokes: Sequence[int], /) -> None:
        """$class_Py5Shape_set_strokes"""
        if isinstance(strokes, types.GeneratorType):
            strokes = list(strokes)
        _Py5ShapeHelper.setStrokes(self._instance, strokes)

    def set_fills(self, fills: Sequence[int], /) -> None:
        """$class_Py5Shape_set_fills"""
        if isinstance(fills, types.GeneratorType):
            fills = list(fills)
        _Py5ShapeHelper.setFills(self._instance, fills)

    def vertices(self, coordinates: Sequence[Sequence[float]], /) -> None:
        """$class_Py5Shape_vertices"""
        if isinstance(coordinates, types.GeneratorType):
            coordinates = list(coordinates)
        _Py5ShapeHelper.vertices(self._instance, coordinates)

    def bezier_vertices(self, coordinates: Sequence[Sequence[float]], /) -> None:
        """$class_Py5Shape_bezier_vertices"""
        if isinstance(coordinates, types.GeneratorType):
            coordinates = list(coordinates)
        _Py5ShapeHelper.bezierVertices(self._instance, coordinates)

    def curve_vertices(self, coordinates: Sequence[Sequence[float]], /) -> None:
        """$class_Py5Shape_curve_vertices"""
        if isinstance(coordinates, types.GeneratorType):
            coordinates = list(coordinates)
        _Py5ShapeHelper.curveVertices(self._instance, coordinates)

    def quadratic_vertices(self, coordinates: Sequence[Sequence[float]], /) -> None:
        """$class_Py5Shape_quadratic_vertices"""
        if isinstance(coordinates, types.GeneratorType):
            coordinates = list(coordinates)
        _Py5ShapeHelper.quadraticVertices(self._instance, coordinates)


{py5shape_class_members_code}
