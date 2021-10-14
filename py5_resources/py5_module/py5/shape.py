# *****************************************************************************
#
#   Part of the py5 library
#   Copyright (C) 2020-2021 Jim Schmitz
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
from pathlib import Path
from typing import overload, List  # noqa
import numpy as np
from nptyping import NDArray, Float, Int  # noqa

from jpype import JException
from jpype.types import JBoolean, JInt, JFloat

from .pmath import _get_pvector_wrapper  # noqa
from .decorators import _ret_str, _convert_hex_color, _convert_hex_color2, _context_wrapper  # noqa


py5shape_class_members_code = None  # DELETE


def _return_list_py5shapes(f):
    @functools.wraps(f)
    def decorated(self_, *args):
        return [Py5Shape(s) for s in f(self_, *args)]
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
        try:
            return Py5Shape(f(self_, *args))
        except JException as e:
            msg = e.message()
            if msg == 'None':
                msg = 'shape file cannot be found'
        raise RuntimeError('cannot load shape ' + str(args[0]) + '. error message: ' + msg)
    return decorated


def _return_numpy_array(f):
    @functools.wraps(f)
    def decorated(self_, *args):
        result = f(self_, *args)
        return np.array(result) if result is not None else None
    return decorated


class Py5Shape:
    """$classdoc_Py5Shape
    """

    def __init__(self, pshape):
        self._instance = pshape


{py5shape_class_members_code}
