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
import io
import base64

from ipykernel.zmqshell import ZMQInteractiveShell
import ipywidgets as widgets
from IPython.display import display, clear_output

import PIL

from .hooks import SketchPortalHook


def sketch_widget(*, frame_rate: float = 10.0, time_limit: float = 0.0,
                  quality: int = 75, scale: float = 1.0,
                  output_widget = None, sketch = None):
    try:
        __IPYTHON__  # type: ignore
        in_ipython_session = True
        in_jupyter_zmq_shell = isinstance(get_ipython(), ZMQInteractiveShell)  # type: ignore
    except NameError:
        in_ipython_session = False
        in_jupyter_zmq_shell = False

    if not in_ipython_session:
        raise RuntimeError('The sketch_widget() function can only be used with IPython and ZMQInteractiveShell')
    if not in_jupyter_zmq_shell:
        raise RuntimeError('The sketch_widget() function can only be used with ZMQInteractiveShell')

    if sketch is None:
        import py5
        sketch = py5.get_current_sketch()
        prefix = ' current'
    else:
        prefix = ''

    if not sketch.is_running:
        raise RuntimeError(f'The {prefix} sketch is not running.')

    if output_widget is None:
        output_widget = widgets.Output(layout=dict(width=f'{sketch.width}px', height=f'{sketch.height}px'))
        display(output_widget)

    def displayer(frame):
        img = PIL.Image.fromarray(frame)
        if scale != 1.0:
            img = img.resize(tuple(int(scale * x) for x in img.size))
        b = io.BytesIO()
        img.save(b, format='JPEG', quality=quality)
        data = {'image/jpeg': base64.b64encode(b.getvalue()).decode('ascii')}
        with output_widget:
            clear_output(wait=True)
            display(data, raw=True)

    if frame_rate <= 0:
        raise RuntimeError('The frame_rate parameter must be greater than zero.')

    if time_limit < 0:
        raise RuntimeError('The time_limit parameter must be greater than or equal to zero.')

    if quality < 1 or quality > 100:
        raise RuntimeError('The quality parameter must be between 1 (worst) and 100 (best).')

    if scale <= 0:
        raise RuntimeError('The scale parameter must be greater than zero.')

    hook = SketchPortalHook(displayer, frame_rate, time_limit)
    sketch._add_post_hook('draw', hook.hook_name, hook)

    time.sleep(5)
