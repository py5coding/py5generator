# -*- coding: utf-8 -*-
# *** FORMAT PARAMS ***
"""
py5 code, interface to the Java version of Processing using PyJNIus.
"""
import sys
from pathlib import Path
import logging
import inspect
import time
import json
from typing import overload, NewType, Any, Callable, Union, Dict, List  # noqa

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
from jnius import autoclass  # noqa
from .methods import Py5Methods, Py5Exception  # noqa


__version__ = '0.1'

logger = logging.getLogger(__name__)


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


_METHODS = ['settings', 'setup', 'draw', 'key_pressed', 'key_typed',
            'key_released', 'mouse_clicked', 'mouse_dragged', 'mouse_moved',
            'mouse_entered', 'mouse_exited', 'mouse_pressed', 'mouse_released',
            'mouse_wheel', 'exit_actual']


class Sketch:

    def __init__(self):
        self._py5applet = _Py5Applet()
        self._methods_to_profile = []
        # must always keep the py5_methods reference count from hitting zero.
        # otherwise, it will be garbage collected and lead to segmentation faults!
        self._py5_methods = None

    def run_sketch(self, block: bool = True) -> None:
        methods = dict([(e, getattr(self, e)) for e in _METHODS if hasattr(self, e)])
        self._run_sketch(methods, block)

    def _run_sketch(self, methods: Dict[str, Callable], block: bool) -> None:
        self._py5_methods = Py5Methods(self)
        self._py5_methods.set_functions(**methods)
        self._py5_methods.profile_functions(self._methods_to_profile)
        self._py5applet.usePy5Methods(self._py5_methods)

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

    def profile_functions(self, function_names):
        if self._py5_methods is None:
            self._methods_to_profile.extend(function_names)
        else:
            self._py5_methods.profile_functions(function_names)

    def profile_draw(self):
        self.profile_functions(['draw'])

    def print_line_profiler_stats(self):
        self._py5_methods.dump_stats()

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

    def get_pixels(self) -> np.ndarray:
        pixels = np.frombuffer(self._py5applet.loadAndGetPixels().tostring(), dtype=np.uint8)
        return pixels.reshape(self.height, self.width, 4).copy()

    def set_pixels(self, new_pixels: np.ndarray):
        self._py5applet.setAndUpdatePixels(new_pixels.flatten().tobytes(), pass_by_reference=False)

    @classmethod
    def load_json(cls, filename: Union[str, Path], **kwargs: Dict[str, Any]) -> Any:
        with open(filename, 'r') as f:
            return json.load(f, **kwargs)

    @classmethod
    def save_json(cls, json_data: Any, filename: Union[str, Path], **kwargs: Dict[str, Any]):
        with open(filename, 'w') as f:
            json.dump(json_data, f, **kwargs)

    @classmethod
    def parse_json(cls, serialized_json: Any, **kwargs: Dict[str, Any]) -> Any:
        return json.loads(serialized_json, **kwargs)


{class_members_code}


_py5sketch = Sketch()
_py5sketch_used = False

{module_members_code}


def run_sketch(function_dict: Dict[str, Any] = None, block: bool = True) -> None:
    """run the py5 sketch

    The optional function_dict parameter needs to a be a dictionary that
    contains the settings, setup, and draw functions.

    You can call it like this:
    ```
        py5.run_sketch(function_dict=locals())
    ```

    But most likely you can just do this:
    ```
        py5.run_sketch()
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
        raise AttributeError('py5 has no function or field named ' + name)


def __dir__():
    return {str_py5_dir}


__all__ = {str_py5_all}
