from typing import Any
import functools

from .methods import Py5Exception
from .mixins.image import _check_pimage_cache_or_convert


class Py5Shader:

    def __init__(self, pshader, pimage_cache):
        self._pshader = pshader
        self._pimage_cache = pimage_cache

    # TODO: need all the typehints

    @_check_pimage_cache_or_convert(1)
    def set(self, *args):
        """$class_py5shader_set"""
        try:
            return self._pshader.set(*args)
        except Exception as e:
            raise Py5Exception(
                e.__class__.__name__,
                str(e),
                'set',
                args)


def _return_py5shader(f):
    @functools.wraps(f)
    def decorated(self_, *args):
        return Py5Shader(f(self_, *args), getattr(self_, '_pimage_cache', None))
    return decorated


def _py5shader_param(f):
    @functools.wraps(f)
    def decorated(self_, *args):
        if isinstance(args[0], Py5Shader):
            args = (args[0]._pshader, *args[1:])
        return f(self_, *args)

    return decorated
