# *****************************************************************************
#
#   Part of the py5 library
#   Copyright (C) 2020-2021 Jim Schmitz
#
#   This library is free software: you can redistribute it and/or modify it
#   under the terms of the GNU Lesser General Public License as published by
#   the Free Software Foundation, either version 2.1 of the License, or (at
#   your option) any later version.
#
#   This library is distributed in the hope that it will be useful, but
#   WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser
#   General Public License for more details.
#
#   You should have received a copy of the GNU Lesser General Public License
#   along with this library. If not, see <https://www.gnu.org/licenses/>.
#
# *****************************************************************************
from typing import TypeVar


Sketch = TypeVar('Sketch')


class Py5SketchPortal:
    pass


def sketch_portal(*, frame_rate: float = 10.0, time_limit: float = 0.0,
                  scale: float = 1.0, quality: int = 75,
                  portal_widget: Py5SketchPortal = None, sketch: Sketch = None) -> None:
    """$module_Py5Tools_sketch_portal"""
    raise RuntimeError('The sketch_widget() function can only be used with IPython and ZMQInteractiveShell (such as Jupyter Lab)')
