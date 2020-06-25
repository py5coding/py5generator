import tempfile

import numpy as np
from PIL import Image
import cairocffi
import cairo
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg


class Converter:

    pimage_functions = []

    def __init__(self, py5applet):
        self._py5applet = py5applet

    def _convert_cairo_to_pshape(self, canvas):
        with tempfile.NamedTemporaryFile(suffix='.svg') as temp:
            canvas.print_svg(temp.name)
            return self._py5applet.loadShape(temp.name)

    def to_pimage(self, obj):
        for converter in Converter.pimage_functions:
            if converter.precondition(obj):
                obj = converter.convert(obj)
                break
        else:
            raise RuntimeError(f'Py5 Converter does not know how to convert {str(obj)}')

        if isinstance(obj, np.ndarray):
            height, width, _ = obj.shape
            return self._py5applet.convertBytesToPImage(obj.tobytes(), width, height, pass_by_reference=False)
        if isinstance(obj, tempfile._TemporaryFileWrapper):
            pimage = self._py5applet.loadImage(obj.name)
            obj.close()
            return pimage

        raise RuntimeError(f'Error in Py5 Converter for {str(obj)}')

    @classmethod
    def register_pimage_conversion(cls, converter_class):
        cls.pimage_functions.append(converter_class)


class NDArrayStrTuple:

    @classmethod
    def precondition(cls, obj):
        return (isinstance(obj, tuple)
                and len(obj) == 2
                and isinstance(obj[0], np.ndarray)
                and obj[0].dtype == np.uint8
                and obj[0].ndim == 3
                and isinstance(obj[1], str)
                and obj[1].upper() in ['RGBA', 'ARGB', 'RGB']
                and obj[0].shape[2] == len(obj[1]))

    @classmethod
    def convert(cls, obj):
        arr, bands = obj
        bands = bands.upper()
        if bands == 'RGBA':
            a, b = np.split(arr, axis=2, indices_or_sections=np.array([3]))
            arr = np.block([b, a])
        elif bands == 'RGB':
            height, width, _ = arr.shape
            arr = np.block([np.full((height, width, 1), 255, dtype=np.uint8), arr])

        return arr


class FigureToNDArray:

    @classmethod
    def precondition(cls, obj):
        return isinstance(obj, Figure)

    @classmethod
    def convert(cls, figure):
        canvas = FigureCanvasAgg(figure)
        canvas.draw()
        return NDArrayStrTuple.convert((np.asarray(canvas.buffer_rgba()), 'RGBA'))


class PillowImageToNDArray:

    @classmethod
    def precondition(cls, obj):
        return isinstance(obj, Image.Image)

    @classmethod
    def convert(cls, img):
        if img.mode not in ['RGB', 'RGBA']:
            img = img.convert(mode='RGB')
        return NDArrayStrTuple.convert((np.asarray(img), img.mode))


class CairoSurfaceToTempfile:

    @classmethod
    def precondition(cls, obj):
        return isinstance(obj, (cairocffi.Surface, cairo.Surface))

    @classmethod
    def convert(cls, surface):
        temp_png = tempfile.NamedTemporaryFile(suffix='.png')
        surface.write_to_png(temp_png.name)
        return temp_png


Converter.register_pimage_conversion(NDArrayStrTuple)
Converter.register_pimage_conversion(FigureToNDArray)
Converter.register_pimage_conversion(PillowImageToNDArray)
Converter.register_pimage_conversion(CairoSurfaceToTempfile)
