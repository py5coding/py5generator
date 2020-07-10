from typing import NewType

from jnius import autoclass


_Py5Applet = autoclass('py5.core.Py5Applet',
                       include_protected=False, include_private=False)
Py5Applet = NewType('Py5Applet', _Py5Applet)
_PGraphics = autoclass('processing.core.PGraphics',
                       include_protected=False, include_private=False)
PGraphics = NewType('PGraphics', _PGraphics)
_PShape = autoclass('processing.core.PShape',
                    include_protected=False, include_private=False)
PShape = NewType('PShape', _PShape)
_PSurface = autoclass('processing.core.PSurface',
                      include_protected=False, include_private=False)
PSurface = NewType('PSurface', _PSurface)

Py5Image = NewType('Py5Image', None)
