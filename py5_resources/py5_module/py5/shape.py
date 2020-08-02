# -*- coding: utf-8 -*-
# *** FORMAT PARAMS ***
from __future__ import annotations

import functools
from typing import overload, List  # noqa
from nptyping import NDArray, Float  # noqa

from .methods import Py5Exception  # noqa
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


class Py5Shape:

    def __init__(self, pshape):
        self._instance = pshape


{py5shape_class_members_code}
