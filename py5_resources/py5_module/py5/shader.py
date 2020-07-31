# -*- coding: utf-8 -*-
# *** FORMAT PARAMS ***
import functools
from typing import overload, List  # noqa

import numpy as np  # noqa

from .base import Py5Base
from .methods import Py5Exception  # noqa
from .image import Py5Image  # noqa
from jpype.types import JArray, JBoolean, JInt, JFloat  # noqa


py5shader_class_members_code = None  # DELETE


def _return_py5shader(f):
    @functools.wraps(f)
    def decorated(self_, *args):
        return Py5Shader(f(self_, *args))
    return decorated


class Py5Shader(Py5Base):

    def __init__(self, pshader):
        self._instance = pshader
        super().__init__(instance=pshader)


{py5shader_class_members_code}
