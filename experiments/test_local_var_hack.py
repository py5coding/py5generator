"""
I can intercept variable lookup in exec
"""

import py5

USER_CODE = """
def settings():
    size(500, 500, JAVA2D)


def setup():
    background(255)
    rect_mode(CENTER)


def draw():
    if is_key_pressed():
        print('frameRate', get_frame_rate())
    fill(random(255), random(255), random(255), 50.0)
    rect(mouse_x, mouse_y, 40, 40)


def mouse_entered():
    print('mouse entered')


def mouse_exited():
    print('mouse exited')
"""

IMPORTS_CODE = """
import py5
from py5 import *
"""

RUN_SKETCH_CODE = """
py5._skip_attrs = {'settings', 'setup', 'draw'}
py5_methods = py5.Py5Methods(settings, setup, draw)
py5_methods.set_events(mouse_entered=mouse_entered,
                       mouse_exited=mouse_exited)
py5.run_sketch(py5_methods=py5_methods, block=True)
"""


class Py5Namespace(dict):

    def __init__(self, py5):
        super().__init__()
        self._py5 = py5

    def __getitem__(self, item):
        if hasattr(self._py5, item):
            return getattr(self._py5, item)
        else:
            return super().__getitem__(item)


py5_ns = Py5Namespace(py5)
exec(IMPORTS_CODE, py5_ns)
exec(USER_CODE, py5_ns)
exec(RUN_SKETCH_CODE, py5_ns)
