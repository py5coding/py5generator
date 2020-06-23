from typing import NewType

from jnius import autoclass


_Py5Applet = autoclass('py5.core.Py5Applet',
                       include_protected=False, include_private=False)
Py5Applet = NewType('Py5Applet', _Py5Applet)
_PImage = autoclass('processing.core.PImage',
                    include_protected=False, include_private=False)
PImage = NewType('PImage', _PImage)
_PGraphics = autoclass('processing.core.PGraphics',
                       include_protected=False, include_private=False)
PGraphics = NewType('PGraphics', _PGraphics)
_PGL = autoclass('processing.opengl.PGL',
                 include_protected=False, include_private=False)
PGL = NewType('PGL', _PGL)
_PShader = autoclass('processing.opengl.PShader',
                     include_protected=False, include_private=False)
PShader = NewType('PShader', _PShader)
_PFont = autoclass('processing.core.PFont',
                   include_protected=False, include_private=False)
PFont = NewType('PFont', _PFont)
_PShape = autoclass('processing.core.PShape',
                    include_protected=False, include_private=False)
PShape = NewType('PShape', _PShape)
_PSurface = autoclass('processing.core.PSurface',
                      include_protected=False, include_private=False)
PSurface = NewType('PSurface', _PSurface)
