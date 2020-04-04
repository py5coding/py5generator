import time

import jnius_config
jnius_config.set_classpath('.', '/home/jim/Projects/git/processing/core/library/*')
from jnius import autoclass  # noqa

PythonPApplet = autoclass('processing.core.PythonPApplet')
PConstants = autoclass('processing.core.PConstants')

_papplet = PythonPApplet()

# *** PY5 GENERATED CONSTANTS ***
{0}

# *** PY5 GENERATED FUNCTIONS ***
{1}

frame_rate = 0
mouse_x = 0
mouse_y = 0


def _handle_settings(settings):
    _papplet.handleSettingsPt1()
    settings()
    _papplet.handleSettingsPt2()


def _update_vars():
    global frame_rate
    frame_rate = _papplet.frameRate
    global mouse_x
    mouse_x = _papplet.mouseX
    global mouse_y
    mouse_y = _papplet.mouseY


def _handle_draw(setup, draw):
    _update_vars()
    _papplet.handleDrawPt1()
    if _papplet.frameCount == 0:
        setup()
    _papplet.handleDrawPt2()
    draw()
    _papplet.handleDrawPt3()

    _papplet.render()


def run_sketch(settings, setup, draw, frameLimit=1000):
    _handle_settings(settings)
    PythonPApplet.setupSketch(['py5 sketch'], _papplet)

    while frameLimit > 0:
        _handle_draw(setup, draw)
        time.sleep(1 / 60)

        frameLimit -= 1
