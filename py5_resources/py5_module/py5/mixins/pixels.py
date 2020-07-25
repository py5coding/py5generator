from pathlib import Path
from typing import overload, List, Union  # noqa

import numpy as np
from PIL import Image
import jpype


class PixelMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._instance = kwargs['instance']
        self._np_pixels = None

    def _replace_instance(self, new_instance):
        self._instance = new_instance
        if hasattr(self, '_java_bb'):
            self._instance.setPixelBuffer(self._java_bb)
        super()._replace_instance(new_instance)

    def _init_np_pixels(self):
        self._py_bb = bytearray(self.width * self.height * 4)
        self._java_bb = jpype.nio.convertToDirectBuffer(self._py_bb)
        self._instance.setPixelBuffer(self._java_bb)
        self._np_pixels = np.asarray(self._py_bb, dtype=np.uint8).reshape(self.height, self.width, 4)

    # *** BEGIN METHODS ***

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

    def set_np_pixels(self, array: np.ndarray, bands: str = 'ARGB') -> None:
        # TODO: simple validation
        assert bands in 'ARGB RGB RGBA'.split()
        assert array.shape[:2] == self.height, self.width
        assert array.shape[2] == len(bands)

        self.load_np_pixels()
        if bands == 'ARGB':
            self._np_pixels[:] = array
        elif bands == 'RGB':
            self._np_pixels[:, :, 0] = 255
            self._np_pixels[:, :, 1:] = array
        elif bands == 'RGBA':
            self._np_pixels[:, :, 0] = array[:, :, 3]
            self._np_pixels[:, :, 1:] = array[:, :, :3]
        self.update_np_pixels()

    def save(self, filename: Union[str, Path], format: str = None, **params) -> None:
        """$class_save"""
        filename = self._instance.savePath(str(filename))
        self.load_np_pixels()
        arr = np.roll(self.np_pixels, -1, axis=2)
        Image.fromarray(arr, mode='RGBA').save(str(filename), format=format, **params)
