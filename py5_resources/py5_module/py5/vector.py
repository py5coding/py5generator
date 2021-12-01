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

# TODO: add typehints
# https://www.python.org/dev/peps/pep-0484/#forward-references
# TODO: add appropriate code to reference and pmath

class Vector(Sequence):

    def __new__(cls, *args, dim=None, dtype=None, copy=True):
        kwarg_dim = dim
        kwarg_dtype = dtype

        dim = 3 if dim is None else dim
        dtype = np.float_ if dtype is None else dtype

        if not isinstance(dtype, (type, np.dtype)) or not np.issubdtype(dtype, np.floating):
            raise RuntimeError('Error: dtype parameter is not a valid numpy float type (i.e., np.float32, np.float64, etc)')

        if len(args) == 0:
            data = np.zeros(dim, dtype=dtype)
        elif len(args) == 1 and isinstance(args[0], Iterable):
            arg0 = args[0]
            if not hasattr(arg0, '__len__'):
                arg0 = list(arg0)
            if 2 <= len(arg0) <= 4:
                if isinstance(arg0, Vector):
                    arg0 = arg0._data
                if isinstance(arg0, np.ndarray):
                    if copy:
                        if kwarg_dtype is not None and arg0.dtype != dtype:
                            data = arg0.astype(dtype)
                        else:
                            data = arg0.copy()
                    else:
                        data = arg0
                else:
                    data = np.array(arg0, dtype=dtype)
            else:
                raise RuntimeError(f'Cannot create a Vector with {len(arg0)} values')
        elif 2 <= len(args) <= 4:
            dtype_ = None or kwarg_dtype
            data_ = []
            for i, item in enumerate(args):
                if isinstance(item, (np.ndarray, Vector)):
                    if np.issubdtype(item.dtype, np.floating) or np.issubdtype(item.dtype, np.integer):
                        if kwarg_dtype is None:
                            dtype_ = item.dtype if dtype_ is None else max(dtype_, item.dtype)
                        data_.extend(item.tolist())
                    else:
                        raise RuntimeError(f'Argument {i} is a numpy array with dtype {item.dtype} and cannot be used in a Vector')
                elif isinstance(item, Iterable):
                    data_.extend(item)
                elif isinstance(item, (int, float, np.integer, np.floating)):
                    data_.append(item)
                else:
                    raise RuntimeError(f'Argument {i} has type {type(item).__name__} and cannot be used used in a Vector')
            if 2 <= len(data_) <= 4:
                data = np.array(data_, dtype=dtype_ or dtype)
            else:
                raise RuntimeError(f'Cannot create a Vector with {len(data_)} values')
        else:
            raise RuntimeError(f'Cannot create Vector instance with {str(args)}')

        dim = len(data)
        dtype = data.dtype

        if kwarg_dim is not None and dim != kwarg_dim:
            raise RuntimeError(f"Error: dim parameter is {kwarg_dim} but Vector values imply dimension of {dim}")
        if kwarg_dtype is not None and dtype != kwarg_dtype:
            raise RuntimeError(f"Error: dtype parameter is {kwarg_dtype} but Vector values imply dtype of {dtype}")

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
                return Vector(self._data[['xyzw'.index(c) for c in name]], dtype=self._data.dtype, copy=True)
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
            raise RuntimeError('Invalid swizzle: repeats are not allowed in assignments')

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
                raise RuntimeError(f"Cannot perform {opname} operation on two Vectors. If you want to do {opname} on the Vector's data elementwise, use the `.data` attribute to access the Vector's data as a numpy array.")
            if inplace:
                if other._data.size > self._data.size:
                    raise RuntimeError(f'Cannot perform in-place {opname} on Vectors {self} and {other} because the in-place Vector has dimension {self._data.size} and the other Vector has higher dimension {other._data.size}. It is possible to do {opname} on these two Vectors, but since the result of this computation will create a new Vector with dimension {other._data.size}, it cannot be done in-place.')
                else:
                    op(self._data[:other._data.size], other._data[:other._data.size])
                    return self
            else:
                a, b = (other, self) if swap else (self, other)
                new_dim = max(a._data.size, b._data.size)
                # this only works when both dtypes are floats
                new_dtype = max(a.dtype, b.dtype)
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
                raise RuntimeError(f'Unable to perform {opname} on a Vector and a {other_type}, probably because of a size mismatch. The error message is: ' + str(e)) from None

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

    def astype(self, dtype):
        return Vector(self._data, dtype=dtype, copy=True)

    def _get_copy(self):
        return Vector(self._data, dtype=self._data.dtype, copy=True)

    copy = property(_get_copy, doc='copy of Vector')

    def tolist(self):
        return self._data.tolist()

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

    def _run_calc(self, other, calc, name, maybe_vector=False):
        other_type = 'numpy array' if isinstance(other, np.ndarray) else f'{type(other).__name__} object'
        if isinstance(other, Vector):
            if self._data.size == other._data.size:
                other = other._data
            else:
                raise RuntimeError(f'Vector dimensions must be the same to calculate the {name} two Vectors')

        if isinstance(other, np.ndarray):
            try:
                result = calc(self._data, other)
                return Vector(result, copy=False) if maybe_vector and result.ndim == 1 and 2 <= result.size <= 4 else result
            except ValueError as e:
                raise RuntimeError(f'Unable to calculate the {name} between a Vector and {other_type}, probably because of a size mismatch. The error message is: ' + str(e)) from None
        else:
            raise RuntimeError(f'Do not know how to calculate the {name} {type(self).__name__} and {type(other).__name__}')

    # TODO: rotate around vector

    def lerp(self, other, amt):
        return self._run_calc(other, lambda s, o: s + (o - s) * amt, 'lerp of', maybe_vector=True)

    def dist(self, other):
        return self._run_calc(other, lambda s, o: np.sqrt(np.sum((s - o)**2, axis=-1)), 'distance between')

    def dot(self, other):
        return self._run_calc(other, lambda s, o: (s * o).sum(axis=-1), 'dot product for')

    def angle_between(self, other):
        def _angle_between(s, o):
            # s is always a Vector's data, o may be a Vector or numpy array of any (hopefully broadcastable) size
            s_n = s / np.sum(s**2)**0.5
            o_n = o / np.sum(o**2, axis=-1)**0.5
            return np.arccos((s_n * o_n).sum(axis=-1))
        return self._run_calc(other, _angle_between, 'angle between')

    def cross(self, other):
        if self._data.size == 2:
            return self._run_calc(other, lambda s, o: s[..., 0] * o[..., 1] - s[..., 1] * o[..., 0], 'cross product for')
        elif self._data.size == 3:
            def _cross(s, o):
                return np.array([(s[..., 1] * o[..., 2] - s[..., 2] * o[..., 1]).T,
                                 (s[..., 2] * o[..., 0] - s[..., 0] * o[..., 2]).T,
                                 (s[..., 0] * o[..., 1] - s[..., 1] * o[..., 0]).T]).T
            return self._run_calc(other, _cross, 'cross product for', maybe_vector=True)
        else:
            raise RuntimeError(f'Do not know how to calculate the cross product for {type(self).__name__} and {type(other).__name__}')

    def _get_mag(self):
        return np.sum(self._data**2)**0.5

    def set_mag(self, mag):
        self.normalize()
        self._data *= mag
        return self

    def _get_mag_sq(self):
        return np.sum(self._data**2)

    def set_mag_sq(self, mag_sq):
        self.normalize()
        self._data *= mag_sq**0.5
        return self

    def normalize(self):
        mag = np.sum(self._data**2)**0.5
        if mag > 0:
            self._data /= mag
            return self
        else:
            raise RuntimeError('Cannot normalize Vector of zeros')

    def _get_norm(self):
        return self.copy.normalize()

    mag = property(_get_mag, set_mag, doc='vector magnitude')
    mag_sq = property(_get_mag_sq, set_mag_sq, doc='vector magnitude squared')
    norm = property(_get_norm, doc='normalized vector')

    def set_limit(self, max_mag):
        mag_sq = np.sum(self._data**2)
        if mag_sq > max_mag * max_mag:
            self._data *= max_mag / (mag_sq**0.5)
        return self

    def heading(self):
        if self._data.size == 2:
            return np.arctan2(self._data[1], self._data[0])
        elif self._data.size == 3:
            return (np.arctan2(self._data[1], self._data[0]),
                    np.arctan2((self._data[:2]**2).sum()**0.5, self._data[2]))
        else:
            return (np.arctan2(self._data[1], self._data[0]),
                    np.arctan2((self._data[:2]**2).sum()**0.5, self._data[2]),
                    np.arctan2((self._data[:3]**2).sum()**0.5, self._data[3]))

    # TODO: how to keep Vector3D from inheriting methods that only make sense for 2D vectors?
    @classmethod
    def from_heading(cls, angle, dtype=np.float_):
        return Vector(np.cos(angle), np.sin(angle), dtype=dtype)

    @classmethod
    def random(cls, dim=2, *, dtype=np.float_):
        if dim == 2:
            return Vector(np.cos(angle := np.random.rand() * 2 * np.pi), np.sin(angle), dtype=dtype)
        elif dim == 3:
            return Vector((v := np.random.randn(3).astype(dtype)) / (v**2).sum()**0.5, copy=False)
        elif dim == 4:
            return Vector((v := np.random.randn(4).astype(dtype)) / (v**2).sum()**0.5, copy=False)
        else:
            raise RuntimeError(f'Cannot create a random Vector with dimension {dim}')


class Vector2D(Vector):

    def __new__(cls, *args, dtype=np.float_):
        return super().__new__(cls, *args, dim=2, dtype=dtype)

    def rotate(self, angle):
        sin_angle = np.sin(angle)
        cos_angle = np.cos(angle)
        rot = np.array([[cos_angle, -sin_angle], [sin_angle, cos_angle]])
        self._data[:] = rot @ self._data
        return self

    @classmethod
    def random(cls, *, dtype=np.float_):
        return super().random(2, dtype=dtype)


class Vector3D(Vector):

    def __new__(cls, *args, dtype=np.float_):
        return super().__new__(cls, *args, dim=3, dtype=dtype)

    def _get_z(self):
        return self._data[2]

    def _set_z(self, val):
        self._data[2] = val

    z = property(_get_z, _set_z, doc='z coordinate')

    def rotate(self, angle, dim):
        sin_angle = np.sin(angle)
        cos_angle = np.cos(angle)
        if dim in [0, 'x']:
            rot = np.array([[1, 0, 0], [0, cos_angle, -sin_angle], [0, sin_angle, cos_angle]])
        elif dim in [1, 'y']:
            rot = np.array([[cos_angle, 0, sin_angle], [0, 1, 0], [-sin_angle, 0, cos_angle]])
        elif dim in [2, 'z']:
            rot = np.array([[cos_angle, -sin_angle, 0], [sin_angle, cos_angle, 0], [0, 0, 1]])
        else:
            raise RuntimeError("dim parameter must be 0, 1, or 2, or one of 'x', 'y', and 'z'")
        self._data[:] = rot @ self._data
        return self

    @classmethod
    def random(cls, *, dtype=np.float_):
        return super().random(3, dtype=dtype)


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

    @classmethod
    def random(cls, *, dtype=np.float_):
        return super().random(4, dtype=dtype)
