# *****************************************************************************
#
#   Part of the py5 library
#   Copyright (C) 2020-2026 Jim Schmitz
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
from typing import Sequence, overload  # noqa

import numpy as np  # noqa
import numpy.typing as npt  # noqa
from jpype import JClass

from . import spelling
from .base import Py5Base
from .color import Py5Color  # noqa
from .decorators import (
    _context_wrapper,
    _convert_hex_color,
    _hex_converter,
    _return_color,
    _text_fix_str,
)
from .font import Py5Font  # noqa
from .image import Py5Image, _return_py5image  # noqa
from .mixins import PixelPy5GraphicsMixin
from .pmath import _get_matrix_wrapper  # noqa
from .shader import Py5Shader, _load_py5shader, _return_py5shader  # noqa
from .shape import Py5Shape, _load_py5shape, _return_py5shape  # noqa

py5graphics_class_members_code = None  # DELETE


def _return_py5graphics(f):
    @functools.wraps(f)
    def decorated(self_, *args):
        ret = f(self_, *args)
        if ret is not None:
            return Py5Graphics(ret)

    return decorated


def _name_renderer(renderer_name, clsname):
    def _decorator(f):
        @functools.wraps(f)
        def decorated(self_, *args):
            return f(self_, *args, _renderer_name=renderer_name, _clsname=clsname)

        return decorated

    return _decorator


_Py5GraphicsHelper = JClass("py5.core.Py5GraphicsHelper")


class Py5Graphics(PixelPy5GraphicsMixin, Py5Base):
    """$classdoc_Py5Graphics"""

    _py5_object_cache = weakref.WeakSet()

    PI = np.pi
    HALF_PI = np.pi / 2
    THIRD_PI = np.pi / 3
    QUARTER_PI = np.pi / 4
    TWO_PI = 2 * np.pi
    TAU = 2 * np.pi
    RAD_TO_DEG = 180 / np.pi
    DEG_TO_RAD = np.pi / 180

    def __new__(cls, pgraphics):
        for o in cls._py5_object_cache:
            if pgraphics == o._instance:
                return o
        else:
            o = object.__new__(Py5Graphics)
            cls._py5_object_cache.add(o)
            return o

    def __init__(self, pgraphics):
        if pgraphics == getattr(self, "_instance", None):
            # this is a cached Py5Graphics object, don't re-run __init__()
            return

        self._instance = pgraphics
        super().__init__(instance=pgraphics)

    def __str__(self) -> str:
        return (
            f"Py5Graphics(width="
            + str(self._get_width())
            + ", height="
            + str(self._get_height())
            + ")"
        )

    def __repr__(self) -> str:
        return self.__str__()

    def __getattr__(self, name):
        raise AttributeError(spelling.error_msg("Py5Graphics", name, self))

    def _activate_context_manager(self, exit_function, exit_args):
        self._context_manager_exit_function = exit_function
        self._context_manager_exit_args = exit_args

    def __enter__(self):
        if not (
            hasattr(self, "_context_manager_exit_function")
            and hasattr(self, "_context_manager_exit_args")
        ):
            raise RuntimeError(
                "Cannot use this Py5Graphics object as a context manager"
            )
        return self

    def __exit__(self, *exc):
        self._context_manager_exit_function(*self._context_manager_exit_args)

    # *** BEGIN METHODS ***

    def points(self, coordinates: Sequence[Sequence[float]], /) -> None:
        """$class_Py5Graphics_points"""
        if isinstance(coordinates, types.GeneratorType):
            coordinates = list(coordinates)
        _Py5GraphicsHelper.points(self._instance, coordinates)

    def lines(self, coordinates: Sequence[Sequence[float]], /) -> None:
        """$class_Py5Graphics_lines"""
        if isinstance(coordinates, types.GeneratorType):
            coordinates = list(coordinates)
        _Py5GraphicsHelper.lines(self._instance, coordinates)

    def vertices(self, coordinates: Sequence[Sequence[float]], /) -> None:
        """$class_Py5Graphics_vertices"""
        if isinstance(coordinates, types.GeneratorType):
            coordinates = list(coordinates)
        _Py5GraphicsHelper.vertices(self._instance, coordinates)

    def bezier_vertices(self, coordinates: Sequence[Sequence[float]], /) -> None:
        """$class_Py5Graphics_bezier_vertices"""
        if isinstance(coordinates, types.GeneratorType):
            coordinates = list(coordinates)
        _Py5GraphicsHelper.bezierVertices(self._instance, coordinates)

    def curve_vertices(self, coordinates: Sequence[Sequence[float]], /) -> None:
        """$class_Py5Graphics_curve_vertices"""
        if isinstance(coordinates, types.GeneratorType):
            coordinates = list(coordinates)
        _Py5GraphicsHelper.curveVertices(self._instance, coordinates)

    def quadratic_vertices(self, coordinates: Sequence[Sequence[float]], /) -> None:
        """$class_Py5Graphics_quadratic_vertices"""
        if isinstance(coordinates, types.GeneratorType):
            coordinates = list(coordinates)
        _Py5GraphicsHelper.quadraticVertices(self._instance, coordinates)

    @overload
    def create_shape(self) -> Py5Shape:
        """$class_Py5Graphics_create_shape"""
        pass

    @overload
    def create_shape(self, type: int, /) -> Py5Shape:
        """$class_Py5Graphics_create_shape"""
        pass

    @overload
    def create_shape(self, kind: int, /, *p: float) -> Py5Shape:
        """$class_Py5Graphics_create_shape"""
        pass

    @_return_py5shape
    def create_shape(self, *args) -> Py5Shape:
        """$class_Py5Graphics_create_shape"""
        return _Py5GraphicsHelper.createShape(self._instance, *args)

    @overload
    def color(self, c: int, /) -> int:
        """$class_Py5Graphics_color"""
        pass

    @overload
    def color(self, c: int, alpha: float, /) -> int:
        """$class_Py5Graphics_color"""
        pass

    @overload
    def color(self, c: int, alpha: int, /) -> int:
        """$class_Py5Graphics_color"""
        pass

    @overload
    def color(self, gray: float, /) -> int:
        """$class_Py5Graphics_color"""
        pass

    @overload
    def color(self, gray: float, alpha: float, /) -> int:
        """$class_Py5Graphics_color"""
        pass

    @overload
    def color(self, v1: float, v2: float, v3: float, /) -> int:
        """$class_Py5Graphics_color"""
        pass

    @overload
    def color(self, v1: float, v2: float, v3: float, a: float, /) -> int:
        """$class_Py5Graphics_color"""
        pass

    @overload
    def color(self, v1: int, v2: int, v3: int, /) -> int:
        """$class_Py5Graphics_color"""
        pass

    @overload
    def color(self, v1: int, v2: int, v3: int, a: int, /) -> int:
        """$class_Py5Graphics_color"""
        pass

    @overload
    def color(self, hex_code: str, /) -> int:
        """$class_Sketch_color"""
        pass

    @overload
    def color(self, hex_code: str, alpha: int, /) -> int:
        """$class_Sketch_color"""
        pass

    def color(self, *args) -> int:
        """$class_Py5Graphics_color"""
        args = list(args)

        if not isinstance(args[0], Py5Color):
            if (new_arg := _hex_converter(args[0])) is not None:
                args[0] = Py5Color(new_arg, _creator_instance=self)

            if len(args) == 1 and isinstance(args[0], Py5Color):
                return args[0]

        return Py5Color(self._instance.color(*args), _creator_instance=self)


{py5graphics_class_members_code}
