# *****************************************************************************
#
#   Part of the py5 library
#   Copyright (C) 2020-2023 Jim Schmitz
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
from __future__ import annotations

import sys
import tempfile
import time
from pathlib import Path
from typing import Callable, Iterable

import numpy as np
import numpy.typing as npt
import PIL
from jpype import JClass
from PIL.Image import Image as PIL_Image

from .. import environ as _environ
from .. import imported as _imported
from .hooks import (
    GrabFramesHook,
    QueuedBatchProcessingHook,
    SaveFramesHook,
    ScreenshotHook,
)

Sketch = "Sketch"


def screenshot(*, sketch: Sketch = None, hook_post_draw: bool = False) -> PIL_Image:
    """$module_Py5Tools_screenshot"""
    import py5

    if sketch is None:
        sketch = py5.get_current_sketch()
        using_current_sketch = True
    else:
        using_current_sketch = False

    if sketch.is_dead:
        msg = f'The {"current " if using_current_sketch else ""}Sketch is dead. The py5_tools.screenshot() function cannot be used on a Sketch in the dead state.'
        if using_current_sketch:
            msg += f' Call {"" if _imported.get_imported_mode() else "py5."}reset_py5() to reset py5 to the ready state.'
        raise RuntimeError(msg)

    if py5.bridge.check_run_method_callstack():
        msg = "Calling py5_tools.screenshot() from within a py5 user function is not allowed. Please move this code to outside the Sketch or consider using save_frame() instead."
        raise RuntimeError(msg)

    if sketch._py5_bridge.has_function("draw"):
        hook = ScreenshotHook()
        sketch._add_post_hook(
            "post_draw" if hook_post_draw else "draw", hook.hook_name, hook
        )

        while not hook.is_ready and not hook.is_terminated:
            time.sleep(0.005)
            if hook.is_ready:
                return PIL.Image.fromarray(hook.pixels, mode="RGB")
            elif hook.is_terminated and hook.exception:
                raise RuntimeError("error running magic: " + str(hook.exception))
    else:
        if isinstance(
            sketch.get_graphics()._instance, JClass("processing.opengl.PGraphicsOpenGL")
        ):
            msg = "The py5_tools.screenshot() function cannot be used on an OpenGL Sketch with no draw() function."
            raise RuntimeError(msg)
        else:
            sketch.load_np_pixels()
            return PIL.Image.fromarray(sketch.np_pixels[:, :, 1:], mode="RGB")


def save_frames(
    dirname: str,
    *,
    filename: str = "frame_####.png",
    period: float = 0.0,
    start: int = None,
    limit: int = 0,
    sketch: Sketch = None,
    hook_post_draw: bool = False,
    block: bool = False,
    display_progress: bool = True,
) -> None:
    """$module_Py5Tools_save_frames"""
    import py5

    if sketch is None:
        sketch = py5.get_current_sketch()
        using_current_sketch = True
    else:
        using_current_sketch = False

    if sketch.is_dead:
        msg = f'The {"current " if using_current_sketch else ""}Sketch is dead. The py5_tools.save_frames() function cannot be used on a Sketch in the dead state.'
        if using_current_sketch:
            msg += f' Call {"" if _imported.get_imported_mode() else "py5."}reset_py5() to reset py5 to the ready state.'
        raise RuntimeError(msg)

    if block and sys.platform == "darwin" and _environ.Environment().in_ipython_session:
        raise RuntimeError("Blocking is not allowed on OSX when run from IPython")

    if block and py5.bridge.check_run_method_callstack():
        msg = "Calling py5_tools.save_frames() from within a py5 user function with `block=True` is not allowed. Please move this code to outside the Sketch or set `block=False`."
        raise RuntimeError(msg)

    dirname = Path(dirname)
    if not dirname.exists():
        dirname.mkdir(parents=True)

    hook = SaveFramesHook(dirname, filename, period, start, limit, display_progress)
    sketch._add_post_hook(
        "post_draw" if hook_post_draw else "draw", hook.hook_name, hook
    )

    if block:
        while not hook.is_ready and not hook.is_terminated:
            time.sleep(0.1)


def offline_frame_processing(
    func: Callable[[npt.NDArray[np.uint8]], None],
    *,
    limit: int = 0,
    period: float = 0.0,
    batch_size: int = 1,
    complete_func: Callable[[], None] = None,
    stop_processing_func: Callable[[], bool] = None,
    sketch: Sketch = None,
    hook_post_draw: bool = False,
    queue_limit: int = None,
    block: bool = None,
) -> None:
    """$module_Py5Tools_offline_frame_processing"""
    import py5

    if sketch is None:
        sketch = py5.get_current_sketch()
        using_current_sketch = True
    else:
        using_current_sketch = False

    if sketch.is_dead:
        msg = f'The {"current " if using_current_sketch else ""}Sketch is dead. The py5_tools.offline_frame_processing() function cannot be used on a Sketch in the dead state.'
        if using_current_sketch:
            msg += f' Call {"" if _imported.get_imported_mode() else "py5."}reset_py5() to reset py5 to the ready state.'
        raise RuntimeError(msg)

    if block and py5.bridge.check_run_method_callstack():
        msg = "Calling py5_tools.offline_frame_processing() from within a py5 user function with `block=True` is not allowed. Please move this code to outside the Sketch or set `block=False`."
        raise RuntimeError(msg)

    hook = QueuedBatchProcessingHook(
        period,
        limit,
        batch_size,
        func,
        complete_func=complete_func,
        stop_processing_func=stop_processing_func,
        queue_limit=queue_limit,
    )
    sketch._add_post_hook(
        "post_draw" if hook_post_draw else "draw", hook.hook_name, hook
    )

    if block:
        while not hook.is_ready and not hook.is_terminated:
            time.sleep(0.1)


def animated_gif(
    filename: str,
    *,
    count: int = 0,
    period: float = 0.0,
    frame_numbers: Iterable = None,
    duration: float = 0.0,
    loop: int = 0,
    optimize: bool = True,
    sketch: Sketch = None,
    hook_post_draw: bool = False,
    block: bool = False,
) -> None:
    """$module_Py5Tools_animated_gif"""
    import py5

    if count > 0 and frame_numbers is None:
        # ok
        pass
    elif (
        count == 0 and frame_numbers is not None and isinstance(frame_numbers, Iterable)
    ):
        # ok, but check period is still 0.0
        if period != 0.0:
            raise RuntimeError(
                "Must not pass period parameter when using the frame_numbers parameter"
            )
    else:
        # not ok
        raise RuntimeError(
            "Must either pass count > 0 or pass frame_numbers an iterable, but not both"
        )

    if duration <= 0.0:
        raise RuntimeError(
            "Must pass a duration > 0.0 to specify the time delay between frames in the animated gif"
        )

    if sketch is None:
        sketch = py5.get_current_sketch()
        using_current_sketch = True
    else:
        using_current_sketch = False

    if sketch.is_dead:
        msg = f'The {"current " if using_current_sketch else ""}Sketch is dead. The py5_tools.animated_gif() function cannot be used on a Sketch in the dead state.'
        if using_current_sketch:
            msg += f' Call {"" if _imported.get_imported_mode() else "py5."}reset_py5() to reset py5 to the ready state.'
        raise RuntimeError(msg)

    if block and sys.platform == "darwin" and _environ.Environment().in_ipython_session:
        raise RuntimeError("Blocking is not allowed on OSX when run from IPython")

    if block and py5.bridge.check_run_method_callstack():
        msg = "Calling py5_tools.animated_gif() from within a py5 user function with `block=True` is not allowed. Please move this code to outside the Sketch or set `block=False`."
        raise RuntimeError(msg)

    filename = Path(filename)

    def complete_func(hook):
        if not filename.parent.exists():
            filename.parent.mkdir(parents=True)

        img1 = PIL.Image.fromarray(hook.frames[0], mode="RGB")
        imgs = [PIL.Image.fromarray(arr, mode="RGB") for arr in hook.frames[1:]]
        img1.save(
            filename,
            save_all=True,
            duration=1000 * duration,
            loop=loop,
            optimize=optimize,
            append_images=imgs,
        )

        hook.status_msg("animated gif written to " + str(filename))

    hook_setup = bool(frame_numbers and 0 in frame_numbers)
    hook = GrabFramesHook(
        frame_numbers, period, count, complete_func, hooked_setup=hook_setup
    )
    sketch._add_post_hook(
        "post_draw" if hook_post_draw else "draw", hook.hook_name, hook
    )
    if hook_setup:
        sketch._add_post_hook("setup", hook.hook_name, hook)

    if block:
        while not hook.is_ready and not hook.is_terminated:
            time.sleep(0.1)


def capture_frames(
    *,
    count: float = 0,
    period: float = 0.0,
    frame_numbers: Iterable = None,
    sketch: Sketch = None,
    hook_post_draw: bool = False,
    block: bool = False,
) -> list[PIL_Image]:
    """$module_Py5Tools_capture_frames"""
    import py5

    if count > 0 and frame_numbers is None:
        # ok
        pass
    elif (
        count == 0 and frame_numbers is not None and isinstance(frame_numbers, Iterable)
    ):
        # ok, but check period is still 0.0
        if period != 0.0:
            raise RuntimeError(
                "Must not pass period parameter when using the frame_numbers parameter"
            )
    else:
        # not ok
        raise RuntimeError(
            "Must either pass count > 0 or pass frame_numbers an iterable, but not both"
        )

    if sketch is None:
        sketch = py5.get_current_sketch()
        using_current_sketch = True
    else:
        using_current_sketch = False

    if sketch.is_dead:
        msg = f'The {"current " if using_current_sketch else ""}Sketch is dead. The py5_tools.capture_frames() function cannot be used on a Sketch in the dead state.'
        if using_current_sketch:
            msg += f' Call {"" if _imported.get_imported_mode() else "py5."}reset_py5() to reset py5 to the ready state.'
        raise RuntimeError(msg)

    if block and sys.platform == "darwin" and _environ.Environment().in_ipython_session:
        raise RuntimeError("Blocking is not allowed on OSX when run from IPython")

    if block and py5.bridge.check_run_method_callstack():
        msg = "Calling py5_tools.capture_frames() from within a py5 user function with `block=True` is not allowed. Please move this code to outside the Sketch or set `block=False`."
        raise RuntimeError(msg)

    results = []

    def complete_func(hook):
        results.extend([PIL.Image.fromarray(arr, mode="RGB") for arr in hook.frames])
        hook.status_msg(f"captured {len(hook.frames)} frames")

    hook_setup = bool(frame_numbers and 0 in frame_numbers)
    hook = GrabFramesHook(
        frame_numbers, period, count, complete_func, hooked_setup=hook_setup
    )
    sketch._add_post_hook(
        "post_draw" if hook_post_draw else "draw", hook.hook_name, hook
    )
    if hook_setup:
        sketch._add_post_hook("setup", hook.hook_name, hook)

    if block:
        while not hook.is_ready and not hook.is_terminated:
            time.sleep(0.1)

    return results


__all__ = [
    "screenshot",
    "save_frames",
    "offline_frame_processing",
    "animated_gif",
    "capture_frames",
]
