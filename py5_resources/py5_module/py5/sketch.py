# -*- coding: utf-8 -*-
# *** FORMAT PARAMS ***
import time
import os
from pathlib import Path
import tempfile
from typing import overload, Any, Callable, Union, Dict, List  # noqa

import numpy as np

from .methods import Py5Methods, Py5Exception  # noqa
from .java_types import _Py5Applet, Py5Applet, _Py5Image

from .base import Py5Base
from .mixins import MathMixin, DataMixin, ThreadsMixin, PixelMixin
from .mixins.threads import Py5Promise  # noqa
from .shader import Py5Shader, _return_py5shader, _py5shader_param  # noqa
from .font import Py5Font, _return_py5font, _py5font_param  # noqa
from .shape import Py5Shape, _return_py5shape, _py5shape_param  # noqa
from .surface import Py5Surface, _return_py5surface  # noqa
from .graphics import Py5Graphics, _return_py5graphics, _py5graphics_param  # noqa
from .image import Py5Image, _return_py5image, _py5image_param  # noqa
from .converter import Converter


sketch_class_members_code = None  # DELETE

_METHODS = ['settings', 'setup', 'draw', 'key_pressed', 'key_typed',
            'key_released', 'mouse_clicked', 'mouse_dragged', 'mouse_moved',
            'mouse_entered', 'mouse_exited', 'mouse_pressed', 'mouse_released',
            'mouse_wheel', 'exiting']


class Sketch(MathMixin, DataMixin, ThreadsMixin, PixelMixin, Py5Base):

    _cls = _Py5Applet

    def __init__(self, *args, **kwargs):
        self._py5applet = _Py5Applet()
        super().__init__(instance=self._py5applet)
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

    def save_frame(self, filename: Union[str, Path], format: str = None, **params) -> None:
        """$class_save_frame"""
        self.save(self._instance.insertFrame(str(filename)), format, **params)

    # *** Py5Image methods ***

    def create_image(self, width: int, height: int, mode: str) -> Py5Image:
        """$class_create_image"""
        pimage = _Py5Image()
        pimage.init(width, height, mode)
        pimage.parent = self._instance

        return Py5Image(pimage)

    def create_image_from_numpy(self, array: np.ndarray, bands: str = 'ARGB', dst: Py5Image = None) -> Py5Image:
        """$class_create_image_from_numpy"""
        height, width, _ = array.shape

        if dst:
            py5_img = dst
        else:
            pimg = _Py5Image()
            pimg.init(width, height, self.ARGB)
            pimg.parent = self._instance
            py5_img = Py5Image(pimg)

        py5_img.load_np_pixels()

        # TODO: what about single channel alpha masks?
        if bands == 'ARGB':
            py5_img.np_pixels[:] = array
        elif bands == 'RGB':
            py5_img.np_pixels[:, :, 0] = 255
            py5_img.np_pixels[:, :, 1:] = array
        elif bands == 'RGBA':
            py5_img.np_pixels[:, :, 0] = array[:, :, 3]
            py5_img.np_pixels[:, :, 1:] = array[:, :, :3]
        else:
            raise RuntimeError(f'what does ' + str(bands) + ' mean?')

        py5_img.update_np_pixels()

        return py5_img

    def convert_image(self, obj: Any, dst: Py5Image = None) -> Py5Image:
        """$class_convert_image"""
        result = Converter._convert(obj)
        if isinstance(result, (Path, str)):
            return self.load_image(result, dst=dst)
        elif isinstance(result, tempfile._TemporaryFileWrapper):
            return self.load_image(result.name, dst=dst)
        elif isinstance(result, np.ndarray):
            # TODO: the converter should not reshuffle the bands, it should
            # be done with create_image_from_numpy
            return self.create_image_from_numpy(result, bands='ARGB', dst=dst)

    def load_image(self, filename: Union[str, Path], dst: Py5Image = None) -> Py5Image:
        """$class_load_image"""
        # TODO: if this is an image Processing cannot load, use PIL instead.
        # TODO: also handle svg files
        pimg = self._instance.loadImage(str(filename))
        if dst:
            dst._replace_instance(pimg)
            return dst
        else:
            return Py5Image(pimg)

    def request_image(self, filename: Union[str, Path]) -> Py5Promise:
        """$class_request_image"""
        return self.launch_promise_thread(self.load_image, args=(filename,))


{sketch_class_members_code}
