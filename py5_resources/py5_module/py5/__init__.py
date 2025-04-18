# *****************************************************************************
#
#   Part of the py5 library
#   Copyright (C) 2020-2025 Jim Schmitz
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
py5 is a version of Processing for Python 3.9+. It makes the Processing Java libraries available to the CPython interpreter using JPype.
"""
from __future__ import annotations

import inspect
import os
import platform
import sys
import warnings
from io import BytesIO
from pathlib import Path
from typing import Any, Callable, Sequence, Union, overload  # noqa

import jpype.imports  # noqa
import numpy as np  # noqa
import numpy.typing as npt  # noqa
import py5_tools
import py5_tools.environ  # noqa
from jpype import JClass  # noqa
from jpype.types import JArray, JChar, JFloat, JInt, JString  # noqa
from PIL import Image  # noqa
from py5_tools.constants import VERSION as __version__

_environ = py5_tools.environ.Environment()

if not py5_tools.is_jvm_running():
    base_path = (
        Path(getattr(sys, "_MEIPASS")) / "py5"
        if hasattr(sys, "_MEIPASS")
        else Path(__file__).absolute().parent
    )

    if platform.system() == "Darwin":
        # Make sure Python appears on the MacOS Dock
        # This is necessary, otherwise MacOS will not like to let JAVA2D Sketches get focus
        try:
            from AppKit import (
                NSURL,
                NSApplication,
                NSApplicationActivationPolicyRegular,
                NSImage,
            )

            # this adds a white square to the dock
            app = NSApplication.sharedApplication()
            app.setActivationPolicy_(NSApplicationActivationPolicyRegular)

            # set the dock icon to the py5 logo
            icon_path = base_path.parent / "py5_tools/resources/logo.icns"
            icon_url = NSURL.fileURLWithPath_(str(icon_path))
            icon_image = NSImage.alloc().initWithContentsOfURL_(icon_url)
            app.setApplicationIconImage_(icon_image)

            # cleanup
            del app, icon_path, icon_url, icon_image
            del NSURL, NSApplication, NSApplicationActivationPolicyRegular, NSImage
        except:
            pass

    if platform.system() == "Windows":
        # This code is here so that later win32gui code works correctly. The
        # `focus_window(handle)` method in `Py5Bridge` is used to move Sketch
        # windows to the foreground
        try:
            from win32com import client as win32com_client

            shell = win32com_client.Dispatch("WScript.Shell")

            # send the most benign key possible. this can't possibly do anything
            shell.SendKeys(chr(0))

            # cleanup
            del win32com_client, shell
        except:
            pass

    # add py5 jars to the classpath first
    py5_tools.add_jars(str(base_path / "jars"))
    # add stored processing libraries
    py5_tools.add_jars(py5_tools.processing.library_storage_dir())
    # if the cwd has a jars subdirectory, add that next
    py5_tools.add_jars(Path("jars"))
    # if the PY5_JARS environment variable exists, add those jars
    if py5_classpath := os.environ.get("PY5_JARS"):
        py5_tools.add_jars(Path(py5_classpath))

    try:
        py5_tools.jvm._start_jvm()
        started_jvm = True
    except:
        started_jvm = False

    debug_info = py5_tools.get_jvm_debug_info()
    java_version = debug_info["jvm version"][0]
    if not started_jvm or java_version < 17:
        print("py5 is unable to start a Java 17 Virtual Machine.", file=sys.stderr)
        print(
            "This library requires Java 17 to be installed and a properly set JAVA_HOME environment variable.",
            file=sys.stderr,
        )
        print(
            "Here is some debug info about your installation that might help you identify the source of this problem.",
            file=sys.stderr,
        )
        print(debug_info, file=sys.stderr)
        raise RuntimeError("py5 is unable to start Java 17 Virtual Machine")

    if JClass("py5.util.CheckHeadless")().test():
        raise RuntimeError(
            "py5 is unable to run correctly in headless mode. Make sure you are running in a graphical environment and that your Java Virtual Machine is not a Headless JVM."
        )

import py5_tools.colors.css4 as css4_colors  # noqa
import py5_tools.colors.mpl_cmaps as mpl_cmaps  # noqa
import py5_tools.colors.xkcd as xkcd_colors  # noqa
from py5_tools import split_setup as _split_setup

from . import object_conversion  # noqa
from . import reference
from . import spelling as _spelling
from .bridge import register_exception_msg  # noqa
from .color import Py5Color  # noqa
from .create_font_tool import create_font_file  # noqa
from .image_conversion import NumpyImageArray, register_image_conversion  # noqa
from .render_helper import render, render_frame, render_frame_sequence, render_sequence
from .shape_conversion import register_shape_conversion  # noqa
from .sketch import (
    Py5Font,
    Py5Graphics,
    Py5Image,
    Py5KeyEvent,
    Py5MouseEvent,
    Py5Promise,
    Py5Shader,
    Py5Shape,
    Py5Surface,
    Sketch,
)
from .vector import Py5Vector, Py5Vector2D, Py5Vector3D, Py5Vector4D  # noqa

try:
    from py5_tools.magics import load_ipython_extension  # noqa
except ImportError:
    # IPython must not be installed
    pass

_PY5_USE_IMPORTED_MODE = py5_tools.get_imported_mode()
py5_tools._lock_imported_mode()

object_conversion.init_jpype_converters()

warnings.filterwarnings("once", category=DeprecationWarning, module="py5")

sketch_module_members_code = None  # DELETE
run_sketch_pre_run_code = None  # DELETE
println = None  # DELETE

_py5sketch = Sketch()

{sketch_module_members_code}


def run_sketch(
    block: bool = None,
    *,
    py5_options: list[str] = None,
    sketch_args: list[str] = None,
    sketch_functions: dict[str, Callable] = None,
    jclassname: str = None,
    jclass_params: tuple[Any] = (),
    _osx_alt_run_method: bool = True,
) -> None:
    """$module_Sketch_run_sketch"""
    caller_locals = inspect.stack()[1].frame.f_locals
    caller_globals = inspect.stack()[1].frame.f_globals
    functions, function_param_counts = bridge._extract_py5_user_function_data(
        sketch_functions if sketch_functions else caller_locals
    )
    functions = _split_setup.transform(
        functions,
        caller_globals,
        caller_locals,
        println,
        mode="imported" if _PY5_USE_IMPORTED_MODE else "module",
    )

    if functions is None:
        return

    if (
        not set(functions.keys()) & set(["settings", "setup", "draw"])
        and not jclassname
    ):
        warnings.warn(
            (
                "Unable to find settings, setup, or draw functions. "
                "Your sketch will be a small gray square. "
                "If that isn't what you intended, you need to make sure "
                "your implementation of those functions are available in "
                "the local namespace that made the `run_sketch()` call."
            ),
            stacklevel=2,
        )

    global _py5sketch
    if _py5sketch.is_running:
        print(
            "Sketch is already running. To run a new sketch, exit the running sketch first.",
            file=sys.stderr,
        )
        return
    if _py5sketch.is_dead or jclassname:
        _py5sketch = Sketch(jclassname=jclassname, jclass_params=jclass_params)

    _prepare_dynamic_variables(caller_locals, caller_globals)

    _py5sketch._run_sketch(
        functions,
        function_param_counts,
        block,
        py5_options=py5_options,
        sketch_args=sketch_args,
        _caller_locals=caller_locals,
        _caller_globals=caller_globals,
        _osx_alt_run_method=_osx_alt_run_method,
    )


def get_current_sketch() -> Sketch:
    """$module_Py5Functions_get_current_sketch"""
    return _py5sketch


def reset_py5(*, jclassname: str = None, _force=False) -> bool:
    """$module_Py5Functions_reset_py5"""
    global _py5sketch
    if _force or jclassname or _py5sketch.is_dead:
        _py5sketch = Sketch(jclassname=jclassname)
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
        raise AttributeError(_spelling.error_msg("", name, _py5sketch, module=True))


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
    for dvar in (
        py5_tools.reference.PY5_DYNAMIC_VARIABLES
        + py5_tools.reference.PY5_PYTHON_DYNAMIC_VARIABLES
    ):
        if dvar in caller_globals:
            caller_globals.pop(dvar)
        if _PY5_USE_IMPORTED_MODE:
            if dvar in py5_tools.reference.PY5_DYNAMIC_VARIABLES:
                caller_locals[dvar] = getattr(_py5sketch, "_get_" + dvar)
            else:
                caller_locals[dvar] = getattr(_py5sketch, dvar)


_prepare_dynamic_variables(locals(), globals())


if platform.system() == "Darwin" and _environ.in_ipython_session:
    if _environ.ipython_shell.active_eventloop != "osx":
        print(
            "Importing py5 on macOS but the necessary Jupyter macOS event loop has not been activated. I'll activate it for you, but next time, execute `%gui osx` before importing this library."
        )
        _environ.ipython_shell.run_line_magic("gui", "osx")
