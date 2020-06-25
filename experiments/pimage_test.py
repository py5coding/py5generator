import numpy as np
import pandas as pd

import matplotlib.style as mplstyle
import matplotlib
import cairo
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

    # img = py5.load_image('/tmp/example.svg')
    # img = py5.load_image('/mnt/readynas_data/DataBackup/ffhq_dataset/jpg/01003.jpg').resize((500, 500))
    # py5.image(img, py5.width / 2, py5.height / 2)

    # figure = pd._testing.makeTimeDataFrame().plot().figure
    # py5.image(figure, py5.width / 2, py5.height / 2)

    # img = np.zeros((500, 500, 4), dtype=np.uint8)
    # img[:, :, 0] = 255
    # img[:200, :, 1] = 200
    # img[100:400, :, 2] = 100
    # img[300:, :, 3] = 150
    # py5.image((img, 'ARGB'), py5.width / 2, py5.height / 2)

    with cairo.RecordingSurface(cairo.Content.COLOR_ALPHA, cairo.Rectangle(0, 0, 200, 200)) as surface:
    # with cairo.SVGSurface(None, 200, 200) as surface:
        context = cairo.Context(surface)
        x, y, x1, y1 = 0.1, 0.5, 0.4, 0.9
        x2, y2, x3, y3 = 0.6, 0.1, 0.9, 0.5
        context.scale(200, 200)
        context.set_line_width(0.04)
        context.move_to(x, y)
        context.curve_to(x1, y1, x2, y2, x3, y3)
        context.stroke()
        context.set_source_rgba(1, 0.2, 0.2, 0.6)
        context.set_line_width(0.02)
        context.move_to(x, y)
        context.line_to(x1, y1)
        context.move_to(x2, y2)
        context.line_to(x3, y3)
        context.stroke()
        py5.image(surface, py5.width / 2, py5.height / 2)

    py5.no_loop()


py5.run_sketch(block=True)
