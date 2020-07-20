import numpy as np

import py5
from py5.image import Py5Image

_Py5Image = py5.JClass('py5.core.Py5Image')


height = 600
width = 800

img = np.full((height, width, 4), 42, dtype=np.uint8)


def create_py5image(img, bands='ARGB'):
    height, width, _ = img.shape

    pimg = _Py5Image()
    pimg.init(width, height, py5.ARGB)

    py5_img = Py5Image(pimg)
    py5_img.load_pixel_array()
    if bands == 'ARGB':
        py5_img.pixel_array[:] = img
    elif bands == 'RGB':
        py5_img.pixel_array[:, :, 0] = 255
        py5_img.pixel_array[:, :, 1:] = img
    elif bands == 'RGBA':
        py5_img.pixel_array[:, :, 0] = img[:, :, 3]
        py5_img.pixel_array[:, :, 1:] = img[:, :, :3]
    else:
        raise RuntimeError(f'what does {str(bands)} mean?')

    py5_img.update_pixel_array()

    return py5_img


def create_py5image2(img):
    height, width, _ = img.shape

    pimg = _Py5Image()
    pimg.init(width, height, py5.ARGB)
    # pimg.setPixels(img.tobytes())

    py5_img = Py5Image(pimg)

    return py5_img
