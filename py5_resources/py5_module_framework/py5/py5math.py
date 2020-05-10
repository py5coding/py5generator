import numpy as np


# TODO: these should all be Sketch class methods.

# TODO: should these type hints include numpy arrays? the code will still work,
# and note some of them already return scalar numpy arrays anyway.


###############################################################################
# TRIGONOMETRY
###############################################################################


def acos(value: float) -> float:
    return np.arccos(value)


def asin(value: float) -> float:
    return np.arcsin(value)


def atan(value: float) -> float:
    return np.arctan(value)


def atan2(y: float, x: float) -> float:
    return np.arctan2(y, x)


def cos(angle: float) -> float:
    return np.cos(angle)


def degrees(radians: float) -> float:
    return np.degrees(radians)


def radians(degrees: float) -> float:
    return np.radians(degrees)


def sin(angle: float) -> float:
    return np.sin(angle)


def tan(angle: float) -> float:
    return np.tan(angle)


###############################################################################
# CALCULATION
###############################################################################


def constrain(amt: float, low: float, high: float):
    return np.where(amt < low, low, np.where(amt > high, high, amt))


def lerp(start: float, stop: float, amt: float):
    return amt * (stop - start) + start


def sq(n: float) -> float:
    return n * n
