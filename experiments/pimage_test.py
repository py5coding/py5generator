import numpy as np
import pandas as pd

import matplotlib.style as mplstyle
import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg
matplotlib.use('agg')
# mplstyle.use('fast')
mplstyle.use(['ggplot', 'fast'])

from PIL import Image

import py5


def settings():
    py5.size(712, 512)


def draw():
    py5.image_mode(py5.CENTER)
    py5.background(0)
    # py5.fill(255)
    # py5.rect(0, 0, py5.width / 2, py5.height / 2)

    # img = np.zeros((50, 20, 4), dtype=np.uint8)
    # img[:, :, 3] = 255
    # img[:30, :, 2] = 255
    # img[10:40, :, 1] = 255
    # img[20:, :, 0] = 255

    def convert_pillow_image_to_pimage(img):
        X = convert_rgba_to_argb(np.asarray(img.convert("RGBA")))
        height, width, _ = X.shape
        return py5.get_py5applet().convertBytesToPImage(X.tobytes(), width, height, pass_by_reference=False)

    def convert_rgba_to_argb(X):
        a, b = np.split(X, axis=2, indices_or_sections=np.array([3]))
        return np.block([b, a])

    def convert_figure_to_pimage(figure):
        canvas = FigureCanvasAgg(figure)
        canvas.draw()
        X = convert_rgba_to_argb(np.asarray(canvas.buffer_rgba()))
        height, width, _ = X.shape
        return py5.get_py5applet().convertBytesToPImage(X.tobytes(), width, height, pass_by_reference=False)

    # img = Image.open('../py5projects/drawingtutor/data/jpg/01003.jpg').resize((500, 500))
    # py5.image(convert_pillow_image_to_pimage(img), py5.width / 2, py5.height / 2)

    figure = pd._testing.makeTimeDataFrame().plot().figure
    py5.image(convert_figure_to_pimage(figure), py5.width / 2, py5.height / 2)

    py5.no_loop()


py5.run_sketch(block=True)
