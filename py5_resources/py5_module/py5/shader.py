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
from typing import overload, List, Any  # noqa
from nptyping import NDArray, Float, Int  # noqa

import numpy as np  # noqa

from .base import Py5Base
from .image import Py5Image  # noqa
from jpype.types import JException, JArray, JBoolean, JInt, JFloat  # noqa
from .pmath import _py5vector_to_pvector, _numpy_to_pvector, _numpy_to_pmatrix2d, _numpy_to_pmatrix3d  # noqa
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
        raise RuntimeError('cannot load shader file ' + str(args[0]) + '. error message: ' + msg)
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


class Py5Shader(Py5Base):
    """$classdoc_Py5Shader
    """

    def __init__(self, pshader):
        self._instance = pshader
        super().__init__(instance=pshader)


{py5shader_class_members_code}
