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
import sys
import time
from pathlib import Path
import tempfile
from typing import Callable, NewType, List, Any
from nptyping import NDArray, UInt8

import PIL
import PIL.ImageFile

from .hooks import ScreenshotHook, SaveFramesHook, GrabFramesHook, QueuedBatchProcessingHook
from .. import environ as _environ


Sketch = 'Sketch'
PIL_ImageFile = NewType('PIL_ImageFile', PIL.ImageFile.ImageFile)


def screenshot(*, sketch: Sketch = None, hook_post_draw: bool = False) -> PIL.ImageFile.ImageFile:
    """$module_Py5Tools_screenshot"""
    if sketch is None:
        import py5
        sketch = py5.get_current_sketch()
        prefix = ' current'
    else:
        prefix = ''

    if not sketch.is_running:
        raise RuntimeError(f'The {prefix} sketch is not running.')

    with tempfile.TemporaryDirectory() as tempdir:
        temp_png = Path(tempdir) / 'output.png'
        hook = ScreenshotHook(temp_png)
        sketch._add_post_hook('post_draw' if hook_post_draw else 'draw', hook.hook_name, hook)

        while not hook.is_ready and not hook.is_terminated:
            time.sleep(0.005)

        if hook.is_ready:
            return PIL.Image.open(temp_png)
        elif hook.is_terminated and hook.exception:
            raise RuntimeError('error running magic: ' + str(hook.exception))


def save_frames(dirname: str, *, filename: str = 'frame_####.png',
                period: float = 0.0, start: int = None, limit: int = 0,
                sketch: Sketch = None, hook_post_draw: bool = False,
                block: bool = False) -> None:
    """$module_Py5Tools_save_frames"""
    if sketch is None:
        import py5
        sketch = py5.get_current_sketch()
        prefix = ' current'
    else:
        prefix = ''

    if not sketch.is_running:
        raise RuntimeError(f'The {prefix} sketch is not running.')
    if block and sys.platform == 'darwin' and _environ.Environment().in_ipython_session:
        raise RuntimeError('blocking is not allowed on OSX')

    dirname = Path(dirname)
    if not dirname.exists():
        dirname.mkdir(parents=True)

    hook = SaveFramesHook(dirname, filename, period, start, limit)
    sketch._add_post_hook('post_draw' if hook_post_draw else 'draw', hook.hook_name, hook)

    if block:
        while not hook.is_ready and not hook.is_terminated:
            time.sleep(0.1)


def offline_frame_processing(func: Callable[[NDArray[(Any, Any, Any, 3), UInt8]], None], *, 
                             limit: int = 0, period: float = 0.0, batch_size: int = 1,
                             complete_func: Callable[[], None] = None,
                             stop_processing_func: Callable[[], bool] = None,
                             sketch: Sketch = None, hook_post_draw: bool = False,
                             queue_limit: int = None, block: bool = None) -> None:
    """$module_Py5Tools_offline_frame_processing"""
    if sketch is None:
        import py5
        sketch = py5.get_current_sketch()
        prefix = ' current'
    else:
        prefix = ''

    if not sketch.is_running:
        raise RuntimeError(f'The {prefix} sketch is not running.')

    hook = QueuedBatchProcessingHook(period, limit, batch_size, func,
                                     complete_func=complete_func,
                                     stop_processing_func=stop_processing_func,
                                     queue_limit=queue_limit)
    sketch._add_post_hook('post_draw' if hook_post_draw else 'draw', hook.hook_name, hook)

    if block:
        while not hook.is_ready and not hook.is_terminated:
            time.sleep(0.1)


def animated_gif(filename: str, count: int, period: float, duration: float, *,
                 loop: int = 0, optimize: bool = True, sketch: Sketch = None,
                 hook_post_draw: bool = False, block: bool = False) -> None:
    """$module_Py5Tools_animated_gif"""
    if sketch is None:
        import py5
        sketch = py5.get_current_sketch()
        prefix = ' current'
    else:
        prefix = ''

    if not sketch.is_running:
        raise RuntimeError(f'The {prefix} sketch is not running.')
    if block and sys.platform == 'darwin' and _environ.Environment().in_ipython_session:
        raise RuntimeError('blocking is not allowed on OSX')

    filename = Path(filename)

    def complete_func(hook):
        if not filename.parent.exists():
            filename.parent.mkdir(parents=True)

        img1 = PIL.Image.fromarray(hook.frames[0], mode='RGB')
        imgs = [PIL.Image.fromarray(arr, mode='RGB') for arr in hook.frames[1:]]
        img1.save(filename, save_all=True, duration=1000 * duration,
                    loop=loop, optimize=optimize, append_images=imgs)

        hook.status_msg('animated gif written to ' + str(filename))

    hook = GrabFramesHook(period, count, complete_func)
    sketch._add_post_hook('post_draw' if hook_post_draw else 'draw', hook.hook_name, hook)

    if block:
        while not hook.is_ready and not hook.is_terminated:
            time.sleep(0.1)


def capture_frames(count: float, *, period: float = 0.0, sketch: Sketch = None,
                   hook_post_draw: bool = False, block: bool = False) -> List[PIL_ImageFile]:
    """$module_Py5Tools_capture_frames"""
    if sketch is None:
        import py5
        sketch = py5.get_current_sketch()
        prefix = ' current'
    else:
        prefix = ''

    if not sketch.is_running:
        raise RuntimeError(f'The {prefix} sketch is not running.')
    if block and sys.platform == 'darwin' and _environ.Environment().in_ipython_session:
        raise RuntimeError('blocking is not allowed on OSX')

    results = []

    def complete_func(hook):
        results.extend([PIL.Image.fromarray(arr, mode='RGB') for arr in hook.frames])
        hook.status_msg(f'captured {count} frames')

    hook = GrabFramesHook(period, count, complete_func)
    sketch._add_post_hook('post_draw' if hook_post_draw else 'draw', hook.hook_name, hook)

    if block:
        while not hook.is_ready and not hook.is_terminated:
            time.sleep(0.1)

    return results


__all__ = ['screenshot', 'save_frames', 'offline_frame_processing', 'animated_gif', 'capture_frames']
