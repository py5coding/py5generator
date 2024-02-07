# *****************************************************************************
#
#   Part of the py5 library
#   Copyright (C) 2020-2023 Jim Schmitz
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
from __future__ import annotations

import traceback
import types
import warnings
from pathlib import Path
from typing import Any, Union, overload

import numpy as np
import numpy.typing as npt
from jpype import JClass

_OpenSimplex2S = JClass("py5.util.OpenSimplex2S")


def _non_py5_stacklevel():
    f = str(Path(__file__).parent.parent)
    for i, t in enumerate(reversed(traceback.extract_stack())):
        if t.filename.startswith(f):
            continue
        else:
            return i


class MathMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._instance = kwargs["instance"]
        self._rng = np.random.default_rng()

    # *** BEGIN METHODS ***

    @classmethod
    def hex_color(cls, color: int) -> str:
        """$class_Sketch_hex_color"""
        return "#%06X%02X" % (color & 0xFFFFFF, (color >> 24) & 0xFF)

    @classmethod
    def sin(cls, angle: Union[float, npt.ArrayLike]) -> Union[float, npt.NDArray]:
        """$class_Sketch_sin"""
        return np.sin(angle)

    @classmethod
    def cos(cls, angle: Union[float, npt.ArrayLike]) -> Union[float, npt.NDArray]:
        """$class_Sketch_cos"""
        return np.cos(angle)

    @classmethod
    def tan(cls, angle: Union[float, npt.ArrayLike]) -> Union[float, npt.NDArray]:
        """$class_Sketch_tan"""
        return np.tan(angle)

    @classmethod
    def asin(cls, value: Union[float, npt.ArrayLike]) -> Union[float, npt.NDArray]:
        """$class_Sketch_asin"""
        return np.arcsin(value)

    @classmethod
    def acos(cls, value: Union[float, npt.ArrayLike]) -> Union[float, npt.NDArray]:
        """$class_Sketch_acos"""
        return np.arccos(value)

    @classmethod
    def atan(cls, value: Union[float, npt.ArrayLike]) -> Union[float, npt.NDArray]:
        """$class_Sketch_atan"""
        return np.arctan(value)

    @classmethod
    def atan2(
        cls, y: Union[float, npt.ArrayLike], x: Union[float, npt.ArrayLike]
    ) -> Union[float, npt.NDArray]:
        """$class_Sketch_atan2"""
        return np.arctan2(y, x)

    @classmethod
    def degrees(cls, radians: Union[float, npt.ArrayLike]) -> Union[float, npt.NDArray]:
        """$class_Sketch_degrees"""
        return np.degrees(radians)

    @classmethod
    def radians(cls, degrees: Union[float, npt.ArrayLike]) -> Union[float, npt.NDArray]:
        """$class_Sketch_radians"""
        return np.radians(degrees)

    @classmethod
    def constrain(
        cls,
        amt: Union[float, npt.NDArray],
        low: Union[float, npt.NDArray],
        high: Union[float, npt.NDArray],
    ) -> Union[float, npt.NDArray]:
        """$class_Sketch_constrain"""
        return np.where(amt < low, low, np.where(amt > high, high, amt))

    @classmethod
    def remap(
        cls,
        value: Union[float, npt.NDArray],
        start1: Union[float, npt.NDArray],
        stop1: Union[float, npt.NDArray],
        start2: Union[float, npt.NDArray],
        stop2: Union[float, npt.NDArray],
    ) -> Union[float, npt.NDArray]:
        """$class_Sketch_remap"""
        denom = stop1 - start1
        if denom == 0:
            warnings.warn(
                f"remap({value}, {start1}, {stop1}, {start2}, {stop2}) called, which returns NaN (not a number)",
                stacklevel=_non_py5_stacklevel(),
            )
            return float("nan")
        else:
            return start2 + (stop2 - start2) * ((value - start1) / denom)

    @overload
    def dist(
        cls,
        x1: Union[float, npt.NDArray],
        y1: Union[float, npt.NDArray],
        x2: Union[float, npt.NDArray],
        y2: Union[float, npt.NDArray],
        /,
    ) -> Union[float, npt.NDArray]:
        """$class_Sketch_dist"""
        pass

    @overload
    def dist(
        cls,
        x1: Union[float, npt.NDArray],
        y1: Union[float, npt.NDArray],
        z1: Union[float, npt.NDArray],
        x2: Union[float, npt.NDArray],
        y2: Union[float, npt.NDArray],
        z2: Union[float, npt.NDArray],
        /,
    ) -> Union[float, npt.NDArray]:
        """$class_Sketch_dist"""
        pass

    @classmethod
    def dist(cls, *args: Union[float, npt.NDArray]) -> float:
        """$class_Sketch_dist"""
        if len(args) % 2 == 1:
            raise RuntimeError(f"Cannot apply dist function to arguments {args}")
        return (
            sum(
                [
                    (a - b) ** 2
                    for a, b in zip(args[: (len(args) // 2)], args[(len(args) // 2) :])
                ]
            )
            ** 0.5
        )

    @classmethod
    def lerp(
        cls,
        start: Union[float, npt.NDArray],
        stop: Union[float, npt.NDArray],
        amt: Union[float, npt.NDArray],
    ) -> Union[float, npt.NDArray]:
        """$class_Sketch_lerp"""
        return amt * (stop - start) + start

    @overload
    def mag(
        cls, a: Union[float, npt.NDArray], b: Union[float, npt.NDArray], /
    ) -> float:
        """$class_Sketch_mag"""
        pass

    @overload
    def mag(
        cls,
        a: Union[float, npt.NDArray],
        b: Union[float, npt.NDArray],
        c: Union[float, npt.NDArray],
        /,
    ) -> float:
        """$class_Sketch_mag"""
        pass

    @classmethod
    def mag(cls, *args: Union[float, npt.NDArray]) -> float:
        """$class_Sketch_mag"""
        return sum([x * x for x in args]) ** 0.5

    @classmethod
    def norm(
        cls,
        value: Union[float, npt.NDArray],
        start: Union[float, npt.NDArray],
        stop: Union[float, npt.NDArray],
    ) -> Union[float, npt.NDArray]:
        """$class_Sketch_norm"""
        return (value - start) / (stop - start)

    @classmethod
    def sq(cls, value: Union[float, npt.NDArray]) -> Union[float, npt.NDArray]:
        """$class_Sketch_sq"""
        return value * value

    @classmethod
    def sqrt(
        cls, value: Union[float, npt.NDArray]
    ) -> Union[float, complex, npt.NDArray]:
        """$class_Sketch_sqrt"""
        return value**0.5

    @classmethod
    def floor(cls, value: Union[float, npt.ArrayLike]) -> Union[int, npt.NDArray]:
        """$class_Sketch_floor"""
        return np.floor(value).astype(np.int64)

    @classmethod
    def ceil(cls, value: Union[float, npt.ArrayLike]) -> Union[int, npt.NDArray]:
        """$class_Sketch_ceil"""
        return np.ceil(value).astype(np.int64)

    @classmethod
    def exp(cls, value: Union[float, npt.ArrayLike]) -> Union[float, npt.NDArray]:
        """$class_Sketch_exp"""
        return np.exp(value)

    @classmethod
    def log(cls, value: Union[float, npt.ArrayLike]) -> Union[float, npt.NDArray]:
        """$class_Sketch_log"""
        return np.log(value)

    def _get_np_random(self) -> np.random.Generator:  # @decorator
        """$class_Sketch_np_random"""
        return self._rng

    np_random: np.random.Generator = property(
        fget=_get_np_random, doc="""$class_Sketch_np_random"""
    )

    def random_seed(self, seed: int) -> None:
        """$class_Sketch_random_seed"""
        self._rng = np.random.default_rng(seed)

    @overload
    def random(self) -> float:
        """$class_Sketch_random"""
        pass

    @overload
    def random(self, high: float, /) -> float:
        """$class_Sketch_random"""
        pass

    @overload
    def random(self, low: float, high: float, /) -> float:
        """$class_Sketch_random"""
        pass

    def random(self, *args: float) -> float:
        """$class_Sketch_random"""
        if len(args) == 0:
            return self._rng.uniform()
        elif len(args) == 1:
            high = args[0]
            if isinstance(high, (int, np.integer, float)):
                return self._rng.uniform(0, high)
        elif len(args) == 2:
            low, high = args
            if isinstance(low, (int, np.integer, float)) and isinstance(
                high, (int, np.integer, float)
            ):
                return self._rng.uniform(low, high)

        types = ",".join([type(a).__name__ for a in args])
        raise TypeError(f"No matching overloads found for Sketch.random({types})")

    @overload
    def random_int(self) -> int:
        """$class_Sketch_random_int"""
        pass

    @overload
    def random_int(self, high: int, /) -> int:
        """$class_Sketch_random_int"""
        pass

    @overload
    def random_int(self, low: int, high: int, /) -> int:
        """$class_Sketch_random_int"""
        pass

    def random_int(self, *args: int) -> int:
        """$class_Sketch_random_int"""
        if len(args) == 0:
            return self._rng.integers(0, 1, endpoint=True)
        elif len(args) == 1:
            high = args[0]
            if isinstance(high, (int, np.integer)):
                return self._rng.integers(0, high, endpoint=True)
        elif len(args) == 2:
            low, high = args
            if isinstance(low, (int, np.integer)) and isinstance(
                high, (int, np.integer)
            ):
                return self._rng.integers(low, high, endpoint=True)

        types = ",".join([type(a).__name__ for a in args])
        raise TypeError(f"No matching overloads found for Sketch.random_int({types})")

    def random_choice(self, objects: list[Any]) -> Any:
        """$class_Sketch_random_choice"""
        if len(objects):
            return objects[self._rng.integers(0, len(objects))]
        else:
            return None

    def random_sample(
        self, objects: list[Any], size: int = 1, replace: bool = True
    ) -> list[Any]:
        """$class_Sketch_random_sample"""
        if len(objects):
            if isinstance(objects, types.GeneratorType):
                objects = list(objects)
            indices = self._rng.choice(range(len(objects)), size=size, replace=replace)
            if not isinstance(objects, list):
                try:
                    return objects[indices]
                except:
                    pass
            return [objects[idx] for idx in indices]
        else:
            return []

    @overload
    def random_gaussian(self) -> float:
        """$class_Sketch_random_gaussian"""
        pass

    @overload
    def random_gaussian(self, loc: float, /) -> float:
        """$class_Sketch_random_gaussian"""
        pass

    @overload
    def random_gaussian(self, loc: float, scale: float, /) -> float:
        """$class_Sketch_random_gaussian"""
        pass

    def random_gaussian(self, *args: float) -> float:
        """$class_Sketch_random_gaussian"""
        if len(args) == 0:
            return self._rng.normal()
        elif len(args) == 1:
            loc = args[0]
            if isinstance(loc, (int, np.integer)):
                return self._rng.normal(loc)
        elif len(args) == 2:
            loc, scale = args
            if isinstance(loc, (int, np.integer, float)) and isinstance(
                scale, (int, np.integer, float)
            ):
                return self._rng.normal(loc, scale)

        types = ",".join([type(a).__name__ for a in args])
        raise TypeError(
            f"No matching overloads found for Sketch.random_gaussian({types})"
        )

    @overload
    def noise(self, x: Union[float, npt.NDArray], /) -> Union[float, npt.NDArray]:
        """$class_Sketch_noise"""
        pass

    @overload
    def noise(
        self, x: Union[float, npt.NDArray], y: Union[float, npt.NDArray], /
    ) -> Union[float, npt.NDArray]:
        """$class_Sketch_noise"""
        pass

    @overload
    def noise(
        self,
        x: Union[float, npt.NDArray],
        y: Union[float, npt.NDArray],
        z: Union[float, npt.NDArray],
        /,
    ) -> Union[float, npt.NDArray]:
        """$class_Sketch_noise"""
        pass

    def noise(self, *args) -> Union[float, npt.NDArray]:
        """$class_Sketch_noise"""
        if any(isinstance(arg, np.ndarray) for arg in args):
            arrays = np.broadcast_arrays(*args)
            return np.array(
                self._instance.noiseArray(*[a.flatten() for a in arrays])
            ).reshape(arrays[0].shape)
        else:
            return self._instance.noise(*args)

    @overload
    def os_noise(
        self, x: Union[float, npt.NDArray], y: Union[float, npt.NDArray], /
    ) -> Union[float, npt.NDArray]:
        """$class_Sketch_os_noise"""
        pass

    @overload
    def os_noise(
        self,
        x: Union[float, npt.NDArray],
        y: Union[float, npt.NDArray],
        z: Union[float, npt.NDArray],
        /,
    ) -> Union[float, npt.NDArray]:
        """$class_Sketch_os_noise"""
        pass

    @overload
    def os_noise(
        self,
        x: Union[float, npt.NDArray],
        y: Union[float, npt.NDArray],
        z: Union[float, npt.NDArray],
        w: Union[float, npt.NDArray],
        /,
    ) -> Union[float, npt.NDArray]:
        """$class_Sketch_os_noise"""
        pass

    def os_noise(self, *args) -> Union[float, npt.NDArray]:
        """$class_Sketch_os_noise"""
        if any(isinstance(arg, np.ndarray) for arg in args):
            arrays = np.broadcast_arrays(*args)
            return np.array(
                self._instance.osNoiseArray(*[a.flatten() for a in arrays])
            ).reshape(arrays[0].shape)
        else:
            return self._instance.osNoise(*args)
