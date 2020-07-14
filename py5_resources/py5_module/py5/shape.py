# -*- coding: utf-8 -*-
# *** FORMAT PARAMS ***
from __future__ import annotations

import functools
from typing import overload, List  # noqa

from .methods import Py5Exception  # noqa


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


def _py5shape_param(argnum):
    def decorator(f):
        @functools.wraps(f)
        def decorated(self_, *args):
            if len(args) > argnum and isinstance(args[argnum], Py5Shape):
                args = (*args[:argnum], args[argnum]._instance, *args[(argnum + 1):])
            return f(self_, *args)
        return decorated
    return decorator


class Py5Shape:

    def __init__(self, pshape):
        self._instance = pshape


{py5shape_class_members_code}
