import sys
import os
from multiprocessing import Process
from pathlib import Path
import tempfile
import textwrap

from . import jvm


_CODE_FRAMEWORK = """
import py5

with open('{0}', 'r') as f:
    eval(compile(f.read(), '{0}', 'exec'))

py5.run_sketch(block=True)
"""


_STANDARD_CODE_TEMPLATE = """
import py5

def settings():
    py5.size({0}, {1}, py5.{2})


def setup():
{4}

    py5.save_frame("{3}")
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


def run_sketch(sketch_path, classpath=None, new_process=False):
    sketch_path = Path(sketch_path)
    if not sketch_path.exists():
        print(f'file {sketch_path} not found')
        return

    # TODO: this should allow sketches with no functions, ie a bunch of commands that get put into a setup
    # TODO: this should not require a settings() and should pull out the necessary stuff from setup()
    def _run_sketch(sketch_path, classpath):
        if not jvm.is_jvm_running():
            if classpath:
                jvm.add_classpath(classpath)
            jvm.add_jars(sketch_path.parent / 'jars')

        import py5
        if not py5.get_current_sketch().is_ready:
            py5.reset_py5()
        sys.path.extend([str(sketch_path.absolute().parent), os.getcwd()])
        from .namespace import Py5Namespace
        py5_ns = Py5Namespace(py5)
        exec(_CODE_FRAMEWORK.format(sketch_path), py5_ns)

    if new_process:
        p = Process(target=_run_sketch, args=(sketch_path, classpath))
        p.start()
        return p
    else:
        _run_sketch(sketch_path, classpath)


def run_single_frame_sketch(renderer, code, width, height, user_ns, safe_exec):

    # TODO: what about the DXF renderer? others?
    if renderer == 'SVG':
        template = _ALT_CODE_TEMPLATE
        suffix = '.svg'
        read_mode = 'r'
    elif renderer == 'PDF':
        template = _ALT_CODE_TEMPLATE
        suffix = '.pdf'
        read_mode = 'rb'
    else:
        template = _STANDARD_CODE_TEMPLATE
        suffix = '.png'
        read_mode = 'rb'

    import py5
    if not py5.get_current_sketch().is_ready:
        py5.reset_py5()

    if safe_exec:
        prepared_code = textwrap.indent(code, '    ')
    else:
        user_ns['_py5_user_ns'] = user_ns
        prepared_code = f'    exec("""{code}""", _py5_user_ns)'

    temp_py = tempfile.NamedTemporaryFile(suffix='.py')
    temp_out = tempfile.NamedTemporaryFile(suffix=suffix)

    with open(temp_py.name, 'w') as f:
        code = template.format(width, height, renderer, temp_out.name, prepared_code)
        f.write(code)

    exec(_CODE_FRAMEWORK.format(temp_py.name), user_ns)

    if not safe_exec:
        del user_ns['_py5_user_ns']

    py5.reset_py5()

    temp_py.close()

    with open(temp_out.name, read_mode) as f:
        result = f.read()

    temp_out.close()
    return result


__all__ = ['run_sketch', 'run_single_frame_sketch']
