"""
Py5 code, interface to the Java version of Processing using PyJNIus.

This file is created by the py5generator package. Do not edit!
"""
import time

import jnius_config
jnius_config.add_options('-Xrs', '-Xmx4096m')
jnius_config.set_classpath(
    '.', '/home/jim/Projects/git/processing/core/library/*')
from jnius import autoclass, detach  # noqa
from jnius import JavaField, JavaClass, MetaJavaClass, JavaMethod, JavaStaticMethod, JavaMultipleMethod  # noqa


class PythonPApplet(JavaClass, metaclass=MetaJavaClass):
    __javaclass__ = 'processing/core/PythonPApplet'

    background = JavaMultipleMethod([('(I)V', False, False),
                                     ('(IF)V', False, False),
                                     ('(F)V', False, False),
                                     ('(FF)V', False, False),
                                     ('(FFF)V', False, False),
                                     ('(FFFF)V', False, False)])
    size = JavaMultipleMethod([('(II)V', False, False),
                               ('(IILjava/lang/String;)V', False, False),
                               ('(IILjava/lang/String;Ljava/lang/String;)V', False, False)])
    rectMode = JavaMethod('(I)V')
    random = JavaMultipleMethod([('(F)F', False, False),
                                 ('(FF)F', False, False)])
    fill = JavaMethod('(FFFF)V')
    rect = JavaMethod('(FFFF)V')

    frameRate = JavaField('F')
    frameCount = JavaField('I')
    mouseX = JavaField('I')
    mouseY = JavaField('I')

    surface = JavaField('Lprocessing/core/PSurface;')
    getSurface = JavaMethod('()Lprocessing/core/PSurface;')

    handleSettingsPt1 = JavaMethod('()V')
    handleSettingsPt2 = JavaMethod('()V')
    handleDrawPt1 = JavaMethod('()V')
    handleDrawPt2 = JavaMethod('()V')
    handleDrawPt3 = JavaMethod('()V')
    setupSketch = JavaStaticMethod('([Ljava/lang/String;Lprocessing/core/PApplet;)V')
    render = JavaMethod('()V')


# PythonPApplet = autoclass('processing.core.PythonPApplet')
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
    _papplet.surface.setFrameRate(frame_rate)
    # _papplet.getSurface().setFrameRate(frame_rate)


def run_sketch(settings, setup, draw, frameLimit=1000):
    # handle settings
    _papplet.handleSettingsPt1()
    settings()
    _papplet.handleSettingsPt2()

    PythonPApplet.setupSketch([''], _papplet)

    while frameLimit > 0:
        start = time.time()

        # handle draw
        _update_vars()
        _papplet.handleDrawPt1()
        if _papplet.frameCount == 0:
            setup()
        _papplet.handleDrawPt2()
        draw()
        _papplet.handleDrawPt3()
        _papplet.render()

        time.sleep(max(0, _frame_rate_period - (time.time() - start)))

        frameLimit -= 1

    detach()
