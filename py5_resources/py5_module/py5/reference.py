# *****************************************************************************
#
#   Part of the py5 library
#   Copyright (C) 2020-2023 Jim Schmitz
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
# *** FORMAT PARAMS ***
# *** SKIP AUTOPEP8 ***


method_signatures_lookup_str = None  # DELETE

METHODS = dict(
    settings=[0],
    setup=[0],
    draw=[0],
    pre_draw=[0],
    post_draw=[0],
    key_pressed=[0, 1],
    key_typed=[0, 1],
    key_released=[0, 1],
    mouse_clicked=[0, 1],
    mouse_dragged=[0, 1],
    mouse_moved=[0, 1],
    mouse_entered=[0, 1],
    mouse_exited=[0, 1],
    mouse_pressed=[0, 1],
    mouse_released=[0, 1],
    mouse_wheel=[0, 1],
    window_moved=[0],
    window_resized=[0],
    exiting=[0],
    movie_event=[1],
)

FILE_CLASS_LOOKUP = dict(
    [
        (("font.py",), "Py5Font"),
        (("graphics.py",), "Py5Graphics"),
        (("image.py",), "Py5Image"),
        (("shader.py",), "Py5Shader"),
        (("shape.py",), "Py5Shape"),
        (("sketch.py",), "Sketch"),
        (("surface.py",), "Py5Surface"),
        (("mixins", "data.py"), "Sketch"),
        (("mixins", "math.py"), "Sketch"),
        (("mixins", "pixels.py"), "Sketch"),
        (("mixins", "threads.py"), "Sketch"),
        (("keyevent.py",), "Py5KeyEvent"),
        (("mouseevent.py",), "Py5MouseEvent"),
    ]
)

METHOD_SIGNATURES_LOOKUP = dict([{method_signatures_lookup_str}])
