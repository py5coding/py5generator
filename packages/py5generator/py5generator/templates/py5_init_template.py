"""
Py5 code, interface to the Java version of Processing using PyJNIus.

This file is created by the py5generator package. Do not edit!
"""
import time

import jnius_config
jnius_config.add_options('-Xrs', '-Xmx4096m')
jnius_config.set_classpath('.', '/home/jim/Projects/git/processing/core/library/*')
from jnius import autoclass, detach  # noqa

PythonPApplet = autoclass('processing.core.PythonPApplet')
_papplet = PythonPApplet()


# *** PY5 GENERATED STATIC CONSTANTS ***
{0}


# *** PY5 GENERATED DYNAMIC VARIABLES ***
{1}


def _update_vars():
    {2}


# *** PY5 GENERATED FUNCTIONS ***
{3}


def _handle_settings(settings):
    _papplet.handleSettingsPt1()
    settings()
    _papplet.handleSettingsPt2()


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
    PythonPApplet.setupSketch([''], _papplet)

    while frameLimit > 0:
        _handle_draw(setup, draw)
        time.sleep(1 / 60)

        frameLimit -= 1

    detach()
