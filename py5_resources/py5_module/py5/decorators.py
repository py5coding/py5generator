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
import functools
import re

import numpy as np
from jpype.types import JInt, JString

try:
    import colour
except ImportError:
    colour = None

try:
    import matplotlib as mpl
    import matplotlib.colors as mcolors
except ImportError:
    mpl = None
    mcolors = None

from .color import Py5Color

HEX_3DIGIT_COLOR_REGEX = re.compile(r"#[0-9A-F]{3}" + chr(36))
HEX_4DIGIT_COLOR_REGEX = re.compile(r"#[0-9A-F]{4}" + chr(36))
HEX_6DIGIT_COLOR_REGEX = re.compile(r"#[0-9A-F]{6}" + chr(36))
HEX_8DIGIT_COLOR_REGEX = re.compile(r"#[0-9A-F]{8}" + chr(36))


def _text_fix_str(f):
    @functools.wraps(f)
    def decorated(self_, *args):
        if isinstance(args[0], str):
            args = [JString(args[0]), *args[1:]]
        elif isinstance(args[0], int):
            args = [JInt(args[0]), *args[1:]]
        return f(self_, *args)

    return decorated


def _ret_str(f):
    @functools.wraps(f)
    def decorated(self_, *args):
        result = f(self_, *args)
        return str(result) if isinstance(result, JString) else result

    return decorated


def _hex_converter(arg):
    if isinstance(arg, str):
        if arg.startswith("#"):
            if HEX_3DIGIT_COLOR_REGEX.match(arg.upper()):
                return JInt(int("0xFF" + "".join([c + c for c in arg[1:]]), base=16))
            elif HEX_4DIGIT_COLOR_REGEX.match(arg.upper()):
                return JInt(
                    int(
                        "0x" + "".join([arg[i] + arg[i] for i in [4, 1, 2, 3]]), base=16
                    )
                )
            elif HEX_6DIGIT_COLOR_REGEX.match(arg.upper()):
                return JInt(int("0xFF" + arg[1:], base=16))
            elif HEX_8DIGIT_COLOR_REGEX.match(arg.upper()):
                return JInt(int("0x" + arg[7:] + arg[1:7], base=16))
        else:
            try:
                if mcolors is not None:
                    return JInt(int("0xFF" + mcolors.to_hex(arg)[1:], base=16))
            except:
                return None
    elif isinstance(arg, (int, np.integer)) and 0x7FFFFFFF < arg <= 0xFFFFFFFF:
        return JInt(arg)
    elif colour is not None and isinstance(arg, colour.Color):
        return JInt(int("0xFF" + arg.hex_l[1:], base=16))

    return None


def _matplotlib_cmap_converter(cmap, cmap_range, arg):
    return JInt(int("0xFF" + mcolors.to_hex(cmap(arg / cmap_range))[1:], base=16))


# both of the following two decorators should be named something else but they
# are all over the place and it would be a pain to change them now.


def _convert_hex_color(indices=[0]):
    def _hex_color(f):
        @functools.wraps(f)
        def decorated(self_, *args):
            args = list(args)
            for i, arg in [(i, args[i]) for i in indices if i < len(args)]:
                if (
                    hasattr(self_, "_cmap")
                    and self_._cmap is not None
                    and isinstance(args[i], (int, np.integer, float, np.floating))
                    and not isinstance(args[i], Py5Color)
                ):
                    args[i] = _matplotlib_cmap_converter(
                        self_._cmap, self_._cmap_range, args[i]
                    )
                elif (new_arg := _hex_converter(arg)) is not None:
                    args[i] = new_arg
            return f(self_, *args)

        return decorated

    return _hex_color


def _convert_hex_color2(f):
    @functools.wraps(f)
    def decorated(self_, *args):
        args = list(args)
        if (
            hasattr(self_, "_cmap")
            and self_._cmap is not None
            and isinstance(args[0], (int, np.integer, float, np.floating))
            and not isinstance(args[0], Py5Color)
        ):
            args[0] = _matplotlib_cmap_converter(
                self_._cmap, self_._cmap_range, args[0]
            )
        elif len(args) == 1 and (new_arg := _hex_converter(args[0])):
            args[0] = new_arg
        elif len(args) == 2 and (new_arg := _hex_converter(args[1])):
            args[1] = new_arg
        return f(self_, *args)

    return decorated


# TODO: this is a mess. since this is only used in two places, move this to
# Sketch and Py5Graphics and get rid of this decorator.
def _create_color():
    def _hex_color(f):
        @functools.wraps(f)
        def decorated(self_, *args):
            args = list(args)
            if (
                hasattr(self_, "_cmap")
                and self_._cmap is not None
                and not isinstance(args[0], Py5Color)
                and isinstance(args[0], (int, np.integer, float, np.floating))
            ):
                new_arg = _matplotlib_cmap_converter(
                    self_._cmap, self_._cmap_range, args[0]
                )
                if len(args) == 1:
                    return Py5Color(new_arg, _creator_instance=self_)
                elif (
                    len(args) == 2
                    and hasattr(self_, "is_running")
                    and not self_.is_running
                ):
                    alpha = int(
                        round(255 * np.clip(args[1] / self_._cmap_alpha_range, 0, 1))
                    )
                    return Py5Color(
                        (new_arg & 0x00FFFFFF) | ((alpha & 0xFF) << 24),
                        _creator_instance=self_,
                    )
                else:
                    args[0] = new_arg
            elif (
                not isinstance(args[0], Py5Color)
                and (new_arg := _hex_converter(args[0])) is not None
            ):
                # this decorator is only used for Sketch.color and
                # Py5Graphics.color.
                if len(args) == 1:
                    # therefore, if we get here, we have already created
                    # the color int value correctly and can just return
                    # that without a call to the Processing Java method.
                    # this also ensures the correct value is returned if
                    # this is called before the Sketch is started.
                    return Py5Color(new_arg, _creator_instance=self_)
                else:
                    args[0] = new_arg
            return Py5Color(f(self_, *args), _creator_instance=self_)

        return decorated

    return _hex_color


def _return_color(f):
    @functools.wraps(f)
    def decorated(self_, *args):
        return Py5Color(f(self_, *args), _creator_instance=self_)

    return decorated


class _Py5ContextManager:
    def __init__(self, exit_function, exit_args=()):
        self._exit_function = exit_function
        self._exit_args = exit_args

    def __enter__(self):
        pass

    def __exit__(self, *exc):
        self._exit_function(*self._exit_args)


def _context_wrapper(exit_function_name, exit_attr_args=()):
    def _decorator(f):
        @functools.wraps(f)
        def decorated(self_, *args):
            exit_args = tuple(getattr(self_, arg) for arg in exit_attr_args)
            exit_function = getattr(self_, exit_function_name)
            out = f(self_, *args)
            if out is None:
                return _Py5ContextManager(exit_function, exit_args=exit_args)
            elif hasattr(out, "_activate_context_manager"):
                out._activate_context_manager(exit_function, exit_args)
            return out

        return decorated

    return _decorator
