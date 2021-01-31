# *****************************************************************************
#
#   Part of the py5 library
#   Copyright (C) 2020-2021 Jim Schmitz
#
#   This library is free software: you can redistribute it and/or modify it
#   under the terms of the GNU Lesser General Public License as published by
#   the Free Software Foundation, either version 2.1 of the License, or (at
#   your option) any later version.
#
#   This library is distributed in the hope that it will be useful, but
#   WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser
#   General Public License for more details.
#
#   You should have received a copy of the GNU Lesser General Public License
#   along with this library. If not, see <https://www.gnu.org/licenses/>.
#
# *****************************************************************************
# -*- coding: utf-8 -*-
# *** FORMAT PARAMS ***
"""
py5 makes Processing available to the CPython interpreter using JPype.
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

from .methods import register_exception_msg  # noqa
from .sketch import Sketch, Py5Surface, Py5Graphics, Py5Image, Py5Shader, Py5Shape, Py5Font, Py5Promise, _in_ipython_session  # noqa
from .render_helper import render_frame, render_frames, render, render_sequence  # noqa
from .create_font_tool import create_font_file  # noqa
from .image_conversion import register_image_conversion, NumpyImageArray  # noqa
from . import reference
from . import java_conversion  # noqa
try:
    from py5_tools.magics import load_ipython_extension  # noqa
except ModuleNotFoundError:
    # IPython must not be installed
    pass


__version__ = '0.3a5_dev0'

logger = logging.getLogger(__name__)

java_conversion.init_jpype_converters()

sketch_module_members_code = None  # DELETE
run_sketch_pre_run_code = None  # DELETE

_py5sketch = Sketch()

{sketch_module_members_code}


def run_sketch(block: bool = None,
               py5_options: List = None,
               sketch_args: List = None) -> None:
    """$module_Sketch_run_sketch"""
    # Before running the sketch, delete the module fields that need to be kept
    # uptodate. This will allow the module `__getattr__` function return the
    # proper values.
    if block is None:
        block = not _in_ipython_session

    try:
        {run_sketch_pre_run_code}
    except NameError:
        # these variables might have already been removed
        pass

    function_dict = inspect.stack()[1].frame.f_locals
    methods = dict([(e, function_dict[e]) for e in reference.METHODS if e in function_dict and callable(function_dict[e])])

    if not set(methods.keys()) & set(['settings', 'setup', 'draw']):
        print(("Unable to find settings, setup, or draw functions. "
               "Your sketch will be a small boring gray square. "
               "If that isn't what you intended, you need to make sure "
               "your implementation of those functions are available in "
               "the local namespace that made the `run_sketch()` call."))

    global _py5sketch
    if _py5sketch.is_running:
        print('Sketch is already running. To run a new sketch, exit the running sketch first.')
        return
    if _py5sketch.is_dead:
        _py5sketch = Sketch()

    _py5sketch._run_sketch(methods, block, py5_options, sketch_args)


def get_current_sketch() -> Sketch:
    """missing docstring"""
    return _py5sketch


def reset_py5() -> None:
    """missing docstring"""
    global _py5sketch
    _py5sketch = Sketch()


def prune_tracebacks(prune: bool):
    """missing docstring"""
    from . import methods
    methods._prune_tracebacks = prune


def set_stackprinter_style(style: str):
    """missing docstring"""
    from . import methods
    methods._stackprinter_style = style


def __getattr__(name):
    if hasattr(_py5sketch, name):
        return getattr(_py5sketch, name)
    else:
        raise AttributeError('py5 has no function or field named ' + name)


def __dir__():
    return reference.PY5_DIR_STR


__all__ = reference.PY5_ALL_STR
