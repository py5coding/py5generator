"""
Py5 code, interface to the Java version of Processing using PyJNIus.

This file is created by the py5generator package. Do not edit!
"""
import time
import threading

import jnius_config
jnius_config.add_options('-Xrs', '-Xmx4096m')
jnius_config.set_classpath(
    '.',
    '/home/jim/Projects/ITP/pythonprocessing/processing/core/library/*',
    # '/home/jim/Projects/git/processing/core/library/*',
    # '/home/jim/Projects/ITP/pythonprocessing/py5/experiments/processing_jars/*',
    '/home/jim/Projects/ITP/pythonprocessing/py5/experiments/libraries/*')
from jnius import autoclass, detach  # noqa
from jnius import JavaField, JavaStaticField, JavaMethod, JavaStaticMethod  # noqa


PApplet = autoclass('processing.core.PApplet',
                    include_protected=False, include_private=False)
PApplet.activatePythonTaskBlocker = JavaMethod('()V')
PApplet.getPythonTaskBlocker = JavaMethod('()Lprocessing/core/PythonTaskBlocker;')
_papplet = PApplet()
_papplet.activatePythonTaskBlocker()
_python_task_blocker = _papplet.getPythonTaskBlocker()

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


def run_sketch(settings, setup, draw, frameLimit=1000):

    print('calling run sketch')

    def _papplet_runsketch():
        PApplet.runSketch([''], _papplet)

    jvm_thread = threading.Thread(target=_papplet_runsketch)
    jvm_thread.start()

    print('starting loop')

    while frameLimit > 0:
        task = _python_task_blocker.getPythonTask()
        if not task:
            time.sleep(0.001)
            continue
        _update_vars()
        if task == "settings":
            settings()
        if task == "setup":
            setup()
        elif task == "draw":
            draw()
            frameLimit -= 1
        elif task == "exit":
            break
        _python_task_blocker.continueJava()

    detach()
