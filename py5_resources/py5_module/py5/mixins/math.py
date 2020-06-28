import numpy as np


class MathMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # *** BEGIN METHODS ***

    @classmethod
    def sin(cls, angle: float) -> float:
        return np.sin(angle)

    @classmethod
    def cos(cls, angle: float) -> float:
        return np.cos(angle)

    @classmethod
    def tan(cls, angle: float) -> float:
        return np.tan(angle)

    @classmethod
    def asin(cls, value: float) -> float:
        return np.arcsin(value)

    @classmethod
    def acos(cls, value: float) -> float:
        return np.arccos(value)

    @classmethod
    def atan(cls, value: float) -> float:
        return np.arctan(value)

    @classmethod
    def atan2(cls, y: float, x: float) -> float:
        return np.arctan2(y, x)

    @classmethod
    def degrees(cls, radians: float) -> float:
        return np.degrees(radians)

    @classmethod
    def radians(cls, degrees: float) -> float:
        return np.radians(degrees)

    @classmethod
    def constrain(cls, amt: float, low: float, high: float) -> float:
        return np.where(amt < low, low, np.where(amt > high, high, amt))

    @classmethod
    def dist(cls, *args) -> float:
        p1 = args[:(len(args) // 2)]
        p2 = args[(len(args) // 2):]
        assert len(p1) == len(p2)
        return sum([(a - b)**2 for a, b in zip(p1, p2)])**0.5

    @classmethod
    def lerp(cls, start: float, stop: float, amt: float):
        return amt * (stop - start) + start

    @classmethod
    def mag(cls, *args) -> float:
        return sum([x * x for x in args])**0.5

    @classmethod
    def norm(cls, value: float, start: float, stop: float) -> float:
        return (value - start) / (stop - start)

    @classmethod
    def sq(cls, n: float) -> float:
        return n * n
