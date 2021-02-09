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
from pathlib import Path
import tempfile
import textwrap

from . import utils


# TODO: this code is only used by magics.py, but perhaps should be used to
# execute reference documentation example code. at least rename the file to
# something else.

_CODE_FRAMEWORK = """
import py5

{2}

with open('{0}', 'r') as f:
    eval(compile(f.read(), '{0}', 'exec'))

py5.run_sketch(block=True)
if {1} and py5.is_dead_from_error:
    py5.exit_sketch()
"""


_STANDARD_CODE_TEMPLATE = """
import py5

def settings():
    py5.size({0}, {1}, py5.{2})


def setup():
{4}

    py5.save_frame("{3}", use_thread=False)
    py5.exit_sketch()
"""


_ALT_CODE_TEMPLATE = """
import py5

def settings():
    py5.size({0}, {1}, py5.{2}, "{3}")


def setup():
{4}

    py5.exit_sketch()
"""


_DXF_CODE_TEMPLATE = """
import py5

def settings():
    py5.size({0}, {1}, py5.P3D)


def setup():
    py5.begin_raw(py5.DXF, "{3}")

{4}

    py5.end_raw()
    py5.exit_sketch()
"""


def run_single_frame_sketch(renderer, code, width, height, user_ns, safe_exec):
    if renderer == 'SVG':
        template = _ALT_CODE_TEMPLATE
        suffix = '.svg'
        read_mode = 'r'
    elif renderer == 'PDF':
        template = _ALT_CODE_TEMPLATE
        suffix = '.pdf'
        read_mode = 'rb'
    elif renderer == 'DXF':
        template = _DXF_CODE_TEMPLATE
        suffix = '.dxf'
        read_mode = 'r'
    else:
        template = _STANDARD_CODE_TEMPLATE
        suffix = '.png'
        read_mode = 'rb'

    import py5
    if py5.get_current_sketch().is_running:
        print('You must exit the currently running sketch before running another sketch.')
        return None

    if safe_exec:
        prepared_code = textwrap.indent(code, '    ')
        prepared_code = utils.fix_triple_quote_str(prepared_code)
    else:
        user_ns['_py5_user_ns'] = user_ns
        code = code.replace('"""', r'\"\"\"')
        prepared_code = f'    exec("""{code}""", _py5_user_ns)'

    with tempfile.TemporaryDirectory() as tempdir:
        temp_py = Path(tempdir) / 'py5_code.py'
        temp_out = Path(tempdir) / ('output' + suffix)

        with open(temp_py, 'w') as f:
            code = template.format(width, height, renderer, temp_out.as_posix(), prepared_code)
            f.write(code)

        exec(_CODE_FRAMEWORK.format(temp_py.as_posix(), True, ''), user_ns)

        if temp_out.exists():
            with open(temp_out, read_mode) as f:
                result = f.read()
        else:
            result = None

    py5.reset_py5()

    if not safe_exec:
        del user_ns['_py5_user_ns']

    return result


__all__ = ['run_single_frame_sketch']
