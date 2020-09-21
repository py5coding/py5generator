# -*- coding: utf-8 -*-
# *** FORMAT PARAMS ***
# *** SKIP AUTOPEP8 ***
import re

method_signatures_lookup_str = None  # DELETE

# TODO: move this to reference.py?? or somewhere else?
METHOD_SIGNATURES_LOOKUP = dict([
    {method_signatures_lookup_str}
])

JPYPE_TYPEERROR_REGEX = re.compile(r'No matching overloads found for [\w\.]*(\([^\)]*\))')

FILE_CLASS_LOOKUP = dict([
    ('font.py', 'Py5Font'),
    ('graphics.py', 'Py5Graphics'),
    ('image.py', 'Py5Image'),
    ('shader.py', 'Py5Shader'),
    ('shape.py', 'Py5Shape'),
    ('sketch.py', 'Sketch'),
    ('surface.py', 'Py5Surface'),
    # TODO: would these work correctly on windows?
    ('mixins/data.py', 'Sketch'),
    ('mixins/math.py', 'Sketch'),
    ('mixins/pixels.py', 'Sketch'),
    ('mixins/threads.py', 'Sketch'),
])


def handle_typeerror(exc_type_name, exc_msg, py5info):
    if py5info:
        filename, fname = py5info[-1]
        print(filename, fname)
        signatures = METHOD_SIGNATURES_LOOKUP.get((FILE_CLASS_LOOKUP.get(filename), fname))
        if signatures and (m := JPYPE_TYPEERROR_REGEX.search(exc_msg)):
            passed = m.groups(1)[0].replace(',', ', ')
            exc_msg = 'The parameter types ' + passed + ' are invalid for method ' + fname + '.\n'
            exc_msg += 'Your parameters must match one of the following signatures:\n'
            exc_msg += '\n'.join([' * ' + fname + sig for sig in signatures])

    return exc_msg


CUSTOM_EXCEPTION_MSGS = dict(
    ZeroDivisionError='Dividing by zero? Madness!!!',
    TypeError=handle_typeerror,
)
