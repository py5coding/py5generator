from jpype import _jcustomizer

from .sketch import Py5Graphics, Py5Image, Py5Font, Py5Shape, Py5Shader


@_jcustomizer.JConversion("processing.core.PImage", instanceof=Py5Image)
def _py5image_convert(jcls, obj):
    return obj._instance


@_jcustomizer.JConversion("processing.core.PImage", instanceof=Py5Graphics)
def _py5graphics_convert(jcls, obj):
    return obj._instance


@_jcustomizer.JConversion("processing.core.PFont", instanceof=Py5Font)
def _py5font_convert(jcls, obj):
    return obj._instance


@_jcustomizer.JConversion("processing.core.PShape", instanceof=Py5Shape)
def _py5shape_convert(jcls, obj):
    return obj._instance


@_jcustomizer.JConversion("processing.opengl.PShader", instanceof=Py5Shader)
def _py5shader_convert(jcls, obj):
    return obj._instance
