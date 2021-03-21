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
from typing import overload, Union, Any, List

import numpy as np

import noise


class MathMixin:

    _rng = np.random.default_rng()

    SIMPLEX_NOISE = 1  # CODEBUILDER INCLUDE
    PERLIN_NOISE = 2  # CODEBUILDER INCLUDE
    _NOISE_MODE = SIMPLEX_NOISE
    _NOISE_SEED = _rng.integers(0, 1024)
    _NOISE_OCTAVES = 4
    _NOISE_PERSISTENCE = 0.5
    _NOISE_LACUNARITY = 2.0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # *** BEGIN METHODS ***

    @classmethod
    def sin(cls, angle: float) -> float:
        """$class_Sketch_sin"""
        return np.sin(angle)

    @classmethod
    def cos(cls, angle: float) -> float:
        """$class_Sketch_cos"""
        return np.cos(angle)

    @classmethod
    def tan(cls, angle: float) -> float:
        """$class_Sketch_tan"""
        return np.tan(angle)

    @classmethod
    def asin(cls, value: float) -> float:
        """$class_Sketch_asin"""
        return np.arcsin(value)

    @classmethod
    def acos(cls, value: float) -> float:
        """$class_Sketch_acos"""
        return np.arccos(value)

    @classmethod
    def atan(cls, value: float) -> float:
        """$class_Sketch_atan"""
        return np.arctan(value)

    @classmethod
    def atan2(cls, y: float, x: float) -> float:
        """$class_Sketch_atan2"""
        return np.arctan2(y, x)

    @classmethod
    def degrees(cls, radians: float) -> float:
        """$class_Sketch_degrees"""
        return np.degrees(radians)

    @classmethod
    def radians(cls, degrees: float) -> float:
        """$class_Sketch_radians"""
        return np.radians(degrees)

    @classmethod
    def constrain(cls, amt: float, low: float, high: float) -> float:
        """$class_Sketch_constrain"""
        return np.where(amt < low, low, np.where(amt > high, high, amt))

    @classmethod
    def remap(cls, value: float, start1: float, stop1: float, start2: float, stop2: float) -> float:
        """$class_Sketch_remap"""
        return start2 + (stop2 - start2) * ((value - start1) / (stop1 - start1))

    @overload
    def dist(cls, x1: float, y1: float, x2: float, y2: float) -> float:
        """$class_Sketch_dist"""
        pass

    @overload
    def dist(cls, x1: float, y1: float, z1: float, x2: float, y2: float, z2: float) -> float:
        """$class_Sketch_dist"""
        pass

    @classmethod
    def dist(cls, *args: float) -> float:
        """$class_Sketch_dist"""
        if len(args) % 2 == 1:
            raise RuntimeError(f'Cannot apply dist function to arguments {args}')
        return sum([(a - b)**2 for a, b in zip(args[:(len(args) // 2)], args[(len(args) // 2):])])**0.5

    @classmethod
    def lerp(cls, start: float, stop: float, amt: float) -> float:
        """$class_Sketch_lerp"""
        return amt * (stop - start) + start

    @overload
    def mag(cls, a: float, b: float) -> float:
        """$class_Sketch_mag"""
        pass

    @overload
    def mag(cls, a: float, b: float, c: float) -> float:
        """$class_Sketch_mag"""
        pass

    @classmethod
    def mag(cls, *args: float) -> float:
        """$class_Sketch_mag"""
        return sum([x * x for x in args])**0.5

    @classmethod
    def norm(cls, value: float, start: float, stop: float) -> float:
        """$class_Sketch_norm"""
        return (value - start) / (stop - start)

    @classmethod
    def sq(cls, value: float) -> float:
        """$class_Sketch_sq"""
        return value * value

    @classmethod
    def sqrt(cls, value: float) -> Union[float, complex]:
        """$class_Sketch_sqrt"""
        return value**0.5

    @classmethod
    def floor(cls, value: float) -> int:
        """$class_Sketch_floor"""
        return int(np.floor(value))

    @classmethod
    def ceil(cls, value: float) -> int:
        """$class_Sketch_ceil"""
        return int(np.ceil(value))

    @classmethod
    def exp(cls, value: float) -> float:
        """$class_Sketch_exp"""
        return np.exp(value)

    @classmethod
    def log(cls, value: float) -> float:
        """$class_Sketch_log"""
        return np.log(value)

    @classmethod
    def random_seed(cls, seed: int) -> None:
        """$class_Sketch_random_seed"""
        cls._rng = np.random.default_rng(seed)

    @overload
    def random(cls) -> float:
        """$class_Sketch_random"""
        pass

    @overload
    def random(cls, high: float) -> float:
        """$class_Sketch_random"""
        pass

    @overload
    def random(cls, low: float, high: float) -> float:
        """$class_Sketch_random"""
        pass

    @classmethod
    def random(cls, *args: float) -> float:
        """$class_Sketch_random"""
        if len(args) == 0:
            return cls._rng.uniform()
        elif len(args) == 1:
            high = args[0]
            if isinstance(high, (int, float)):
                return cls._rng.uniform(0, high)
        elif len(args) == 2:
            low, high = args
            if isinstance(low, (int, float)) and isinstance(high, (int, float)):
                return cls._rng.uniform(low, high)

        types = ','.join([type(a).__name__ for a in args])
        raise TypeError(f'No matching overloads found for Sketch.random({types})')

    @overload
    def random_int(cls) -> int:
        """$class_Sketch_random_int"""
        pass

    @overload
    def random_int(cls, high: int) -> int:
        """$class_Sketch_random_int"""
        pass

    @overload
    def random_int(cls, low: int, high: int) -> int:
        """$class_Sketch_random_int"""
        pass

    @classmethod
    def random_int(cls, *args: int) -> int:
        """$class_Sketch_random_int"""
        if len(args) == 0:
            return cls._rng.integers(0, 1, endpoint=True)
        elif len(args) == 1:
            high = args[0]
            if isinstance(high, int):
                return cls._rng.integers(0, high, endpoint=True)
        elif len(args) == 2:
            low, high = args
            if isinstance(low, int) and isinstance(high, int):
                return cls._rng.integers(low, high, endpoint=True)

        types = ','.join([type(a).__name__ for a in args])
        raise TypeError(f'No matching overloads found for Sketch.random_int({types})')

    @classmethod
    def random_choice(cls, objects: List[Any]) -> Any:
        """$class_Sketch_random_choice"""
        return cls._rng.choice(objects)

    @overload
    def random_gaussian(cls) -> float:
        """$class_Sketch_random_gaussian"""
        pass

    @overload
    def random_gaussian(cls, loc: float) -> float:
        """$class_Sketch_random_gaussian"""
        pass

    @overload
    def random_gaussian(cls, loc: float, scale: float) -> float:
        """$class_Sketch_random_gaussian"""
        pass

    @classmethod
    def random_gaussian(cls, *args: float) -> float:
        """$class_Sketch_random_gaussian"""
        if len(args) == 0:
            return cls._rng.normal()
        elif len(args) == 1:
            loc = args[0]
            if isinstance(loc, int):
                return cls._rng.normal(loc)
        elif len(args) == 2:
            loc, scale = args
            if isinstance(loc, (int, float)) and isinstance(scale, (int, float)):
                return cls._rng.normal(loc, scale)

        types = ','.join([type(a).__name__ for a in args])
        raise TypeError(f'No matching overloads found for Sketch.random_gaussian({types})')

    @overload
    def noise(cls, x: float, **kwargs) -> float:
        """$class_Sketch_noise"""
        pass

    @overload
    def noise(cls, x: float, y: float, **kwargs) -> float:
        """$class_Sketch_noise"""
        pass

    @overload
    def noise(cls, x: float, y: float, z: float, **kwargs) -> float:
        """$class_Sketch_noise"""
        pass

    @overload
    def noise(cls, x: float, y: float, z: float, w: float, **kwargs) -> float:
        """$class_Sketch_noise"""
        pass

    @classmethod
    def noise(cls, *args, **kwargs) -> float:
        """$class_Sketch_noise"""
        len_args = len(args)
        noise_args = {
            'octaves': cls._NOISE_OCTAVES,
            'persistence': cls._NOISE_PERSISTENCE,
            'lacunarity': cls._NOISE_LACUNARITY,
            'base': cls._NOISE_SEED,
            # this will override other parameters if specified by the user
            **kwargs
        }
        noisef = lambda *x, **_: x[0]
        if cls._NOISE_MODE == cls.PERLIN_NOISE:
            if not len_args in [1, 2, 3]:
                raise RuntimeError('Sorry, Perlin noise can only be generated in 1, 2, or 3 dimensions.')
            noisef = {1: noise.pnoise1, 2: noise.pnoise2, 3: noise.pnoise3}[len_args]
        elif cls._NOISE_MODE == cls.SIMPLEX_NOISE:
            if not len_args in [1, 2, 3, 4]:
                raise RuntimeError('Sorry, Simplex noise can only be generated in 1, 2, 3, or 4 dimensions.')
            noisef = {1: noise.snoise2, 2: noise.snoise2, 3: noise.snoise3, 4: noise.snoise4}[len_args]
            if len_args == 1:
                args = args[0], 0
            if len_args in [3, 4]:
                del noise_args['base']
        if any(isinstance(v, np.ndarray) for v in args):
            noisef = np.vectorize(noisef)
        return noisef(*args, **noise_args)

    @classmethod
    def noise_mode(cls, mode: int) -> None:
        """$class_Sketch_noise_mode"""
        if mode in [cls.PERLIN_NOISE, cls.SIMPLEX_NOISE]:
            cls._NOISE_MODE = mode

    @classmethod
    def noise_detail(cls, octaves: float = None, persistence: float = None,
                     lacunarity: float = None) -> None:
        """$class_Sketch_noise_detail"""
        if octaves:
            cls._NOISE_OCTAVES = octaves
        if persistence:
            cls._NOISE_PERSISTENCE = persistence
        if lacunarity:
            cls._NOISE_LACUNARITY = lacunarity

    @classmethod
    def noise_seed(cls, seed: int) -> None:
        """$class_Sketch_noise_seed"""
        # NOTE: perlin noise requires integer seeds
        cls._NOISE_SEED = seed
