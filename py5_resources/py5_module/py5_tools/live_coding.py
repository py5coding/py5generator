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
from pathlib import Path

import py5 as _py5
import stackprinter

"""
TODO: bug on first run when there is only a setup function
TODO: ability to run-py5 Sketch code one and only one time per live coding session. this would be useful for loading models, etc
TODO: use overlay for frame rate and frame count
TODO: support user function for formatting filenames images and code copies are saved to?
TODO: insert controller to namespace that can interact with a live coding controller, include info like counter, number of saves, etc
TODO: use sys.modules dict and importlib.reload to manage imported modules and reload if necessary
TODO: should work in jupyter notebook, and maybe the py5 kernel also

https://ipython.readthedocs.io/en/stable/config/callbacks.html

from IPython import get_ipython
kernel = get_ipython()
kernel.events.register('post_execute', callback) # or 'post_run_cell'
"""


class MockRunSketch:

    def __init__(self):
        self.kwargs = {}

    def __call__(self, *args, **kwargs):
        if "sketch_functions" in kwargs:
            kwargs.pop("sketch_functions")

        self.kwargs = kwargs


class UserFunctionWrapper:
    exception_state = False

    def __new__(self, sketch: _py5.Sketch, name, f, param_count):
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
            _py5.bridge.handle_exception(self.sketch.println, *sys.exc_info())
            self.sketch.println("*" * 80)


class UserFunctionWrapperZeroParams(UserFunctionWrapper):
    def __call__(self):
        self.call_f()


class UserFunctionWrapperOneParam(UserFunctionWrapper):
    def __call__(self, arg):
        self.call_f(arg)


def exec_user_code(sketch, filename):
    for method_name in _py5.reference.METHODS:
        globals().pop(method_name, None)

    with open(filename, "r") as f:

        exec(compile(f.read(), filename=filename, mode="exec"), globals())

    functions, function_param_counts = _py5.bridge._extract_py5_user_function_data(
        globals()
    )
    functions = (
        _py5._split_setup.transform(
            functions, globals(), globals(), sketch.println, mode="module"
        )
        or {}
    )

    for fname in ["settings", "draw", "key_typed"]:
        if fname not in functions:
            functions[fname] = lambda: None
            function_param_counts[fname] = 0

    functions = {
        name: UserFunctionWrapper(sketch, name, f, function_param_counts.get(name, 0))
        for name, f in functions.items()
    }

    if UserFunctionWrapper.exception_state:
        UserFunctionWrapper.exception_state = False
        sketch.loop()

    return functions, function_param_counts


class SyncDraw:
    def __init__(
        self,
        filename,
        *,
        always_rerun_setup=False,
        always_on_top=True,
        screenshot_dir=None,
        code_backup_dir=None,
        watch_dir=None,
    ):
        self.filename = Path(filename)
        self.always_rerun_setup = always_rerun_setup
        self.always_on_top = always_on_top
        self.screenshot_dir = Path(screenshot_dir) if screenshot_dir else Path(".")
        self.code_backup_dir = Path(code_backup_dir) if code_backup_dir else Path(".")

        if watch_dir:
            self.getmtime = lambda f: max(
                (os.path.getmtime(ff) for ff in f.parent.glob("**/*") if ff.is_file()),
                default=0,
            )
        else:
            self.getmtime = os.path.getmtime

        self.screenshot_dir.mkdir(exist_ok=True)
        self.code_backup_dir.mkdir(exist_ok=True)

        self.mtime = None
        self.functions = {}
        self.user_supplied_draw = False
        self.user_setup_code = None
        self.run_setup_again = False

    def pre_setup_hook(self, s: _py5.Sketch):
        if self.always_on_top:
            s.get_surface().set_always_on_top(True)

    def pre_draw_hook(self, s: _py5.Sketch):
        if self.run_setup_again:
            # in case user doesn't call background in setup
            s.background(204)

            if "setup" in self.functions:
                self.functions["setup"]()
            self.run_setup_again = False

    def pre_key_typed_hook(self, s: _py5.Sketch):
        if s.key == "R":
            self.run_setup_again = True
        elif s.key in "ABS":
            datestr = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
            if s.key in "AS":
                s.save_frame(self.screenshot_dir / f"screenshot_{datestr}.png")
            if s.key in "AB":
                new_filename = Path(self.filename).stem + "_" + datestr + ".py"
                with open(self.filename, "r") as f:
                    with open(self.code_backup_dir / new_filename, "w") as f2:
                        f2.write(f.read())

    def keep_functions_current(self, s: _py5.Sketch, first_call=False):
        try:
            if self.mtime != (new_mtime := self.getmtime(self.filename)) or first_call:
                self.mtime = new_mtime

                self.functions, function_param_counts = exec_user_code(s, self.filename)

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


def launch_live_coding(
    filename,
    *,
    always_rerun_setup=False,
    always_on_top=True,
    screenshot_dir=None,
    code_backup_dir=None,
    watch_dir=False,
):
    if _py5.is_dead:
        _py5.reset_py5()

    try:
        # this needs to be before keep_functions_current() is called
        _real_run_sketch = _py5.run_sketch
        _py5.run_sketch = (_mock_run_sketch := MockRunSketch())

        sync_draw = SyncDraw(
            filename,
            always_rerun_setup=always_rerun_setup,
            always_on_top=always_on_top,
            screenshot_dir=screenshot_dir,
            code_backup_dir=code_backup_dir,
            watch_dir=watch_dir,
        )

        sketch = _py5.get_current_sketch()
        sketch._add_pre_hook("setup", "sync_setup", sync_draw.pre_setup_hook)
        sketch._add_pre_hook("draw", "sync_draw", sync_draw.pre_draw_hook)
        sketch._add_pre_hook(
            "key_typed", "sync_key_typed", sync_draw.pre_key_typed_hook
        )

        if sync_draw.keep_functions_current(sketch, first_call=True):
            sketch.launch_repeating_thread(
                sync_draw.keep_functions_current,
                "keep_functions_current",
                time_delay=0.01,
                args=(sketch,),
            )

            _real_run_sketch(
                sketch_functions=sync_draw.functions, **_mock_run_sketch.kwargs
            )

        else:
            sketch.println("Error in live coding startup...please fix and try again")

    except Exception as e:
        print(e)
