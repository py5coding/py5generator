from typing import NewType

from jnius import autoclass


_Py5Applet = autoclass('py5.core.Py5Applet',
                       include_protected=False, include_private=False)
Py5Applet = NewType('Py5Applet', _Py5Applet)

_PImage = autoclass('processing.core.PImage',
                    include_protected=False, include_private=False)
Py5Image = NewType('Py5Image', None)
