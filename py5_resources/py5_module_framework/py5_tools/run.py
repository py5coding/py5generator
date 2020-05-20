import sys
import os
import builtins
from multiprocessing import Process
from pathlib import Path

from . import jvm


_CODE_FRAMEWORK = """
import py5
from py5 import *

with open('{0}', 'r') as f:
    eval(compile(f.read(), '{0}', 'exec'))

py5.run_sketch(block=True)
"""


class Py5Namespace(dict):

    def __init__(self, py5):
        super().__init__()
        self._py5 = py5

    def __getitem__(self, item):
        try:
            return super().__getitem__(item)
        except KeyError:
            if hasattr(self._py5, item):
                return getattr(self._py5, item)
            elif hasattr(builtins, item):
                return getattr(builtins, item)
            else:
                raise KeyError(f'{item} not found')


def run_sketch(sketch_path, classpath=None, new_process=False):
    sketch_path = Path(sketch_path)
    if not sketch_path.exists():
        print(f'file {sketch_path} not found')
        return

    def _run_sketch(sketch_path, classpath):
        if classpath:
            jvm.add_classpath(classpath)
        jvm.add_jars(sketch_path.parent / 'jars')

        import py5
        sys.path.extend([str(sketch_path.absolute().parent), os.getcwd()])
        py5_ns = Py5Namespace(py5)
        exec(_CODE_FRAMEWORK.format(sketch_path), py5_ns)

    if new_process:
        p = Process(target=_run_sketch, args=(sketch_path, classpath))
        p.start()
        return p
    else:
        _run_sketch(sketch_path, classpath)


__all__ = ['run_sketch']
