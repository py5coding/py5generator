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
class LiveCodingController:

    def __init__(self):
        import py5

        self._sketch = py5.get_current_sketch()
        self._sync_draw = self._sketch._get_sync_draw()

    def screenshot(self, screenshot_name: str = None):
        if self._sketch.is_running and self._sync_draw is not None:
            self._sync_draw.take_screenshot(
                self._sketch, screenshot_name=screenshot_name
            )

    def archive_code(self, archive_name: str = None):
        if self._sketch.is_running and self._sync_draw is not None:
            self._sync_draw.archive_code(self._sketch, archive_name=archive_name)

    def backup(self, backup_name: str = None):
        self.screenshot(screenshot_name=backup_name)
        self.archive_code(archive_name=backup_name)

    def _get_exec_code_count(self):
        if self._sketch.is_running and self._sync_draw is not None:
            return self._sync_draw.exec_code_count
        else:
            return 0

    exec_code_count = property(_get_exec_code_count)


def get_controller():
    return LiveCodingController()
