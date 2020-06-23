import numpy as np
from PIL import Image
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.backends.backend_cairo import FigureCanvasCairo


class Converter:

    pimage_functions = {}
    pshape_functions = {}

    def __init__(self, py5applet):
        self.py5applet = py5applet

    def _convert_numpy_to_pimage(self, arr, bands):
        height, width, _ = arr.shape
        bands = bands.upper()
        if bands == 'RGBA':
            a, b = np.split(arr, axis=2, indices_or_sections=np.array([3]))
            arr = np.block([b, a])
        elif bands == 'RGB':
            arr = np.block([np.full((height, width, 1), 255, dtype=np.uint8), arr])

        return self.py5applet.convertBytesToPImage(arr.tobytes(), width, height, pass_by_reference=False)

    def _convert_cairo_to_pshape(self, canvas):
        canvas.print_svg('/tmp/test.svg')
        return self.py5applet.loadShape('/tmp/test.svg')

    def to_pimage(self, obj):
        if type(obj) in Converter.pimage_functions:
            return self._convert_numpy_to_pimage(*Converter.pimage_functions[type(obj)](obj))
        elif (isinstance(obj, tuple)
              and len(obj) == 2
              and isinstance(obj[0], np.ndarray)
              and obj[0].dtype == np.uint8
              and isinstance(obj[1], str)
              and obj[1].upper() in ['RGBA', 'ARGB', 'RGB']):
            return self._convert_numpy_to_pimage(*obj)
        else:
            raise RuntimeError(f'Py5 Converter does not know how to convert an object of type {str(type(obj))}')

    def to_pshape(self, obj):
        if type(obj) in Converter.pshape_functions:
            return self._convert_cairo_to_pshape(Converter.pshape_functions[type(obj)](obj))
        else:
            raise RuntimeError(f'Py5 Converter does not know how to convert an object of type {str(type(obj))}')

    @classmethod
    def register_pimage_conversion(cls, obj_type, function):
        cls.pimage_functions[obj_type] = function

    @classmethod
    def register_pshape_conversion(cls, obj_type, function):
        cls.pshape_functions[obj_type] = function


def convert_figure_to_pimage(figure):
    canvas = FigureCanvasAgg(figure)
    canvas.draw()
    return np.asarray(canvas.buffer_rgba()), 'RGBA'


def convert_pillow_image_to_pimage(img):
    return np.asarray(img), img.mode


def convert_figure_to_shape(figure):
    canvas = FigureCanvasCairo(figure)
    canvas.draw()
    return canvas


Converter.register_pimage_conversion(Figure, convert_figure_to_pimage)
Converter.register_pimage_conversion(Image.Image, convert_pillow_image_to_pimage)

Converter.register_pshape_conversion(Figure, convert_figure_to_shape)
