# -*- coding: utf-8 -*-
# *** FORMAT PARAMS ***
from __future__ import annotations

import functools
from typing import overload, List  # noqa

import numpy as np
import jpype

from .methods import Py5Exception  # noqa


py5image_class_members_code = None  # DELETE


def _return_py5image(f):
    @functools.wraps(f)
    def decorated(self_, *args):
        ret = f(self_, *args)
        if ret is not None:
            return Py5Image(ret)
    return decorated


def _py5image_param(argnum):
    def decorator(f):
        @functools.wraps(f)
        def decorated(self_, *args):
            if isinstance(args[argnum], Py5Image):
                args = (*args[:argnum],
                        args[argnum]._instance,
                        *args[(argnum + 1):])
            return f(self_, *args)
        return decorated
    return decorator


class Py5Image:

    def __init__(self, pimage):
        self._instance = pimage
        self._np_pixels = None

    def _init_np_pixels(self):
        py_bb = bytearray(self.width * self.height * 4)
        java_bb = jpype.nio.convertToDirectBuffer(py_bb)
        self._instance.setPixelBuffer(java_bb)
        self._np_pixels = np.asarray(py_bb, dtype=np.uint8).reshape(self.height, self.width, 4)

    def load_np_pixels(self) -> None:
        if self._np_pixels is None:
            self._init_np_pixels()
        self._instance.loadAndPutPixels()

    def update_np_pixels(self) -> None:
        if self._np_pixels is None:
            self._init_np_pixels()
        self._instance.getAndUpdatePixels()

    @property
    def np_pixels(self) -> np.ndarray:
        return self._np_pixels

    def set_np_pixels(self, array, bands='ARGB'):
        # TODO: simple validation
        assert bands in 'ARGB RGB RGBA'.split()
        assert array.shape[:2] == self.height, self.width
        assert array.shape[2] == len(bands)

        self.load_pixel_array()
        if bands == 'ARGB':
            self.pixel_array[:] = array
        elif bands == 'RGB':
            self.pixel_array[:, :, 0] = 255
            self.pixel_array[:, :, 1:] = array
        elif bands == 'RGBA':
            self.pixel_array[:, :, 0] = array[:, :, 3]
            self.pixel_array[:, :, 1:] = array[:, :, :3]
        self.update_pixel_array()

    @property
    def width(self) -> int:
        return self._instance.width

    @property
    def height(self) -> int:
        return self._instance.height
