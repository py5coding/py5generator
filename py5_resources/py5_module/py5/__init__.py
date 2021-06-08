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
import inspect
from typing import overload, Any, Callable, Union, Dict, List, Tuple  # noqa
from nptyping import NDArray, Float, Int  # noqa

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
    py5_tools.jvm._start_jvm()

from .methods import register_exception_msg  # noqa
from .sketch import Sketch, Py5Surface, Py5Graphics, Py5Image, Py5Shader, Py5Shape, Py5Font, Py5Promise, _in_ipython_session  # noqa
from .render_helper import render_frame, render_frame_sequence, render, render_sequence  # noqa
from .create_font_tool import create_font_file  # noqa
from .image_conversion import register_image_conversion, NumpyImageArray  # noqa
from . import reference
from . import java_conversion  # noqa
try:
    from py5_tools.magics import load_ipython_extension  # noqa
except ModuleNotFoundError:
    # IPython must not be installed
    pass


__version__ = '0.4a2.dev0'

_PY5_USE_IMPORTED_MODE = py5_tools.imported.get_imported_mode()

java_conversion.init_jpype_converters()

sketch_module_members_code = None  # DELETE
run_sketch_pre_run_code = None  # DELETE

_py5sketch = Sketch()

{sketch_module_members_code}


def run_sketch(block: bool = None, *,
               py5_options: List[str] = None,
               sketch_args: List[str] = None,
               stream_redirect: Callable = None,
               sketch_functions: Dict[str, Callable] = None) -> None:
    """$module_Sketch_run_sketch"""
    if block is None:
        block = not _in_ipython_session

    sketch_functions = sketch_functions or inspect.stack()[1].frame.f_locals
    functions = dict([(e, sketch_functions[e]) for e in reference.METHODS if e in sketch_functions and callable(sketch_functions[e])])

    if not set(functions.keys()) & set(['settings', 'setup', 'draw']):
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

    _prepare_dynamic_variables(sketch_functions)

    _py5sketch._run_sketch(functions, block, py5_options, sketch_args, stream_redirect)


def get_current_sketch() -> Sketch:
    """$module_Py5Functions_get_current_sketch"""
    return _py5sketch


def reset_py5() -> bool:
    """$module_Py5Functions_reset_py5"""
    global _py5sketch
    if _py5sketch.is_dead:
        _py5sketch = Sketch()
        if _PY5_USE_IMPORTED_MODE:
            caller_locals = inspect.stack()[1].frame.f_locals
            _prepare_dynamic_variables(caller_locals)
        return True
    else:
        return False


def prune_tracebacks(prune: bool) -> None:
    """$module_Py5Functions_prune_tracebacks"""
    from . import methods
    methods._prune_tracebacks = prune


def set_stackprinter_style(style: str) -> None:
    """$module_Py5Functions_set_stackprinter_style"""
    from . import methods
    methods._stackprinter_style = style


def __getattr__(name):
    if hasattr(_py5sketch, name):
        return getattr(_py5sketch, name)
    else:
        raise AttributeError('py5 has no function or field named ' + name)


def __dir__():
    return py5_tools.reference.PY5_DIR_STR


__all__ = py5_tools.reference.PY5_ALL_STR
if _PY5_USE_IMPORTED_MODE:
    __all__.extend(py5_tools.reference.PY5_DYNAMIC_VARIABLES)


def _prepare_dynamic_variables(caller_locals):
    """prepare the dynamic variables for sketch execution.

    Before running the sketch, delete the module fields like `mouse_x` that need
    to be kept current as the sketch runs. This will allow the module's
    `__getattr__` function return the proper values.

    When running in imported mode, place variables in the the caller's local
    namespace that link to the Sketch's dynamic variable property objects.
    """
    for dvar in py5_tools.reference.PY5_DYNAMIC_VARIABLES:
        if dvar in globals():
            globals().pop(dvar)
        if _PY5_USE_IMPORTED_MODE:
            caller_locals[dvar] = getattr(_py5sketch, '_get_' + dvar)


_prepare_dynamic_variables(locals())
