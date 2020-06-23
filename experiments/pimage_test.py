import numpy as np
import pandas as pd

import matplotlib.style as mplstyle
import matplotlib
# from matplotlib.backends.backend_agg import FigureCanvasAgg
# from matplotlib.backends.backend_svg import FigureCanvasSVG
# from matplotlib.backends.backend_cairo import FigureCanvasCairo
# from cairo import SVGSurface, SVG_VERSION_1_1
from PIL import Image
import py5

mplstyle.use(['ggplot', 'fast'])
matplotlib.use('svg')
mplstyle.use('fast')


def settings():
    py5.size(712, 512)


def draw():
    py5.image_mode(py5.CENTER)
    py5.shape_mode(py5.CENTER)
    py5.background(0)

    # def convert_figure_to_shape(figure):
    #     canvas = FigureCanvasCairo(figure)
    #     canvas.draw()
    #     canvas.print_svg('/tmp/test.svg')
    #     return py5.get_py5applet().loadShape('/tmp/test.svg')

    # img = Image.open('/mnt/readynas_data/DataBackup/ffhq_dataset/jpg/01003.jpg').resize((500, 500))
    # py5.image(img, py5.width / 2, py5.height / 2)

    # figure = pd._testing.makeTimeDataFrame().plot().figure
    # py5.image(figure, py5.width / 2, py5.height / 2)

    # img = np.zeros((500, 500, 4), dtype=np.uint8)
    # img[:, :, 0] = 255
    # img[:200, :, 1] = 200
    # img[100:400, :, 2] = 100
    # img[300:, :, 3] = 150
    # py5.image((img, 'ARGB'), py5.width / 2, py5.height / 2)

    figure = pd._testing.makeTimeDataFrame().plot().figure
    py5.shape(figure, py5.width / 2, py5.height / 2)

    py5.no_loop()


py5.run_sketch(block=True)
