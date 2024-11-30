# *****************************************************************************
#
#   Part of the py5 library
#   Copyright (C) 2020-2024 Jim Schmitz
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
# *** FORMAT PARAMS ***
from __future__ import annotations

import functools
import inspect
import os
import platform
import sys
import time
import types
import uuid
import warnings
from io import BytesIO
from pathlib import Path
from typing import Any, Callable, Union, overload  # noqa

import jpype
import numpy as np
import numpy.typing as npt
import py5_tools
import py5_tools.environ as _environ
from jpype.types import JArray, JClass, JException, JInt  # noqa
from py5_tools.printstreams import _DefaultPrintlnStream, _DisplayPubPrintlnStream

from . import image_conversion, reference, shape_conversion, spelling
from .base import Py5Base
from .bridge import Py5Bridge, _extract_py5_user_function_data
from .color import Py5Color  # noqa
from .decorators import (
    _context_wrapper,
    _convert_hex_color,
    _hex_converter,
    _return_color,
    _text_fix_str,
)
from .font import Py5Font, _load_py5font, _return_list_str, _return_py5font  # noqa
from .graphics import Py5Graphics, _return_py5graphics  # noqa
from .image import Py5Image, _return_py5image  # noqa
from .keyevent import Py5KeyEvent, _convert_jchar_to_chr, _convert_jint_to_int  # noqa
from .mixins import DataMixin, MathMixin, PixelMixin, PrintlnStream, ThreadsMixin
from .mixins.threads import Py5Promise  # noqa
from .mouseevent import Py5MouseEvent  # noqa
from .pmath import _get_matrix_wrapper  # noqa
from .shader import Py5Shader, _load_py5shader, _return_py5shader  # noqa
from .shape import Py5Shape, _load_py5shape, _return_py5shape  # noqa
from .surface import Py5Surface, _return_py5surface  # noqa
from .utilities import Py5Utilities

try:
    import matplotlib as mpl
    import matplotlib.colors as mcolors
    from matplotlib.colors import Colormap
except:
    mpl = None
    mcolors = None
    Colormap = "matplotlib.colors.Colormap"

sketch_class_members_code = None  # DELETE

_Sketch = jpype.JClass("py5.core.Sketch")
_SketchBase = jpype.JClass("py5.core.SketchBase")


try:
    # be aware that __IPYTHON__ and get_ipython() are inserted into the user namespace late in the kernel startup process
    __IPYTHON__  # type: ignore
    # type: ignore
    if (
        sys.platform == "darwin"
        and (_ipython_shell := get_ipython()).active_eventloop != "osx"
    ):
        print(
            "Importing py5 on macOS but the necessary Jupyter macOS event loop has not been activated. I'll activate it for you, but next time, execute `%gui osx` before importing this library."
        )
        _ipython_shell.run_line_magic("gui", "osx")
except Exception:
    pass


_PY5_LAST_WINDOW_X = None
_PY5_LAST_WINDOW_Y = None


def _deprecated_g(f):
    @functools.wraps(f)
    def decorated(self_, *args):
        warnings.warn(
            "Accessing the primary Py5Graphics object with `g` is deprecated. Please use `get_graphics()` instead.",
            category=DeprecationWarning,
            stacklevel=3 if py5_tools.imported.get_imported_mode() else 4,
        )
        return f(self_, *args)

    return decorated


def _auto_convert_to_py5image(argnum):
    def _decorator(f):
        @functools.wraps(f)
        def decorated(self_, *args):
            if len(args) > argnum:
                args = list(args)
                img = args[argnum]
                if isinstance(img, image_conversion.NumpyImageArray):
                    args[argnum] = self_.create_image_from_numpy(img.array, img.bands)
                elif not isinstance(
                    img, (Py5Image, Py5Graphics)
                ) and image_conversion._convertable(img):
                    args[argnum] = self_.convert_image(img)
            return f(self_, *args)

        return decorated

    return _decorator


def _auto_convert_to_py5shape(f):
    @functools.wraps(f)
    def decorated(self_, *args):
        if len(args) >= 1:
            args = list(args)
            shape = args[0]
            if not isinstance(shape, Py5Shape) and shape_conversion._convertable(shape):
                args[0] = self_.convert_shape(shape)
        return f(self_, *args)

    return decorated


def _generator_to_list(f):
    @functools.wraps(f)
    def decorated(self_, *args):
        if isinstance(args[0], types.GeneratorType):
            args = list(args[0]), *args[1:]
        return f(self_, *args)

    return decorated


def _settings_only(name):
    def _decorator(f):
        @functools.wraps(f)
        def decorated(self_, *args):
            if self_._py5_bridge.current_running_method == "settings":
                return f(self_, *args)
            else:
                raise RuntimeError(
                    "Cannot call the "
                    + name
                    + "() method here. Either move it to a settings() function or move it to closer to the start of setup()."
                )

        return decorated

    return _decorator


class Sketch(MathMixin, DataMixin, ThreadsMixin, PixelMixin, PrintlnStream, Py5Base):
    """$classdoc_Sketch"""

    _py5_object_cache = set()
    _cls = _Sketch

    def __new__(cls, *args, **kwargs):
        _instance = kwargs.get("_instance")

        # remove dead or malformed Sketch instances from the object cache
        cls._py5_object_cache = set(
            s
            for s in cls._py5_object_cache
            if hasattr(s, "_instance") and not s.is_dead
        )
        if _instance:
            for s in cls._py5_object_cache:
                if _instance == s._instance:
                    return s
            else:
                raise RuntimeError(
                    "Failed to locate cached Sketch class for provided py5.core.Sketch instance"
                )
        else:
            s = object.__new__(cls)
            cls._py5_object_cache.add(s)
            return s

    def __init__(self, *args, **kwargs):
        _instance = kwargs.get("_instance")
        jclassname = kwargs.get("jclassname")
        jclass_params = kwargs.get("jclass_params", ())

        if _instance:
            if _instance == getattr(self, "_instance", None):
                # this is a cached Sketch object, don't re-run __init__()
                return
            else:
                raise RuntimeError(
                    "Unexpected Situation: Passed py5.core.Sketch instance does not match existing py5.core.Sketch instance. What is going on?"
                )

        Sketch._cls = JClass(jclassname) if jclassname else _Sketch
        instance = Sketch._cls(*jclass_params)
        if not isinstance(instance, _SketchBase):
            raise RuntimeError("Java instance must inherit from py5.core.SketchBase")

        super().__init__(instance=instance)
        self._methods_to_profile = []
        self._pre_hooks_to_add = []
        self._post_hooks_to_add = []
        # must always keep the _py5_bridge reference count from hitting zero.
        # otherwise, it will be garbage collected and lead to segmentation faults!
        self._py5_bridge = None
        self._environ = None
        iconPath = Path(__file__).parent.parent / "py5_tools/resources/logo-64x64.png"
        if iconPath.exists() and hasattr(self._instance, "setPy5IconPath"):
            self._instance.setPy5IconPath(str(iconPath))
        elif hasattr(sys, "_MEIPASS"):
            warnings.warn(
                "py5 logo image cannot be found. You are running this Sketch with pyinstaller and the image is missing from the packaging. I'm going to nag you about this until you fix it.",
                stacklevel=3,
            )
        Sketch._cls.setJOGLProperties(str(Path(__file__).parent))
        self.utils = Py5Utilities(self)
        self._sync_draw = None

        self._py5_convert_image_cache = dict()
        self._py5_convert_shape_cache = dict()
        self._cmap = None
        self._cmap_range = 0
        self._cmap_alpha_range = 0

    def __str__(self):
        return (
            f"Sketch(width="
            + str(self._get_width())
            + ", height="
            + str(self._get_height())
            + ", renderer="
            + str(self._instance.getRendererName())
            + ")"
        )

    def __repr__(self):
        return self.__str__()

    def __getattr__(self, name):
        raise AttributeError(spelling.error_msg("Sketch", name, self))

    def run_sketch(
        self,
        block: bool = None,
        *,
        py5_options: list = None,
        sketch_args: list = None,
        _osx_alt_run_method: bool = True,
    ) -> None:
        """$class_Sketch_run_sketch"""
        if not hasattr(self, "_instance"):
            raise RuntimeError(
                (
                    "py5 internal problem: did you create a class with an `__init__()` "
                    "method without a call to `super().__init__()`?"
                )
            )

        methods, method_param_counts = _extract_py5_user_function_data(
            dict(
                [
                    (e, getattr(self, e))
                    for e in reference.METHODS.keys()
                    if hasattr(self, e)
                ]
            )
        )

        caller_locals = inspect.stack()[1].frame.f_locals
        caller_globals = inspect.stack()[1].frame.f_globals

        self._run_sketch(
            methods,
            method_param_counts,
            block,
            py5_options=py5_options,
            sketch_args=sketch_args,
            _caller_locals=caller_locals,
            _caller_globals=caller_globals,
            _osx_alt_run_method=_osx_alt_run_method,
        )

    def _run_sketch(
        self,
        methods: dict[str, Callable],
        method_param_counts: dict[str, int],
        block: bool,
        *,
        py5_options: list[str] = None,
        sketch_args: list[str] = None,
        _caller_locals: dict[str, Any] = None,
        _caller_globals: dict[str, Any] = None,
        _osx_alt_run_method: bool = True,
    ) -> None:
        self._environ = _environ.Environment()
        self.set_println_stream(
            _DisplayPubPrintlnStream()
            if self._environ.in_jupyter_zmq_shell
            else _DefaultPrintlnStream()
        )

        self._py5_bridge = Py5Bridge(self)
        self._py5_bridge.set_caller_locals_globals(_caller_locals, _caller_globals)
        self._py5_bridge.add_functions(methods, method_param_counts)
        self._py5_bridge.profile_functions(self._methods_to_profile)
        self._py5_bridge.add_pre_hooks(self._pre_hooks_to_add)
        self._py5_bridge.add_post_hooks(self._post_hooks_to_add)
        self._instance.buildPy5Bridge(
            self._py5_bridge,
            self._environ.in_ipython_session,
            self._environ.in_jupyter_zmq_shell,
        )

        if not py5_options:
            py5_options = []
        if not sketch_args:
            sketch_args = []
        if not any([a.startswith("--sketch-path") for a in py5_options]):
            py5_options.append("--sketch-path=" + os.getcwd())
        if (
            not any([a.startswith("--location") for a in py5_options])
            and _PY5_LAST_WINDOW_X is not None
            and _PY5_LAST_WINDOW_Y is not None
        ):
            py5_options.append(
                "--location=" + str(_PY5_LAST_WINDOW_X) + "," + str(_PY5_LAST_WINDOW_Y)
            )
        args = py5_options + [""] + sketch_args

        try:
            if _osx_alt_run_method and platform.system() == "Darwin":
                from PyObjCTools import AppHelper  # type: ignore

                def run():
                    Sketch._cls.runSketch(args, self._instance)
                    if not self._environ.in_ipython_session:
                        while not self.is_dead:
                            time.sleep(0.05)
                        if self.is_dead_from_error:
                            surface = self.get_surface()
                            while not surface.is_stopped():
                                time.sleep(0.05)
                        AppHelper.stopEventLoop()

                if block == False and not self._environ.in_ipython_session:
                    self.println(
                        "On macOS, blocking is mandatory when Sketch is not run through Jupyter. This applies to all renderers.",
                        stderr=True,
                    )

                proxy = jpype.JProxy("java.lang.Runnable", dict(run=run))
                jpype.JClass("java.lang.Thread")(proxy).start()
                if not self._environ.in_ipython_session:
                    AppHelper.runConsoleEventLoop()
            else:
                Sketch._cls.runSketch(args, self._instance)
        except Exception as e:
            self.println(
                "Java exception thrown by Sketch.runSketch:\n" + str(e), stderr=True
            )

        if platform.system() == "Darwin" and self._environ.in_ipython_session and block:
            if (renderer := self._instance.getRendererName()) in [
                "JAVA2D",
                "P2D",
                "P3D",
                "FX2D",
            ]:
                self.println(
                    "On macOS, blocking is not allowed when Sketch using the",
                    renderer,
                    "renderer is run though Jupyter.",
                    stderr=True,
                )
                block = False

        if block or (block is None and not self._environ.in_ipython_session):
            # wait for the sketch to finish
            surface = self.get_surface()
            if surface._instance is not None:
                while not surface.is_stopped() and not hasattr(
                    self, "_shutdown_initiated"
                ):
                    time.sleep(0.25)

            # Wait no more than 1 second for any shutdown tasks to complete.
            # This will not wait for the user's `exiting` method, as it has
            # already been called. It will not wait for any threads to exit, as
            # that code calls `stop_all_threads(wait=False)` in its shutdown
            # procedure. Bottom line, this currently doesn't do very much but
            # might if a mixin had more complex shutdown steps.
            time_waited = 0
            while time_waited < 1.0 and not hasattr(self, "_shutdown_complete"):
                pause = 0.01
                time_waited += pause
                time.sleep(pause)

    def _shutdown(self):
        global _PY5_LAST_WINDOW_X
        global _PY5_LAST_WINDOW_Y
        if (
            hasattr(self._instance, "lastWindowX")
            and hasattr(self._instance, "lastWindowY")
            and self._instance.lastWindowX is not None
            and self._instance.lastWindowY is not None
        ):
            _PY5_LAST_WINDOW_X = int(self._instance.lastWindowX)
            _PY5_LAST_WINDOW_Y = int(self._instance.lastWindowY)
        super()._shutdown()

    def _terminate_sketch(self):
        self._instance.noLoop()
        self._shutdown_initiated = True
        self._shutdown()

    def _add_pre_hook(self, method_name, hook_name, function):
        if self._py5_bridge is None:
            self._pre_hooks_to_add.append((method_name, hook_name, function))
        else:
            self._py5_bridge.add_pre_hook(method_name, hook_name, function)

    def _remove_pre_hook(self, method_name, hook_name):
        if self._py5_bridge is None:
            self._pre_hooks_to_add = [
                x
                for x in self._pre_hooks_to_add
                if x[0] != method_name and x[1] != hook_name
            ]
        else:
            self._py5_bridge.remove_pre_hook(method_name, hook_name)

    def _add_post_hook(self, method_name, hook_name, function):
        if self._py5_bridge is None:
            self._post_hooks_to_add.append((method_name, hook_name, function))
        else:
            self._py5_bridge.add_post_hook(method_name, hook_name, function)

    def _remove_post_hook(self, method_name, hook_name):
        if self._py5_bridge is None:
            self._post_hooks_to_add = [
                x
                for x in self._post_hooks_to_add
                if x[0] != method_name and x[1] != hook_name
            ]
        else:
            self._py5_bridge.remove_post_hook(method_name, hook_name)

    # *** BEGIN METHODS ***

    PI = np.pi  # CODEBUILDER INCLUDE
    HALF_PI = np.pi / 2  # CODEBUILDER INCLUDE
    THIRD_PI = np.pi / 3  # CODEBUILDER INCLUDE
    QUARTER_PI = np.pi / 4  # CODEBUILDER INCLUDE
    TWO_PI = 2 * np.pi  # CODEBUILDER INCLUDE
    TAU = 2 * np.pi  # CODEBUILDER INCLUDE
    RAD_TO_DEG = 180 / np.pi  # CODEBUILDER INCLUDE
    DEG_TO_RAD = np.pi / 180  # CODEBUILDER INCLUDE
    CMAP = 6  # CODEBUILDER INCLUDE

    @overload
    def sketch_path(self) -> Path:
        """$class_Sketch_sketch_path"""
        pass

    @overload
    def sketch_path(self, where: str, /) -> Path:
        """$class_Sketch_sketch_path"""
        pass

    def sketch_path(self, *args) -> Path:
        """$class_Sketch_sketch_path"""
        if not self.is_running:
            msg = (
                "Calling method sketch_path() when Sketch is not running. "
                + "The returned value will not be correct on all platforms. Consider "
                + "calling this after setup() or perhaps using the Python standard "
                + "library methods os.getcwd() or pathlib.Path.cwd()."
            )
            warnings.warn(msg)
        if len(args) <= 1:
            return Path(str(self._instance.sketchPath(*args)))
        else:
            # this exception will be replaced with a more informative one by the custom exception handler
            raise TypeError("The parameters are invalid for method sketch_path()")

    def _get_is_ready(self) -> bool:  # @decorator
        """$class_Sketch_is_ready"""
        surface = self.get_surface()
        # if there is no surface yet, the sketch can be run.
        return surface._instance is None

    is_ready: bool = property(fget=_get_is_ready, doc="""$class_Sketch_is_ready""")

    def _get_is_running(self) -> bool:  # @decorator
        """$class_Sketch_is_running"""
        surface = self.get_surface()
        if surface._instance is None:
            # Sketch has not been run yet
            return False
        else:
            return not surface.is_stopped() and not hasattr(self, "_shutdown_initiated")

    is_running: bool = property(
        fget=_get_is_running, doc="""$class_Sketch_is_running"""
    )

    def _get_is_dead(self) -> bool:  # @decorator
        """$class_Sketch_is_dead"""
        surface = self.get_surface()
        if surface._instance is None:
            # Sketch has not been run yet
            return False
        return surface.is_stopped() or hasattr(self, "_shutdown_initiated")

    is_dead: bool = property(fget=_get_is_dead, doc="""$class_Sketch_is_dead""")

    def _get_is_dead_from_error(self) -> bool:  # @decorator
        """$class_Sketch_is_dead_from_error"""
        return self.is_dead and not self._instance.getSuccess()

    is_dead_from_error: bool = property(
        fget=_get_is_dead_from_error, doc="""$class_Sketch_is_dead_from_error"""
    )

    def _get_is_mouse_pressed(self) -> bool:  # @decorator
        """$class_Sketch_is_mouse_pressed"""
        return self._instance.isMousePressed()

    is_mouse_pressed: bool = property(
        fget=_get_is_mouse_pressed, doc="""$class_Sketch_is_mouse_pressed"""
    )

    def _get_is_key_pressed(self) -> bool:  # @decorator
        """$class_Sketch_is_key_pressed"""
        return self._instance.isKeyPressed()

    is_key_pressed: bool = property(
        fget=_get_is_key_pressed, doc="""$class_Sketch_is_key_pressed"""
    )

    def hot_reload_draw(self, draw: Callable) -> None:
        """$class_Sketch_hot_reload_draw"""
        methods, method_param_counts = _extract_py5_user_function_data(dict(draw=draw))
        if "draw" in methods:
            self._py5_bridge.add_functions(methods, method_param_counts)
        else:
            self.println("The new draw() function must take no parameters")

    def profile_functions(self, function_names: list[str]) -> None:
        """$class_Sketch_profile_functions"""
        if self._py5_bridge is None:
            self._methods_to_profile.extend(function_names)
        else:
            self._py5_bridge.profile_functions(function_names)

    def profile_draw(self) -> None:
        """$class_Sketch_profile_draw"""
        self.profile_functions(["draw"])

    def print_line_profiler_stats(self) -> None:
        """$class_Sketch_print_line_profiler_stats"""
        self._py5_bridge.dump_stats()

    def _insert_frame(self, what, num=None):
        """Utility function to insert a number into a filename.

        This is just like PApplet's insertFrame method except it allows you to
        override the frameCount with something else.
        """
        if num is None:
            num = self._instance.frameCount
        first = what.find("#")
        last = len(what) - what[::-1].find("#")
        if first != -1 and last - first > 1:
            count = last - first
            numstr = str(num)
            numprefix = "0" * (count - len(numstr))
            what = what[:first] + numprefix + numstr + what[last:]
        return what

    def save_frame(
        self,
        filename: Union[str, Path, BytesIO],
        *,
        format: str = None,
        drop_alpha: bool = True,
        use_thread: bool = False,
        **params,
    ) -> None:
        """$class_Sketch_save_frame"""
        if not isinstance(filename, BytesIO):
            filename = self._insert_frame(str(filename))
        self.save(
            filename,
            format=format,
            drop_alpha=drop_alpha,
            use_thread=use_thread,
            **params,
        )

    def select_folder(
        self, prompt: str, callback: Callable, default_folder: str = None
    ) -> None:
        """$class_Sketch_select_folder"""
        if (
            not isinstance(prompt, str)
            or not callable(callback)
            or (default_folder is not None and not isinstance(default_folder, str))
        ):
            raise TypeError(
                "This method's signature is select_folder(prompt: str, callback: Callable, default_folder: str)"
            )
        self._generic_select(
            self._instance.py5SelectFolder,
            "select_folder",
            prompt,
            callback,
            default_folder,
        )

    def select_input(
        self, prompt: str, callback: Callable, default_file: str = None
    ) -> None:
        """$class_Sketch_select_folder"""
        if (
            not isinstance(prompt, str)
            or not callable(callback)
            or (default_file is not None and not isinstance(default_file, str))
        ):
            raise TypeError(
                "This method's signature is select_input(prompt: str, callback: Callable, default_file: str)"
            )
        self._generic_select(
            self._instance.py5SelectInput,
            "select_input",
            prompt,
            callback,
            default_file,
        )

    def select_output(
        self, prompt: str, callback: Callable, default_file: str = None
    ) -> None:
        """$class_Sketch_select_folder"""
        if (
            not isinstance(prompt, str)
            or not callable(callback)
            or (default_file is not None and not isinstance(default_file, str))
        ):
            raise TypeError(
                "This method's signature is select_output(prompt: str, callback: Callable, default_file: str)"
            )
        self._generic_select(
            self._instance.py5SelectOutput,
            "select_output",
            prompt,
            callback,
            default_file,
        )

    def _generic_select(
        self,
        py5f: Callable,
        name: str,
        prompt: str,
        callback: Callable,
        default_folder: str = None,
    ) -> None:
        callback_sig = inspect.signature(callback)
        if (
            len(callback_sig.parameters) != 1
            or list(callback_sig.parameters.values())[0].kind
            == inspect.Parameter.KEYWORD_ONLY
        ):
            raise RuntimeError(
                "The callback function must have one and only one positional argument"
            )

        key = "_PY5_SELECT_CALLBACK_" + str(uuid.uuid4())

        def wrapped_callback_py5_no_prune(selection):
            return callback(selection if selection is None else Path(selection))

        py5_tools.config.register_processing_mode_key(
            key, wrapped_callback_py5_no_prune, callback_once=True
        )

        if platform.system() == "Darwin":
            if self._environ.in_ipython_session:
                raise RuntimeError(
                    "Sorry, py5's "
                    + name
                    + "() method doesn't work on macOS when the Sketch is run through Jupyter. However, there are some IPython widgets you can use instead."
                )
            else:

                def _run():
                    py5f(key, prompt, default_folder)

                proxy = jpype.JProxy("java.lang.Runnable", dict(run=_run))
                jpype.JClass("java.lang.Thread")(proxy).start()
        else:
            py5f(key, prompt, default_folder)

    def _set_sync_draw(self, sync_draw):
        self._sync_draw = sync_draw

    def _get_sync_draw(self):
        return self._sync_draw

    # *** Py5Image methods ***

    def create_image_from_numpy(
        self, array: npt.NDArray[np.uint8], bands: str = "ARGB", *, dst: Py5Image = None
    ) -> Py5Image:
        """$class_Sketch_create_image_from_numpy"""
        height, width = array.shape[:2]

        if dst:
            if width != dst.pixel_width or height != dst.pixel_height:
                raise RuntimeError("array size does not match size of dst Py5Image")
            py5_img = dst
        else:
            py5_img = self.create_image(width, height, self.ARGB)

        py5_img.set_np_pixels(array, bands)

        return py5_img

    def convert_image(
        self, obj: Any, *, dst: Py5Image = None, **kwargs: dict[str, Any]
    ) -> Py5Image:
        """$class_Sketch_convert_image"""
        if isinstance(obj, (Py5Image, Py5Graphics)):
            return obj
        result = image_conversion._convert(self, obj, **kwargs)
        if isinstance(result, (Path, str)):
            return self.load_image(result, dst=dst)
        elif isinstance(result, image_conversion.NumpyImageArray):
            return self.create_image_from_numpy(result.array, result.bands, dst=dst)
        else:
            # could be Py5Image or something comparable
            return result

    def convert_cached_image(
        self, obj: Any, force_conversion: bool = False, **kwargs: dict[str, Any]
    ) -> Py5Image:
        """$class_Sketch_convert_cached_image"""
        try:
            obj_in_cache = obj in self._py5_convert_image_cache
            hashable = True
        except TypeError:
            obj_in_cache = False
            hashable = False
            warnings.warn(
                "cannot cache convert image results for unhashable "
                + str(obj.__class__.__module__)
                + "."
                + str(obj.__class__.__name__)
                + " object"
            )

        if obj_in_cache and not force_conversion:
            return self._py5_convert_image_cache[obj]
        else:
            converted_obj = self.convert_image(obj, **kwargs)

            if hashable:
                self._py5_convert_image_cache[obj] = converted_obj

            return converted_obj

    def convert_shape(self, obj: Any, **kwargs: dict[str, Any]) -> Py5Shape:
        """$class_Sketch_convert_shape"""
        if isinstance(obj, Py5Shape):
            return obj
        return shape_conversion._convert(self, obj, **kwargs)

    def convert_cached_shape(
        self, obj: Any, force_conversion: bool = False, **kwargs: dict[str, Any]
    ) -> Py5Shape:
        """$class_Sketch_convert_cached_shape"""
        try:
            obj_in_cache = obj in self._py5_convert_shape_cache
            hashable = True
        except TypeError:
            obj_in_cache = False
            hashable = False
            warnings.warn(
                "cannot cache convert shape results for unhashable "
                + str(obj.__class__.__module__)
                + "."
                + str(obj.__class__.__name__)
                + " object"
            )

        if obj_in_cache and not force_conversion:
            return self._py5_convert_shape_cache[obj]
        else:
            converted_obj = self.convert_shape(obj, **kwargs)

            if hashable:
                self._py5_convert_shape_cache[obj] = converted_obj

            return converted_obj

    def load_image(
        self, image_path: Union[str, Path], *, dst: Py5Image = None
    ) -> Py5Image:
        """$class_Sketch_load_image"""
        try:
            pimg = self._instance.loadImage(str(image_path))
        except JException as e:
            msg = "cannot load image file " + str(image_path)
            if e.message() == "None":
                msg += ". error message: either the file cannot be found or the file does not contain valid image data."
            else:
                msg += ". error message: " + e.message()
        else:
            if pimg and pimg.width > 0:
                if dst:
                    if (
                        pimg.pixel_width != dst.pixel_width
                        or pimg.pixel_height != dst.pixel_height
                    ):
                        raise RuntimeError(
                            "size of loaded image does not match size of dst Py5Image"
                        )
                    dst._replace_instance(pimg)
                    return dst
                else:
                    return Py5Image(pimg)
            else:
                raise RuntimeError(
                    "cannot load image file "
                    + str(image_path)
                    + ". error message: either the file cannot be found or the file does not contain valid image data."
                )
        raise RuntimeError(msg)

    def request_image(self, image_path: Union[str, Path]) -> Py5Promise:
        """$class_Sketch_request_image"""
        return self.launch_promise_thread(self.load_image, args=(image_path,))

    @overload
    def color_mode(self, mode: int, /) -> None:
        """$class_Sketch_color_mode"""
        pass

    @overload
    def color_mode(self, mode: int, max1: float, max2: float, max3: float, /) -> None:
        """$class_Sketch_color_mode"""
        pass

    @overload
    def color_mode(
        self, mode: int, max1: float, max2: float, max3: float, max_a: float, /
    ) -> None:
        """$class_Sketch_color_mode"""
        pass

    @overload
    def color_mode(self, mode: int, max: float, /) -> None:
        """$class_Sketch_color_mode"""
        pass

    @overload
    def color_mode(self, colormap_mode: int, color_map: str, /) -> None:
        """$class_Sketch_color_mode"""
        pass

    @overload
    def color_mode(self, colormap_mode: int, color_map_instance: Colormap, /) -> None:
        """$class_Sketch_color_mode"""
        pass

    @overload
    def color_mode(self, colormap_mode: int, color_map: str, max_map: float, /) -> None:
        """$class_Sketch_color_mode"""
        pass

    @overload
    def color_mode(
        self, colormap_mode: int, color_map_instance: Colormap, max_map: float, /
    ) -> None:
        """$class_Sketch_color_mode"""
        pass

    @overload
    def color_mode(
        self, colormap_mode: int, color_map: str, max_map: float, max_a: float, /
    ) -> None:
        """$class_Sketch_color_mode"""
        pass

    @overload
    def color_mode(
        self,
        colormap_mode: int,
        color_map_instance: Colormap,
        max_map: float,
        max_a: float,
        /,
    ) -> None:
        """$class_Sketch_color_mode"""
        pass

    def color_mode(self, mode: int, *args) -> None:
        """$class_Sketch_color_mode"""
        # don't allow users to call this before the Sketch starts running
        if not self.is_running:
            raise RuntimeError(
                "color_mode() cannot be called for a Sketch that is not running."
            )

        if mode == self.CMAP:
            if mpl is None:
                raise RuntimeError(
                    "matplotlib must be installed to use CMAP color mode"
                )
            args = list(args)
            if len(args) == 0:
                raise TypeError(
                    "When using the CMAP color mode, the second parameter must be an instance of matplotlib.colors.Colormap or a string representing a matplotlib colormap name"
                )
            if isinstance(args[0], str):
                if args[0] in mpl.colormaps:
                    args[0] = mpl.colormaps[args[0]]
                else:
                    raise RuntimeError(
                        "provided colormap name not available in matplotlib"
                    )
            elif not isinstance(args[0], mpl.colors.Colormap):
                raise RuntimeError(
                    "provided colormap is not an instance of mpl.colors.Colormap"
                )

            if len(args) == 1:
                self._cmap = args[0]
                self._cmap_range = 1.0
                self._cmap_alpha_range = 255
            elif len(args) == 2:
                self._cmap = args[0]
                self._cmap_range = args[1]
                self._cmap_alpha_range = 255
            elif len(args) == 3:
                self._cmap = args[0]
                self._cmap_range = args[1]
                self._cmap_alpha_range = args[2]
            else:
                raise TypeError(
                    "When using the CMAP color mode, the arguments must be one of color_mode(CMAP, cmap), color_mode(CMAP, cmap, range), or color_mode(CMAP, cmap, range, alpha_range)"
                )

            self._instance.colorMode(self.RGB, 255, 255, 255, self._cmap_alpha_range)
        else:
            self._cmap = None
            self._cmap_range = 0
            self._cmap_alpha_range = 0
            self._instance.colorMode(mode, *args)

    @overload
    def color(self, fgray: float, /) -> int:
        """$class_Sketch_color"""
        pass

    @overload
    def color(self, fgray: float, falpha: float, /) -> int:
        """$class_Sketch_color"""
        pass

    @overload
    def color(self, gray: int, /) -> int:
        """$class_Sketch_color"""
        pass

    @overload
    def color(self, gray: int, alpha: int, /) -> int:
        """$class_Sketch_color"""
        pass

    @overload
    def color(self, v1: float, v2: float, v3: float, /) -> int:
        """$class_Sketch_color"""
        pass

    @overload
    def color(self, v1: float, v2: float, v3: float, alpha: float, /) -> int:
        """$class_Sketch_color"""
        pass

    @overload
    def color(self, v1: int, v2: int, v3: int, /) -> int:
        """$class_Sketch_color"""
        pass

    @overload
    def color(self, v1: int, v2: int, v3: int, alpha: int, /) -> int:
        """$class_Sketch_color"""
        pass

    @overload
    def color(self, cmap_input: float, /) -> int:
        """$class_Sketch_color"""
        pass

    @overload
    def color(self, cmap_input: float, alpha: int, /) -> int:
        """$class_Sketch_color"""
        pass

    @overload
    def color(self, hex_code: str, /) -> int:
        """$class_Sketch_color"""
        pass

    @overload
    def color(self, hex_code: str, alpha: int, /) -> int:
        """$class_Sketch_color"""
        pass

    def color(self, *args) -> int:
        """$class_Sketch_color"""
        args = list(args)

        if not isinstance(args[0], Py5Color):
            if self._cmap is not None and isinstance(
                args[0], (int, np.integer, float, np.floating)
            ):
                new_arg = JInt(
                    int(
                        "0xFF"
                        + mcolors.to_hex(self._cmap(args[0] / self._cmap_range))[1:],
                        base=16,
                    )
                )
                args[0] = Py5Color(new_arg, _creator_instance=self)

            elif (new_arg := _hex_converter(args[0])) is not None:
                args[0] = Py5Color(new_arg, _creator_instance=self)

            if len(args) == 1 and isinstance(args[0], Py5Color):
                return args[0]

        if self.is_running:
            return Py5Color(self._instance.color(*args), _creator_instance=self)
        else:
            if not hasattr(self, "_dummy_pgraphics"):
                self._dummy_pgraphics = JClass("processing.core.PGraphics")()
                self._dummy_pgraphics.colorMode(self.RGB, 255, 255, 255, 255)

            return Py5Color(self._dummy_pgraphics.color(*args), _creator_instance=self)


{sketch_class_members_code}
