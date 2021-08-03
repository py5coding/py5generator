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
import io

from ipykernel.zmqshell import ZMQInteractiveShell
import ipywidgets as widgets

import PIL

from .hooks import SketchPortalHook


Sketch = 'Sketch'


class Py5SketchPortal(widgets.Image):
    pass


def sketch_portal(*, time_limit: float = 0.0, throttle_frame_rate: float = 30,
                  scale: float = 1.0, quality: int = 75,
                  portal: Py5SketchPortal = None, sketch: Sketch = None,
                  hook_post_draw: bool = False) -> None:
    """$module_Py5Tools_sketch_portal"""
    try:
        __IPYTHON__  # type: ignore
        in_ipython_session = True
        in_jupyter_zmq_shell = isinstance(get_ipython(), ZMQInteractiveShell)  # type: ignore
    except NameError:
        in_ipython_session = False
        in_jupyter_zmq_shell = False

    if not in_ipython_session:
        raise RuntimeError('The sketch_widget() function can only be used with IPython and ZMQInteractiveShell (such as Jupyter Lab)')
    if not in_jupyter_zmq_shell:
        raise RuntimeError('The sketch_widget() function can only be used with ZMQInteractiveShell (such as Jupyter Lab)')

    if sketch is None:
        import py5
        sketch = py5.get_current_sketch()
        prefix = ' current'
    else:
        prefix = ''

    if not sketch.is_running:
        raise RuntimeError(f'The {prefix} sketch is not running')
    if throttle_frame_rate is not None and throttle_frame_rate <= 0:
        raise RuntimeError('The throttle_frame_rate parameter must be None or greater than zero')
    if time_limit < 0:
        raise RuntimeError('The time_limit parameter must be greater than or equal to zero')
    if quality < 1 or quality > 100:
        raise RuntimeError('The quality parameter must be between 1 (worst) and 100 (best)')
    if scale <= 0:
        raise RuntimeError('The scale parameter must be greater than zero')

    if portal is None:
        portal = Py5SketchPortal()
        portal.layout.width = f'{int(scale * sketch.width)}px'
        portal.layout.height = f'{int(scale * sketch.height)}px'
        portal.layout.border = '1px solid gray'

    def displayer(frame):
        img = PIL.Image.fromarray(frame)
        if scale != 1.0:
            img = img.resize(tuple(int(scale * x) for x in img.size))
        b = io.BytesIO()
        img.save(b, format='JPEG', quality=quality)
        portal.value = b.getvalue()

    hook = SketchPortalHook(displayer, throttle_frame_rate, time_limit)

    sketch._add_post_hook('post_draw' if hook_post_draw else 'draw', hook.hook_name, hook)

    exit_button = widgets.Button(description='exit_sketch()')
    exit_button.on_click(lambda x: sketch.exit_sketch())

    return widgets.VBox([portal, exit_button])


__all__ = ['sketch_portal']
