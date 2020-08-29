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


_SVG_CODE_TEMPLATE = """
def settings():
    py5.size({0}, {1}, py5.SVG, "{2}")


def setup():
{3}

    py5.exit_sketch()
"""


_HIDDEN_CODE_TEMPLATE = """
def settings():
    py5.size({0}, {1}, py5.HIDDEN)


def setup():
{3}

    py5.save_frame("{2}")
    py5.exit_sketch()
"""


def run_sketch(sketch_path, classpath=None, new_process=False):
    sketch_path = Path(sketch_path)
    if not sketch_path.exists():
        print(f'file {sketch_path} not found')
        return

    def _run_sketch(sketch_path, classpath):
        if not jvm.is_jvm_running():
            if classpath:
                jvm.add_classpath(classpath)
            jvm.add_jars(sketch_path.parent / 'jars')

        import py5
        if not py5.get_current_sketch().is_ready:
            py5.reset_py5()
        sys.path.extend([str(sketch_path.absolute().parent), os.getcwd()])
        from py5.namespace import Py5Namespace
        py5_ns = Py5Namespace(py5)
        exec(_CODE_FRAMEWORK.format(sketch_path), py5_ns)

    if new_process:
        p = Process(target=_run_sketch, args=(sketch_path, classpath))
        p.start()
        return p
    else:
        _run_sketch(sketch_path, classpath)


def run_single_frame_sketch(renderer, code, width, height, user_ns=None, suppress_warnings=False):

    if renderer == 'SVG':
        template = _SVG_CODE_TEMPLATE
        suffix = '.svg'
        read_mode = 'r'
    elif renderer == 'HIDDEN':
        template = _HIDDEN_CODE_TEMPLATE
        suffix = '.png'
        read_mode = 'rb'

    temp_py = tempfile.NamedTemporaryFile(suffix='.py')
    temp_out = tempfile.NamedTemporaryFile(suffix=suffix)

    with open(temp_py.name, 'w') as f:
        code = template.format(width, height, temp_out.name,
                               textwrap.indent(code, ' ' * 4))
        f.write(code)

    import py5
    if not py5.get_current_sketch().is_ready:
        py5.reset_py5()
    from py5.namespace import Py5Namespace
    py5_ns = Py5Namespace(py5, user_ns=user_ns,
                          suppress_warnings=suppress_warnings)
    exec(_CODE_FRAMEWORK.format(temp_py.name), py5_ns)
    # exec(_CODE_FRAMEWORK.format(temp_py.name), user_ns)

    py5.reset_py5()

    temp_py.close()

    with open(temp_out.name, read_mode) as f:
        result = f.read()

    temp_out.close()
    return result


__all__ = ['run_sketch', 'run_single_frame_sketch']
