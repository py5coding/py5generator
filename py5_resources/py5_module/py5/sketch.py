# -*- coding: utf-8 -*-
# *** FORMAT PARAMS ***
import time
from typing import overload, NewType, Any, Callable, Union, Dict, List  # noqa

import numpy as np

from .methods import Py5Methods
from .java_types import _Py5Applet, Py5Applet
from .java_types import *  # noqa

from .mixins import MathMixin, DataMixin, ImageMixin


class_members_code = None  # DELETE

_METHODS = ['settings', 'setup', 'draw', 'key_pressed', 'key_typed',
            'key_released', 'mouse_clicked', 'mouse_dragged', 'mouse_moved',
            'mouse_entered', 'mouse_exited', 'mouse_pressed', 'mouse_released',
            'mouse_wheel', 'exit_actual']


class SketchBase:

    def __init__(self, py5applet):
        self._py5applet = py5applet

    def get_py5applet(self) -> Py5Applet:
        return self._py5applet


class Sketch(MathMixin, DataMixin, ImageMixin, SketchBase):

    def __init__(self, *args, **kwargs):
        super().__init__(py5applet=_Py5Applet())
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

    # *** Pixel methods ***

    def get_pixels(self) -> np.ndarray:
        pixels = np.frombuffer(self._py5applet.loadAndGetPixels().tostring(), dtype=np.uint8)
        return pixels.reshape(self.height, self.width, 4).copy()

    def set_pixels(self, new_pixels: np.ndarray):
        self._py5applet.setAndUpdatePixels(new_pixels.flatten().tobytes(), pass_by_reference=False)


{class_members_code}
