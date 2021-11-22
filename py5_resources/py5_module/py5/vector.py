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
import re

import numpy as np


class Vector(Sequence):

    def __new__(cls, *args, dim=None, dtype=None, copy=True):
        kwarg_dim = dim
        kwarg_dtype = dtype

        dim = 3 if dim is None else dim
        dtype = np.float_ if dtype is None else dtype

        if not isinstance(dtype, (type, np.dtype)) or not np.issubdtype(dtype, np.floating):
            raise RuntimeError('Error: dtype parameter is not a valid numpy float type (i.e., np.float32, np.float64, etc)')

        # TODO: should be able to pass in another Vector class, such as Vector(v, 0), to make a new vector that is larger

        if len(args) == 0:
            data = np.zeros(dim, dtype=dtype)
        elif len(args) == 1 and isinstance(args[0], Iterable) and 2 <= len(args[0]) <= 4:
            arg0 = args[0]
            if isinstance(arg0, Vector):
                arg0 = arg0._data
            if isinstance(arg0, np.ndarray):
                if copy:
                    if arg0.dtype != dtype:
                        data = arg0.astype(dtype)
                    else:
                        data = arg0.copy()
                else:
                    data = arg0
            else:
                data = np.array(arg0, dtype=dtype)
        elif 2 <= len(args) <= 4:
            data = np.array(args, dtype=dtype)
        else:
            raise RuntimeError(f'Cannot create Vector instance with {str(args)}')

        dim = len(data)
        dtype = data.dtype

        if  kwarg_dim is not None and dim != kwarg_dim:
            raise RuntimeError(f"Error: dim parameter is {kwarg_dim} but vector values imply dimension of {dim}")
        if  kwarg_dtype is not None and dtype != kwarg_dtype:
            raise RuntimeError(f"Error: dtype parameter is {kwarg_dtype} but vector values imply dtype of {dtype}")

        if dim == 2:
            v = object.__new__(Vector2D)
        elif dim == 3:
            v = object.__new__(Vector3D)
        elif dim == 4:
            v = object.__new__(Vector4D)
        else:
            raise RuntimeError(f'why is dim == {dim}?')

        v._data = data

        return v

    def __getattr__(self, name):
        if hasattr(self, '_data') and not (set(name) - set('xyzw'[:self._data.size])):
            if 2 <= len(name) <= 4:
                return Vector(self._data[['xyzw'.index(c) for c in name]], copy=True)
            else:
                raise RuntimeError('Invalid swizzle: length must be between 2 and 4 characters')
        else:
            raise AttributeError(f"'Vector' object has no attribute '{name}'")

    def __setattr__(self, name, val):
        if name.startswith('_') or not (hasattr(self, '_data') and not (set(name) - set('xyzw'[:self._data.size]))):
            super().__setattr__(name, val)
        elif len(name) == len(set(name)):
            if not isinstance(val, Iterable) or len(val) in [1, len(name)]:
                self._data[['xyzw'.index(c) for c in name]] = val
            else:
                raise RuntimeError(f'Mismatch: value length of {len(val)} cannot be assigned to swizzle of length {len(name)}')
        else:
            raise RuntimeError('Invalid swizzle: repeats are not allowed')

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, val):
        self._data[key] = val

    def __len__(self):
        return self._data.size

    def __iter__(self):
        return self._data.__iter__()

    def __str__(self):
        vals = ', '.join(re.split(r'\s+', str(self._data)[1:-1].strip()))
        return f'Vector{self._data.size}D({vals})'

    def __repr__(self):
        return f'Vector{self._data.size}D{repr(self._data)[5:]}'

    def _run_op(self, op, other, opname, swap=False, inplace=False, allow2vectors=False):
        if isinstance(other, Vector):
            if not allow2vectors:
                raise RuntimeError(f'Cannot perform {opname} operation on two vectors.')
            if inplace:
                if other._data.size > self._data.size:
                    raise RuntimeError(f'Cannot perform in-place {opname} on vectors {self} and {other} because the in-place vector has dimension {self._data.size} and the other vector has higher dimension {other._data.size}. It is possible to do {opname} on the two vectors, but since the result of this computation will create a new vector with dimension {other._data.size}, it cannot be done in-place.')
                else:
                    op(self._data[:other._data.size], other._data[:other._data.size])
                    return self
            else:
                a, b = (other, self) if swap else (self, other)
                new_dim = max(a._data.size, b._data.size)
                new_dtype = max(a.dtype, b.dtype)  # this only works when both dtypes are floats
                if a._data.size < new_dim:
                    new_data = np.array(b._data, dtype=new_dtype)
                    new_data[:a._data.size] = op(a._data, new_data[:a._data.size])
                    return Vector(new_data, dim=new_dim, copy=False)
                elif b._data.size < new_dim:
                    new_data = np.array(a._data, dtype=new_dtype)
                    new_data[:b._data.size] = op(new_data[:b._data.size], b._data)
                    return Vector(new_data, dim=new_dim, copy=False)
                else:
                    return Vector(op(a._data, b._data), dim=new_dim, copy=False)
        else:
            try:
                if inplace:
                    op(self._data, other)
                    return self
                else:
                    a, b = (other, self._data) if swap else (self._data, other)
                    result = op(a, b)
                    return Vector(result, copy=False) if result.ndim == 1 and 2 <= result.size <= 4 else result
            except ValueError as e:
                other_type = 'numpy array' if isinstance(other, np.ndarray) else f'{type(other).__name__} object'
                raise RuntimeError(f'Unable to perform {opname} on vector and {other_type}, probably because of a size mismatch. The error message is: ' + str(e)) from None

    def __add__(self, other):
        return self._run_op(operator.add, other, 'addition', allow2vectors=True)

    def __iadd__(self, other):
        return self._run_op(operator.iadd, other, 'addition', inplace=True, allow2vectors=True)

    def __radd__(self, other):
        return self._run_op(operator.add, other, 'addition', swap=True, allow2vectors=True)

    def __sub__(self, other):
        return self._run_op(operator.sub, other, 'subtraction', allow2vectors=True)

    def __isub__(self, other):
        return self._run_op(operator.isub, other, 'subtraction', inplace=True, allow2vectors=True)

    def __rsub__(self, other):
        return self._run_op(operator.sub, other, 'subtraction', swap=True, allow2vectors=True)

    def __mul__(self, other):
        return self._run_op(operator.mul, other, 'multiplication')

    def __imul__(self, other):
        return self._run_op(operator.imul, other, 'multiplication', inplace=True)

    def __rmul__(self, other):
        return self._run_op(operator.mul, other, 'multiplication', swap=True)

    def __truediv__(self, other):
        return self._run_op(operator.truediv, other, 'division')

    def __itruediv__(self, other):
        return self._run_op(operator.itruediv, other, 'division', inplace=True)

    def __rtruediv__(self, other):
        return self._run_op(operator.truediv, other, 'division', swap=True)

    def __floordiv__(self, other):
        return self._run_op(operator.floordiv, other, 'integer division')

    def __ifloordiv__(self, other):
        return self._run_op(operator.ifloordiv, other, 'integer division', inplace=True)

    def __rfloordiv__(self, other):
        return self._run_op(operator.floordiv, other, 'integer division', swap=True)

    def __mod__(self, other):
        return self._run_op(operator.mod, other, 'modular division')

    def __imod__(self, other):
        return self._run_op(operator.imod, other, 'modular division', inplace=True)

    def __rmod__(self, other):
        return self._run_op(operator.mod, other, 'modular division', swap=True)

    def __divmod__(self, other):
        return self._run_op(operator.floordiv, other, 'integer division'), self._run_op(operator.mod, other, 'modular division')

    def __rdivmod__(self, other):
        return self._run_op(operator.floordiv, other, 'integer division', swap=True), self._run_op(operator.mod, other, 'modular division', swap=True)

    def __pow__(self, other):
        return self._run_op(operator.pow, other, 'power')

    def __ipow__(self, other):
        return self._run_op(operator.ipow, other, 'power', inplace=True)

    def __matmul__(self, other):
        return self._run_op(operator.matmul, other, 'matrix multiplication')

    def __rmatmul__(self, other):
        return self._run_op(operator.matmul, other, 'matrix multiplication', swap=True)

    def __pos__(self):
        return self

    def __neg__(self):
        return Vector(-self._data, copy=False)

    def __abs__(self):
        return Vector(np.abs(self._data), copy=False)

    def __round__(self):
        return Vector(np.round(self._data), copy=False)

    def __bool__(self):
        return any(self._data != 0.0)

    def __eq__(self, other):
        return isinstance(other, type(self)) and all(self._data == other._data)

    def __ne__(self, other):
        return not isinstance(other, type(self)) or any(self._data != other._data)

    # TODO: need to create a lot of helper functions

    def astype(self, dtype):
        return Vector(self._data, dtype=dtype, copy=True)

    def copy(self):
        return Vector(self._data, dtype=self._data.dtype, copy=True)

    def heading(self):
        return np.arctan2(self._data[1], self._data[0])

    def _get_x(self):
        return self._data[0]

    def _set_x(self, val):
        self._data[0] = val

    def _get_y(self):
        return self._data[1]

    def _set_y(self, val):
        self._data[1] = val

    def _get_data(self):
        return self._data

    def _get_dim(self):
        return self._data.size

    def _get_dtype(self):
        return self._data.dtype

    x = property(_get_x, _set_x, doc='x coordinate')
    y = property(_get_y, _set_y, doc='y coordinate')
    data = property(_get_data, doc='numpy data array')
    dim = property(_get_dim, doc='vector dimension')
    dtype = property(_get_dtype, doc='vector dtype')

    # TODO: how to keep Vector3D from inheriting methods that only make sense for 2D vectors?
    @classmethod
    def from_angle(cls, angle, length=1):
        return Vector(length * np.cos(angle), length * np.sin(angle))

    @classmethod
    def random2D(cls):
        return Vector.from_angle(np.random.rand() * 2 * np.pi)


class Vector2D(Vector):

    def __new__(cls, *args, dtype=np.float_):
        return super().__new__(cls, *args, dim=2, dtype=dtype)


class Vector3D(Vector):

    def __new__(cls, *args, dtype=np.float_):
        return super().__new__(cls, *args, dim=3, dtype=dtype)

    def _get_z(self):
        return self._data[2]

    def _set_z(self, val):
        self._data[2] = val

    z = property(_get_z, _set_z, doc='z coordinate')


class Vector4D(Vector):

    def __new__(cls, *args, dtype=np.float_):
        return super().__new__(cls, *args, dim=4, dtype=dtype)

    def _get_z(self):
        return self._data[2]

    def _set_z(self, val):
        self._data[2] = val

    def _get_w(self):
        return self._data[3]

    def _set_w(self, val):
        self._data[3] = val

    z = property(_get_z, _set_z, doc='z coordinate')
    w = property(_get_w, _set_w, doc='w coordinate')
