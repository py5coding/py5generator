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
import re
import inspect


COMMENT_LINE = re.compile(r'^\s+#.*' + chr(36), flags=re.MULTILINE)
DOCSTRING = re.compile(r'^\s+"""[^"]*"""', flags=re.MULTILINE | re.DOTALL)

MODULE_MODE_METHOD_LINE = re.compile(r'^\s+py5\.(\w+)\([^\)]*\)')
CLASS_MODE_METHOD_LINE = re.compile(r'^\s+self\.(\w+)\([^\)]*\)')
IMPORTED_MODE_METHOD_LINE = re.compile(r'^\s+(\w+)\([^\)]*\)')

FAUX_SETTINGS_FUNCTION_TEMPLATE = "def settings():\n"
FAUX_SETUP_FUNCTION_TEMPLATE = "def setup():\n"
FAUX_SETTINGS_METHOD_TEMPLATE = "def settings(self):\n"
FAUX_SETUP_METHOD_TEMPLATE = "def setup(self):\n"


def split_setup(functions, sketch_locals, *, mode):
    # return if there is nothing to do
    if 'settings' in functions or 'setup' not in functions:
        return functions

    if mode == 'module':
        METHOD_LINE = MODULE_MODE_METHOD_LINE
        FAUX_SETTINGS_TEMPLATE = FAUX_SETTINGS_FUNCTION_TEMPLATE
        FAUX_SETUP_TEMPLATE = FAUX_SETUP_FUNCTION_TEMPLATE
    elif mode == 'class':
        METHOD_LINE = CLASS_MODE_METHOD_LINE
        FAUX_SETTINGS_TEMPLATE = FAUX_SETTINGS_METHOD_TEMPLATE
        FAUX_SETUP_TEMPLATE = FAUX_SETUP_METHOD_TEMPLATE
    elif mode == 'imported':
        METHOD_LINE = IMPORTED_MODE_METHOD_LINE
        FAUX_SETTINGS_TEMPLATE = FAUX_SETTINGS_FUNCTION_TEMPLATE
        FAUX_SETUP_TEMPLATE = FAUX_SETUP_FUNCTION_TEMPLATE
    else:
        raise RuntimeError('unknown mode')
    
    setup = functions['setup']
    source_code = inspect.getsource(setup).strip()

    # remove comments
    source_code = COMMENT_LINE.sub('', source_code)
    # remove docstrings
    for docstring in DOCSTRING.findall(source_code):
        source_code = source_code.replace(docstring, (len(docstring.split('\n')) - 1) * '\n')

    # find the cutoff point
    for i, line in enumerate(source_code.split('\n')):
        if i > 0 and line.strip() and not ((m := METHOD_LINE.match(line)) and m.groups()[0] in ['size', 'full_screen', 'smooth', 'no_smooth', 'pixel_density']):
            break
    cutoff = i

    # build the fake code
    lines, lineno = inspect.getsourcelines(setup)
    filename = inspect.getfile(setup)
    fake_settings_code = (lineno - 1) * '\n' + FAUX_SETTINGS_TEMPLATE + ''.join(lines[1:cutoff])
    fake_setup_code = (lineno - 1) * '\n' + FAUX_SETUP_TEMPLATE + (cutoff - 1) * '\n' + ''.join(lines[cutoff:])
    
    # if the fake settings code is empty, there's no need to change anything
    if len(COMMENT_LINE.sub('', fake_settings_code).strip().split('\n')) > 1:
        # compile the fake code
        exec(compile(fake_settings_code, filename=filename, mode='exec'), sketch_locals, functions)
        # if the fake setup code is empty, get rid of it. otherwise, compile it
        if len(COMMENT_LINE.sub('', fake_setup_code).strip().split('\n')) == 1:
            del functions['setup']
        else:
            exec(compile(fake_setup_code, filename=filename, mode='exec'), sketch_locals, functions)

    return functions
