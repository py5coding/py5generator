# flake8: noqa
"""
Test "from py5 import *" mode.
"""


from py5 import *


def settings():
    size(500, 500, JAVA2D)


def setup():
    background(255)


def draw():
    print('frameRate', frame_rate)
    fill(random(255), random(255), random(255), 50.0)
    rect(mouse_x, mouse_y, 40, 40)


# TODO: this function doesn't exist, but it should
run_sketch2(settings, setup, draw)
