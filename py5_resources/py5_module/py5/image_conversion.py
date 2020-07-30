import io
from pathlib import Path
import tempfile

import numpy as np
from PIL import Image


pimage_functions = []


def _convert(obj):
    for precondition, convert_function in pimage_functions:
        if precondition(obj):
            obj = convert_function(obj)
            break
    else:
        raise RuntimeError(f'Py5 Converter is not able to convert {str(obj)}')

    return obj


def register_image_conversion(precondition, convert_function):
    pimage_functions.append((precondition, convert_function))


###############################################################################
# BUILT-IN CONVERSTION FUNCTIONS
###############################################################################


def ndarray_str_tuple_precondition(obj):
    return (isinstance(obj, tuple)
            and len(obj) == 2
            and isinstance(obj[0], np.ndarray)
            and obj[0].dtype == np.uint8
            and obj[0].ndim == 3
            and isinstance(obj[1], str)
            and obj[1].upper() in ['RGBA', 'ARGB', 'RGB']
            and obj[0].shape[2] == len(obj[1]))


def ndarray_str_tuple_adjustment(obj):
    arr, bands = obj
    bands = bands.upper()
    if bands == 'RGBA':
        arr = np.roll(arr, 1, axis=2)
    elif bands == 'RGB':
        height, width, _ = arr.shape
        arr = np.block([np.full((height, width, 1), 255, dtype=np.uint8), arr])

    return arr


register_image_conversion(ndarray_str_tuple_precondition, ndarray_str_tuple_adjustment)


def pillow_image_to_ndarray_precondition(obj):
    return isinstance(obj, Image.Image)


def pillow_image_to_ndarray_converter(img):
    if img.mode not in ['RGB', 'RGBA']:
        img = img.convert(mode='RGB')
    return ndarray_str_tuple_adjustment((np.asarray(img), img.mode))


register_image_conversion(pillow_image_to_ndarray_precondition, pillow_image_to_ndarray_converter)


###############################################################################
# Py5 requires Pillow and numpy to be installed. The below libraries may or may
# not be installed. If they are, this registers their associated conversion
# functions.
###############################################################################


try:
    import cairosvg  # noqa
    import cairocffi  # noqa

    def svg_file_to_ndarray_precondition(obj):
        if isinstance(obj, (str, Path)):
            return Path(obj).suffix.lower() == '.svg'
        else:
            return False

    def svg_file_to_ndarray_converter(filename):
        filename = Path(filename)
        with open(filename, 'r') as f:
            img = Image.open(io.BytesIO(cairosvg.svg2png(file_obj=f)))
            return pillow_image_to_ndarray_converter(img)

    register_image_conversion(svg_file_to_ndarray_precondition, svg_file_to_ndarray_converter)
except ModuleNotFoundError:
    pass


try:
    import cairocffi  # noqa

    def cairocffi_surface_to_tempfile_precondition(obj):
        return isinstance(obj, cairocffi.Surface)

    def cairo_surface_to_tempfile_converter(surface):
        temp_png = tempfile.NamedTemporaryFile(suffix='.png')
        surface.write_to_png(temp_png.name)
        return temp_png

    register_image_conversion(cairocffi_surface_to_tempfile_precondition, cairo_surface_to_tempfile_converter)
except ModuleNotFoundError:
    pass


try:
    import cairo  # noqa

    def cairo_surface_to_tempfile_precondition(obj):
        return isinstance(obj, cairo.Surface)

    register_image_conversion(cairo_surface_to_tempfile_precondition, cairo_surface_to_tempfile_converter)
except ModuleNotFoundError:
    pass


try:
    from matplotlib.figure import Figure  # noqa
    from matplotlib.backends.backend_agg import FigureCanvasAgg  # noqa

    def figure_to_ndarray_precondition(obj):
        return isinstance(obj, Figure)

    def figure_to_ndarray_converter(figure):
        canvas = FigureCanvasAgg(figure)
        canvas.draw()
        return ndarray_str_tuple_adjustment((np.asarray(canvas.buffer_rgba()), 'RGBA'))

    register_image_conversion(figure_to_ndarray_precondition, figure_to_ndarray_converter)
except ModuleNotFoundError:
    pass
