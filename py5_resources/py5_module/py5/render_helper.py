import functools

from PIL import Image

from .sketch import Sketch


class RenderHelperSketch(Sketch):
    def __init__(self, setup, draw, width, height, renderer, *, limit=1,
                 setup_args=None, setup_kwargs=None, draw_args=None, draw_kwargs=None):
        super().__init__()
        if renderer not in [Sketch.HIDDEN, Sketch.JAVA2D, Sketch.P2D, Sketch.P3D]:
            raise RuntimeError(f'Processing Renderer {renderer} not yet supported')
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


def render_frame(draw: callable, width: int, height: int,
                 renderer: str = Sketch.HIDDEN, *, draw_args: tuple = None,
                 draw_kwargs: dict = None):
    """missing docstring"""
    ahs = RenderHelperSketch(None, draw, width, height, renderer,
                                draw_args=draw_args, draw_kwargs=draw_kwargs)
    ahs.run_sketch(block=True)

    if not ahs.is_dead_from_error and ahs.output:
        return ahs.output[0]


def render_frames(draw: callable, width: int, height: int,
                  renderer: str = Sketch.HIDDEN, *, limit: int = 1,
                  setup: callable = None,
                  setup_args: tuple = None, setup_kwargs: dict = None,
                  draw_args: tuple = None, draw_kwargs: dict = None):
    """missing docstring"""
    ahs = RenderHelperSketch(setup, draw, width, height, renderer, limit=limit,
                                setup_args=setup_args, setup_kwargs=setup_kwargs,
                                draw_args=draw_args, draw_kwargs=draw_kwargs)
    ahs.run_sketch(block=True)

    if not ahs.is_dead_from_error:
        return ahs.output


def render(width: int, height: int, renderer: str = Sketch.HIDDEN):
    """missing docstring"""
    def decorator(draw):
        @functools.wraps(draw)
        def run_render_frame(*draw_args, **draw_kwargs):
            return render_frame(draw, width, height, renderer,
                                draw_args=draw_args, draw_kwargs=draw_kwargs)
        return run_render_frame
    return decorator
