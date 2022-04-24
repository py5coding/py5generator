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
# *** FORMAT PARAMS ***
from __future__ import annotations

import functools

from jpype.types import JChar

py5keyevent_class_members_code = None  # DELETE
py5mouseevent_class_members_code = None  # DELETE


def _convert_jchar_to_chr(f):
    @functools.wraps(f)
    def decorated(self_, *args):
        result = f(self_, *args)
        if isinstance(result, JChar):
            result = chr(result)
        return result
    return decorated

class Py5KeyEvent:
    """$classdoc_Py5KeyEvent
    """

    def __init__(self, pkeyevent):
        self._instance = pkeyevent


{py5keyevent_class_members_code}


class Py5MouseEvent:
    """$classdoc_Py5MouseEvent
    """

    def __init__(self, pmouseevent):
        self._instance = pmouseevent


{py5mouseevent_class_members_code}
