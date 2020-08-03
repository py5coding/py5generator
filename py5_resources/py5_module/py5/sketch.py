# -*- coding: utf-8 -*-
# *** FORMAT PARAMS ***
import time
import os
from pathlib import Path
import tempfile
from typing import overload, Any, Callable, Union, Dict, List  # noqa
from nptyping import NDArray, Float  # noqa

import jpype
from jpype.types import JArray, JString, JFloat, JInt, JChar  # noqa

import numpy as np  # noqa

from .methods import Py5Methods, Py5Exception  # noqa
from .base import Py5Base
from .mixins import MathMixin, DataMixin, ThreadsMixin, PixelMixin
from .mixins.threads import Py5Promise  # noqa
from .image import Py5Image, _return_py5image  # noqa
from .shape import Py5Shape, _return_py5shape  # noqa
from .surface import Py5Surface, _return_py5surface  # noqa
from .shader import Py5Shader, _return_py5shader  # noqa
from .font import Py5Font, _return_py5font  # noqa
from .graphics import Py5Graphics, _return_py5graphics  # noqa
from .pmath import _get_matrix_wrapper  # noqa
from . import image_conversion
from .image_conversion import NumpyImageArray


sketch_class_members_code = None  # DELETE

_METHODS = ['settings', 'setup', 'draw', 'key_pressed', 'key_typed',
            'key_released', 'mouse_clicked', 'mouse_dragged', 'mouse_moved',
            'mouse_entered', 'mouse_exited', 'mouse_pressed', 'mouse_released',
            'mouse_wheel', 'exiting']


_Py5Applet = jpype.JClass('py5.core.Py5Applet')


class Sketch(MathMixin, DataMixin, ThreadsMixin, PixelMixin, Py5Base):

    _cls = _Py5Applet

    def __init__(self, *args, **kwargs):
        self._py5applet = _Py5Applet()
        super().__init__(instance=self._py5applet)
        self._methods_to_profile = []
        # must always keep the py5_methods reference count from hitting zero.
        # otherwise, it will be garbage collected and lead to segmentation faults!
        self._py5_methods = None

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

        try:
            _Py5Applet.runSketch(args, self._py5applet)
        except Exception as e:
            print('exception thrown by Py5Applet.runSketch:', e)

        if block:
            # wait for the sketch to finish
            surface = self.get_surface()
            if surface._instance is not None:
                while not surface.is_stopped():
                    time.sleep(0.25)

            # wait no more than 1 second for any shutdown tasks to complete
            time_waited = 0
            while not hasattr(self, '_shutdown_complete') and time_waited < 1.0:
                pause = 0.01
                time_waited += pause
                time.sleep(pause)

    def _shutdown(self):
        super()._shutdown()

    def _terminate_sketch(self):
        surface = self.get_surface()
        if surface._instance is not None:
            surface.stop_thread()
        self._shutdown()

    # *** BEGIN METHODS ***

    def exit_sketch(self) -> None:
        """$class_exit_sketch"""
        # TODO: why do I need this if statement? and if I remove it, I am then basically just
        # renaming exit to exit_sketch and don't need this at all.
        if not self.get_surface().is_stopped():
            self._py5applet.exit()

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

    def save_frame(self, filename: Union[str, Path], format: str = None, **params) -> None:
        """$class_save_frame"""
        self.save(self._instance.insertFrame(str(filename)), format, **params)

    # *** Py5Image methods ***

    def create_image_from_numpy(self, numpy_image: NumpyImageArray, dst: Py5Image = None) -> Py5Image:
        """$class_create_image_from_numpy"""
        height, width = numpy_image.array.shape[:2]

        if dst:
            if width != dst.pixel_width or height != dst.pixel_height:
                raise RuntimeError("array size does not match size of dst Py5Image")
            py5_img = dst
        else:
            py5_img = self.create_image(width, height, self.ARGB)

        py5_img.set_np_pixels(numpy_image.array, numpy_image.bands)

        return py5_img

    def convert_image(self, obj: Any, dst: Py5Image = None) -> Py5Image:
        """$class_convert_image"""
        result = image_conversion._convert(obj)
        if isinstance(result, (Path, str)):
            return self.load_image(result, dst=dst)
        elif isinstance(result, tempfile._TemporaryFileWrapper):
            return self.load_image(result.name, dst=dst)
        elif isinstance(result, NumpyImageArray):
            return self.create_image_from_numpy(result, dst=dst)

    def load_image(self, filename: Union[str, Path], dst: Py5Image = None) -> Py5Image:
        """$class_load_image"""
        pimg = self._instance.loadImage(str(filename))
        if dst:
            if pimg.pixel_width != dst.pixel_width or pimg.pixel_height != dst.pixel_height:
                raise RuntimeError("size of loaded image does not match size of dst Py5Image")
            dst._replace_instance(pimg)
            return dst
        else:
            return Py5Image(pimg)

    def request_image(self, filename: Union[str, Path]) -> Py5Promise:
        """$class_request_image"""
        return self.launch_promise_thread(self.load_image, args=(filename,))


{sketch_class_members_code}
