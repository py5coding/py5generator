# -*- coding: utf-8 -*-
# *** FORMAT PARAMS ***
# *** SKIP AUTOPEP8 ***

method_signatures_lookup_str = None  # DELETE

METHODS = ['settings', 'setup', 'draw', 'pre_draw', 'post_draw',
           'key_pressed', 'key_typed', 'key_released',
           'mouse_clicked', 'mouse_dragged', 'mouse_moved', 'mouse_entered',
           'mouse_exited', 'mouse_pressed', 'mouse_released', 'mouse_wheel',
           'exiting']

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
