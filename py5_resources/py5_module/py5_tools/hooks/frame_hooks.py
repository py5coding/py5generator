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
import time
from pathlib import Path
import tempfile
from typing import NewType, List

import PIL
import PIL.ImageFile

from .hooks import ScreenshotHook, SaveFramesHook, GrabFramesHook


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
                sketch: Sketch = None, hook_post_draw: bool = False) -> List[str]:
    """$module_Py5Tools_save_frames"""
    if sketch is None:
        import py5
        sketch = py5.get_current_sketch()
        prefix = ' current'
    else:
        prefix = ''

    if not sketch.is_running:
        raise RuntimeError(f'The {prefix} sketch is not running.')

    dirname = Path(dirname)
    if not dirname.exists():
        dirname.mkdir(parents=True)

    hook = SaveFramesHook(dirname, filename, period, start, limit)
    sketch._add_post_hook('post_draw' if hook_post_draw else 'draw', hook.hook_name, hook)

    if limit:
        while not hook.is_ready and not hook.is_terminated:
            time.sleep(0.02)
            print(f'saving frame {len(hook.filenames)}/{limit}', end='\r')
        print(f'saving frame {len(hook.filenames)}/{limit}')

        if hook.is_ready:
            return hook.filenames

    if hook.is_terminated and hook.exception:
        raise RuntimeError('error running magic: ' + str(hook.exception))


def animated_gif(filename: str, count: int, period: float, duration: float, *,
                 loop: int = 0, optimize: bool = True, sketch: Sketch = None,
                 hook_post_draw: bool = False) -> str:
    """$module_Py5Tools_animated_gif"""
    if sketch is None:
        import py5
        sketch = py5.get_current_sketch()
        prefix = ' current'
    else:
        prefix = ''

    if not sketch.is_running:
        raise RuntimeError(f'The {prefix} sketch is not running.')

    filename = Path(filename)

    hook = GrabFramesHook(period, count)
    sketch._add_post_hook('post_draw' if hook_post_draw else 'draw', hook.hook_name, hook)

    while not hook.is_ready and not hook.is_terminated:
        time.sleep(0.05)
        print(f'collecting frame {len(hook.frames)}/{count}', end='\r')
    print(f'collecting frame {len(hook.frames)}/{count}')

    if hook.is_ready:
        if not filename.parent.exists():
            filename.parent.mkdir(parents=True)

        img1 = PIL.Image.fromarray(hook.frames[0], mode='RGB')
        imgs = [PIL.Image.fromarray(arr, mode='RGB') for arr in hook.frames[1:]]
        img1.save(filename, save_all=True, duration=1000 * duration,
                    loop=loop, optimize=optimize, append_images=imgs)

        return str(filename)

    elif hook.is_terminated and hook.exception:
        raise RuntimeError('error running magic: ' + str(hook.exception))


def capture_frames(count: float, *, period: float = 0.0, sketch: Sketch = None,
                   hook_post_draw: bool = False) -> List[PIL_ImageFile]:
    """$module_Py5Tools_capture_frames"""
    if sketch is None:
        import py5
        sketch = py5.get_current_sketch()
        prefix = ' current'
    else:
        prefix = ''

    if not sketch.is_running:
        raise RuntimeError(f'The {prefix} sketch is not running.')

    hook = GrabFramesHook(period, count)
    sketch._add_post_hook('post_draw' if hook_post_draw else 'draw', hook.hook_name, hook)

    while not hook.is_ready and not hook.is_terminated:
        time.sleep(0.05)
        print(f'collecting frame {len(hook.frames)}/{count}', end='\r')
    print(f'collecting frame {len(hook.frames)}/{count}')

    if hook.is_ready:
        return [PIL.Image.fromarray(arr, mode='RGB') for arr in hook.frames]
    elif hook.is_terminated and hook.exception:
        raise RuntimeError('error running magic: ' + str(hook.exception))
