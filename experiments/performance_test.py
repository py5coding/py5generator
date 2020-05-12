# import time

import py5


def settings():
    py5.size(500, 500, py5.P2D)


def setup():
    py5.background(255)
    py5.rect_mode(py5.CENTER)


def draw():
    for i in range(10000):
        py5.fill(py5.random(255), py5.random(255), py5.random(255), 40)

    py5.rect(py5.mouse_x, py5.mouse_y, 50, 50)

    print(py5.get_frame_rate())


py5.run_sketch(block=True)
