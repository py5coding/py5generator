import py5
from py5 import autoclass

ColorBlindness = autoclass('colorblind.ColorBlindness')
colorBlindness = None


def settings():
    py5.size(500, 500, py5.P2D)


def setup():
    py5.background(255)
    py5.rect_mode(py5.CENTER)
    py5.set_frame_rate(30)

    # global colorBlindness
    # colorBlindness = ColorBlindness(py5._papplet)
    # colorBlindness.simulateProtanopia()


def draw():
    if py5.key_pressed:
        print('frameRate', py5.frame_rate)
    py5.fill(py5.random(255), py5.random(255), py5.random(255), 50.0)
    py5.rect(py5.mouse_x, py5.mouse_y, 40, 40)


# py5.run_sketch(settings, setup, draw)
callbacks = py5.Py5Callbacks(settings, setup, draw)
py5.run_sketch2(callbacks)
