from typing import NewType

from jnius import autoclass


_Py5Applet = autoclass('py5.core.Py5Applet',
                       include_protected=False, include_private=False)
Py5Applet = NewType('Py5Applet', _Py5Applet)
_PGraphics = autoclass('processing.core.PGraphics',
                       include_protected=False, include_private=False)
PGraphics = NewType('PGraphics', _PGraphics)

Py5Image = NewType('Py5Image', None)
