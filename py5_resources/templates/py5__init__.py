"""
py5 code, interface to the Java version of Processing using PyJNIus.

This file is created by the py5generator package. Do not edit!
"""
import sys
from pathlib import Path
import logging
import traceback
import inspect
import stackprinter
import time
from typing import Any, Callable, Dict, List

import numpy as np

import py5_tools


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
from jnius import autoclass, PythonJavaClass, java_method  # noqa


__version__ = '0.1'

logger = logging.getLogger(__name__)

_prune_tracebacks = True

try:
    from IPython.core import ultratb
    _tbhandler = ultratb.VerboseTB(color_scheme='NoColor', tb_offset=1)
except Exception:
    def _tbhandler(exc_type, exc_value, exc_tb):
        tbe = traceback.TracebackException(exc_type, exc_value, exc_tb)
        # method_name = 'draw'
        # msg = 'exception running ' + method_name + ': ' + str(exc_value)
        tb = list(tbe.format())
        msg = '\n' + tb[0] + ''.join(tb[2:-1]) + '\n' + tb[-1]
        print(msg)


_Py5Applet = autoclass('py5.core.Py5Applet',
                       include_protected=False, include_private=False)


class Py5Methods(PythonJavaClass):
    __javainterfaces__ = ['py5/core/Py5Methods']

    def __init__(self):
        self._functions = dict()

    def set_functions(self, **kwargs):
        self._functions.update(kwargs)

    def set_py5applet(self, _py5applet):
        self._py5applet = _py5applet

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
                prev_tb = exc_tb
                start_tb = exc_tb.tb_next
                tb = start_tb
                while hasattr(tb, 'tb_next') and hasattr(tb, 'tb_frame') and tb.tb_frame.f_code.co_filename != __file__:
                    prev_tb = tb
                    tb = tb.tb_next
                prev_tb.tb_next = None

            exc_value.__suppress_context__ = True
            stackprinter.show(thing=(exc_type, exc_value, exc_tb.tb_next), show_vals='line')
            # _tbhandler(exc_type, exc_value, exc_tb)

            sys.last_type, sys.last_value, sys.last_traceback = exc_type, exc_value, exc_tb
            self._py5applet.getSurface().stopThread()


class Py5Exception(Exception):

    def __init__(self, exception_classname, msg, method, stack, args, kwargs):
        super().__init__()
        self.exception_classname = exception_classname
        self.msg = msg
        self.method = method
        self.stack = stack
        self.args = args
        self.kwargs = kwargs

    def format_stack_trace(self):
        out = '\n' + ('-' * 75) + '\n' + self.exception_classname + '\n'
        for s in self.stack:
            out += s.filename + ' in ' + s.function + '\n'
            out += (' ' * 6) + str(s.lineno) + (' ' * 5) + s.code_context[s.index]
        return out

        return out

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
        py5_methods = Py5Methods()
        py5_methods.set_functions(**methods)
        py5_methods.set_py5applet(self._py5applet)

        # pass the py5_methods object to the py5applet object while also
        # keeping the py5_methods reference count from hitting zero. otherwise,
        # it will be garbage collected and lead to segmentation faults!
        self._py5applet.usePy5Methods(py5_methods)
        self._py5_methods = py5_methods

        _Py5Applet.runSketch([''], self._py5applet)

        if block:
            # wait for the sketch to finish
            surface = self._py5applet.getSurface()
            while not surface.isStopped():
                time.sleep(0.25)

    def exit_sketch(self) -> None:
        """Exit the sketch
        """
        if not self._py5applet.getSurface().isStopped():
            self._py5applet.exit()

    def get_py5applet(self) -> _Py5Applet:
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
    def constrain(cls, amt: float, low: float, high: float):
        return np.where(amt < low, low, np.where(amt > high, high, amt))

    @classmethod
    def lerp(cls, start: float, stop: float, amt: float):
        return amt * (stop - start) + start

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


{0}


_py5sketch = Sketch()
_py5sketch_used = False

{1}


def run_sketch(function_dict: Dict[str, Any] = None, block: bool = True) -> None:
    """run the py5 sketch

    The function_dict needs to a be a dictionary that contains the settings,
    setup, and draw functions.

    Most likely you want to call it like this:
    ```
        py5.run_sketch(function_dict=locals())
    ```
    """
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
    return {2}


__all__ = {3}


class Py5ExceptHook:

    def __init__(self, except_hook):
        self._except_hook = except_hook

    def __call__(self, type_, value, traceback):
        print('****** Exception thrown:' + type_ + ' ********')
        self._except_hook(type_, value, traceback)


sys.excepthook = Py5ExceptHook(sys.excepthook)
