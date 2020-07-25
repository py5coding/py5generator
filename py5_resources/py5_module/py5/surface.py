# -*- coding: utf-8 -*-
# *** FORMAT PARAMS ***
import functools
from typing import overload, Any  # noqa

from .methods import Py5Exception  # noqa
from .image import Py5Image, _return_py5image  # noqa


py5surface_class_members_code = None  # DELETE


def _return_py5surface(f):
    @functools.wraps(f)
    def decorated(self_, *args):
        return Py5Surface(f(self_, *args), getattr(self_, '_pimage_cache', None))
    return decorated


class Py5Surface:

    def __init__(self, psurface, pimage_cache):
        self._instance = psurface
        self._pimage_cache = pimage_cache


{py5surface_class_members_code}
