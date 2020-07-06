from typing import overload, List

from jnius import autoclass

from ..methods import Py5Exception


class Py5Font:

    _PFont = autoclass('processing.core.PFont',
                       include_protected=False, include_private=False)

    def __init__(self, pfont):
        self._pfont = pfont

    @classmethod
    def list(cls):
        return cls._PFont.list()


class FontMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # *** BEGIN METHODS ***

    @overload
    def create_font(self, name: str, size: float) -> Py5Font:
        """$class_create_font"""
        pass

    @overload
    def create_font(self, name: str, size: float, smooth: bool) -> Py5Font:
        """$class_create_font"""
        pass

    @overload
    def create_font(self, name: str, size: float, smooth: bool, charset: List[chr]) -> Py5Font:
        """$class_create_font"""
        pass

    def create_font(self, *args) -> Py5Font:
        """$class_create_font"""
        try:
            return Py5Font(self._py5applet.createFont(*args))
        except Exception as e:
            raise Py5Exception(
                e.__class__.__name__,
                str(e),
                'create_font',
                args)

    def load_font(self, filename: str) -> Py5Font:
        """$class_load_font"""
        try:
            return Py5Font(self._py5applet.loadFont(filename))
        except Exception as e:
            raise Py5Exception(
                e.__class__.__name__,
                str(e),
                'load_font',
                [filename])

    @overload
    def text_font(self, which: Py5Font) -> None:
        """$class_text_font"""
        pass

    @overload
    def text_font(self, which: Py5Font, size: float) -> None:
        """$class_text_font"""
        pass

    def text_font(self, *args) -> None:
        """$class_text_font"""
        try:
            if isinstance(args[0], Py5Font):
                args = (args[0]._pfont, *args[1:])
            return self._py5applet.textFont(*args)
        except Exception as e:
            raise Py5Exception(e.__class__.__name__, str(e), 'text_font', args)
