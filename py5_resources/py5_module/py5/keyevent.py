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
# *** FORMAT PARAMS ***
from __future__ import annotations

import functools
import weakref

from jpype.types import JInt, JChar

from . import spelling

py5keyevent_class_members_code = None  # DELETE


def _convert_jchar_to_chr(f):
    @functools.wraps(f)
    def decorated(self_, *args):
        result = f(self_, *args)
        if isinstance(result, JChar):
            result = chr(result)
        return result
    return decorated


def _convert_jint_to_int(f):
    @functools.wraps(f)
    def decorated(self_, *args):
        result = f(self_, *args)
        if isinstance(result, JInt):
            result = int(result)
        return result
    return decorated


class Py5KeyEvent:
    """$classdoc_Py5KeyEvent
    """
    _py5_object_cache = weakref.WeakSet()

    def __new__(cls, pkeyevent):
        for o in cls._py5_object_cache:
            if pkeyevent == o._instance:
                return o
        else:
            o = object.__new__(Py5KeyEvent)
            o._instance = pkeyevent
            cls._py5_object_cache.add(o)
            return o

    def __str__(self):
        key = self.get_key()
        action = self.get_action()

        action_str = 'UNKNOWN'
        for k, v in Py5KeyEvent.__dict__.items():
            if k == k.upper() and action == v:
                action_str = k
                break

        if key == '\uffff':  # py5.CODED
            key = 'CODED'

        return f"Py5KeyEvent(key=" + key + ", action=" + action_str + ")"

    def __repr__(self):
        return self.__str__()


    def __getattr__(self, name):
        raise AttributeError(spelling.error_msg('Py5KeyEvent', name, self))

{py5keyevent_class_members_code}
