"""
py5 code, interface to the Java version of Processing using PyJNIus.

This file is created by the py5generator package. Do not edit!
"""
import sys
from pathlib import Path
import logging
import traceback
import time

import py5_tools


if not py5_tools.py5_started:
    current_classpath = py5_tools.get_classpath()
    base_path = Path(
        getattr(sys, '_MEIPASS', Path(__file__).absolute().parent))
    # add py5 jars to the classpath first
    py5_tools.set_classpath(str(base_path / 'jars' / '*'))
    # if the cwd has a jars subdirectory, add that next
    py5_tools.add_jars(Path('jars'))
    # put the original classpath at the end while avoiding duplicates
    py5_tools.add_classpath(*[p for p in current_classpath
                              if p not in py5_tools.get_classpath()])
    py5_tools.py5_started = True
from jnius import autoclass, PythonJavaClass, java_method  # noqa


__version__ = '0.1'

logger = logging.getLogger(__name__)

_Py5Applet = autoclass('py5.core.Py5Applet',
                       include_protected=False, include_private=False)


# *** PY5 GENERATED STATIC CONSTANTS ***
{0}


class Py5Methods(PythonJavaClass):
    __javainterfaces__ = ['py5/core/Py5Methods']

    def __init__(self):
        self._functions = dict()

    def set_functions(self, **kwargs):
        self._functions.update(kwargs)

    def set_py5applet(self, _py5applet):
        self._py5applet = _py5applet

    @java_method('()[Ljava/lang/Object;')
    def get_function_list(self):
        return self._functions.keys()

    def _stop_error(self, msg):
        exc_type, exc_value, exc_tb = sys.exc_info()
        tbe = traceback.TracebackException(exc_type, exc_value, exc_tb)
        tb = list(tbe.format())
        logger.critical(msg + '\n' + tb[0] + ''.join(tb[2:-1]) + '\n' + tb[-1])
        # this stops the sketch but does not exit, leaving the window visible.
        # if the screen disappeared it would be harder to debug the error
        # call the `exit_sketch()` method to close and exit the window.
        self._py5applet.getSurface().stopThread()

    @java_method('(Ljava/lang/String;[Ljava/lang/Object;)V')
    def run_method(self, method_name, params):
        try:
            if method_name in self._functions:
                self._functions[method_name](*params)
        except Exception as e:
            msg = 'exception running ' + method_name + ': ' + str(e)
            self._stop_error(msg)


_METHODS = ['settings', 'setup', 'draw', 'key_pressed', 'key_typed',
            'key_released', 'mouse_clicked', 'mouse_dragged', 'mouse_moved',
            'mouse_entered', 'mouse_exited', 'mouse_pressed', 'mouse_released',
            'mouse_wheel', 'exit_actual']


class Sketch:

    def __init__(self):
        self._py5applet = _Py5Applet()

    def run_sketch(self, local_dict=None, block=False):
        py5_methods = Py5Methods()
        if local_dict:
            methods = dict([(e, local_dict[e]) for e in _METHODS if e in local_dict])
        else:
            methods = dict([(e, getattr(self, e)) for e in _METHODS if hasattr(self, e)])
        py5_methods.set_functions(**methods)
        py5_methods.set_py5applet(self._py5applet)

        # pass the py5_methods object to the py5applet object while also
        # keeping the py5_methods reference count from hitting zero. otherwise,
        # it will be garbage collected and lead to segmentation faults!
        self._py5applet.usePy5Methods(py5_methods)
        self._py5_methods = py5_methods

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


_py5sketch = Sketch()
_py5sketch_used = False


def reset_py5():
    """ attempt to reset the py5 library so a new sketch can be executed.

    Note there are race conditions between this and `stop_sketch`. If you call
    this immediately after `stop_sketch` you might experience problems.
    """
    global _py5sketch
    global _py5sketch_used
    _py5sketch = Sketch()
    _py5sketch_used = False


def __getattr__(name):
    if hasattr(_py5sketch, name):
        return getattr(_py5sketch, name)
    else:
        raise AttributeError('py5 has no function or method named ' + name)


def __dir__():
    return {2}


__all__ = {3}
