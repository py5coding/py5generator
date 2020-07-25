from jpype import _jcustomizer

from .sketch import Py5Image, Py5Font


@_jcustomizer.JConversion("processing.core.PImage", instanceof=Py5Image)
def _pimage_convert(jcls, obj):
    return obj._instance


@_jcustomizer.JConversion("processing.core.PFont", instanceof=Py5Font)
def _pfont_convert(jcls, obj):
    return obj._instance
