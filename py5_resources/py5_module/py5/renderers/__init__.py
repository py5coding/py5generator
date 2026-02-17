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
import importlib.metadata
import sys

for entry_point in importlib.metadata.entry_points(group="py5_renderer"):
    try:
        # load renderer library
        renderer_library = entry_point.load()

        # create alias name and inject it into sys.modules
        alias_name = __name__ + "." + entry_point.name
        sys.modules[alias_name] = renderer_library

        # add renderer library to this modules's namespace
        setattr(sys.modules[__name__], entry_point.name, renderer_library)
    except Exception as e:
        print(
            "Error loading py5 renderer from entry point "
            + entry_point.name
            + ": "
            + str(e),
            file=sys.stderr,
        )
