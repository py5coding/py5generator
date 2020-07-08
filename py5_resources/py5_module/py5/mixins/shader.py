from typing import overload, Any
import functools

from ..methods import Py5Exception
from .image import _check_pimage_cache_or_convert


class Py5Shader:

    def __init__(self, pshader, pimage_cache):
        self._pshader = pshader
        self._pimage_cache = pimage_cache

    @_check_pimage_cache_or_convert(1)
    def set_image(self, name: str, tex: Any, cache: bool = False):
        """$class_py5shader_set_image"""
        try:
            return self._pshader.set(name, tex)
        except Exception as e:
            raise Py5Exception(
                e.__class__.__name__,
                str(e),
                'set_image',
                (name, tex))

    # TODO: need all the typehints

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


class ShaderMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # *** BEGIN METHODS ***

    @overload
    def load_shader(self, fragFilename: str) -> Py5Shader:
        """$class_load_shader"""
        pass

    @overload
    def load_shader(self, fragFilename: str, vertFilename: str) -> Py5Shader:
        """$class_load_shader"""
        pass

    @_return_py5shader
    def load_shader(self, *args) -> Py5Shader:
        """$class_load_shader"""
        try:
            return self._py5applet.loadShader(*args)
        except Exception as e:
            raise Py5Exception(
                e.__class__.__name__,
                str(e),
                'load_shader',
                args)

    @overload
    def shader(self, shader: Py5Shader) -> None:
        """$class_shader"""
        pass

    @overload
    def shader(self, shader: Py5Shader, kind: int) -> None:
        """$class_shader"""
        pass

    @_py5shader_param
    def shader(self, *args) -> None:
        """$class_shader"""
        try:
            return self._py5applet.shader(*args)
        except Exception as e:
            raise Py5Exception(e.__class__.__name__, str(e), 'shader', args)

    @overload
    def apply_filter(self, shader: Py5Shader) -> None:
        """$class_apply_filter"""
        pass

    @overload
    def apply_filter(self, kind: int) -> None:
        """$class_apply_filter"""
        pass

    @overload
    def apply_filter(self, kind: int, param: float) -> None:
        """$class_apply_filter"""
        pass

    @_py5shader_param
    def apply_filter(self, *args) -> None:
        """$class_apply_filter"""
        try:
            return self._py5applet.filter(*args)
        except Exception as e:
            raise Py5Exception(e.__class__.__name__, str(e), 'apply_filter', args)
