import sys
import functools
from typing import Callable, Tuple, Dict, List, NewType

import numpy as np

import PIL
import PIL.ImageFile
from PIL import Image

from .sketch import Sketch


PIL_ImageFile = NewType('PIL_ImageFile', PIL.ImageFile.ImageFile)


class RenderHelperSketch(Sketch):
    def __init__(self, setup, draw, width, height, renderer, *, limit=1,
                 setup_args=None, setup_kwargs=None, draw_args=None, draw_kwargs=None):
        super().__init__()
        self._setup = setup
        self._draw = draw
        self._width = width
        self._height = height
        self._renderer = renderer
        self._limit = limit
        self._setup_args = setup_args or []
        self._setup_kwargs = setup_kwargs or {}
        self._draw_args = draw_args or []
        self._draw_kwargs = draw_kwargs or {}
        self.output = []

    def settings(self):
        self.size(self._width, self._height, self._renderer)

    def setup(self):
        if self._setup:
            self._setup(self, *self._setup_args, **self._setup_kwargs)

    def draw(self):
        self._draw(self, *self._draw_args, **self._draw_kwargs)
        self.load_np_pixels()
        self.output.append(Image.fromarray(self.np_pixels[:, :, 1:]))
        if self.frame_count == self._limit:
            self.exit_sketch()


class RenderHelperGraphicsCanvas(Sketch):
    def __init__(self, setup, draw, width, height, renderer, *, limit=1,
                 setup_args=None, setup_kwargs=None, draw_args=None, draw_kwargs=None):
        super().__init__()
        self._setup = setup
        self._draw = draw
        self._width = width
        self._height = height
        self._renderer = renderer
        self._limit = limit
        self._setup_args = setup_args or []
        self._setup_kwargs = setup_kwargs or {}
        self._draw_args = draw_args or []
        self._draw_kwargs = draw_kwargs or {}
        self.output = []
        self._g = None

    def settings(self):
        self.size(100, 100, self._renderer)

    def setup(self):
        self.frame_rate(1000)  # performance boost :)
        self._g = self.create_graphics(self._width, self._height, self._renderer)
        # this begin/end draw pair is necessary when using the opengl renderers
        self._g.begin_draw()
        self._g.end_draw()

    def draw(self):
        self._g.begin_draw()
        if self.frame_count == 1 and self._setup:
            # call setup here so that _g can be drawn upon
            self._setup(self._g, *self._setup_args, **self._setup_kwargs)
        self._draw(self._g, *self._draw_args, **self._draw_kwargs)
        self._g.end_draw()
        self._g.load_np_pixels()
        g_pixels = np.dstack((self._g.np_pixels[:, :, 1:], self._g.np_pixels[:, :, 0]))
        self.output.append(Image.fromarray(g_pixels))
        if self.frame_count >= self._limit:
            self.exit_sketch()


def _check_allowed_renderer(renderer):
    renderer_name = {Sketch.SVG: 'SVG', Sketch.PDF: 'PDF', Sketch.DXF: 'DXF', Sketch.P2D: 'P2D', Sketch.P3D: 'P3D'}.get(renderer, renderer)
    renderers = [Sketch.HIDDEN, Sketch.JAVA2D] if sys.platform == 'darwin' else [Sketch.HIDDEN, Sketch.JAVA2D, Sketch.P2D, Sketch.P3D]
    if renderer not in renderers:
        return f'sorry, the render helper tools do not support the {renderer_name} renderer' + (' on OSX.' if sys.platform == 'darwin' else '.')
    else:
        return None


def _osx_renderer_check(renderer):
    if sys.platform == 'darwin' and renderer == Sketch.JAVA2D:
        print('sorry, the render helper tools do not support the JAVA2D renderer on OSX. Using the HIDDEN renderer instead.')
        return Sketch.HIDDEN
    else:
        return renderer


def render_frame(draw: Callable, width: int, height: int,
                 renderer: str = Sketch.HIDDEN, *,
                 draw_args: Tuple = None, draw_kwargs: Dict = None,
                 use_py5graphics=False) -> PIL.ImageFile.ImageFile:
    """$module_Py5Functions_render_frame"""
    if msg :=_check_allowed_renderer(renderer):
        print(msg, file=sys.stderr)
        return None
    renderer = _osx_renderer_check(renderer)

    HelperClass = RenderHelperGraphicsCanvas if use_py5graphics else RenderHelperSketch
    ahs = HelperClass(None, draw, width, height, renderer,
                      draw_args=draw_args, draw_kwargs=draw_kwargs)
    ahs.run_sketch(block=True)

    if not ahs.is_dead_from_error and ahs.output:
        return ahs.output[0]


def render_frame_sequence(draw: Callable, width: int, height: int,
                          renderer: str = Sketch.HIDDEN, *,
                          limit: int = 1, setup: Callable = None,
                          setup_args: Tuple = None, setup_kwargs: Dict = None,
                          draw_args: Tuple = None, draw_kwargs: Dict = None,
                          use_py5graphics=False) -> List[PIL_ImageFile]:
    """$module_Py5Functions_render_frame_sequence"""
    if msg :=_check_allowed_renderer(renderer):
        print(msg, file=sys.stderr)
        return None
    renderer = _osx_renderer_check(renderer)

    HelperClass = RenderHelperGraphicsCanvas if use_py5graphics else RenderHelperSketch
    ahs = HelperClass(setup, draw, width, height, renderer, limit=limit,
                      setup_args=setup_args, setup_kwargs=setup_kwargs,
                      draw_args=draw_args, draw_kwargs=draw_kwargs)
    ahs.run_sketch(block=True)

    if not ahs.is_dead_from_error:
        return ahs.output


def render(width: int, height: int, renderer: str = Sketch.HIDDEN, *,
           use_py5graphics=False) -> PIL.ImageFile.ImageFile:
    """$module_Py5Functions_render"""
    if msg :=_check_allowed_renderer(renderer):
        raise RuntimeError(msg)
    renderer = _osx_renderer_check(renderer)

    def decorator(draw):
        @functools.wraps(draw)
        def run_render_frame(*draw_args, **draw_kwargs):
            return render_frame(draw, width, height, renderer,
                                draw_args=draw_args, draw_kwargs=draw_kwargs,
                                use_py5graphics=use_py5graphics)
        return run_render_frame
    return decorator


def render_sequence(width: int, height: int, renderer: str = Sketch.HIDDEN, *,
                    limit: int = 1, setup: Callable = None,
                    setup_args: Tuple = None, setup_kwargs: Dict = None,
                    use_py5graphics=False) -> List[PIL_ImageFile]:
    """$module_Py5Functions_render_sequence"""
    if msg :=_check_allowed_renderer(renderer):
        raise RuntimeError(msg)
    renderer = _osx_renderer_check(renderer)

    def decorator(draw):
        @functools.wraps(draw)
        def run_render_frames(*draw_args, **draw_kwargs):
            return render_frame_sequence(draw, width, height, renderer,
                                         limit=limit, setup=setup,
                                         setup_args=setup_args, setup_kwargs=setup_kwargs,
                                         draw_args=draw_args, draw_kwargs=draw_kwargs,
                                         use_py5graphics=use_py5graphics)
        return run_render_frames
    return decorator
