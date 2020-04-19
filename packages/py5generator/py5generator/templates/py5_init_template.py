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
        self._key_pressed = None
        self._key_typed = None
        self._key_released = None
        self._mouse_clicked = None
        self._mouse_dragged = None
        self._mouse_moved = None
        self._mouse_entered = None
        self._mouse_exited = None
        self._mouse_pressed = None
        self._mouse_released = None
        self._mouse_wheel = None

    def set_events(self, **kwargs):
        self._key_pressed = kwargs.get('key_pressed')
        self._key_typed = kwargs.get('key_typed')
        self._key_released = kwargs.get('key_released')
        self._mouse_clicked = kwargs.get('mouse_clicked')
        self._mouse_dragged = kwargs.get('mouse_dragged')
        self._mouse_moved = kwargs.get('mouse_moved')
        self._mouse_entered = kwargs.get('mouse_entered')
        self._mouse_exited = kwargs.get('mouse_exited')
        self._mouse_pressed = kwargs.get('mouse_pressed')
        self._mouse_released = kwargs.get('mouse_released')
        self._mouse_wheel = kwargs.get('mouse_wheel')

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
    def key_pressed(self):
        if self._key_pressed:
            self._key_pressed()

    @java_method('()V')
    def key_typed(self):
        if self._key_typed:
            self._key_typed()

    @java_method('()V')
    def key_released(self):
        if self._key_released:
            self._key_released()

    @java_method('()V')
    def exit_actual(self):
        detach()

    @java_method('()V')
    def mouse_clicked(self):
        if self._mouse_clicked:
            self._mouse_clicked()

    @java_method('()V')
    def mouse_dragged(self):
        if self._mouse_dragged:
            self._mouse_dragged()

    @java_method('()V')
    def mouse_moved(self):
        if self._mouse_moved:
            self._mouse_moved()

    @java_method('()V')
    def mouse_entered(self):
        if self._mouse_entered:
            self._mouse_entered()

    @java_method('()V')
    def mouse_exited(self):
        if self._mouse_exited:
            self._mouse_exited()

    @java_method('()V')
    def mouse_pressed(self):
        if self._mouse_pressed:
            self._mouse_pressed()

    @java_method('()V')
    def mouse_released(self):
        if self._mouse_released:
            self._mouse_released()

    @java_method('(Lprocessing/event/MouseEvent;)V')
    def mouse_wheel(self, event):
        if self._mouse_wheel:
            self._mouse_wheel(event)


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
