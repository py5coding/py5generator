import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.style as mplstyle
import matplotlib
import cairocffi
from py5 import Sketch

matplotlib.use('agg')
mplstyle.use(['ggplot', 'fast'])


class TestPImage(Sketch):

    def settings(self):
        self.size(700, 700)

    def setup(self):
        self.img1 = self.create_image(200, 5, self.ARGB)
        self.img1.load_np_pixels()
        self.img1.np_pixels[:, :, :2] = 255
        self.img1.update_np_pixels()

        self.img2 = self.load_image('/mnt/readynas_data/DataBackup/ffhq_dataset/jpg/01003.jpg')
        figure = pd._testing.makeTimeDataFrame().plot().figure
        self.figure = self.convert_image(figure)
        plt.close(figure)

        array = np.zeros((700, 700, 4), dtype=np.uint8)
        array[:280, :, 0] = 200  # R
        array[140:560, :, 1] = 100  # G
        array[420:, :, 2] = 150  # B
        array[:, :, 3] = 255  # A
        self.img3 = self.create_image_from_numpy(array, bands='RGBA')

        surface = cairocffi.RecordingSurface(cairocffi.CONTENT_COLOR_ALPHA, (0, 0, 200, 200))
        context = cairocffi.Context(surface)
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
        self.surface = self.convert_image(surface)

    def draw(self):
        self.image_mode(self.CENTER)
        self.shape_mode(self.CENTER)
        self.background(self.img3)

        self.image(self.img1, self.width / 2, self.height / 2)
        self.image(self.img2, self.width / 2, self.height / 2, 500, 500)
        self.image(self.figure, self.width / 2, self.height / 2)
        self.image(self.surface, self.width / 2, self.height / 2)

        copy = self.get(10, 20, 400, 500)
        self.image(copy, self.width / 2, self.height / 2)

        self.no_loop()


test = TestPImage()
test.run_sketch(block=False)
