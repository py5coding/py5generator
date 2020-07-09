import functools

from jnius import autoclass


class Py5Font:

    _PFont = autoclass('processing.core.PFont',
                       include_protected=False, include_private=False)

    def __init__(self, pfont):
        self._pfont = pfont

    @classmethod
    def list(cls):
        return cls._PFont.list()


def _return_py5font(f):
    @functools.wraps(f)
    def decorated(self_, *args):
        return Py5Font(f(self_, *args))

    return decorated


def _py5font_param(f):
    @functools.wraps(f)
    def decorated(self_, *args):
        if isinstance(args[0], Py5Font):
            args = (args[0]._pfont, *args[1:])
        return f(self_, *args)

    return decorated
