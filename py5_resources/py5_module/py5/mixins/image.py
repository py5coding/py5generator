import io
from pathlib import Path
import weakref
import functools
from typing import overload, NewType, Any, Callable, Union, Dict, List  # noqa

from PIL import Image
import cairosvg

from ..converter import Converter
from .threads import Py5Promise, ThreadsMixin


class PImageCache:

    def __init__(self, py5applet):
        self._converter = Converter(py5applet)
        self._weak_image_refs = []

    def flush_image_cache(self) -> None:
        self._weak_image_refs = []

    def _check_cache(self, image):
        if isinstance(image, tuple):
            image = image[0]
        for ref, pimage in reversed(self._weak_image_refs):
            if ref() is None:
                self._weak_image_refs.remove((ref, pimage))
            if image is ref():
                return pimage
        return None

    def _store_cache(self, image, pimage):
        if isinstance(image, tuple):
            image = image[0]
        self._weak_image_refs.append((weakref.ref(image), pimage))

    def check_cache_or_convert(self, image, cache):
        pimage = None
        cache_hit = False

        if cache:
            pimage = self._check_cache(image)
            if pimage is not None:
                cache_hit = True

        if pimage is None:
            pimage = self._converter.to_pimage(image)

        if cache and not cache_hit:
            self._store_cache(image, pimage)

        return pimage


def _check_pimage_cache_or_convert(argnum):
    def decorator(f):
        @functools.wraps(f)
        def decorated(self_, *args, cache=False):
            try:
                pimage_cache = getattr(self_, '_pimage_cache', None)
                if pimage_cache:
                    args = (*args[:argnum],
                            pimage_cache.check_cache_or_convert(args[argnum], cache),
                            *args[(argnum + 1):])
                else:
                    print('pimage cache not set???')
            except Exception:
                # if args[0] is not already a PImage the function call will fail
                pass
            return f(self_, *args)
        return decorated
    return decorator


class ImageMixin(ThreadsMixin):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._py5applet = kwargs['py5applet']
        self._pimage_cache = PImageCache(self._py5applet)

    def flush_image_cache(self) -> None:
        """$class_flush_image_cache"""
        self._pimage_cache.flush_image_cache()

    # TODO: what about alpha mask images?
    # TODO: are there other PImage functions I should be paying attention to?

    # *** BEGIN METHODS ***

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

    def request_image(self, filename: Union[str, Path]) -> Py5Promise:
        """$class_request_image"""
        return self.launch_promise_thread(self.load_image, args=(filename,))
