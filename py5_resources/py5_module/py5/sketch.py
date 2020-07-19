# -*- coding: utf-8 -*-
# *** FORMAT PARAMS ***
import time
import os
from pathlib import Path
from typing import overload, Any, Callable, Union, Dict, List  # noqa

import numpy as np
from PIL import Image

from .methods import Py5Methods, Py5Exception  # noqa
from .java_types import _Py5Applet, Py5Applet
from .java_types import *  # noqa

from .mixins import MathMixin, DataMixin, ImageMixin, ThreadsMixin
from .mixins.threads import Py5Promise  # noqa
from .mixins.image import PImageCache, _check_pimage_cache_or_convert  # noqa
from .shader import Py5Shader, _return_py5shader, _py5shader_param  # noqa
from .font import Py5Font, _return_py5font, _py5font_param  # noqa
from .shape import Py5Shape, _return_py5shape, _py5shape_param  # noqa
from .surface import Py5Surface, _return_py5surface  # noqa
from .graphics import Py5Graphics, _return_py5graphics, _py5graphics_param  # noqa


sketch_class_members_code = None  # DELETE

_METHODS = ['settings', 'setup', 'draw', 'key_pressed', 'key_typed',
            'key_released', 'mouse_clicked', 'mouse_dragged', 'mouse_moved',
            'mouse_entered', 'mouse_exited', 'mouse_pressed', 'mouse_released',
            'mouse_wheel', 'exiting']


class Py5Base:

    def __init__(self, instance):
        self._instance = instance

    def _shutdown(self):
        self._shutdown_complete = True


class Sketch(MathMixin, DataMixin, ImageMixin, ThreadsMixin, Py5Base):

    _cls = _Py5Applet

    def __init__(self, *args, **kwargs):
        self._py5applet = _Py5Applet()
        super().__init__(instance=self._py5applet)
        self.set_pimage_cache(PImageCache(self._py5applet))
        self._methods_to_profile = []
        # must always keep the py5_methods reference count from hitting zero.
        # otherwise, it will be garbage collected and lead to segmentation faults!
        self._py5_methods = None

    def get_py5applet(self) -> Py5Applet:
        return self._py5applet

    def run_sketch(self, block: bool = True, py5_options: List = None, sketch_args: List = None) -> None:
        """$class_run_sketch"""
        if not hasattr(self, '_instance'):
            raise RuntimeError(
                ('py5 internal problem: did you create a class with an `__init__()` '
                 'method without a call to `super().__init__()`?')
            )

        methods = dict([(e, getattr(self, e)) for e in _METHODS if hasattr(self, e)])
        self._run_sketch(methods, block, py5_options, sketch_args)

    def _run_sketch(self,
                    methods: Dict[str, Callable],
                    block: bool,
                    py5_options: List = None,
                    sketch_args: List = None) -> None:
        self._py5_methods = Py5Methods(self)
        self._py5_methods.set_functions(**methods)
        self._py5_methods.profile_functions(self._methods_to_profile)
        self._py5applet.usePy5Methods(self._py5_methods)

        if not py5_options: py5_options = []
        if not sketch_args: sketch_args = []
        if not any([a.startswith('--sketch-path') for a in py5_options]):
            py5_options.append('--sketch-path=' + os.getcwd())
        args = py5_options + [''] + sketch_args

        _Py5Applet.runSketch(args, self._py5applet)

        if block:
            # wait for the sketch to finish
            surface = self.get_surface()
            while not surface.is_stopped():
                time.sleep(0.25)

            # wait no more than 1 second for any shutdown tasks to complete
            time_waited = 0
            while not hasattr(self, '_shutdown_complete') and time_waited < 1.0:
                pause = 0.01
                time_waited += pause
                time.sleep(pause)

    def exit_sketch(self) -> None:
        """$class_exit_sketch"""
        if not self.get_surface().is_stopped():
            self._py5applet.exit()

    def _shutdown(self):
        super()._shutdown()

    def _terminate_sketch(self):
        self.get_surface().stop_thread()
        self._shutdown()

    # *** BEGIN METHODS ***

    def hot_reload_draw(self, draw: Callable) -> None:
        """$class_hot_reload_draw"""
        self._py5_methods.set_functions(**dict(draw=draw))

    def profile_functions(self, function_names: List[str]) -> None:
        """$class_profile_functions"""
        if self._py5_methods is None:
            self._methods_to_profile.extend(function_names)
        else:
            self._py5_methods.profile_functions(function_names)

    def profile_draw(self) -> None:
        """$class_profile_draw"""
        self.profile_functions(['draw'])

    def print_line_profiler_stats(self) -> None:
        """$class_print_line_profiler_stats"""
        self._py5_methods.dump_stats()

    # *** Pixel methods ***

    def get_pixels(self) -> np.ndarray:
        """$class_get_pixels"""
        pixels = np.frombuffer(self._instance.loadAndGetPixels(), dtype=np.uint8)
        return pixels.reshape(self.height, self.width, 4).copy()

    def set_pixels(self, new_pixels: np.ndarray) -> None:
        """$class_set_pixels"""
        self._instance.setAndUpdatePixels(new_pixels.flatten().tobytes(), pass_by_reference=False)

    def save_frame(self, filename: Union[str, Path], format: str = None, **params) -> None:
        """$class_save_frame"""
        # these are the same function calls Processing uses before saving a frame to a file
        filename = self._instance.savePath(self._instance.insertFrame(str(filename)))
        arr = np.roll(self.get_pixels(), -1, axis=2)
        Image.fromarray(arr, mode='RGBA').save(str(filename), format=format, **params)


{sketch_class_members_code}
