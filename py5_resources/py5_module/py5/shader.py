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
from typing import Any, overload  # noqa

import numpy as np  # noqa
import numpy.typing as npt  # noqa
from jpype.types import JArray, JBoolean, JException, JFloat, JInt  # noqa

from . import spelling
from .image import Py5Image  # noqa
from .pmath import (_numpy_to_pmatrix2d, _numpy_to_pmatrix3d,  # noqa
                    _numpy_to_pvector, _py5vector_to_pvector)
from .vector import Py5Vector

py5shader_class_members_code = None  # DELETE


def _return_py5shader(f):
    @functools.wraps(f)
    def decorated(self_, *args):
        return Py5Shader(f(self_, *args))
    return decorated


def _load_py5shader(f):
    @functools.wraps(f)
    def decorated(self_, *args):
        try:
            return Py5Shader(f(self_, *args))
        except JException as e:
            msg = e.message()
            if msg == 'None':
                msg = 'shader file cannot be found'
        raise RuntimeError('cannot load shader file ' +
                           str(args[0]) + '. error message: ' + msg)
    return decorated


def _py5shader_set_wrapper(f):
    @functools.wraps(f)
    def decorated(self_, name, *args):
        if isinstance(args[0], np.ndarray):
            array = args[0]
            if array.shape in [(2,), (3,)]:
                args = _numpy_to_pvector(array), *args[1:]
            elif array.shape == (2, 3):
                args = _numpy_to_pmatrix2d(array), *args[1:]
            elif array.shape == (4, 4):
                args = _numpy_to_pmatrix3d(array), *args[1:]
        elif isinstance(args[0], Py5Vector):
            args = _py5vector_to_pvector(args[0]), *args[1:]
        else:
            def fix_type(arg):
                if isinstance(arg, bool):
                    return JBoolean(arg)
                elif isinstance(arg, int):
                    return JInt(arg)
                elif isinstance(arg, float):
                    return JFloat(arg)
                else:
                    return arg
            args = [fix_type(a) for a in args]
        return f(self_, name, *args)
    return decorated


class Py5Shader:
    """$classdoc_Py5Shader
    """
    _py5_object_cache = weakref.WeakSet()

    def __new__(cls, pshader):
        for o in cls._py5_object_cache:
            if pshader == o._instance:
                return o
        else:
            o = object.__new__(Py5Shader)
            o._instance = pshader
            cls._py5_object_cache.add(o)
            return o

    def __str__(self) -> str:
        return f"Py5Shader(id=" + str(id(self)) + ")"

    def __repr__(self) -> str:
        return self.__str__()

    def __getattr__(self, name):
        raise AttributeError(spelling.error_msg('Py5Shader', name, self))


{py5shader_class_members_code}
