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
import inspect

from .. import environ

######################################################################
# JUPYTER NOTEBOOK LIVE CODING
######################################################################

post_execute_callback = None


class PostExecuteCallback:
    def __init__(self, sync_draw, sketch):
        self.sync_draw = sync_draw
        self.sketch = sketch

    def new_sketch(self, sync_draw, sketch):
        self.sync_draw = sync_draw
        self.sketch = sketch

    def __call__(self):
        self.sync_draw.keep_functions_current_from_globals(self.sketch)


def activate(
    *,
    always_rerun_setup: bool = True,
    always_on_top: bool = True,
    activate_keyboard_shortcuts: bool = False,
    archive_dir: str = "archive",
):
    """$module_Py5Tools_live_coding_activate"""
    global post_execute_callback

    import py5

    from .syncing import LIVE_CODING_GLOBALS, SyncDraw

    if not environ.Environment().in_ipython_session:
        raise RuntimeError("activate() must be called from an IPython session")

    caller_globals = inspect.stack()[1].frame.f_globals

    try:
        sync_draw = SyncDraw(
            LIVE_CODING_GLOBALS,
            global_namespace=caller_globals,
            always_rerun_setup=always_rerun_setup,
            always_on_top=always_on_top,
            activate_keyboard_shortcuts=activate_keyboard_shortcuts,
            # both default to False
            # show_framerate=False,
            # watch_dir=False,
            archive_dir=archive_dir,
        )

        sketch = py5.get_current_sketch()

        if sketch.is_running:
            if sketch._get_sync_draw() is None:
                msg = "activate() cannot be called while the current Sketch is running"
            else:
                msg = "activate() has already been called and activated"
            raise RuntimeError(msg)
        if not sketch.is_ready:
            py5.reset_py5()
            sketch = py5.get_current_sketch()

        sync_draw._init_hooks(sketch)

        # setup callback to keep functions synced after cell execution
        if post_execute_callback is None:
            post_execute_callback = PostExecuteCallback(sync_draw, sketch)

            from IPython import get_ipython

            # https://ipython.readthedocs.io/en/stable/config/callbacks.html
            get_ipython().events.register("post_execute", post_execute_callback)
        else:
            post_execute_callback.new_sketch(sync_draw, sketch)

        if sync_draw.keep_functions_current_from_globals(sketch):
            py5.run_sketch(sketch_functions=sync_draw.functions)
        else:
            sketch.println("Error in live coding startup...please fix and try again")

    except Exception as e:
        print(e)
