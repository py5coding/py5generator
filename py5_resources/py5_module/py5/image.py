# -*- coding: utf-8 -*-
# *** FORMAT PARAMS ***
from __future__ import annotations

import functools
from typing import overload, List, Union  # noqa

from .base import Py5Base
from .mixins import PixelMixin


py5image_class_members_code = None  # DELETE


def _return_py5image(f):
    @functools.wraps(f)
    def decorated(self_, *args):
        ret = f(self_, *args)
        if ret is not None:
            return Py5Image(ret)
    return decorated


class Py5Image(PixelMixin, Py5Base):

    def __init__(self, pimage):
        self._instance = pimage
        super().__init__(instance=pimage)


{py5image_class_members_code}
