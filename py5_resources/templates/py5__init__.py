"""
py5 code, interface to the Java version of Processing using PyJNIus.

This file is created by the py5generator package. Do not edit!
"""
import sys
from pathlib import Path
import logging
import traceback
import time

import jnius_config
if not jnius_config.vm_running:
    current_classpath = jnius_config.get_classpath()
    base_path = Path(
        getattr(sys, '_MEIPASS', Path(__file__).absolute().parent))
    jnius_config.set_classpath(str(base_path / 'jars' / '*'))
    jnius_config.add_classpath(
        *[p for p in current_classpath if p not in jnius_config.get_classpath()])
from jnius import autoclass, JavaMultipleMethod, JavaMethod, PythonJavaClass, java_method  # noqa

logger = logging.getLogger(__name__)

_Py5Applet = autoclass('py5.core.Py5Applet',
                       include_protected=False, include_private=False)


# *** PY5 GENERATED STATIC CONSTANTS ***
{0}


class Py5Methods(PythonJavaClass):
    __javainterfaces__ = ['py5/core/Py5Methods']

    def __init__(self, settings, setup, draw):
        self._functions = dict()
        self._functions['settings'] = settings
        self._functions['setup'] = setup
        self._functions['draw'] = draw

    def set_events(self, **kwargs):
        self._functions.update(kwargs)

    def _stop_error(self, msg):
        exc_type, exc_value, exc_tb = sys.exc_info()
        tbe = traceback.TracebackException(exc_type, exc_value, exc_tb)
        tb = list(tbe.format())
        logger.critical(msg + '\n' + tb[0] + ''.join(tb[2:-1]) + '\n' + tb[-1])
        _py5applet.getSurface().stopThread()

    @java_method('(Ljava/lang/String;[Ljava/lang/Object;)V')
    def run_method(self, method_name, params):
        try:
            if method_name in self._functions:
                self._functions[method_name](*params)
        except Exception as e:
            msg = 'exception running ' + method_name + ': ' + str(e)
            self._stop_error(msg)


_EVENT_METHODS = ['key_pressed', 'key_typed', 'key_released',
                  'mouse_clicked', 'mouse_dragged', 'mouse_moved', 'mouse_entered',
                  'mouse_exited', 'mouse_pressed', 'mouse_released', 'mouse_wheel',
                  'exit_actual']


class Py5Applet:

    def __init__(self):
        self._py5applet = _Py5Applet()

    def settings(self):
        pass

    def setup(self):
        pass

    def draw(self):
        pass

    def run_sketch(self, py5_methods=None, block=False):
        if not py5_methods:
            py5_methods = Py5Methods(self.settings, self.setup, self.draw)
        events = dict([(e, getattr(self, e)) for e in _EVENT_METHODS if hasattr(self, e)])
        py5_methods.set_events(**events)
        self._py5applet.usePy5Methods(py5_methods)
        _Py5Applet.runSketch([''], self._py5applet)

        if block:
            # wait for the sketch to finish
            surface = self._py5applet.getSurface()
            while not surface.isStopped():
                time.sleep(0.25)

    def exit_sketch(self):
        if self._py5applet.getSurface().isStopped():
            self._py5applet.exit()

    def get_py5applet(self):
        return self._py5applet


{1}


_py5applet = Py5Applet()
_py5applet_used = False


def reset_py5():
    """ attempt to reset the py5 library so a new sketch can be executed.

    Note there are race conditions between this and `stop_sketch`. If you call
    this immediately after `stop_sketch` you might experience problems.
    """
    global _py5applet
    global _py5applet_used
    _py5applet = Py5Applet()
    _py5applet_used = False


def __getattr__(name):
    if hasattr(_py5applet, name):
        return getattr(_py5applet, name)
    else:
        raise AttributeError('py5 has no function or method named ' + name)


def __dir__():
    return {2}
