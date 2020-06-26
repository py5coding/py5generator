import io
from pathlib import Path
from typing import overload, NewType, Any, Callable, Union, Dict, List  # noqa

from PIL import Image
import cairosvg

from ..converter import Converter


class ImageMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._py5applet = kwargs['py5applet']
        self._converter = Converter(self._py5applet)
        self._pimage_cache = dict()

    @overload
    def image(self, img: Any, a: float, b: float, cache: bool) -> None:
        """$class_image"""
        pass

    @overload
    def image(self, img: Any, a: float, b: float, c: float, d: float, cache: bool) -> None:
        """$class_image"""
        pass

    def image(self, *args, cache: bool = False) -> None:
        """$class_image"""
        arg0_id = id(args[0])
        if cache and arg0_id in self._pimage_cache:
            pimage = self._pimage_cache[arg0_id]
        else:
            pimage = self._converter.to_pimage(args[0])

        if cache:
            self._pimage_cache[arg0_id] = pimage

        self._py5applet.image(pimage, *args[1:])

    # TODO: what about alpha mask images?
    # TODO: are there other PImage functions I should be paying attention to?
    # TODO: does caching actually work?

    def create_image(self, mode: str, width: int, height: int, color: Any) -> Image.Image:
        """$class_create_image"""
        return Image.new(mode, (width, height), color)

    def load_image(self, filename: Union[str, Path]) -> Image.Image:
        """$class_load_image"""
        filename = Path(filename)
        if filename.suffix.lower() == '.svg':
            with open(filename, 'r') as f:
                return Image.open(io.BytesIO(cairosvg.svg2png(file_obj=f)))
        else:
            return Image.open(filename)

    def texture(self, image: Any, cache: bool = False) -> None:
        """$class_texture"""
        image_id = id(image)
        if cache and image_id in self._pimage_cache:
            pimage = self._pimage_cache[image_id]
        else:
            pimage = self._converter.to_pimage(image)
        if cache:
            self._pimage_cache[image_id] = pimage

        self._py5applet.texture(pimage)
