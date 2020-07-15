# -*- coding: utf-8 -*-
# *** FORMAT PARAMS ***
import functools
from typing import overload, List  # noqa

from jnius import autoclass

from .methods import Py5Exception  # noqa
from .shape import Py5Shape, _return_py5shape  # noqa


py5font_class_members_code = None  # DELETE


def _return_py5font(f):
    @functools.wraps(f)
    def decorated(self_, *args):
        return Py5Font(f(self_, *args))

    return decorated


def _py5font_param(f):
    @functools.wraps(f)
    def decorated(self_, *args):
        if isinstance(args[0], Py5Font):
            args = (args[0]._instance, *args[1:])
        return f(self_, *args)

    return decorated


class Py5Font:

    _cls = autoclass('processing.core.PFont', include_protected=False, include_private=False)
    CHARSET = _cls.CHARSET

    def __init__(self, pfont):
        self._instance = pfont


{py5font_class_members_code}
