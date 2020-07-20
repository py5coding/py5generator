from typing import NewType

from jpype import JClass


_Py5Applet = JClass('py5.core.Py5Applet')
Py5Applet = NewType('Py5Applet', _Py5Applet)

_Py5Image = JClass('py5.core.Py5Image')
