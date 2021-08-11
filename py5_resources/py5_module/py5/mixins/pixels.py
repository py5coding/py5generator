# *****************************************************************************
#
#   Part of the py5 library
#   Copyright (C) 2020-2021 Jim Schmitz
#
#   This library is free software: you can redistribute it and/or modify it
#   under the terms of the GNU Lesser General Public License as published by
#   the Free Software Foundation, either version 2.1 of the License, or (at
#   your option) any later version.
#
#   This library is distributed in the hope that it will be useful, but
#   WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser
#   General Public License for more details.
#
#   You should have received a copy of the GNU Lesser General Public License
#   along with this library. If not, see <https://www.gnu.org/licenses/>.
#
# *****************************************************************************
import threading
from pathlib import Path
from typing import overload, List, Union  # noqa

import numpy as np
from PIL import Image
import jpype

from ..type_decorators import _hex_converter


_Sketch = jpype.JClass('py5.core.Sketch')


class PixelArray:
    """$module_Sketch_pixels"""

    def __init__(self, instance):
        self.instance = instance

    def __getitem__(self, index):
        if self.instance.pixels is None:
            raise RuntimeError("Cannot get pixel colors because load_pixels() has not been called")

        return self.instance.pixels[index]

    def __setitem__(self, index, val):
        if self.instance.pixels is None:
            raise RuntimeError("Cannot set pixel colors because load_pixels() has not been called")

        if (newval := _hex_converter(val)) is not None:
            val = newval

        if isinstance(val, (int, np.integer)):
            try:
                self.instance.pixels[index] = val
            except:
                raise RuntimeError('Cannot parse "' + str(val) + '" as a color') from None
        else:
            raise RuntimeError('Cannot parse "' + str(val) + '" as a color')


class PixelMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._instance = kwargs['instance']
        self._np_pixels = None
        self.pixels = PixelArray(self._instance)

    def _replace_instance(self, new_instance):
        self._instance = new_instance
        super()._replace_instance(new_instance)

    def _init_np_pixels(self):
        width = self.pixel_width if hasattr(self, 'pixel_width') else self.width
        height = self.pixel_height if hasattr(self, 'pixel_height') else self.height
        self._py_bb = bytearray(width * height * 4)
        self._java_bb = jpype.nio.convertToDirectBuffer(self._py_bb)
        self._np_pixels = np.asarray(self._py_bb, dtype=np.uint8).reshape(height, width, 4)

    # *** BEGIN METHODS ***

    def load_np_pixels(self) -> None:
        """$class_Sketch_load_np_pixels"""
        if self._np_pixels is None:
            self._init_np_pixels()
        self._instance.loadPixels()
        self._java_bb.asIntBuffer().put(self._instance.pixels)

    def update_np_pixels(self) -> None:
        """$class_Sketch_update_np_pixels"""
        if self._np_pixels is None:
            self._init_np_pixels()
        self._java_bb.asIntBuffer().get(self._instance.pixels)
        self._instance.updatePixels()

    def _get_np_pixels(self) -> np.ndarray:  # @decorator
        """$class_Sketch_np_pixels"""
        return self._np_pixels
    np_pixels: np.ndarray = property(fget=_get_np_pixels)

    def set_np_pixels(self, array: np.ndarray, bands: str = 'ARGB') -> None:
        """$class_Sketch_set_np_pixels"""
        self.load_np_pixels()
        if bands == 'L':
            self._np_pixels[:, :, 0] = 255
            self._np_pixels[:, :, 1:] = array[:, :, None] if array.ndim == 2 else array
        elif bands == 'ARGB':
            self._np_pixels[:] = array
        elif bands == 'RGB':
            self._np_pixels[:, :, 0] = 255
            self._np_pixels[:, :, 1:] = array
        elif bands == 'RGBA':
            self._np_pixels[:, :, 0] = array[:, :, 3]
            self._np_pixels[:, :, 1:] = array[:, :, :3]
        self.update_np_pixels()

    def save(self, filename: Union[str, Path], *, format: str = None, drop_alpha: bool = True, use_thread: bool = False, **params) -> None:
        """$class_Sketch_save"""
        sketch_instance = self._instance if isinstance(self._instance, _Sketch) else self._instance.parent
        filename = Path(str(sketch_instance.savePath(str(filename))))
        self.load_np_pixels()
        arr = self.np_pixels[:, :, 1:] if drop_alpha else np.roll(self.np_pixels, -1, axis=2)

        if use_thread:
            def _save(arr, filename, format, params):
                Image.fromarray(arr).save(filename, format=format, **params)

            t = threading.Thread(target=_save, args=(arr, filename, format, params), daemon=True)
            t.start()
        else:
            Image.fromarray(arr).save(filename, format=format, **params)

    # *** END METHODS ***


class PixelPy5GraphicsMixin(PixelMixin):

    def load_np_pixels(self) -> None:
        """$class_Py5Graphics_load_np_pixels"""
        return super().load_np_pixels()

    def update_np_pixels(self) -> None:
        """$class_Py5Graphics_update_np_pixels"""
        return super().update_np_pixels()

    def _get_np_pixels(self) -> np.ndarray:  # @decorator
        """$class_Py5Graphics_np_pixels"""
        return super()._get_np_pixels()
    np_pixels: np.ndarray = property(fget=_get_np_pixels)

    def set_np_pixels(self, array: np.ndarray, bands: str = 'ARGB') -> None:
        """$class_Py5Graphics_set_np_pixels"""
        return super().set_np_pixels(array, bands)

    def save(self, filename: Union[str, Path], *, format: str = None, drop_alpha: bool = True, use_thread: bool = False, **params) -> None:
        """$class_Py5Graphics_save"""
        return super().save(filename, format=format, drop_alpha=drop_alpha, use_thread=use_thread, **params)


class PixelPy5ImageMixin(PixelMixin):

    def load_np_pixels(self) -> None:
        """$class_Py5Image_load_np_pixels"""
        return super().load_np_pixels()

    def update_np_pixels(self) -> None:
        """$class_Py5Image_update_np_pixels"""
        return super().update_np_pixels()

    def _get_np_pixels(self) -> np.ndarray:  # @decorator
        """$class_Py5Image_np_pixels"""
        return super()._get_np_pixels()
    np_pixels: np.ndarray = property(fget=_get_np_pixels)

    def set_np_pixels(self, array: np.ndarray, bands: str = 'ARGB') -> None:
        """$class_Py5Image_set_np_pixels"""
        return super().set_np_pixels(array, bands)

    def save(self, filename: Union[str, Path], *, format: str = None, drop_alpha: bool = True, use_thread: bool = False, **params) -> None:
        """$class_Py5Image_save"""
        return super().save(filename, format=format, drop_alpha=drop_alpha, use_thread=use_thread, **params)
