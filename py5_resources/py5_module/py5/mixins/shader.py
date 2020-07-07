from typing import overload

from jnius import autoclass

from ..methods import Py5Exception
from ..converter import Converter


class Py5Shader:

    _PShader = autoclass('processing.opengl.PShader',
                         include_protected=False, include_private=False)

    def __init__(self, pshader, py5applet):
        self._pshader = pshader
        self._py5applet = py5applet
        self._converter = Converter(self._py5applet)

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

    def set_image(self, name, tex):
        """$class_py5shader_set"""
        try:
            # TODO this should use a cache
            return self._pshader.set(name, self._converter.to_pimage(tex))
        except Exception as e:
            raise Py5Exception(
                e.__class__.__name__,
                str(e),
                'set_image',
                (name, tex))


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

    def load_shader(self, *args) -> Py5Shader:
        """$class_load_shader"""
        try:
            return Py5Shader(self._py5applet.loadShader(*args), self._py5applet)
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

    def shader(self, *args) -> None:
        """$class_shader"""
        try:
            if isinstance(args[0], Py5Shader):
                args = (args[0]._pshader, *args[1:])
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

    def apply_filter(self, *args) -> None:
        """$class_apply_filter"""
        try:
            if isinstance(args[0], Py5Shader):
                args = (args[0]._pshader, *args[1:])
            return self._py5applet.filter(*args)
        except Exception as e:
            raise Py5Exception(e.__class__.__name__, str(e), 'apply_filter', args)
