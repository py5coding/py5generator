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
import operator
from collections.abc import Sequence, Iterable

import numpy as np


class Vector(Sequence):

    def __new__(cls, *args, **kwargs):
        data = np.zeros(3, dtype=np.float32)
        dim = None

        if len(args) == 0:
            dim = 3
        elif len(args) == 1 and isinstance(args[0], Iterable) and 2 <= len(args[0]) <= 3:
            dim = len(args[0])
            data[:dim] = args[0][:dim]
        elif 2 <= len(args) <= 3:
            dim = len(args)
            data[:dim] = args[:dim]
        else:
            raise RuntimeError(f'Cannot create Vector instance with {str(args)}')

        if 'dim' in kwargs and dim != kwargs['dim']:
            raise RuntimeError(f"Error: dim parameter is {kwargs['dim']} but vector values imply dimension of {dim}")

        if dim == 2:
            v = object.__new__(Vector2D)
        elif dim == 3:
            v = object.__new__(Vector3D)
        else:
            raise RuntimeError(f'why is dim == {dim}?')

        v._data = data
        v._dim = dim
        v._swizzle_lut = {c:i for i, c in enumerate('xyz'[:dim])}

        return v

    def __getattr__(self, name):
        if name.startswith('_'):
            super().__getattr__(name)
        else:
            if 2 <= len(name) <= 4 and all(c in self._swizzle_lut for c in name):
                return Vector([self._data[self._swizzle_lut[c]] for c in name])
            else:
                raise RuntimeError('Invalid swizzle')

    def __setattr__(self, name, val):
        if name.startswith('_'):
            super().__setattr__(name, val)
        else:
            if hasattr(self, '_data') and hasattr(self, '_swizzle_lut') and all(c in self._swizzle_lut for c in name):
                if len(name) == len(set(name)):
                    self._data[[self._swizzle_lut[c] for c in name]] = val
                else:
                    raise RuntimeError('Invalid swizzle')
            else:
                super().__setattr__(name, val)

    # required by Sequence
    def __getitem__(self, key):
        # TODO: what if key > dim?
        return self._data[key]

    # should this be here?
    def __setitem__(self, key, val):
        if key in [0, 1]:
            self._data[key] = val
        else:
            raise RuntimeError('error')

    # required by Sequence
    def __len__(self):
        return self._dim

    # redundant, already provided by Sequence
    def __iter__(self):
        return self._data[:self._dim].__iter__()

    def __str__(self):
        return f"Vector{self._dim}D({str(self._data[:self._dim])[1:-1].strip().replace(' ', ', ')})"

    def __repr__(self):
        return str(self)

    def _run_op(self, op, other, swap=False):
        if isinstance(other, Vector):
            a, b = (other, self) if swap else (self, other)
            return Vector(op(a._data, b._data), dim=max(a._dim, b._dim))
        else:
            a, b = (other, self._data[:self._dim]) if swap else (self._data[:self._dim], other)
            result = op(a, b)
            return Vector(result) if result.ndim == 1 and result.size in [2, 3] else result

    def __add__(self, other):
        return self._run_op(operator.add, other)

    def __radd__(self, other):
        return self._run_op(operator.add, other, swap=True)

    def __sub__(self, other):
        return self._run_op(operator.sub, other)

    def __rsub__(self, other):
        return self._run_op(operator.sub, other, swap=True)

    def __mul__(self, other):
        return self._run_op(operator.mul, other)

    def __rmul__(self, other):
        return self._run_op(operator.mul, other, swap=True)

    def __truediv__(self, other):
        # TODO: what does dividing mean for vectors? Also 2D vectors will accumulate a 0 / 0 for z value
        return self._run_op(operator.truediv, other)

    def __rtruediv__(self, other):
        return self._run_op(operator.truediv, other, swap=True)

    def __floordiv__(self, other):
        return self._run_op(operator.floordiv, other)

    def __rfloordiv__(self, other):
        return self._run_op(operator.floordiv, other, swap=True)

    def __pow__(self, other):
        return self._run_op(operator.pow, other)

    def __matmul__(self, other):
        return self._run_op(operator.matmul, other)

    def __rmatmul__(self, other):
        return self._run_op(operator.matmul, other, swap=True)

    def __pos__(self):
        return self

    def __neg__(self):
        return Vector(-self._data)

    def copy(self):
        return Vector(self._data.copy())

    def heading(self):
        return np.arctan2(self._data[1], self._data[0])

    # TODO: how to keep Vector3D from inheriting methods that only make sense for 2D vectors?
    @classmethod
    def from_angle(cls, angle, length=1):
        return Vector(length * np.cos(angle), length * np.sin(angle))

    @classmethod
    def random2D(cls):
        return Vector.from_angle(np.random.rand() * 2 * np.pi)


class Vector2D(Vector):

    def __new__(cls, *args):
        return super().__new__(cls, *args, dim=2)

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


class Vector3D(Vector):

    def __new__(cls, *args):
        return super().__new__(cls, *args, dim=3)

    def _get_x(self):
        return self._data[0]

    def _set_x(self, val):
        self._data[0] = val

    def _get_y(self):
        return self._data[1]

    def _set_y(self, val):
        self._data[1] = val

    def _get_z(self):
        return self._data[2]

    def _set_z(self, val):
        self._data[2] = val

    x = property(_get_x, _set_x, doc='x coordinate')
    y = property(_get_y, _set_y, doc='y coordinate')
    z = property(_get_z, _set_z, doc='z coordinate')
