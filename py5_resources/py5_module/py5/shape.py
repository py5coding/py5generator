# -*- coding: utf-8 -*-
# *** FORMAT PARAMS ***
import functools

from .methods import Py5Exception


def _return_py5shape(f):
    @functools.wraps(f)
    def decorated(self_, *args):
        return Py5Shape(f(self_, *args))
    return decorated


def _py5shape_param(f):
    @functools.wraps(f)
    def decorated(self_, *args):
        if isinstance(args[0], Py5Shape):
            args = (args[0]._instance, *args[1:])
        return f(self_, *args)

    return decorated


class Py5Shape:

    def __init__(self, pshape):
        self._instance = pshape
