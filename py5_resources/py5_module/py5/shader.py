# -*- coding: utf-8 -*-
# *** FORMAT PARAMS ***
import functools
from typing import overload, List  # noqa

from .methods import Py5Exception  # noqa
from .image import Py5Image, _return_py5image, _py5image_param  # noqa


py5shader_class_members_code = None  # DELETE


def _return_py5shader(f):
    @functools.wraps(f)
    def decorated(self_, *args):
        return Py5Shader(f(self_, *args), getattr(self_, '_pimage_cache', None))
    return decorated


def _py5shader_param(f):
    @functools.wraps(f)
    def decorated(self_, *args):
        if isinstance(args[0], Py5Shader):
            args = (args[0]._instance, *args[1:])
        return f(self_, *args)

    return decorated


class Py5Shader:

    def __init__(self, pshader, pimage_cache):
        self._instance = pshader
        self._pimage_cache = pimage_cache


{py5shader_class_members_code}
