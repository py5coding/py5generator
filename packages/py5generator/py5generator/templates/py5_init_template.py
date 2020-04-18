"""
Py5 code, interface to the Java version of Processing using PyJNIus.

This file is created by the py5generator package. Do not edit!
"""
import threading

import jnius_config
jnius_config.add_options('-Xrs', '-Xmx4096m')
jnius_config.set_classpath(
    '.',
    '/home/jim/Projects/ITP/pythonprocessing/py5/jars/2.4/*',
    # '/home/jim/Projects/ITP/pythonprocessing/processing/core/library/*',
    # '/home/jim/Projects/git/processing/core/library/*',
    # '/home/jim/Projects/ITP/pythonprocessing/py5/experiments/processing_jars/*',
    '/home/jim/Projects/ITP/pythonprocessing/py5/experiments/libraries/*')
from jnius import autoclass, detach  # noqa
from jnius import JavaField, JavaStaticField, JavaMethod, JavaStaticMethod  # noqa
from jnius import PythonJavaClass, java_method  # noqa


class Py5Callbacks(PythonJavaClass):
    __javainterfaces__ = ['processing/core/PythonCallbacks']

    def __init__(self, settings, setup, draw):
        self._settings = settings
        self._setup = setup
        self._draw = draw

    @java_method('()V')
    def settings(self):
        self._settings()

    @java_method('()V')
    def setup(self):
        self._setup()

    @java_method('()V')
    def draw(self):
        _update_vars()
        self._draw()


PApplet = autoclass('processing.core.PApplet',
                    include_protected=False, include_private=False)
_papplet = PApplet()

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
    _papplet.getSurface().setFrameRate(frame_rate)


def run_sketch(settings, setup, draw):

    callbacks = Py5Callbacks(settings, setup, draw)
    _papplet.setPythonCallbacks(callbacks)

    # def _papplet_runsketch():
    PApplet.runSketch([''], _papplet)

    # jvm_thread = threading.Thread(target=_papplet_runsketch)
    # jvm_thread.start()

    detach()


def run_sketch2(callbacks):
    _papplet.setPythonCallbacks(callbacks)

    # def _papplet_runsketch():
    PApplet.runSketch([''], _papplet)

    # jvm_thread = threading.Thread(target=_papplet_runsketch)
    # jvm_thread.start()

    detach()
