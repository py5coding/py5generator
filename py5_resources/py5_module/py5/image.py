# -*- coding: utf-8 -*-
# *** FORMAT PARAMS ***
from __future__ import annotations

import functools
from typing import overload, List, Union  # noqa

from .base import Py5Base, _py5base_param  # noqa
from .mixins import PixelMixin
from .methods import Py5Exception  # noqa


py5image_class_members_code = None  # DELETE


def _return_py5image(f):
    @functools.wraps(f)
    def decorated(self_, *args):
        ret = f(self_, *args)
        if ret is not None:
            return Py5Image(ret)
    return decorated


def _py5image_param(argnum):
    def decorator(f):
        @functools.wraps(f)
        def decorated(self_, *args):
            # TODO: this is an ugly hack but will be removed when I use the jpype conversion functionality
            if isinstance(args[argnum], Py5Image) or hasattr(args[argnum], '_instance'):
                args = (*args[:argnum],
                        args[argnum]._instance,
                        *args[(argnum + 1):])
            return f(self_, *args)
        return decorated
    return decorator


class Py5Image(PixelMixin, Py5Base):

    def __init__(self, pimage):
        self._instance = pimage
        super().__init__(instance=pimage)


{py5image_class_members_code}
