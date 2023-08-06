# *****************************************************************************
#
#   Part of the py5 library
#   Copyright (C) 2020-2023 Jim Schmitz
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
from __future__ import annotations

import threading
from pathlib import Path
from io import BytesIO
from typing import overload, Union  # noqa

import numpy as np
import numpy.typing as npt
from PIL import Image
from PIL.Image import Image as PIL_Image
import jpype

from ..decorators import _hex_converter


_Sketch = jpype.JClass('py5.core.Sketch')


class PixelArray:
    """$module_Sketch_pixels"""

    def __init__(self, instance):
        self._instance = instance

    def __getitem__(self, index):
        if self._instance.pixels is None:
            raise RuntimeError("Cannot get pixel colors because load_pixels() has not been called")

        return self._instance.pixels[index]

    def __setitem__(self, index, val):
        if self._instance.pixels is None:
            raise RuntimeError("Cannot set pixel colors because load_pixels() has not been called")

        if (newval := _hex_converter(val)) is not None:
            val = newval

        self._instance.pixels[index] = val

    def __len__(self):
        if self._instance.pixels is None:
            raise RuntimeError("Cannot get pixel length because load_pixels() has not been called")

        return len(self._instance.pixels)


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

    def _get_np_pixels(self) -> npt.NDArray[np.uint8]:  # @decorator
        """$class_Sketch_np_pixels"""
        return self._np_pixels
    np_pixels: npt.NDArray[np.uint8] = property(fget=_get_np_pixels, doc="""$class_Sketch_np_pixels""")

    def set_np_pixels(self, array: npt.NDArray[np.uint8], bands: str = 'ARGB') -> None:
        """$class_Sketch_set_np_pixels"""
        self.load_np_pixels()
        if bands == 'L':
            self._np_pixels[:, :, 0] = 255
            self._np_pixels[:, :, 1:] = array[:, :, None] if array.ndim == 2 else array
        elif bands == 'ARGB':
            self._np_pixels[:] = array[:, :, :4]
        elif bands == 'RGB':
            self._np_pixels[:, :, 0] = 255
            self._np_pixels[:, :, 1:] = array[:, :, :3]
        elif bands == 'RGBA':
            self._np_pixels[:, :, 0] = array[:, :, 3]
            self._np_pixels[:, :, 1:] = array[:, :, :3]
        elif bands == 'BGR':
            self._np_pixels[:, :, 0] = 255
            self._np_pixels[:, :, 1:] = array[:, :, 2::-1]
        elif bands == 'BGRA':
            self._np_pixels[:, :, 0] = array[:, :, 3]
            self._np_pixels[:, :, 1:] = array[:, :, 2::-1]
        else:
            raise RuntimeError(f"Unknown `bands` value '{bands}'. Supported values are 'L', 'ARGB', 'RGB', 'RGBA', 'BGR', and 'BGRA'.")
        self.update_np_pixels()

    @overload
    def get_np_pixels(self, *, bands: str = 'ARGB', dst: npt.NDArray[np.uint8] = None) -> npt.NDArray[np.uint8]:
        """$class_Sketch_get_np_pixels"""
        pass

    @overload
    def get_np_pixels(self, x: int, y: int, w: int, h: int, /, *, bands: str = 'ARGB', dst: npt.NDArray[np.uint8] = None) -> npt.NDArray[np.uint8]:
        """$class_Sketch_get_np_pixels"""
        pass

    def get_np_pixels(self, *args, **kwargs) -> npt.NDArray[np.uint8]:
        """$class_Sketch_get_np_pixels"""
        self.load_np_pixels()

        if len(args) == 4:
            x, y, w, h = args
        elif len(args) == 0:
            x, y, h, w = 0, 0, *self.np_pixels.shape[:2]
        else:
            raise TypeError(f"Received {len(args)} out of 4 positional arguments for x, y, w, and h.")

        bands = kwargs.get('bands', 'ARGB')
        dst = kwargs.get('dst', None)

        x_slice = slice(x, x + w)
        y_slice = slice(y, y + h)

        if bands == 'L':
            pixels = (self._np_pixels[y_slice, x_slice][:, :, 1:] @ [0.299, 0.587, 0.114]).astype(np.uint8)
        elif bands == 'ARGB':
            pixels = self._np_pixels[y_slice, x_slice]
        elif bands == 'RGB':
            pixels = self._np_pixels[y_slice, x_slice, 1:]
        elif bands == 'RGBA':
            pixels = np.roll(self._np_pixels[y_slice, x_slice], -1, axis=2)
        elif bands == 'BGR':
            pixels = self._np_pixels[y_slice, x_slice, 3:0:-1]
        elif bands == 'BGRA':
            pixels = np.dstack([self._np_pixels[y_slice, x_slice, 3:0:-1], self._np_pixels[y_slice, x_slice, 0]])
        else:
            raise RuntimeError(f"Unknown `bands` value '{bands}'. Supported values are 'L', 'ARGB', 'RGB', 'RGBA', 'BGR', and 'BGRA'.")

        if dst is not None:
            if dst.shape != pixels.shape:
                raise ValueError(f"Destination array has shape {dst.shape} but expected {pixels.shape}")
            else:
                dst[:] = pixels
                return dst
        else:
            return pixels if pixels.base is None else pixels.copy()

    @overload
    def to_pil(self) -> PIL_Image:
        """$class_Sketch_to_pil"""
        pass

    @overload
    def to_pil(self, x: int, y: int, w: int, h: int, /) -> PIL_Image:
        """$class_Sketch_to_pil"""
        pass

    def to_pil(self, *args) -> PIL_Image:
        """$class_Sketch_to_pil"""
        return Image.fromarray(self.get_np_pixels(*args, bands='RGBA'))

    def save(self, filename: Union[str, Path, BytesIO], *, format: str = None, drop_alpha: bool = True, use_thread: bool = False, **params) -> None:
        """$class_Sketch_save"""
        sketch_instance = self._instance if isinstance(self._instance, _Sketch) else self._instance.parent
        if not isinstance(filename, BytesIO):
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


# NOTE: changes to the below method signatures will not update the reference docs automatically
# could also add this information to generator/reference.py but it is simpler to copy-paste from
# the Sketch doc files to the Py5Graphics and Py5Image doc files.
# Both of these classes are necessary so that the docstings will be correct.

class PixelPy5GraphicsMixin(PixelMixin):

    def load_np_pixels(self) -> None:
        """$class_Py5Graphics_load_np_pixels"""
        return super().load_np_pixels()

    def update_np_pixels(self) -> None:
        """$class_Py5Graphics_update_np_pixels"""
        return super().update_np_pixels()

    def _get_np_pixels(self) -> npt.NDArray[np.uint8]:  # @decorator
        """$class_Py5Graphics_np_pixels"""
        return super()._get_np_pixels()
    np_pixels: npt.NDArray[np.uint8] = property(fget=_get_np_pixels, doc="""$class_Py5Graphics_np_pixels""")

    def set_np_pixels(self, array: npt.NDArray[np.uint8], bands: str = 'ARGB') -> None:
        """$class_Py5Graphics_set_np_pixels"""
        return super().set_np_pixels(array, bands)

    def get_np_pixels(self, x: int, y: int, w: int, h: int, *, bands: str = 'ARGB', dst: npt.NDArray[np.uint8] = None) -> npt.NDArray[np.uint8]:
        """$class_Py5Graphics_get_np_pixels"""
        return super().get_np_pixels(x, y, w, h, bands=bands, dst=dst)

    @overload
    def to_pil(self) -> PIL_Image:
        """$class_Py5Graphics_to_pil"""
        pass

    @overload
    def to_pil(self, x: int, y: int, w: int, h: int, /) -> PIL_Image:
        """$class_Py5Graphics_to_pil"""
        pass

    def to_pil(self, *args) -> PIL_Image:
        """$class_Py5Graphics_to_pil"""
        return super().to_pil(*args)

    def save(self, filename: Union[str, Path, BytesIO], *, format: str = None, drop_alpha: bool = True, use_thread: bool = False, **params) -> None:
        """$class_Py5Graphics_save"""
        return super().save(filename, format=format, drop_alpha=drop_alpha, use_thread=use_thread, **params)


class PixelPy5ImageMixin(PixelMixin):

    def load_np_pixels(self) -> None:
        """$class_Py5Image_load_np_pixels"""
        return super().load_np_pixels()

    def update_np_pixels(self) -> None:
        """$class_Py5Image_update_np_pixels"""
        return super().update_np_pixels()

    def _get_np_pixels(self) -> npt.NDArray[np.uint8]:  # @decorator
        """$class_Py5Image_np_pixels"""
        return super()._get_np_pixels()
    np_pixels: npt.NDArray[np.uint8] = property(fget=_get_np_pixels, doc="""$class_Py5Image_np_pixels""")

    def set_np_pixels(self, array: npt.NDArray[np.uint8], bands: str = 'ARGB') -> None:
        """$class_Py5Image_set_np_pixels"""
        return super().set_np_pixels(array, bands)

    def get_np_pixels(self, x: int, y: int, w: int, h: int, *, bands: str = 'ARGB', dst: npt.NDArray[np.uint8] = None) -> npt.NDArray[np.uint8]:
        """$class_Py5Image_get_np_pixels"""
        return super().get_np_pixels(x, y, w, h, bands=bands, dst=dst)

    @overload
    def to_pil(self) -> PIL_Image:
        """$class_Py5Image_to_pil"""
        pass

    @overload
    def to_pil(self, x: int, y: int, w: int, h: int, /) -> PIL_Image:
        """$class_Py5Image_to_pil"""
        pass

    def to_pil(self, *args) -> PIL_Image:
        """$class_Py5Image_to_pil"""
        return super().to_pil(*args)

    def save(self, filename: Union[str, Path, BytesIO], *, format: str = None, drop_alpha: bool = True, use_thread: bool = False, **params) -> None:
        """$class_Py5Image_save"""
        return super().save(filename, format=format, drop_alpha=drop_alpha, use_thread=use_thread, **params)
