# -*- coding: utf-8 -*-
"""
py5 code, interface to the Java version of Processing using PyJNIus.

This file is created by the py5generator package. Do not edit!
"""
import sys
from pathlib import Path
import logging
import inspect
import stackprinter
import time
from typing import overload, NewType, Any, Callable, Dict, List

import numpy as np

import py5_tools

class_members_code = None  # DELETE
module_members_code = None  # DELETE
run_sketch_pre_run_code = None  # DELETE
str_py5_dir = None  # DELETE
str_py5_all = None  # DELETE

if not py5_tools.py5_started:
    current_classpath = py5_tools.get_classpath()
    base_path = Path(
        getattr(sys, '_MEIPASS', Path(__file__).absolute().parent))
    # add py5 jars to the classpath first
    py5_tools.set_classpath(str(base_path / 'jars' / '*'))
    # if the cwd has a jars subdirectory, add that next
    py5_tools.add_jars(Path('jars'))
    # put the original classpath at the end while avoiding duplicates
    py5_tools.add_classpath(*[p for p in current_classpath
                              if p not in py5_tools.get_classpath()])
    py5_tools.py5_started = True
from jnius import autoclass, PythonJavaClass, java_method, JavaException  # noqa


__version__ = '0.1'

logger = logging.getLogger(__name__)


# *** stacktrace configuration ***
# set stackprinter color style. Default is plaintext. Other choices are darkbg,
# darkbg2, darkbg3, lightbg, lightbg2, lightbg3.
_stackprinter_style = 'plaintext'
# prune tracebacks to only show only show stack levels in the user's py5 code.
_prune_tracebacks = True


_Py5Applet = autoclass('py5.core.Py5Applet',
                       include_protected=False, include_private=False)
Py5Applet = NewType('Py5Applet', _Py5Applet)
_PImage = autoclass('processing.core.PImage',
                    include_protected=False, include_private=False)
PImage = NewType('PImage', _PImage)
_PGraphics = autoclass('processing.core.PGraphics',
                       include_protected=False, include_private=False)
PGraphics = NewType('PGraphics', _PGraphics)
_PGL = autoclass('processing.opengl.PGL',
                 include_protected=False, include_private=False)
PGL = NewType('PGL', _PGL)
_PShader = autoclass('processing.opengl.PShader',
                     include_protected=False, include_private=False)
PShader = NewType('PShader', _PShader)
_PFont = autoclass('processing.core.PFont',
                   include_protected=False, include_private=False)
PFont = NewType('PFont', _PFont)
_PShape = autoclass('processing.core.PShape',
                    include_protected=False, include_private=False)
PShape = NewType('PShape', _PShape)
_PSurface = autoclass('processing.core.PSurface',
                      include_protected=False, include_private=False)
PSurface = NewType('PSurface', _PSurface)


class Py5Methods(PythonJavaClass):
    __javainterfaces__ = ['py5/core/Py5Methods']

    def __init__(self, sketch):
        self._sketch = sketch
        self._functions = dict()

    def set_functions(self, **kwargs):
        self._functions.update(kwargs)

    @java_method('()[Ljava/lang/Object;')
    def get_function_list(self):
        return self._functions.keys()

    @java_method('(Ljava/lang/String;[Ljava/lang/Object;)V')
    def run_method(self, method_name, params):
        try:
            if method_name in self._functions:
                self._functions[method_name](*params)
        except Exception:
            exc_type, exc_value, exc_tb = sys.exc_info()

            if _prune_tracebacks:
                def _prune_traceback(exc_tb):
                    # remove py5 traceback frames at the top and bottom of the stack
                    prev_tb = exc_tb
                    start_tb = exc_tb.tb_next
                    tb = start_tb
                    while hasattr(tb, 'tb_next') and hasattr(tb, 'tb_frame') and tb.tb_frame.f_code.co_filename != __file__:
                        prev_tb = tb
                        tb = tb.tb_next
                    prev_tb.tb_next = None
                    return exc_tb

                exc_tb = _prune_traceback(exc_tb)
                prev_exc = exc_value
                next_exc = exc_value.__context__
                while next_exc:
                    while isinstance(prev_exc, Py5Exception) and isinstance(next_exc, JavaException):
                        prev_exc.__context__ = next_exc.__context__
                        next_exc = next_exc.__context__
                    if not next_exc:
                        break
                    next_exc.__traceback__ = _prune_traceback(next_exc.__traceback__)
                    prev_exc = next_exc
                    next_exc = next_exc.__context__

            stackprinter.show(thing=(exc_type, exc_value, exc_tb.tb_next),
                              show_vals='line',
                              style=_stackprinter_style,
                              suppressed_paths=[r"lib/python.*?/site-packages/numpy/",
                                                r"lib/python.*?/site-packages/py5/",
                                                r"lib/python.*?/site-packages/jnius/"])

            sys.last_type, sys.last_value, sys.last_traceback = exc_type, exc_value, exc_tb
            self._sketch.get_surface().stopThread()


class Py5Exception(Exception):

    def __init__(self, exception_classname, msg, method, args, kwargs):
        super().__init__()
        self.exception_classname = exception_classname
        self.msg = msg
        self.method = method
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        return self.exception_classname + ' thrown while calling ' + self.method + ': ' + self.msg

    def __repr__(self):
        return str(self)


_METHODS = ['settings', 'setup', 'draw', 'key_pressed', 'key_typed',
            'key_released', 'mouse_clicked', 'mouse_dragged', 'mouse_moved',
            'mouse_entered', 'mouse_exited', 'mouse_pressed', 'mouse_released',
            'mouse_wheel', 'exit_actual']


class Sketch:

    def __init__(self):
        self._py5applet = _Py5Applet()

    def run_sketch(self, block: bool = True) -> None:
        methods = dict([(e, getattr(self, e)) for e in _METHODS if hasattr(self, e)])
        self._run_sketch(methods, block)

    def _run_sketch(self, methods: Dict[str, Callable], block: bool) -> None:
        py5_methods = Py5Methods(self)
        py5_methods.set_functions(**methods)

        # pass the py5_methods object to the py5applet object while also
        # keeping the py5_methods reference count from hitting zero. otherwise,
        # it will be garbage collected and lead to segmentation faults!
        self._py5applet.usePy5Methods(py5_methods)
        self._py5_methods = py5_methods

        _Py5Applet.runSketch([''], self._py5applet)

        if block:
            # wait for the sketch to finish
            surface = self.get_surface()
            while not surface.isStopped():
                time.sleep(0.25)

    def exit_sketch(self) -> None:
        """Exit the sketch
        """
        if not self.get_surface().isStopped():
            self._py5applet.exit()

    def get_py5applet(self) -> Py5Applet:
        return self._py5applet

    def hot_reload_draw(self, draw):
        self._py5_methods.set_functions(**dict(draw=draw))

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

    @classmethod
    def pixels_to_numpy(cls, pixels: List[int], colors: str = 'RGBA') -> np.ndarray:
        np_pixels = np.array(pixels, dtype=np.uint32)
        out = np.empty(shape=(np_pixels.size, len(colors)), dtype=np.uint8)

        for i, c in enumerate(list(colors.upper())):
            if c == 'A':
                out[:, i] = (np_pixels & 0xFF000000) >> 24
            elif c == 'R':
                out[:, i] = (np_pixels & 0x00FF0000) >> 16
            elif c == 'G':
                out[:, i] = (np_pixels & 0x0000FF00) >> 8
            elif c == 'B':
                out[:, i] = (np_pixels & 0x000000FF)

        return out

    @classmethod
    def numpy_to_pixels(cls, pixel_array: np.ndarray, colors: str = 'RGBA') -> List[int]:
        assert len(colors) == pixel_array.shape[-1]
        colors = colors.upper()
        pixel_array = pixel_array.astype(np.int32).reshape(
            pixel_array.size // len(colors), len(colors))

        blue_index = colors.find('B')
        pixel_array[:, blue_index] |= pixel_array[:, colors.find('R')] << 16
        pixel_array[:, blue_index] |= pixel_array[:, colors.find('G')] << 8
        if 'A' in colors:
            pixel_array[:, blue_index] |= pixel_array[:, colors.find('A')] << 24
        else:
            pixel_array[:, blue_index] |= 0xFF000000

        return pixel_array[:, blue_index].tolist()


{class_members_code}


_py5sketch = Sketch()
_py5sketch_used = False

{module_members_code}


def run_sketch(function_dict: Dict[str, Any] = None, block: bool = True) -> None:
    """run the py5 sketch

    The function_dict needs to a be a dictionary that contains the settings,
    setup, and draw functions.

    Most likely you want to call it like this:
    ```
        py5.run_sketch(function_dict=locals())
    ```
    """
    # Before running the sketch, delete the module fields that need to be kept
    # uptodate. This will allow the module `__getattr__` function return the
    # proper values.
    try:
        {run_sketch_pre_run_code}
    except NameError:
        # these variables might have already been removed
        pass

    if not function_dict:
        function_dict = inspect.stack()[1].frame.f_locals
    methods = dict([(e, function_dict[e]) for e in _METHODS if e in function_dict])

    if not set(methods.keys()) & set(['settings', 'setup', 'draw']):
        print(("Unable to find settings, setup, or draw functions. "
               "Your sketch will be a small boring gray square. "
               "If this isn't what you intended, try this instead:\n"
               "py5.run_sketch(function_dict=locals())"))

    _py5sketch._run_sketch(methods, block)


def reset_py5() -> None:
    """ attempt to reset the py5 library so a new sketch can be executed.

    There are race conditions between this and `stop_sketch`. If you call this
    immediately after `stop_sketch` you might experience problems. This function
    is here as a convenience to people who need it and are willing to cope with
    the race condition issue.
    """
    global _py5sketch
    global _py5sketch_used
    _py5sketch = Sketch()
    _py5sketch_used = False


def __getattr__(name):
    if hasattr(_py5sketch, name):
        return getattr(_py5sketch, name)
    else:
        raise AttributeError('py5 has no function or method named ' + name)


def __dir__():
    return {str_py5_dir}


__all__ = {str_py5_all}
