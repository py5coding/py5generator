# -*- coding: utf-8 -*-
# *** FORMAT PARAMS ***
from __future__ import annotations

import functools
from pathlib import Path
from typing import overload, List  # noqa
from nptyping import NDArray, Float  # noqa

from jpype import JException
from jpype.types import JBoolean, JInt, JFloat

from .pmath import _get_pvector_wrapper  # noqa


py5shape_class_members_code = None  # DELETE


def _return_list_py5shapes(f):
    @functools.wraps(f)
    def decorated(self_, *args):
        return [Py5Shape(s) for s in f(self_, *args)]
    return decorated


def _return_py5shape(f):
    @functools.wraps(f)
    def decorated(self_, *args):
        return Py5Shape(f(self_, *args))
    return decorated


def _py5shape_type_fixer(f):
    @functools.wraps(f)
    def decorated(self_, *args):
        args = list(args)
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
        return f(self_, *tuple(args))
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


class Py5Shape:
    """$classdoc_Py5Shape"""

    def __init__(self, pshape):
        self._instance = pshape


{py5shape_class_members_code}
