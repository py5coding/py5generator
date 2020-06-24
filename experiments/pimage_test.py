import numpy as np
import pandas as pd

import matplotlib.style as mplstyle
import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg
# from matplotlib.backends.backend_svg import FigureCanvasSVG
from matplotlib.backends.backend_cairo import FigureCanvasCairo
import cairocffi
import cairosvg
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
    py5.background(128)

    img = py5.load_image('/tmp/example.svg')
    # img = py5.load_image('/mnt/readynas_data/DataBackup/ffhq_dataset/jpg/01003.jpg').resize((500, 500))
    py5.image(img, py5.width / 2, py5.height / 2)

    # figure = pd._testing.makeTimeDataFrame().plot().figure
    # py5.image(figure, py5.width / 2, py5.height / 2)

    # img = np.zeros((500, 500, 4), dtype=np.uint8)
    # img[:, :, 0] = 255
    # img[:200, :, 1] = 200
    # img[100:400, :, 2] = 100
    # img[300:, :, 3] = 150
    # py5.image((img, 'ARGB'), py5.width / 2, py5.height / 2)

    # figure = pd._testing.makeTimeDataFrame().plot().figure
    # py5.shape(figure, py5.width / 2, py5.height / 2)

    py5.no_loop()


py5.run_sketch(block=True)

# https://cairocffi.readthedocs.io/en/stable/api.html#surfaces
# https://github.com/matplotlib/matplotlib/blob/master/lib/matplotlib/backends/backend_cairo.py

# https://github.com/Kozea/CairoSVG/blob/master/cairosvg/surface.py
# https://cairosvg.org/documentation/



# with open('/tmp/example.svg', 'r') as f:
#     tree = cairosvg.parser.Tree(file_obj=f)
#     surface1 = cairosvg.surface.SVGSurface(tree, None, 72)
#     surface2 = cairosvg.surface.PNGSurface(tree, None, 72)

