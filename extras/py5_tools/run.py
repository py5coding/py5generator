import builtins
from pathlib import Path

import jnius_config


_CODE_FRAMEWORK = """
import py5
from py5 import *

{0}

py5.run_sketch(local_dict=locals(), block=True)
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


def run_sketch(sketch_path, classpath=None):
    sketch_path = Path(sketch_path)
    if not sketch_path.exists():
        print(f'file {sketch_path} not found')
        return

    with open(sketch_path, 'r') as f:
        code = f.read()

    if classpath:
        jnius_config.add_classpath(classpath)

    sketch_parent_jars = sketch_path.parent / 'jars'
    if sketch_parent_jars.exists():
        for jarfile in sketch_parent_jars.glob("**/*.jar"):
            jnius_config.add_classpath(str(jarfile))

    import py5
    py5_ns = Py5Namespace(py5)
    exec(_CODE_FRAMEWORK.format(code), py5_ns)
