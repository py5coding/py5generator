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


def _get_sketch_and_sync_draw():
    import py5

    sketch = py5.get_current_sketch()
    sync_draw = sketch._get_sync_draw()

    return sketch, sync_draw


def screenshot(screenshot_name: str = None):
    """$module_Py5Tools_live_coding_screenshot"""
    sketch, sync_draw = _get_sketch_and_sync_draw()

    if sketch.is_running and sync_draw is not None:
        screenshot_name = screenshot_name or "screenshot_%Y%m%d_%H%M%S"
        screenshot_name = dt.datetime.now().strftime(screenshot_name)

        sync_draw.take_screenshot(sketch, screenshot_name)


def copy_code(copy_name: str = None):
    """$module_Py5Tools_live_coding_copy_code"""
    sketch, sync_draw = _get_sketch_and_sync_draw()

    if sketch.is_running and sync_draw is not None:
        copy_name = copy_name or "copy_%Y%m%d_%H%M%S"
        copy_name = dt.datetime.now().strftime(copy_name)

        sync_draw.copy_code(sketch, copy_name)


def snapshot(snapshot_name: str = None):
    """$module_Py5Tools_live_coding_snapshot"""
    sketch, sync_draw = _get_sketch_and_sync_draw()

    if sketch.is_running and sync_draw is not None:
        snapshot_name = snapshot_name or "snapshot_%Y%m%d_%H%M%S"
        snapshot_name = dt.datetime.now().strftime(snapshot_name)

        screenshot(screenshot_name=snapshot_name)
        copy_code(copy_name=snapshot_name)


def count() -> int:
    """$module_Py5Tools_live_coding_count"""
    sketch, sync_draw = _get_sketch_and_sync_draw()

    if sketch.is_running and sync_draw is not None:
        return sync_draw.update_count
    else:
        return 0
