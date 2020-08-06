import time
import tempfile

from IPython.display import display, SVG, Image
from IPython.core.magic import Magics, magics_class, cell_magic, line_magic
from IPython.core.magic_arguments import magic_arguments, argument, parse_argstring

import PIL

from .run import run_single_frame_sketch


_unspecified = object()


@magics_class
class Py5Magics(Magics):

    # TODO: change default to not block when running a sketch.

    @magic_arguments()
    @argument('width', type=int, help='width of SVG drawing')
    @argument('height', type=int, help='height of SVG drawing')
    @argument('--no-warnings', dest='suppress_warnings', action='store_true',
              help="suppress name conflict warnings")
    @cell_magic
    def py5drawsvg(self, line, cell):
        """Create an SVG image with py5 and embed result in the notebook.

        For users who are familiar with Processing and py5 programming, you can
        pretend the code in this cell will be executed in a sketch with no
        `draw()` function and your code in the `setup()` function. It will use
        the SVG renderer.

        The below example will create a red square on a gray background:

        %%py5drawsvg 500 250
        background(128)
        fill(255, 0, 0)
        rect(80, 100, 50, 50)

        As this is creating an SVG image, you cannot do operations on the
        `pixels` or `np_pixels` arrays. Use `%%py5draw` instead.

        Code used in this cell can reference functions and variables defined in
        other cells. This will create a name conflict if your functions and
        variables overlap with py5's. A name conflict may cause an error. If
        such a conflict is detected, py5 will issue a helpful warning to alert
        you to the potential problem. You can suppress warnings with the
        --no_warnings flag.
        """
        args = parse_argstring(self.py5drawsvg, line)
        svg = run_single_frame_sketch(
            'SVG', cell, args.width, args.height, user_ns=self.shell.user_ns,
            suppress_warnings=args.suppress_warnings)
        if svg:
            display(SVG(svg))

    @magic_arguments()
    @argument('width', type=int, help='width of PNG drawing')
    @argument('height', type=int, help='height of PNG drawing')
    @argument('--no-warnings', dest='suppress_warnings', action='store_true',
              help="suppress name conflict warnings")
    @cell_magic
    def py5draw(self, line, cell):
        """Create a PNG image with py5 and embed result in the notebook.

        For users who are familiar with Processing and py5 programming, you can
        pretend the code in this cell will be executed in a sketch with no
        `draw()` function and your code in the `setup()` function. It will use
        the default renderer.

        The below example will create a red square on a gray background:

        %%py5draw 500 250
        background(128)
        fill(255, 0, 0)
        rect(80, 100, 50, 50)

        Code used in this cell can reference functions and variables defined in
        other cells. This will create a name conflict if your functions and
        variables overlap with py5's. A name conflict may cause an error. If
        such a conflict is detected, py5 will issue a helpful warning to alert
        you to the potential problem. You can suppress warnings with the
        --no_warnings flag.
        """
        args = parse_argstring(self.py5draw, line)
        png = run_single_frame_sketch(
            'HIDDEN', cell, args.width, args.height, user_ns=self.shell.user_ns,
            suppress_warnings=args.suppress_warnings)
        if png:
            display(Image(png))

    @line_magic
    @magic_arguments()
    @argument('-d', type=int, dest='delay', default=0, help='delay in seconds')
    def py5screenshot(self, line):
        """Take a screenshot of the current running sketch.

        Use the -d argument to wait before taking the screenshot.

        The returned image is a PIL.Image object. It can be assigned to a
        variable or embedded in the notebook.

        Below is an example demonstrating how to take a screenshot after a two
        second delay and assign it to the `img` variable. The image is then
        saved to a file. When run from a notebook, the image is embedded in the
        output.

        img = %py5screenshot -d 2
        img.save('image.png')
        img
        """
        args = parse_argstring(self.py5screenshot, line)
        import py5
        sketch = py5.get_current_sketch()

        if not sketch.is_running:
            print('The current sketch is not running.')
            return

        class Hook:

            def __init__(self, filename):
                self.filename = filename
                self.is_ready = False

            def __call__(self, sketch):
                sketch.save_frame(self.filename)
                self.is_ready = True

        time.sleep(args.delay)

        with tempfile.NamedTemporaryFile(suffix='.png') as png_file:
            hook = Hook(png_file.name)
            sketch._add_post_hook('draw', hook)

            while not hook.is_ready:
                time.sleep(0.01)

            sketch._remove_post_hook('draw')
            img = PIL.Image.open(png_file.name)

            return img


def load_ipython_extension(ipython):
    ipython.register_magics(Py5Magics)
