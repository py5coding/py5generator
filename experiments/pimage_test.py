import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.style as mplstyle
import matplotlib
import cairocffi
import py5

matplotlib.use('agg')
mplstyle.use(['ggplot', 'fast'])


class TestPImage(py5.Sketch):

    def settings(self):
        self.size(712, 512)

    def setup(self):
        self.img1 = py5.create_image("RGB", 200, 5, "red")
        self.img2 = self.load_image('/mnt/readynas_data/DataBackup/ffhq_dataset/jpg/01003.jpg').resize((500, 500))
        self.figure = pd._testing.makeTimeDataFrame().plot().figure

        self.img3 = np.zeros((500, 500, 4), dtype=np.uint8)
        self.img3[:200, :, 0] = 200  # R
        self.img3[100:400, :, 1] = 100  # G
        self.img3[300:, :, 2] = 150  # B
        self.img3[:, :, 3] = 255  # A

        self.surface = cairocffi.RecordingSurface(cairocffi.CONTENT_COLOR_ALPHA, (0, 0, 200, 200))
        context = cairocffi.Context(self.surface)
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

    def draw(self):
        self.image_mode(py5.CENTER)
        self.shape_mode(py5.CENTER)
        self.background(128)

        caching = False

        self.image(self.img1, self.width / 2, self.height / 2, cache=caching)
        self.image(self.img2, self.width / 2, self.height / 2, cache=caching)
        self.image(self.figure, self.width / 2, self.height / 2, cache=caching)
        plt.close(self.figure)
        self.image((self.img3, 'RGBA'), self.width / 2, self.height / 2, cache=caching)
        self.image(self.surface, self.width / 2, self.height / 2, cache=caching)

        # self.no_loop()


test = TestPImage()
test.run_sketch(block=False)
