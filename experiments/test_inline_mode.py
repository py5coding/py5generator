# flake8: noqa
"""
This code demos py5 inline mode. This is useful for users who don't want to
write a Python class.

It can be run from the command line, like so:

$ python test_inline_mode.py
"""

import numpy as np

import py5


def settings():
    py5.size(500, 500, py5.P2D)


def setup():
    py5.background(255)
    py5.rect_mode(py5.CENTER)


def draw():
    if py5.is_key_pressed():
        print('frameRate', py5.get_frame_rate())

    py5.fill(py5.random(255), py5.random(255), py5.random(255), 50.0)
    py5.rect(py5.mouse_x, py5.mouse_y, 40, 40)

    if py5.frame_count == 300:
        py5.save_frame('/tmp/frame_###.png')

    py5.stroke(0, 64)
    random_coords = 500 * np.random.rand(2, 4)
    py5.lines(random_coords)
    py5.stroke(0, 255)
    random_coords = 500 * np.random.rand(50, 2)
    py5.points(random_coords)


def mouse_entered():
    print('mouse entered')


def mouse_exited():
    print('mouse exited')


py5.run_sketch()
