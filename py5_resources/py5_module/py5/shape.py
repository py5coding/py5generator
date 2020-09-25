# -*- coding: utf-8 -*-
# *** FORMAT PARAMS ***
from __future__ import annotations

import functools
from pathlib import Path
from typing import overload, List  # noqa
from nptyping import NDArray, Float  # noqa

from jpype import JException

from .pmath import _get_pvector_wrapper  # noqa


py5shape_class_members_code = None  # DELETE


def _return_list_py5shapes(f):
    @functools.wraps(f)
    def decorated(self_, *args):
        return [Py5Shape(s) for s in f(self_, *args)]
    return decorated


def _return_py5shape(f):
    @functools.wraps(f)
    def decorated(self_, *args):
        return Py5Shape(f(self_, *args))
    return decorated


def _load_py5shape(f):
    @functools.wraps(f)
    def decorated(self_, *args):
        filename = args[0]
        # TODO: this should be in a reusable function
        if isinstance(filename, str):
            filename = Path(filename)
        if not isinstance(filename, Path):
            raise RuntimeError('filename parameter must be string or Path object')
        # TODO: if it is just a filename it might be in the data directory
        # TODO: what about relative paths?
        if not filename.exists():
            raise RuntimeError('filename ' + str(filename) + ' cannot be found')
        try:
            return Py5Shape(f(self_, *args))
        except JException as e:
            msg = e.message()
        raise RuntimeError('cannot load shape ' + str(args[0]) + '. error message: ' + msg)
    return decorated


class Py5Shape:

    def __init__(self, pshape):
        self._instance = pshape


{py5shape_class_members_code}
