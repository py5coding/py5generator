# *****************************************************************************
#
#   Part of the py5 library
#   Copyright (C) 2020-2021 Jim Schmitz
#
#   This library is free software: you can redistribute it and/or modify it
#   under the terms of the GNU Lesser General Public License as published by
#   the Free Software Foundation, either version 2.1 of the License, or (at
#   your option) any later version.
#
#   This library is distributed in the hope that it will be useful, but
#   WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser
#   General Public License for more details.
#
#   You should have received a copy of the GNU Lesser General Public License
#   along with this library. If not, see <https://www.gnu.org/licenses/>.
#
# *****************************************************************************
import time
import re
import io
from pathlib import Path
import tempfile

from IPython.display import display, SVG, Image
from IPython.core.magic import Magics, magics_class, cell_magic, line_magic
from IPython.core.magic_arguments import MagicHelpFormatter, parse_argstring, argument, magic_arguments, kwds

import PIL

from .single_frame import run_single_frame_sketch


class CellMagicHelpFormatter(MagicHelpFormatter):

    def add_usage(self, usage, actions, groups, prefix="::\n\n  %%"):
        super(MagicHelpFormatter, self).add_usage(usage, actions, groups, prefix)


def wait(wait_time, sketch):
    end_time = time.time() + wait_time
    while time.time() < end_time and sketch.is_running:
        time.sleep(0.1)


class BaseHook:

    def __init__(self, hook_name):
        self.hook_name = hook_name
        self.is_ready = False
        self.exception = None
        self.is_terminated = False

    def hook_finished(self, sketch):
        sketch._remove_post_hook('draw', self.hook_name)
        self.is_ready = True

    def hook_error(self, sketch, e):
        self.exception = e
        sketch._remove_post_hook('draw', self.hook_name)
        self.is_terminated = True

    def sketch_terminated(self):
        self.is_terminated = True


class ScreenshotHook(BaseHook):

    def __init__(self, filename):
        super().__init__('py5screenshot_hook')
        self.filename = filename

    def __call__(self, sketch):
        try:
            sketch.save_frame(self.filename, use_thread=False)
            self.hook_finished(sketch)
        except Exception as e:
            self.hook_error(sketch, e)


class SaveFramesHook(BaseHook):

    def __init__(self, dirname, filename, period, start, limit):
        super().__init__('py5save_frames_hook')
        self.dirname = dirname
        self.filename = filename
        self.period = period
        self.start = start
        self.limit = limit
        self.num_offset = None
        self.filenames = []
        self.last_frame_time = 0

    def __call__(self, sketch):
        try:
            if time.time() - self.last_frame_time < self.period:
                return
            if self.num_offset is None:
                self.num_offset = 0 if self.start is None else sketch.frame_count - self.start
            num = sketch.frame_count - self.num_offset
            frame_filename = sketch._insert_frame(
                str(self.dirname / self.filename), num=num)
            sketch.save_frame(frame_filename)
            self.filenames.append(frame_filename)
            self.last_frame_time = time.time()
            if len(self.filenames) == self.limit:
                self.hook_finished(sketch)
        except Exception as e:
            self.hook_error(sketch, e)


class GrabFramesHook(BaseHook):

    def __init__(self, period, count):
        super().__init__('py5grab_frames_hook')
        self.period = period
        self.count = count
        self.frames = []
        self.last_frame_time = 0

    def __call__(self, sketch):
        try:
            if time.time() - self.last_frame_time < self.period:
                return
            sketch.load_np_pixels()
            self.frames.append(sketch.np_pixels[:, :, 1:].copy())
            self.last_frame_time = time.time()
            if len(self.frames) == self.count:
                self.hook_finished(sketch)
        except Exception as e:
            self.hook_error(sketch, e)


@magics_class
class Py5Magics(Magics):

    def _filename_check(self, filename):
        filename = Path(filename)
        if not filename.parent.exists():
            filename.parent.mkdir(parents=True)
        return filename

    def _variable_name_check(self, varname):
        return re.match('^[a-zA-Z_]\w*' + chr(36), varname)

    @magic_arguments()
    @argument(""" DELETE
    $arguments_Py5Magics_py5drawpdf_arguments
    """) # DELETE
    @kwds(formatter_class=CellMagicHelpFormatter)
    @cell_magic
    def py5drawpdf(self, line, cell):
        """$class_Py5Magics_py5drawpdf"""
        args = parse_argstring(self.py5drawpdf, line)
        pdf = run_single_frame_sketch('PDF', cell, args.width, args.height,
                                      self.shell.user_ns, not args.unsafe)
        if pdf:
            filename = self._filename_check(args.filename)
            with open(filename, 'wb') as f:
                f.write(pdf)
            print(f'PDF written to {filename}')

    @magic_arguments()
    @argument(""" DELETE
    $arguments_Py5Magics_py5drawdxf_arguments
    """) # DELETE
    @kwds(formatter_class=CellMagicHelpFormatter)
    @cell_magic
    def py5drawdxf(self, line, cell):
        """$class_Py5Magics_py5drawdxf"""
        args = parse_argstring(self.py5drawdxf, line)
        dxf = run_single_frame_sketch('DXF', cell, args.width, args.height,
                                      self.shell.user_ns, not args.unsafe)
        if dxf:
            filename = self._filename_check(args.filename)
            with open(filename, 'w') as f:
                f.write(dxf)
            print(f'DXF written to {filename}')

    @magic_arguments()
    @argument(""" DELETE
    $arguments_Py5Magics_py5drawsvg_arguments
    """) # DELETE
    @kwds(formatter_class=CellMagicHelpFormatter)
    @cell_magic
    def py5drawsvg(self, line, cell):
        """$class_Py5Magics_py5drawsvg"""
        args = parse_argstring(self.py5drawsvg, line)
        svg = run_single_frame_sketch('SVG', cell, args.width, args.height,
                                      self.shell.user_ns, not args.unsafe)
        if svg:
            if args.filename:
                filename = self._filename_check(args.filename)
                with open(filename, 'w') as f:
                    f.write(svg)
                print(f'SVG drawing written to {filename}')
            display(SVG(svg))

    @magic_arguments()
    @argument(""" DELETE
    $arguments_Py5Magics_py5draw_arguments
    """) # DELETE
    @kwds(formatter_class=CellMagicHelpFormatter)
    @cell_magic
    def py5draw(self, line, cell):
        """$class_Py5Magics_py5draw"""
        args = parse_argstring(self.py5draw, line)

        if args.renderer == 'SVG':
            print('please use %%py5drawsvg for SVG drawings.')
            return
        if args.renderer == 'PDF':
            print('please use %%py5drawpdf for PDFs.')
            return
        if args.renderer not in ['HIDDEN', 'JAVA2D', 'P2D', 'P3D']:
            print(f'unknown renderer {args.renderer}')
            return

        png = run_single_frame_sketch(args.renderer, cell, args.width, args.height,
                                      self.shell.user_ns, not args.unsafe)
        if png:
            if args.filename or args.variable:
                pil_img = PIL.Image.open(io.BytesIO(png)).convert(mode='RGB')
                if args.filename:
                    filename = self._filename_check(args.filename)
                    pil_img.save(filename)
                    print(f'PNG file written to {filename}')
                if args.variable:
                    if self._variable_name_check(args.variable):
                        self.shell.user_ns[args.variable] = pil_img
                        print(f'PIL Image assigned to {args.variable}')
                    else:
                        print(f'Invalid variable name {args.variable}')
            display(Image(png))

    @line_magic
    @magic_arguments()
    @argument(""" DELETE
    $arguments_Py5Magics_py5screenshot_arguments
    """) # DELETE
    def py5screenshot(self, line):
        """$class_Py5Magics_py5screenshot"""
        args = parse_argstring(self.py5screenshot, line)
        import py5
        sketch = py5.get_current_sketch()

        if not sketch.is_running:
            print('The current sketch is not running.')
            return

        wait(args.wait, sketch)

        with tempfile.TemporaryDirectory() as tempdir:
            temp_png = Path(tempdir) / 'output.png'
            hook = ScreenshotHook(temp_png)
            sketch._add_post_hook('draw', hook.hook_name, hook)

            while not hook.is_ready and not hook.is_terminated:
                time.sleep(0.005)

            if hook.is_ready:
                return PIL.Image.open(temp_png)
            elif hook.is_terminated and hook.exception:
                print('error running magic:', hook.exception)

    @line_magic
    @magic_arguments()
    @argument(""" DELETE
    $arguments_Py5Magics_py5saveframes_arguments
    """) # DELETE
    def py5saveframes(self, line):
        """$class_Py5Magics_py5saveframes"""
        args = parse_argstring(self.py5saveframes, line)
        import py5
        sketch = py5.get_current_sketch()

        if not sketch.is_running:
            print('The current sketch is not running.')
            return

        dirname = Path(args.dirname)
        if not dirname.exists():
            dirname.mkdir(parents=True)
        print(f'writing frames to {str(args.dirname)}...')

        wait(args.wait, sketch)

        hook = SaveFramesHook(dirname, args.filename, args.period, args.start, args.limit)
        sketch._add_post_hook('draw', hook.hook_name, hook)

        if args.limit:
            while not hook.is_ready and not hook.is_terminated:
                time.sleep(0.02)
                print(f'saving frame {len(hook.filenames)}/{args.limit}', end='\r')
            print(f'saving frame {len(hook.filenames)}/{args.limit}')

            if hook.is_ready:
                return hook.filenames

        if hook.is_terminated and hook.exception:
            print('error running magic:', hook.exception)

    @line_magic
    @magic_arguments()
    @argument(""" DELETE
    $arguments_Py5Magics_py5animatedgif_arguments
    """) # DELETE
    def py5animatedgif(self, line):
        """$class_Py5Magics_py5animatedgif"""
        args = parse_argstring(self.py5animatedgif, line)
        import py5
        sketch = py5.get_current_sketch()

        if not sketch.is_running:
            print('The current sketch is not running.')
            return

        filename = Path(args.filename)

        wait(args.wait, sketch)

        hook = GrabFramesHook(args.period, args.count)
        sketch._add_post_hook('draw', hook.hook_name, hook)

        while not hook.is_ready and not hook.is_terminated:
            time.sleep(0.05)
            print(f'collecting frame {len(hook.frames)}/{args.count}', end='\r')
        print(f'collecting frame {len(hook.frames)}/{args.count}')

        if hook.is_ready:
            if not filename.parent.exists():
                filename.parent.mkdir(parents=True)

            img1 = PIL.Image.fromarray(hook.frames[0], mode='RGB')
            imgs = [PIL.Image.fromarray(arr, mode='RGB') for arr in hook.frames[1:]]
            img1.save(filename, save_all=True, duration=1000 * args.duration,
                      loop=args.loop, optimize=args.optimize, append_images=imgs)

            return str(filename)

        elif hook.is_terminated and hook.exception:
            print('error running magic:', hook.exception)

    @line_magic
    @magic_arguments()
    @argument(""" DELETE
    $arguments_Py5Magics_py5captureframes_arguments
    """) # DELETE
    def py5captureframes(self, line):
        """$class_Py5Magics_py5captureframes"""
        args = parse_argstring(self.py5captureframes, line)
        import py5
        sketch = py5.get_current_sketch()

        if not sketch.is_running:
            print('The current sketch is not running.')
            return

        wait(args.wait, sketch)

        hook = GrabFramesHook(args.period, args.count)
        sketch._add_post_hook('draw', hook.hook_name, hook)

        while not hook.is_ready and not hook.is_terminated:
            time.sleep(0.05)
            print(f'collecting frame {len(hook.frames)}/{args.count}', end='\r')
        print(f'collecting frame {len(hook.frames)}/{args.count}')

        if hook.is_ready:
            return [PIL.Image.fromarray(arr, mode='RGB') for arr in hook.frames]

        elif hook.is_terminated and hook.exception:
            print('error running magic:', hook.exception)


def load_ipython_extension(ipython):
    ipython.register_magics(Py5Magics)
