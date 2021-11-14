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
from collections.abc import Sequence, Iterable

import numpy as np


class Vector2D(Sequence):

    def __init__(self, *args):
        self._data = None

        if len(args) == 0:
            self._data = np.zeros(2, dtype=np.float32)
        elif len(args) == 1:
            arg = args[0]
            if isinstance(arg, (float, int)):
                self._data = np.array([arg, arg], dtype=np.float32)
            if isinstance(arg, Iterable) and len(arg) == 2:
                self._data = np.array(arg, dtype=np.float32)
        elif len(args) == 2:
            self._data = np.array(args, dtype=np.float32)

        if self._data is None:
            raise RuntimeError(
                f'Cannot create Vector2D instance with {str(args)}')

#     def __getattr__(self, name: str):
#         if name.startswith('__array_'):
#             return getattr(self._data, name)
#         else:
#             raise AttributeError(f"Vector2D has no attribute '{name}'")

    def _get_x(self):
        return self._data[0]

    def _set_x(self, val):
        self._data[0] = val

    def _get_y(self):
        return self._data[1]

    def _set_y(self, val):
        self._data[1] = val

    x = property(_get_x, _set_x, doc='x coordinate')
    y = property(_get_y, _set_y, doc='y coordinate')

    # required by Sequence
    def __getitem__(self, key):
        return self._data[key]

    # should this be here?
    def __setitem__(self, key, val):
        if key in [0, 1]:
            self._data[key] = val
        else:
            raise RuntimeError('error')

    # required by Sequence
    def __len__(self):
        return self._data.__len__()

    # redundant, already provided by Sequence
    def __iter__(self):
        return self._data.__iter__()

    def __str__(self):
        return f"Vector2D({str(self._data)[1:-1].strip().replace(' ', ', ')})"

    def __repr__(self):
        return str(self)

    def __add__(self, other):
        return Vector2D(self._data + other)

    def __radd__(self, other):
        return Vector2D(self._data + other)

    def __sub__(self, other):
        return Vector2D(self._data - other)

    def __rsub__(self, other):
        return Vector2D(other - self._data)

    def __mul__(self, other):
        return Vector2D(self._data * other)

    def __rmul__(self, other):
        return Vector2D(self._data * other)

    def __truediv__(self, other):
        return Vector2D(self._data / other)

    def __floordiv__(self, other):
        return Vector2D(self._data // other)

    def __rtruediv__(self, other):
        return Vector2D(other / self._data)

    def __rfloordiv__(self, other):
        return Vector2D(other // self._data)

    def __pow__(self, other):
        return Vector2D(self._data ** other)

    def __matmul__(self, other):
        return Vector2D(self._data @ other)

    def __rmatmul__(self, other):
        return Vector2D(other @ self._data)

    def __pos__(self):
        return self

    def __neg__(self):
        return Vector2D(-self._data)

    def copy(self):
        return Vector2D(self._data.copy())

    def heading(self):
        return np.arctan2(self._data[1], self._data[0])

    @classmethod
    def from_angle(cls, angle, length=1):
        return Vector2D(length * np.cos(angle), length * np.sin(angle))

    @classmethod
    def random(cls):
        import random
        return Vector2D.from_angle(random.random() * 2 * np.pi)
