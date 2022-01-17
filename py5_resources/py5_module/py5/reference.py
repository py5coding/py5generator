# *****************************************************************************
#
#   Part of the py5 library
#   Copyright (C) 2020-2022 Jim Schmitz
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


METHODS = [
    'settings', 'setup', 'draw', 'pre_draw', 'post_draw',
    'key_pressed', 'key_typed', 'key_released',
    'mouse_clicked', 'mouse_dragged', 'mouse_moved', 'mouse_entered',
    'mouse_exited', 'mouse_pressed', 'mouse_released', 'mouse_wheel',
    'exiting', 'movie_event'
]

FILE_CLASS_LOOKUP = dict([
    (('font.py',), 'Py5Font'),
    (('graphics.py',), 'Py5Graphics'),
    (('image.py',), 'Py5Image'),
    (('shader.py',), 'Py5Shader'),
    (('shape.py',), 'Py5Shape'),
    (('sketch.py',), 'Sketch'),
    (('surface.py',), 'Py5Surface'),
    (('mixins', 'data.py'), 'Sketch'),
    (('mixins', 'math.py'), 'Sketch'),
    (('mixins', 'pixels.py'), 'Sketch'),
    (('mixins', 'threads.py'), 'Sketch'),
])

METHOD_SIGNATURES_LOOKUP = dict([
    {method_signatures_lookup_str}
])
