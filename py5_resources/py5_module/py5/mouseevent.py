# *****************************************************************************
#
#   Part of the py5 library
#   Copyright (C) 2020-2026 Jim Schmitz
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

import weakref

from . import spelling

py5mouseevent_class_members_code = None  # DELETE


class Py5MouseEvent:
    """$classdoc_Py5MouseEvent"""

    _py5_object_cache = weakref.WeakSet()

    def __new__(cls, pmouseevent):
        for o in cls._py5_object_cache:
            if pmouseevent == o._instance:
                return o
        else:
            o = object.__new__(Py5MouseEvent)
            o._instance = pmouseevent
            cls._py5_object_cache.add(o)
            return o

    def __str__(self):
        action = self.get_action()
        action_str = "UNKNOWN"
        for k, v in Py5MouseEvent.__dict__.items():
            if k == k.upper() and action == v:
                action_str = k
                break
        return (
            f"Py5MouseEvent(x="
            + str(self.get_x())
            + ", y="
            + str(self.get_y())
            + ", action="
            + action_str
            + ")"
        )

    def __repr__(self):
        return self.__str__()

    def __getattr__(self, name):
        raise AttributeError(spelling.error_msg("Py5MouseEvent", name, self))


{py5mouseevent_class_members_code}
