"""
Py5 code, interface to the Java version of Processing using PyJNIus.

This file is created by the py5generator package. Do not edit!
"""
import jnius_config
jnius_config.add_options('-Xrs', '-Xmx4096m')
current_classpath = jnius_config.get_classpath()
jnius_config.set_classpath(*{0})
jnius_config.add_classpath('/home/jim/Projects/ITP/pythonprocessing/py5/experiments/libraries/*')
jnius_config.add_classpath(*[p for p in current_classpath if p not in jnius_config.get_classpath()])

from jnius import autoclass, detach  # noqa
from jnius import JavaField, JavaStaticField, JavaMethod, JavaStaticMethod  # noqa
from jnius import PythonJavaClass, java_method  # noqa


class Py5Methods(PythonJavaClass):
    __javainterfaces__ = ['processing/core/Py5Methods']

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

    @java_method('()V')
    def exit_actual(self):
        detach()


PApplet = autoclass('processing.core.PApplet',
                    include_protected=False, include_private=False)
_papplet = PApplet()

_target_frame_rate = 60
_frame_rate_period = 1 / _target_frame_rate


# *** PY5 GENERATED STATIC CONSTANTS ***
{1}


# *** PY5 GENERATED DYNAMIC VARIABLES ***
{2}


def _update_vars():
    {3}


# *** PY5 GENERATED FUNCTIONS ***
{4}


# *** PY5 USER FUNCTIONS ***
def set_frame_rate(frame_rate):
    _papplet.getSurface().setFrameRate(frame_rate)


def run_sketch(settings, setup, draw):

    py5_methods = Py5Methods(settings, setup, draw)
    _papplet.usePy5Methods(py5_methods)

    PApplet.runSketch([''], _papplet)


def run_sketch2(py5_methods):
    _papplet.usePy5Methods(py5_methods)

    PApplet.runSketch([''], _papplet)
