import numpy as np
import pandas as pd

import matplotlib.style as mplstyle
import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg
matplotlib.use('svg')
mplstyle.use('fast')
# mplstyle.use(['ggplot', 'fast'])

from PIL import Image

import py5


def settings():
    py5.size(712, 512)


def draw():
    py5.image_mode(py5.CENTER)
    py5.background(0)

    def convert_pillow_image_to_pimage(img):
        return convert_numpy_to_pimage(np.asarray(img), bands=img.mode)

    def convert_figure_to_pimage(figure):
        canvas = FigureCanvasAgg(figure)
        canvas.draw()
        return convert_numpy_to_pimage(np.asarray(canvas.buffer_rgba()), bands="RGBA")

    def convert_numpy_to_pimage(arr, bands="ARGB"):
        height, width, _ = arr.shape
        if bands == "RGBA":
            a, b = np.split(arr, axis=2, indices_or_sections=np.array([3]))
            arr = np.block([b, a])
        elif bands == "RGB":
            arr = np.block([np.full((height, width, 1), 255, dtype=np.uint8), arr])

        return py5.get_py5applet().convertBytesToPImage(arr.tobytes(), width, height, pass_by_reference=False)

    img = Image.open('../py5projects/drawingtutor/data/jpg/01003.jpg').resize((500, 500))
    py5.image(convert_pillow_image_to_pimage(img), py5.width / 2, py5.height / 2)

    # figure = pd._testing.makeTimeDataFrame().plot().figure
    # py5.image(convert_figure_to_pimage(figure), py5.width / 2, py5.height / 2)

    # img = np.zeros((500, 500, 4), dtype=np.uint8)
    # img[:, :, 0] = 255
    # img[:200, :, 1] = 200
    # img[100:400, :, 2] = 100
    # img[300:, :, 3] = 150
    # py5.image(convert_numpy_to_pimage(img), py5.width / 2, py5.height / 2)

    py5.no_loop()


py5.run_sketch(block=True)
