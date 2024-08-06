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
import sys
import zipfile
from pathlib import Path

import py5
import stackprinter

from ..hooks import frame_hooks

"""
TODO: py5_tools.live_coding doesn't work outside of live_sketch
TODO: this might need to move from py5_tools to py5 because it must import py5?

TODO: use sys.modules dict and importlib.reload to manage imported modules and reload if necessary?
but wait, is there a way to "reset" the global namespace to start fresh? maybe, the generic python interpreter has only a few things in globals() on startup
this would make shre __name__ is correct, among other things, would take care of the import stuff by default

TODO: should work in jupyter notebook, and maybe the py5 kernel also

https://ipython.readthedocs.io/en/stable/config/callbacks.html

from IPython import get_ipython
kernel = get_ipython()
kernel.events.register('post_execute', callback) # or 'post_run_cell'
"""

STARTUP_CODE = """
__name__ = "__main__"
__doc__ = None
__package__ = None
__spec__ = None
__annotations__ = dict()
__file__ = "{0}"
__cached__ = None
"""


def is_subdirectory(d, f):
    d = Path(d).resolve()
    f = Path(f).resolve()
    return f.parts[: len(d.parts)] == d.parts


class MockRunSketch:

    def __init__(self):
        self.kwargs = {}

    def __call__(self, *args, **kwargs):
        if "sketch_functions" in kwargs:
            kwargs.pop("sketch_functions")

        self.kwargs = kwargs


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

            # watch code for changes that will fix the problem and let Sketch continue
            if not self.sketch.has_thread("keep_functions_current"):
                self.sketch.launch_repeating_thread(
                    self.sketch._get_sync_draw().keep_functions_current,
                    "keep_functions_current",
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
    # this clears out any previously defined functions from the global namespace
    for method_name in py5.reference.METHODS:
        globals().pop(method_name, None)

    # execute user code and put new functions into the global namespace
    with open(filename, "r") as f:
        exec(compile(f.read(), filename=filename, mode="exec"), globals())

    functions, function_param_counts = py5.bridge._extract_py5_user_function_data(
        globals()
    )
    functions = (
        py5._split_setup.transform(
            functions, globals(), globals(), sketch.println, mode="module"
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
        filename,
        *,
        always_rerun_setup=False,
        always_on_top=True,
        show_framerate=False,
        watch_dir=None,
        archive_dir=None,
    ):
        self.filename = Path(filename)
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
        self.user_supplied_draw = False
        self.user_setup_code = None
        self.run_setup_again = False

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

        self.keep_functions_current(s)

    def pre_key_typed_hook(self, s: py5.Sketch):
        if s.key == "R":
            self.run_setup_again = True
        if s.key in "AS":
            screenshot_filename = self.take_screenshot(s)
            s.println(f"Screenshot saved to {screenshot_filename}")
        if s.key in "AB":
            archive_filename = self.archive_code()
            s.println(f"Code archived to {archive_filename}")

    def take_screenshot(self, s: py5.Sketch = None, *, screenshot_name: str = None):
        if screenshot_name is None:
            datestr = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_name = f"screenshot_{datestr}.png"

        self.archive_dir.mkdir(exist_ok=True)
        screenshot_filename = self.archive_dir / screenshot_name

        if not screenshot_filename.suffix:
            screenshot_filename = screenshot_filename.with_suffix(".png")

        if s is None:
            screenshot = frame_hooks.screenshot()
            screenshot.save(screenshot_filename)
        else:
            s.save_frame(screenshot_filename)

        return screenshot_filename

    def archive_code(self, *, archive_name: str = None):
        if archive_name is None:
            datestr = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
            archive_name = Path(self.filename).stem + "_" + datestr + ".py"

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

        return archive_filename

    def keep_functions_current(self, s: py5.Sketch, first_call=False):
        try:
            if self.mtime != (new_mtime := self.getmtime(self.filename)) or first_call:
                self.mtime = new_mtime

                self.functions, function_param_counts, self.user_supplied_draw = (
                    exec_user_code(s, self.filename)
                )
                self.exec_code_count += 1

                new_user_setup_code = (
                    inspect.getsource(self.functions["setup"].f)
                    if "setup" in self.functions
                    else None
                )

                if first_call:
                    self.user_setup_code = new_user_setup_code
                else:
                    s._py5_bridge.set_functions(self.functions, function_param_counts)
                    s._instance.buildPy5Bridge(
                        s._py5_bridge,
                        s._environ.in_ipython_session,
                        s._environ.in_jupyter_zmq_shell,
                    )

                    if (
                        self.always_rerun_setup
                        or self.user_setup_code != new_user_setup_code
                    ):
                        self.run_setup_again = True

                    self.user_setup_code = new_user_setup_code

                if UserFunctionWrapper.exception_state:
                    s.println("Resuming Sketch execution...")
                    UserFunctionWrapper.exception_state = False
                    s.loop()

                    if s.has_thread("keep_functions_current"):
                        s.stop_thread("keep_functions_current")

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
            if not s.has_thread("keep_functions_current"):
                s.launch_repeating_thread(
                    self.keep_functions_current,
                    "keep_functions_current",
                    time_delay=0.01,
                    args=(s,),
                )

            return False


def launch_live_coding(
    filename,
    *,
    always_rerun_setup=False,
    always_on_top=True,
    show_framerate=False,
    watch_dir=False,
    archive_dir=None,
):
    try:
        exec(STARTUP_CODE.format(Path(filename).absolute()), globals())

        # this needs to be before keep_functions_current() is called
        _real_run_sketch = py5.run_sketch
        py5.run_sketch = (_mock_run_sketch := MockRunSketch())

        sync_draw = SyncDraw(
            filename,
            always_rerun_setup=always_rerun_setup,
            always_on_top=always_on_top,
            show_framerate=show_framerate,
            watch_dir=watch_dir,
            archive_dir=archive_dir,
        )

        sketch = py5.get_current_sketch()

        sketch._set_sync_draw(sync_draw)

        sketch._add_pre_hook("setup", "sync_pre_setup", sync_draw.pre_setup_hook)
        sketch._add_pre_hook("draw", "sync_pre_draw", sync_draw.pre_draw_hook)
        sketch._add_pre_hook(
            "key_typed", "sync_pre_key_typed", sync_draw.pre_key_typed_hook
        )
        sketch._add_post_hook("setup", "sync_post_setup", sync_draw.post_setup_hook)
        sketch._add_post_hook("draw", "sync_post_draw", sync_draw.post_draw_hook)

        if sync_draw.keep_functions_current(sketch, first_call=True):
            _real_run_sketch(
                sketch_functions=sync_draw.functions, **_mock_run_sketch.kwargs
            )
        else:
            sketch.println("Error in live coding startup...please fix and try again")

    except Exception as e:
        print(e)
