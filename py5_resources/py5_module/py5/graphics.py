# -*- coding: utf-8 -*-
# *** FORMAT PARAMS ***
from __future__ import annotations

import functools
from typing import overload, List  # noqa

from .base import Py5Base
from .mixins import PixelMixin
from .methods import Py5Exception  # noqa
from .shader import _return_py5shader, _py5shader_param  # noqa
from .font import _py5font_param  # noqa
from .shape import _return_py5shape, _py5shape_param  # noqa

from .image import Py5Image, _return_py5image  # noqa
from .converter import Converter


py5graphics_class_members_code = None  # DELETE


def py5graphics_precondition(obj):
    return isinstance(obj, Py5Graphics)


def py5graphics_converter(py5graphics):
    return py5graphics._instance


Converter.register_pimage_conversion(py5graphics_precondition, py5graphics_converter)


def _return_py5graphics(f):
    @functools.wraps(f)
    def decorated(self_, *args):
        ret = f(self_, *args)
        if ret is not None:
            return Py5Graphics(ret)
    return decorated


def _py5graphics_param(f):
    @functools.wraps(f)
    def decorated(self_, *args):
        if isinstance(args[0], Py5Graphics):
            args = (args[0]._instance, *args[1:])
        return f(self_, *args)

    return decorated


class Py5Graphics(PixelMixin, Py5Base):

    def __init__(self, pgraphics):
        self._instance = pgraphics
        super().__init__(instance=pgraphics)


{py5graphics_class_members_code}
