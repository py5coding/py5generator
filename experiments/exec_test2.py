"""
Experiment for how the Processing IDE mode could work, without requiring
the user to type import py5 or from py5 import *
"""

import time

USER_CODE = """
def settings():
    size(500, 500, JAVA2D)


def setup():
    background(255)


def draw():
    print('frameRate', frame_rate)
    fill(random(255), random(255), random(255), 50.0)
    rect(mouse_x, mouse_y, 40, 40)
"""

HANDLE_SETTINGS_CODE = """
_papplet.handleSettingsPt1()
settings()
_papplet.handleSettingsPt2()
PythonPApplet.setupSketch(['Python Processing'], _papplet)
"""

HANDLE_DRAW_CODE = """
_papplet.handleDrawPt1()
if _papplet.frameCount == 0:
    setup()
_papplet.handleDrawPt2()
draw()
_papplet.handleDrawPt3()
_papplet.render()
"""

IMPORTS_CODE = """
from py5 import _papplet, PythonPApplet, _update_vars
from py5 import *
"""

user_ns = dict()
exec(IMPORTS_CODE, user_ns)
exec(USER_CODE, user_ns)

exec(HANDLE_SETTINGS_CODE, user_ns)
for x in range(500):
    user_ns['frame_rate'] = user_ns['_papplet'].frameRate
    user_ns['mouse_x'] = user_ns['_papplet'].mouseX
    user_ns['mouse_y'] = user_ns['_papplet'].mouseY
    exec(HANDLE_DRAW_CODE, user_ns)
    time.sleep(1 / 60)


# user_ns = dict()
# exec(IMPORTS_CODE, user_ns)
# exec(USER_CODE, user_ns)
# exec("run_sketch(settings, setup, draw)", user_ns)
