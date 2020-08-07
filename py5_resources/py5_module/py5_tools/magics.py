import time
import io
from pathlib import Path
import tempfile

from IPython.display import display, clear_output, SVG, Image
from IPython.core.magic import Magics, magics_class, cell_magic, line_magic
from IPython.core.magic_arguments import magic_arguments, argument, parse_argstring

import PIL

from .run import run_single_frame_sketch


_unspecified = object()


@magics_class
class Py5Magics(Magics):

    def _filename_check(self, filename):
        filename = Path(filename)
        if not filename.parent.exists():
            filename.parent.mkdir(parents=True)
        return filename

    @magic_arguments()
    @argument('width', type=int, help='width of SVG drawing')
    @argument('height', type=int, help='height of SVG drawing')
    @argument('--filename', type=str, dest='filename', help='save SVG image to file')
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
            if args.filename:
                filename = self._filename_check(args.filename)
                with open(filename, 'w') as f:
                    f.write(svg)
            display(SVG(svg))

    @magic_arguments()
    @argument('width', type=int, help='width of PNG drawing')
    @argument('height', type=int, help='height of PNG drawing')
    @argument('--filename', dest='filename', help='save image to file')
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
            if args.filename:
                filename = self._filename_check(args.filename)
                PIL.Image.open(io.BytesIO(png)).convert(mode='RGB').save(filename)
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
                sketch._remove_post_hook('draw', 'py5screenshot_hook')
                self.is_ready = True

        time.sleep(args.delay)

        with tempfile.NamedTemporaryFile(suffix='.png') as png_file:
            hook = Hook(png_file.name)
            sketch._add_post_hook('draw', 'py5screenshot_hook', hook)

            while not hook.is_ready:
                time.sleep(0.02)

            img = PIL.Image.open(png_file.name)

            return img

    @line_magic
    @magic_arguments()
    @argument('dirname', type=str, help='directory to save the frames')
    @argument('--filename', type=str, dest='filename', default='frame_####.png',
              help='filename to save frames to')
    @argument('-d', type=int, dest='delay', default=0,
              help='start delay in seconds')
    @argument('--limit', type=int, dest='limit', default=0,
              help='limit the number of frames to save (default 0 means no limit)')
    def py5screencapture(self, line):
        """Save the current running sketch's frames to a directory.

        Use the -d argument to wait before starting.

        If a limit is given, this line magic will wait to return a list of the
        filenames. Otherwise, it will return right away.
        """
        args = parse_argstring(self.py5screencapture, line)
        import py5
        sketch = py5.get_current_sketch()

        if not sketch.is_running:
            print('The current sketch is not running.')
            return

        class Hook:

            def __init__(self, dirname, filename, limit):
                self.dirname = dirname
                self.filename = filename
                self.limit = limit
                self.filenames = []
                self.exception = None
                self.is_ready = False
                print(f'writing frames to {str(dirname)}...')

            def _end_hook(self, sketch):
                sketch._remove_post_hook('draw', 'py5screencapture_hook')
                self.is_ready = True

            def __call__(self, sketch):
                try:
                    filename = sketch._instance.insertFrame(str(self.dirname / self.filename))
                    sketch.save_frame(filename)
                    self.filenames.append(filename)
                    if len(self.filenames) == self.limit:
                        self._end_hook(sketch)
                except Exception as e:
                    self.exception = e
                    self._end_hook(sketch)

        time.sleep(args.delay)

        dirname = Path(args.dirname)
        if not dirname.exists():
            dirname.mkdir(parents=True)

        hook = Hook(dirname, args.filename, args.limit)
        sketch._add_post_hook('draw', 'py5screencapture_hook', hook)

        if args.limit:
            while not hook.is_ready:
                time.sleep(0.02)
                clear_output(wait=True)
                print(f'{len(hook.filenames)} / {args.limit}')

            if hook.exception:
                print('error running py5screencapture:', hook.exception)
            else:
                return hook.filenames


def load_ipython_extension(ipython):
    ipython.register_magics(Py5Magics)
