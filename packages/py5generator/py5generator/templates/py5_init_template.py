"""
Py5 code, interface to the Java version of Processing using PyJNIus.

This file is created by the py5generator package. Do not edit!
"""
import time

import jnius_config
jnius_config.add_options('-Xrs', '-Xmx4096m')
jnius_config.set_classpath(
    '.',
    '/home/jim/Projects/git/processing/core/library/*',
    '/home/jim/Projects/ITP/pythonprocessing/py5/experiments/libraries/*')
from jnius import autoclass, detach  # noqa
from jnius import JavaField, JavaStaticField, JavaMethod, JavaStaticMethod  # noqa


PythonPApplet = autoclass('processing.core.PythonPApplet',
                          include_protected=False, include_private=False)
PythonPApplet._render = JavaMethod('()V')
PythonPApplet._handleSettingsPt1 = JavaMethod('()V')
PythonPApplet._handleSettingsPt2 = JavaMethod('()V')
PythonPApplet._handleDrawPt1 = JavaMethod('()V')
PythonPApplet._handleDrawPt2 = JavaMethod('()V')
PythonPApplet._handleDrawPt3 = JavaMethod('()V')
PythonPApplet._startSurface = JavaMethod('()V')
_papplet = PythonPApplet()


_target_frame_rate = 60
_frame_rate_period = 1 / _target_frame_rate


# *** PY5 GENERATED STATIC CONSTANTS ***
{0}


# *** PY5 GENERATED DYNAMIC VARIABLES ***
{1}


def _update_vars():
    {2}


# *** PY5 GENERATED FUNCTIONS ***
{3}


# *** PY5 USER FUNCTIONS ***
def set_frame_rate(frame_rate):
    global _target_frame_rate
    global _frame_rate_period
    _target_frame_rate = frame_rate
    _frame_rate_period = 1 / frame_rate
    # this isn't really necessary
    # _papplet.surface.setFrameRate(frame_rate)
    # _papplet.getSurface().setFrameRate(frame_rate)


def run_sketch(settings, setup, draw, frameLimit=1000):

    PythonPApplet._setupSketchPt1([''], _papplet)
    # handle settings
    _papplet._handleSettingsPt1()
    settings()
    _papplet._handleSettingsPt2()
    PythonPApplet._setupSketchPt2(_papplet)
    _papplet._startSurface()

    while frameLimit > 0:
        start = time.time()

        # handle draw
        _update_vars()
        _papplet._handleDrawPt1()
        if _papplet.frameCount == 0:
            setup()
        _papplet._handleDrawPt2()
        draw()
        _papplet._handleDrawPt3()
        _papplet._render()

        time.sleep(max(0, _frame_rate_period - (time.time() - start)))

        frameLimit -= 1

    detach()
