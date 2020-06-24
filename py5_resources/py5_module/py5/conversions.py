import io
import tempfile

import numpy as np
from PIL import Image
import cairocffi
import cairo
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.backends.backend_cairo import FigureCanvasCairo


class Converter:

    pimage_functions = []
    pshape_functions = []

    def __init__(self, py5applet):
        self._py5applet = py5applet

    def _convert_numpy_to_pimage(self, arr, bands):
        height, width, _ = arr.shape
        bands = bands.upper()
        if bands == 'RGBA':
            a, b = np.split(arr, axis=2, indices_or_sections=np.array([3]))
            arr = np.block([b, a])
        elif bands == 'RGB':
            arr = np.block([np.full((height, width, 1), 255, dtype=np.uint8), arr])

        return self._py5applet.convertBytesToPImage(arr.tobytes(), width, height, pass_by_reference=False)

    def _convert_cairo_to_pshape(self, canvas):
        with tempfile.NamedTemporaryFile(suffix='.svg') as temp:
            canvas.print_svg(temp.name)
            return self._py5applet.loadShape(temp.name)

    def to_pimage(self, obj):
        orig_obj = obj
        for obj_type, function in Converter.pimage_functions:
            if isinstance(obj, obj_type):
                return self._convert_numpy_to_pimage(*function(obj))

        if isinstance(obj, tuple):
            if (len(obj) == 2
                and isinstance(obj[0], np.ndarray)
                and obj[0].dtype == np.uint8
                and obj[0].ndim == 3
                and isinstance(obj[1], str)
                and obj[1].upper() in ['RGBA', 'ARGB', 'RGB']
                    and obj[0].shape[2] == len(obj[1])):
                return self._convert_numpy_to_pimage(*obj)
            else:
                raise RuntimeError("Tuple parameter must be a numpy array and a string")
        else:
            raise RuntimeError(f'Py5 Converter does not know how to convert an object of type {str(type(orig_obj))}')

    def to_pshape(self, obj):
        if type(obj) in Converter.pshape_functions:
            return self._convert_cairo_to_pshape(Converter.pshape_functions[type(obj)](obj))
        else:
            raise RuntimeError(f'Py5 Converter does not know how to convert an object of type {str(type(obj))}')

    @classmethod
    def register_pimage_conversion(cls, obj_type, function):
        cls.pimage_functions.append((obj_type, function))

    @classmethod
    def register_pshape_conversion(cls, obj_type, function):
        cls.pshape_functions.append((obj_type, function))


def convert_figure_to_ndarray(figure):
    canvas = FigureCanvasAgg(figure)
    canvas.draw()
    return np.asarray(canvas.buffer_rgba()), 'RGBA'


def convert_pillow_image_to_ndarray(img):
    return np.asarray(img), img.mode


def convert_cairo_surface_to_ndarray(surface):
    buffer = io.BytesIO()
    surface.write_to_png(buffer)
    img = Image.open(buffer)
    return convert_pillow_image_to_ndarray(img)


def convert_figure_to_canvas(figure):
    canvas = FigureCanvasCairo(figure)
    canvas.draw()
    return canvas


Converter.register_pimage_conversion(Figure, convert_figure_to_ndarray)
Converter.register_pimage_conversion(Image.Image, convert_pillow_image_to_ndarray)
Converter.register_pimage_conversion(cairocffi.Surface, convert_cairo_surface_to_ndarray)
Converter.register_pimage_conversion(cairo.Surface, convert_cairo_surface_to_ndarray)

Converter.register_pshape_conversion(Figure, convert_figure_to_canvas)
