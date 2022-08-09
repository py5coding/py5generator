# *****************************************************************************
#
#   Part of the py5 library
#   Copyright (C) 2020-2022 Jim Schmitz
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
py5 is a version of Processing for Python 3.8+. It makes the Processing Java libraries available to the CPython interpreter using JPype.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path
from io import BytesIO
import inspect
from typing import overload, Any, Callable, Union  # noqa
import warnings

import numpy as np  # noqa
import numpy.typing as npt  # noqa
from PIL import Image  # noqa
from jpype import JClass  # noqa
import jpype.imports  # noqa
from jpype.types import JArray, JString, JFloat, JInt, JChar  # noqa

import py5_tools

if not py5_tools.is_jvm_running():
    base_path = Path(getattr(sys, '_MEIPASS')) / 'py5' if hasattr(sys, '_MEIPASS') else Path(__file__).absolute().parent
    # add py5 jars to the classpath first
    py5_tools.add_jars(str(base_path / 'jars'))
    # if the cwd has a jars subdirectory, add that next
    py5_tools.add_jars(Path('jars'))
    # if the PY5_CLASSPATH environment variable exists, add those jars
    if (py5_classpath := os.environ.get('PY5_JARS')):
        py5_tools.add_jars(Path(py5_classpath))

    try:
        py5_tools.jvm._start_jvm()
        started_jvm = True
    except:
        started_jvm = False

    debug_info = py5_tools.get_jvm_debug_info()
    java_version = debug_info['jvm version'][0]
    if not started_jvm or java_version < 17:
        print("py5 is unable to start a Java 17 Virtual Machine.", file=sys.stderr)
        print("This library requires Java 17 to be installed and a properly set JAVA_HOME environment variable.", file=sys.stderr)
        print("Here is some debug info about your installation that might help you identify the source of this problem.", file=sys.stderr)
        print(debug_info, file=sys.stderr)
        raise RuntimeError("py5 is unable to start Java 17 Virtual Machine")

from .bridge import register_exception_msg  # noqa
from .sketch import Sketch, Py5Surface, Py5Graphics, Py5Image, Py5Shader, Py5Shape, Py5Font, Py5KeyEvent, Py5MouseEvent, Py5Promise  # noqa
from .render_helper import render_frame, render_frame_sequence, render, render_sequence  # noqa
from .create_font_tool import create_font_file  # noqa
from .image_conversion import register_image_conversion, NumpyImageArray  # noqa
from .vector import Py5Vector, Py5Vector2D, Py5Vector3D, Py5Vector4D  # noqa
from py5_tools import split_setup as _split_setup
from . import reference
from . import java_conversion  # noqa
try:
    from py5_tools.magics import load_ipython_extension  # noqa
except ModuleNotFoundError:
    # IPython must not be installed
    pass


__version__ = '0.8.1a1'

_PY5_USE_IMPORTED_MODE = py5_tools.get_imported_mode()
py5_tools._lock_imported_mode()

java_conversion.init_jpype_converters()

sketch_module_members_code = None  # DELETE
run_sketch_pre_run_code = None  # DELETE
println = None # DELETE

_py5sketch = Sketch()

{sketch_module_members_code}


def run_sketch(block: bool = None, *,
               py5_options: list[str] = None,
               sketch_args: list[str] = None,
               sketch_functions: dict[str, Callable] = None,
               _jclassname: str = None,
               _osx_alt_run_method: bool = True) -> None:
    """$module_Sketch_run_sketch"""
    caller_globals = inspect.stack()[1].frame.f_globals
    caller_locals = inspect.stack()[1].frame.f_locals
    functions, function_param_counts = bridge._extract_py5_user_function_data(sketch_functions if sketch_functions else caller_locals)
    functions = _split_setup.transform(functions, caller_globals, caller_locals, println, mode='imported' if _PY5_USE_IMPORTED_MODE else 'module')

    if not set(functions.keys()) & set(['settings', 'setup', 'draw']):
        warnings.warn(("Unable to find settings, setup, or draw functions. "
                       "Your sketch will be a small boring gray square. "
                       "If that isn't what you intended, you need to make sure "
                       "your implementation of those functions are available in "
                       "the local namespace that made the `run_sketch()` call."),
                       stacklevel=2)

    global _py5sketch
    if _py5sketch.is_running:
        print('Sketch is already running. To run a new sketch, exit the running sketch first.', file=sys.stderr)
        return
    if _py5sketch.is_dead or _jclassname:
        _py5sketch = Sketch(_jclassname=_jclassname)

    _prepare_dynamic_variables(caller_locals, caller_globals)

    _py5sketch._run_sketch(functions, function_param_counts, block, py5_options, sketch_args, _osx_alt_run_method)


def get_current_sketch() -> Sketch:
    """$module_Py5Functions_get_current_sketch"""
    return _py5sketch


def reset_py5(*, _jclassname: str = None, _force=False) -> bool:
    """$module_Py5Functions_reset_py5"""
    global _py5sketch
    if _py5sketch.is_dead or _force or _jclassname:
        _py5sketch = Sketch(_jclassname=_jclassname)
        if _PY5_USE_IMPORTED_MODE:
            caller_locals = inspect.stack()[1].frame.f_locals
            caller_globals = inspect.stack()[1].frame.f_globals
            _prepare_dynamic_variables(caller_locals, caller_globals)
        return True
    else:
        return False


def prune_tracebacks(prune: bool) -> None:
    """$module_Py5Functions_prune_tracebacks"""
    from . import bridge
    bridge._prune_tracebacks = prune


def set_stackprinter_style(style: str) -> None:
    """$module_Py5Functions_set_stackprinter_style"""
    from . import bridge
    bridge._stackprinter_style = style


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


def _prepare_dynamic_variables(caller_locals, caller_globals):
    """prepare the dynamic variables for sketch execution.

    Before running the sketch, delete the module fields like `mouse_x` that need
    to be kept current as the sketch runs. This will allow the module's
    `__getattr__` function return the proper values.

    When running in imported mode, place variables in the the caller's local
    namespace that link to the Sketch's dynamic variable property objects.
    """
    for dvar in py5_tools.reference.PY5_DYNAMIC_VARIABLES + py5_tools.reference.PY5_PYTHON_DYNAMIC_VARIABLES:
        if dvar in caller_globals:
            caller_globals.pop(dvar)
        if _PY5_USE_IMPORTED_MODE:
            if dvar in py5_tools.reference.PY5_DYNAMIC_VARIABLES:
                caller_locals[dvar] = getattr(_py5sketch, '_get_' + dvar)
            else:
                caller_locals[dvar] = getattr(_py5sketch, dvar)


_prepare_dynamic_variables(locals(), globals())
