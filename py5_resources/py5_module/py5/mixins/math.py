from typing import overload, Union

import numpy as np
from numpy.random import MT19937
from numpy.random import RandomState, SeedSequence

import noise


class MathMixin:

    _rs = RandomState(MT19937(SeedSequence()))

    SIMPLEX_NOISE = 1  # CODEBUILDER INCLUDE
    PERLIN_NOISE = 2  # CODEBUILDER INCLUDE
    _NOISE_MODE = SIMPLEX_NOISE
    _NOISE_SEED = 0
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

    @classmethod
    def dist(cls, *args: float) -> float:
        """$class_Sketch_dist"""
        p1 = args[:(len(args) // 2)]
        p2 = args[(len(args) // 2):]
        assert len(p1) == len(p2)
        return sum([(a - b)**2 for a, b in zip(p1, p2)])**0.5

    @classmethod
    def lerp(cls, start: float, stop: float, amt: float) -> float:
        """$class_Sketch_lerp"""
        return amt * (stop - start) + start

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

    @overload
    def random(cls, high: float) -> float:
        """$class_Sketch_random"""
        pass

    @overload
    def random(cls, low: float, high: float) -> float:
        """$class_Sketch_random"""
        pass

    @classmethod
    def random_seed(cls, seed: int) -> None:
        """$class_Sketch_random_seed"""
        cls._rs = RandomState(MT19937(SeedSequence(seed)))

    @classmethod
    def random(cls, *args: float) -> float:
        """$class_Sketch_random"""
        if len(args) == 1:
            high = args[0]
            if isinstance(high, (int, float)):
                return high * cls._rs.rand()
        elif len(args) == 2:
            low, high = args
            if isinstance(low, (int, float)) and isinstance(high, (int, float)):
                return low + (high - low) * cls._rs.rand()

        types = ','.join([type(a).__name__ for a in args])
        raise TypeError(f'No matching overloads found for Sketch.random({types})')

    @classmethod
    def random_gaussian(cls) -> float:
        """$class_Sketch_random_gaussian"""
        return cls._rs.randn()

    # TODO: write typehints

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
                raise RuntimeError('Sorry, this noise function can only generate 1D, 2D, or 3D Perlin noise.')
            noisef = {1: noise.pnoise1, 2: noise.pnoise2, 3: noise.pnoise3}[len_args]
        elif cls._NOISE_MODE == cls.SIMPLEX_NOISE:
            if not len_args in [1, 2, 3, 4]:
                raise RuntimeError('Sorry, this noise function can only generate 1D, 2D, 3D, or 4D Simplex noise.')
            noisef = {1: noise.snoise2, 2: noise.snoise2, 3: noise.snoise3, 4: noise.snoise4}[len_args]
            if len_args == 1:
                args = args[0], 0
        if any(isinstance(v, np.ndarray) for v in args):
            noisef = np.vectorize(noisef)
        return noisef(*args, **noise_args)

    @classmethod
    def noise_mode(cls, mode: int) -> None:
        """$class_Sketch_noise_mode"""
        if mode in [cls.PERLIN_NOISE, cls.SIMPLEX_NOISE]:
            cls._NOISE_MODE = mode

    @classmethod
    def noise_detail(cls, args: float) -> None:
        """$class_Sketch_noise_detail"""
        # TODO: how to write this function cleanly?
        pass

    @classmethod
    def noise_seed(cls, seed: float) -> None:
        """$class_Sketch_noise_seed"""
        cls._NOISE_SEED = seed
