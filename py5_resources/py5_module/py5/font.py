# -*- coding: utf-8 -*-
# *** FORMAT PARAMS ***
import functools
from typing import overload, List  # noqa

import jpype
from jpype import JException, JArray, JString  # noqa

from .shape import Py5Shape, _return_py5shape  # noqa


py5font_class_members_code = None  # DELETE


def _return_py5font(f):
    @functools.wraps(f)
    def decorated(self_, *args):
        return Py5Font(f(self_, *args))
    return decorated


def _load_py5font(f):
    @functools.wraps(f)
    def decorated(self_, *args):
        # TODO: for load_font this prints a Java exception to strerr if the file cannot be found or read
        try:
            ret = f(self_, *args)
        except JException as e:
            msg = e.message()
        else:
            if ret is None:
                msg = 'font file is missing or inaccessible.'
            else:
                return Py5Font(ret)
        raise RuntimeError('cannot load font file ' + str(args[0]) + '. error message: ' + msg)
    return decorated


def _return_list_str(f):
    @functools.wraps(f)
    def decorated(cls_, *args):
        return [str(x) for x in f(cls_, *args) or []]
    return decorated


class Py5Font:
    """$classdoc_Py5Font
    """

    _cls = jpype.JClass('processing.core.PFont')
    CHARSET = _cls.CHARSET

    def __init__(self, pfont):
        self._instance = pfont


{py5font_class_members_code}
