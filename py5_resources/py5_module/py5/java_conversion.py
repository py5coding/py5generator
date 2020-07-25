from jpype import _jcustomizer

from .sketch import Py5Image


@_jcustomizer.JConversion("processing.core.PImage", instanceof=Py5Image)
def _py5image_convert(jcls, obj):
    return obj._instance
