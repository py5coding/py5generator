# -*- coding: utf-8 -*-
# *** FORMAT PARAMS ***
"""
py5 code, interface to the Java version of Processing using JPype.
"""
import sys
from pathlib import Path
import logging
import inspect
from typing import overload, Any, Callable, Union, Dict, List, Tuple  # noqa
from nptyping import NDArray, Float  # noqa

import json  # noqa
import numpy as np  # noqa
from PIL import Image  # noqa
from jpype import JClass  # noqa
from jpype.types import JArray, JString, JFloat, JInt, JChar  # noqa

import py5_tools

if not py5_tools.is_jvm_running():
    base_path = Path(getattr(sys, '_MEIPASS', Path(__file__).absolute().parent))
    # add py5 jars to the classpath first
    py5_tools.add_jars(str(base_path / 'jars'))
    # if the cwd has a jars subdirectory, add that next
    py5_tools.add_jars(Path('jars'))
    py5_tools.start_jvm()

from .methods import Py5Exception  # noqa
from .sketch import Sketch, _METHODS, Py5Surface, Py5Graphics, Py5Image, Py5Shader, Py5Shape, Py5Font, Py5Promise, _in_ipython_session  # noqa
from .create_font_tool import create_font_file  # noqa
from .image_conversion import register_image_conversion, NumpyImageArray  # noqa
from . import java_conversion  # noqa
try:
    from py5_tools.magics import load_ipython_extension  # noqa
except ModuleNotFoundError:
    # IPython must not be installed
    pass


__version__ = '0.2a2'

logger = logging.getLogger(__name__)

java_conversion.init_jpype_converters()

sketch_module_members_code = None  # DELETE
run_sketch_pre_run_code = None  # DELETE
py5_dir_str = None  # DELETE
py5_all_str = None  # DELETE

_py5sketch = Sketch()

{sketch_module_members_code}


def run_sketch(function_dict: Dict[str, Any] = None,
               block: bool = not _in_ipython_session,
               py5_options: List = None,
               sketch_args: List = None) -> None:
    """run the py5 sketch

    The optional function_dict parameter needs to a be a dictionary that
    contains the settings, setup, and draw functions.

    You can call it like this:
    ```
        py5.run_sketch(function_dict=locals())
    ```

    But most likely you can just do this:
    ```
        py5.run_sketch()
    ```
    """
    # Before running the sketch, delete the module fields that need to be kept
    # uptodate. This will allow the module `__getattr__` function return the
    # proper values.
    try:
        {run_sketch_pre_run_code}
    except NameError:
        # these variables might have already been removed
        pass

    if not function_dict:
        function_dict = inspect.stack()[1].frame.f_locals
    methods = dict([(e, function_dict[e]) for e in _METHODS if e in function_dict])

    if not set(methods.keys()) & set(['settings', 'setup', 'draw']):
        print(("Unable to find settings, setup, or draw functions. "
               "Your sketch will be a small boring gray square. "
               "If that isn't what you intended, try this instead:\n"
               "py5.run_sketch(function_dict=locals())"))

    global _py5sketch
    if _py5sketch.is_running:
        print('Sketch is already running. To run a new sketch, exit the running sketch first.')
        return
    if _py5sketch.is_dead:
        _py5sketch = Sketch()

    _py5sketch._run_sketch(methods, block, py5_options, sketch_args)


def get_current_sketch() -> Sketch:
    return _py5sketch


# TODO: error message through Jupyter might not be correct when reset needs to be called
# TODO: run sketch should do the reset for me

def reset_py5() -> None:
    """reset the py5 library so a new sketch can be executed.
    """
    global _py5sketch
    _py5sketch = Sketch()


def prune_tracebacks(prune: bool):
    from . import methods
    methods._prune_tracebacks = prune


def set_stackprinter_style(style: str):
    from . import methods
    methods._stackprinter_style = style


def __getattr__(name):
    if hasattr(_py5sketch, name):
        return getattr(_py5sketch, name)
    else:
        raise AttributeError('py5 has no function or field named ' + name)


def __dir__():
    return {py5_dir_str}


__all__ = {py5_all_str}
