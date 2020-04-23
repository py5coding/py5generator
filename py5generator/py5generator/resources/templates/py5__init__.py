"""
py5 code, interface to the Java version of Processing using PyJNIus.

This file is created by the py5generator package. Do not edit!
"""
import sys
from pathlib import Path
import jnius_config


jnius_config.add_options('-Xrs', '-Xmx4096m')
current_classpath = jnius_config.get_classpath()
base_path = Path(getattr(sys, '_MEIPASS', Path(__file__).absolute().parent))
jnius_config.set_classpath(str(base_path / 'jars' / '*'))
# TODO: find a better way to add the Processing libraries like Camera3D and Colorblindness
jnius_config.add_classpath('/home/jim/Projects/ITP/pythonprocessing/py5development/experiments/libraries/*')
jnius_config.add_classpath(*[p for p in current_classpath if p not in jnius_config.get_classpath()])


from jnius import autoclass, detach  # noqa
from jnius import JavaMultipleMethod, JavaMethod  # noqa
from jnius import PythonJavaClass, java_method  # noqa


class Py5Methods(PythonJavaClass):
    __javainterfaces__ = ['processing/core/Py5Methods']

    def __init__(self, settings, setup, draw):
        self._functions = dict()
        self._functions['settings'] = settings
        self._functions['setup'] = setup
        self._functions['draw'] = draw

    def set_events(self, **kwargs):
        self._functions.update(kwargs)

    @java_method('(Ljava/lang/String;)V')
    def run_method(self, methodName):
        if methodName == 'draw':
            _update_vars()
        elif methodName == 'exitActual':
            detach()

        if methodName in self._functions:
            self._functions[methodName]()

    @java_method('(Lprocessing/event/MouseEvent;)V')
    def mouse_wheel(self, event):
        if self._mouse_wheel:
            self._mouse_wheel(event)


Py5Applet = autoclass('processing.core.Py5Applet',
                      include_protected=False, include_private=False)
_papplet = Py5Applet()


# *** PY5 GENERATED STATIC CONSTANTS ***
{0}


# *** PY5 GENERATED DYNAMIC VARIABLES ***
{1}


def _update_vars():
    {2}


# *** PY5 GENERATED FUNCTIONS ***
{3}


# *** PY5 USER FUNCTIONS ***
def run_sketch(settings, setup, draw):

    py5_methods = Py5Methods(settings, setup, draw)
    _papplet.usePy5Methods(py5_methods)

    Py5Applet.runSketch([''], _papplet)


def run_sketch2(py5_methods):
    _papplet.usePy5Methods(py5_methods)

    Py5Applet.runSketch([''], _papplet)
