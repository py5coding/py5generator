import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.style as mplstyle
import matplotlib
import py5

matplotlib.use('agg')
mplstyle.use(['ggplot', 'fast'])


img1 = None
img2 = None
img3 = None
figure = None


def settings():
    py5.size(712, 512)


def setup():
    global img1
    global img2
    global img3
    global figure
    img1 = py5.create_image("RGB", 200, 5, "red")
    img2 = py5.load_image('/mnt/readynas_data/DataBackup/ffhq_dataset/jpg/01003.jpg').resize((500, 500))
    figure = pd._testing.makeTimeDataFrame().plot().figure

    img3 = np.zeros((500, 500, 4), dtype=np.uint8)
    img3[:200, :, 0] = 200  # R
    img3[100:400, :, 1] = 100  # G
    img3[300:, :, 2] = 150  # B
    img3[:, :, 3] = 255  # A


def draw():
    py5.image_mode(py5.CENTER)
    py5.shape_mode(py5.CENTER)
    py5.background(128)

    caching = True

    py5.image(img1, py5.width / 2, py5.height / 2, cache=caching)
    py5.image(img2, py5.width / 2, py5.height / 2, cache=caching)
    py5.image(figure, py5.width / 2, py5.height / 2, cache=caching)
    plt.close(figure)
    py5.image((img3, 'RGBA'), py5.width / 2, py5.height / 2, cache=caching)


py5.run_sketch(block=True)
