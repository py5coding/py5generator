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
import datetime as dt
import inspect
import os
import platform
import sys
import zipfile
from enum import Enum
from pathlib import Path

import py5
import stackprinter

"""
TODO: fix import problem, need a good way to let user call activate_live_coding()

maybe rename those methods also.

Can also improve this by organizing everything better and adding comments.

TODO: I want to be able to use this with ipython & save code in a file. Combination of both modes
"""


class LiveCodingMode(Enum):
    FILE = 1
    GLOBALS = 2


STARTUP_CODE = """
__name__ = "__main__"
__doc__ = None
__package__ = None
__spec__ = None
__annotations__ = dict()
__file__ = "{0}"
__cached__ = None
"""

# TODO: does this really have to be a global variable?
USER_NAMESPACE = dict()


def init_user_namespace(filename):
    USER_NAMESPACE.clear()
    exec(STARTUP_CODE.format(Path(filename).absolute()), USER_NAMESPACE)


def is_subdirectory(d, f):
    d = Path(d).resolve()
    f = Path(f).resolve()
    return f.parts[: len(d.parts)] == d.parts


class Py5RunSketchBlockException(Exception):
    pass


class MockRunSketch:

    def __init__(self):
        self._kwargs = {}
        self._called = False

    def __call__(self, *args, **kwargs):
        self._called = True
        if "sketch_functions" in kwargs:
            kwargs.pop("sketch_functions")

        self._kwargs = kwargs

        if platform.system() == "Darwin":
            kwargs["block"] = True

        self._functions, self._function_param_counts = (
            py5.bridge._extract_py5_user_function_data(USER_NAMESPACE)
        )

        if "block" not in kwargs or kwargs["block"]:
            raise Py5RunSketchBlockException("run_sketch() blocking")


class UserFunctionWrapper:
    exception_state = False

    def __new__(self, sketch: py5.Sketch, name, f, param_count):
        ufw = object.__new__(
            UserFunctionWrapperOneParam
            if param_count == 1
            else UserFunctionWrapperZeroParams
        )
        ufw.sketch = sketch
        ufw.name = name
        ufw.f = f
        return ufw

    def call_f(self, *args):
        try:
            if self.f is not None and not UserFunctionWrapper.exception_state:
                self.f(*args)
        except Exception as e:
            UserFunctionWrapper.exception_state = True
            self.sketch.no_loop()
            self.sketch.println("*" * 80)
            py5.bridge.handle_exception(self.sketch.println, *sys.exc_info())
            self.sketch.println("*" * 80)

            # if we are in file mode, watch code for changes that will fix the
            # problem if we aren't doing so already
            if (
                self.sketch._get_sync_draw().live_coding_mode == LiveCodingMode.FILE
                and not self.sketch.has_thread("keep_functions_current_from_file")
            ):
                self.sketch.launch_repeating_thread(
                    self.sketch._get_sync_draw().keep_functions_current_from_file,
                    "keep_functions_current_from_file",
                    time_delay=0.01,
                    args=(self.sketch,),
                )


class UserFunctionWrapperZeroParams(UserFunctionWrapper):
    def __call__(self):
        self.call_f()


class UserFunctionWrapperOneParam(UserFunctionWrapper):
    def __call__(self, arg):
        self.call_f(arg)


def exec_user_code(sketch, filename):
    init_user_namespace(filename)

    # execute user code and put new functions into the global namespace

    try:
        with open(filename, "r") as f:
            exec(compile(f.read(), filename=filename, mode="exec"), USER_NAMESPACE)
    except Py5RunSketchBlockException:
        # run_sketch() called, but it is a MockRunSketch instance
        functions, function_param_counts = (
            py5.run_sketch._functions,
            py5.run_sketch._function_param_counts,
        )
    else:
        # the user didn't call run_sketch() in their code. issue a warning later
        functions, function_param_counts = py5.bridge._extract_py5_user_function_data(
            USER_NAMESPACE
        )

    return process_user_functions(
        sketch, functions, function_param_counts, USER_NAMESPACE
    )


def retrieve_user_code(sketch, namespace):
    functions, function_param_counts = py5.bridge._extract_py5_user_function_data(
        namespace
    )

    return process_user_functions(sketch, functions, function_param_counts, namespace)


def process_user_functions(sketch, functions, function_param_counts, namespace):
    functions = (
        py5._split_setup.transform(
            functions, namespace, namespace, sketch.println, mode="module"
        )
        or {}
    )

    user_supplied_draw = "draw" in functions

    for fname in ["setup", "draw", "key_typed"]:
        if fname not in functions:
            functions[fname] = lambda: None
            function_param_counts[fname] = 0

    functions = {
        name: UserFunctionWrapper(sketch, name, f, function_param_counts.get(name, 0))
        for name, f in functions.items()
    }

    return functions, function_param_counts, user_supplied_draw


class SyncDraw:
    def __init__(
        self,
        *,
        filename=None,
        global_namespace=None,
        always_rerun_setup=False,
        always_on_top=True,
        show_framerate=False,
        watch_dir=None,
        archive_dir=None,
    ):
        if global_namespace is None:
            self.live_coding_mode = LiveCodingMode.FILE
            self.filename = Path(filename)
            self.global_namespace = None
        else:
            self.live_coding_mode = LiveCodingMode.GLOBALS
            self.filename = None
            self.global_namespace = global_namespace

        self.always_rerun_setup = always_rerun_setup
        self.always_on_top = always_on_top
        self.archive_dir = Path(archive_dir)
        self.show_framerate = show_framerate
        self.watch_dir = watch_dir

        if self.watch_dir:
            self.getmtime = lambda f: max(
                (
                    os.path.getmtime(ff)
                    for ff in f.parent.glob("**/*")
                    if ff.is_file() and not is_subdirectory(self.archive_dir, ff)
                ),
                default=0,
            )
        else:
            self.getmtime = os.path.getmtime

        self.exec_code_count = 0
        self.mtime = None
        self.capture_pixels = None
        self.functions = {}
        self.function_param_counts = {}
        self.user_supplied_draw = False
        self.user_setup_code = None
        self.run_setup_again = False

    def _init_hooks(self, s: py5.Sketch):
        s._set_sync_draw(self)

        s._add_pre_hook("setup", "sync_pre_setup", self.pre_setup_hook)
        s._add_pre_hook("draw", "sync_pre_draw", self.pre_draw_hook)
        s._add_pre_hook("key_typed", "sync_pre_key_typed", self.pre_key_typed_hook)
        s._add_post_hook("setup", "sync_post_setup", self.post_setup_hook)
        s._add_post_hook("draw", "sync_post_draw", self.post_draw_hook)

    def pre_setup_hook(self, s: py5.Sketch):
        if self.always_on_top:
            s.get_surface().set_always_on_top(True)

    def post_setup_hook(self, s: py5.Sketch):
        if self.always_on_top:
            self.capture_pixels = s.get_pixels()

    def pre_draw_hook(self, s: py5.Sketch):
        if self.run_setup_again:
            s._instance._resetSketch()
            # in case user doesn't call background in setup
            s.background(204)
            self.functions["setup"]()
            self.run_setup_again = False

        if self.capture_pixels is not None:
            s.set_pixels(0, 0, self.capture_pixels)
            self.capture_pixels = None

    def post_draw_hook(self, s: py5.Sketch):
        if (
            self.show_framerate
            and self.user_supplied_draw
            and not UserFunctionWrapper.exception_state
        ):
            msg = f"frame rate: {s.get_frame_rate():0.1f}"
            s.println(msg, end="\r")

        if self.live_coding_mode == LiveCodingMode.FILE:
            self.keep_functions_current_from_file(s)

    def pre_key_typed_hook(self, s: py5.Sketch):
        datestr = dt.datetime.now().strftime("%Y%m%d_%H%M%S")

        if s.key == "R":
            self.run_setup_again = True
        if s.key in "AS":
            self.take_screenshot(s, f"screenshot_{datestr}.png")
        if s.key in "AB":
            self.archive_code(s, f"{self.filename.stem}_{datestr}")

    def take_screenshot(self, s: py5.Sketch, screenshot_name: str):
        if UserFunctionWrapper.exception_state:
            s.println(f"Skipping screenshot due to error state")
            return

        self.archive_dir.mkdir(exist_ok=True)
        screenshot_filename = self.archive_dir / screenshot_name

        if not screenshot_filename.suffix:
            screenshot_filename = screenshot_filename.with_suffix(".png")

        s.save_frame(screenshot_filename)
        s.println(f"Screenshot saved to {screenshot_filename}")

    def archive_code(self, s: py5.Sketch, archive_name: str):
        # TODO: this should never be called in file mode
        if UserFunctionWrapper.exception_state:
            s.println(f"Skipping code archive due to error state")
            return

        self.archive_dir.mkdir(exist_ok=True)
        archive_filename = self.archive_dir / archive_name

        if self.watch_dir:
            archive_filename = archive_filename.with_suffix(".zip")
            with zipfile.ZipFile(archive_filename, "w", zipfile.ZIP_DEFLATED) as zf:
                for ff in self.filename.parent.glob("**/*"):
                    if ff.is_file() and not is_subdirectory(self.archive_dir, ff):
                        zf.write(ff, ff.relative_to(self.filename.parent))
        else:
            archive_filename = archive_filename.with_suffix(".py")
            with open(self.filename, "r") as f:
                with open(archive_filename, "w") as f2:
                    f2.write(f.read())

        s.println(f"Code archived to {archive_filename}")

    def keep_functions_current_from_globals(self, s: py5.Sketch, first_call=False):
        try:
            self.functions, self.function_param_counts, self.user_supplied_draw = (
                retrieve_user_code(s, self.global_namespace)
            )

            self._process_new_functions(
                s,
                first_call,
            )

            if UserFunctionWrapper.exception_state:
                s.println("Resuming Sketch execution...")
                UserFunctionWrapper.exception_state = False
                s.loop()

            return True

        except Exception as e:
            UserFunctionWrapper.exception_state = True
            exc_type, exc_value, exc_tb = sys.exc_info()
            exc_tb = exc_tb.tb_next.tb_next
            msg = "*" * 80 + "\n"
            msg += stackprinter.format(
                thing=(exc_type, exc_value, exc_tb),
                show_vals="line",
                style="plaintext",
                suppressed_paths=[
                    r"lib/python.*?/site-packages/numpy/",
                    r"lib/python.*?/site-packages/py5/",
                    r"lib/python.*?/site-packages/py5tools/",
                ],
            )
            msg += "\n" + "*" * 80
            s.println(msg)

            return False

    def keep_functions_current_from_file(self, s: py5.Sketch, first_call=False):
        try:
            if self.mtime != (new_mtime := self.getmtime(self.filename)) or first_call:
                self.mtime = new_mtime

                self.functions, self.function_param_counts, self.user_supplied_draw = (
                    exec_user_code(s, self.filename)
                )

                self._process_new_functions(
                    s,
                    first_call,
                )

                if UserFunctionWrapper.exception_state:
                    if s.has_thread("keep_functions_current_from_file"):
                        s.stop_thread("keep_functions_current_from_file")

                    s.println("Resuming Sketch execution...")
                    UserFunctionWrapper.exception_state = False
                    s.loop()

            return True

        except Exception as e:
            UserFunctionWrapper.exception_state = True
            exc_type, exc_value, exc_tb = sys.exc_info()
            exc_tb = exc_tb.tb_next.tb_next
            msg = "*" * 80 + "\n"
            msg += stackprinter.format(
                thing=(exc_type, exc_value, exc_tb),
                show_vals="line",
                style="plaintext",
                suppressed_paths=[
                    r"lib/python.*?/site-packages/numpy/",
                    r"lib/python.*?/site-packages/py5/",
                    r"lib/python.*?/site-packages/py5tools/",
                ],
            )
            msg += "\n" + "*" * 80
            s.println(msg)

            # watch code for changes that will fix the problem and let Sketch continue
            if not s.has_thread("keep_functions_current_from_file"):
                s.launch_repeating_thread(
                    self.keep_functions_current_from_file,
                    "keep_functions_current_from_file",
                    time_delay=0.01,
                    args=(s,),
                )

            return False

    def _process_new_functions(
        self,
        s: py5.Sketch,
        first_call=False,
    ):
        self.exec_code_count += 1

        new_user_setup_code = (
            inspect.getsource(self.functions["setup"].f)
            if "setup" in self.functions
            else None
        )

        # TODO: do I really need this first_call variable?
        if first_call:
            self.user_setup_code = new_user_setup_code
        else:
            s._py5_bridge.set_functions(self.functions, self.function_param_counts)
            s._instance.buildPy5Bridge(
                s._py5_bridge,
                s._environ.in_ipython_session,
                s._environ.in_jupyter_zmq_shell,
            )

            if self.always_rerun_setup or self.user_setup_code != new_user_setup_code:
                self.run_setup_again = True

            self.user_setup_code = new_user_setup_code


def activate_live_coding(
    always_rerun_setup=False,
    always_on_top=True,
    archive_dir="archive",
):
    caller_globals = inspect.stack()[1].frame.f_globals

    try:
        sync_draw = SyncDraw(
            global_namespace=caller_globals,
            always_rerun_setup=always_rerun_setup,
            always_on_top=always_on_top,
            show_framerate=False,
            watch_dir=False,
            archive_dir=archive_dir,
        )

        sketch = py5.get_current_sketch()
        sync_draw._init_hooks(sketch)

        # https://ipython.readthedocs.io/en/stable/config/callbacks.html
        def _callback(result):
            sync_draw.keep_functions_current_from_globals(sketch)

        # TODO: should actually check if this is IPython
        from IPython import get_ipython

        kernel = get_ipython()
        kernel.events.register("post_run_cell", _callback)

        if sync_draw.keep_functions_current_from_globals(sketch, first_call=True):
            py5.run_sketch(sketch_functions=sync_draw.functions)
        else:
            # TODO: could this ever happen?
            sketch.println("Error in live coding startup...please fix and try again")

    except Exception as e:
        print(e)


def launch_live_coding(
    filename,
    *,
    always_rerun_setup=False,
    always_on_top=True,
    show_framerate=False,
    watch_dir=False,
    archive_dir="archive",
):
    try:
        init_user_namespace(filename)

        # this needs to be before keep_functions_current_from_file() is called
        _real_run_sketch = py5.run_sketch
        py5.run_sketch = (_mock_run_sketch := MockRunSketch())

        sync_draw = SyncDraw(
            filename=filename,
            always_rerun_setup=always_rerun_setup,
            always_on_top=always_on_top,
            show_framerate=show_framerate,
            watch_dir=watch_dir,
            archive_dir=archive_dir,
        )

        sketch = py5.get_current_sketch()
        sync_draw._init_hooks(sketch)

        if sync_draw.keep_functions_current_from_file(sketch, first_call=True):
            if not _mock_run_sketch._called:
                sketch.println(
                    f"File {filename} has no call to py5's run_sketch() method. py5 will make the call for you, but please add it to the end of the file to avoid this message."
                )

            _real_run_sketch(
                sketch_functions=sync_draw.functions, **_mock_run_sketch._kwargs
            )
        else:
            sketch.println("Error in live coding startup...please fix and try again")

    except Exception as e:
        print(e)
