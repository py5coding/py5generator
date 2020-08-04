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
    size({0}, {1}, SVG, "{2}")


def setup():
{3}

    exit_sketch()
"""


_SVG_FRAMEWORK = """
import py5

with open('{0}', 'r') as f:
    eval(compile(f.read(), '{0}', 'exec'))

py5.run_sketch(block=True)
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
        if py5._py5sketch_used:
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


def draw_svg(code, width, height, user_ns=None, suppress_warnings=False):
    temp_py = tempfile.NamedTemporaryFile(suffix='.py')
    temp_svg = tempfile.NamedTemporaryFile(suffix='.svg')

    with open(temp_py.name, 'w') as f:
        code = _SVG_CODE_TEMPLATE.format(width, height, temp_svg.name,
                                     textwrap.indent(code, ' ' * 4))
        f.write(code)

    import py5
    if py5._py5sketch_used:
        py5.reset_py5()
    from py5.namespace import Py5Namespace
    py5_ns = Py5Namespace(py5, user_ns=user_ns, suppress_warnings=suppress_warnings)
    exec(_SVG_FRAMEWORK.format(temp_py.name), py5_ns)

    temp_py.close()

    with open(temp_svg.name, 'r') as f:
        svg_code = f.read()

    temp_svg.close()
    return svg_code


__all__ = ['run_sketch', 'draw_svg']
