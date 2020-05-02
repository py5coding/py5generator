import builtins
import argparse
from pathlib import Path

import py5


parser = argparse.ArgumentParser(description="Execute py5 sketch",
                                 epilog="this is the epilog")
parser.add_argument(action='store', dest='sketch_path', help='path to py5 sketch')
parser.add_argument('-c', '--classpath', action='store', dest='classpath',
                    help='extra directories to add to classpath')


CODE_FRAMEWORK = """
import py5
from py5 import *

{0}

py5.run_sketch(local_dict=locals(), block=True)
"""


class Py5Namespace(dict):

    def __getitem__(self, item):
        try:
            return super().__getitem__(item)
        except KeyError:
            if hasattr(py5, item):
                return getattr(py5, item)
            elif hasattr(builtins, item):
                return getattr(builtins, item)
            else:
                raise KeyError(f'{item} not found')


def run_sketch(sketch_path):
    sketch_path = Path(sketch_path)
    if not sketch_path.exists():
        print(f'file {sketch_path} not found')
        return

    with open(sketch_path, 'r') as f:
        code = f.read()

    py5_ns = Py5Namespace()
    exec(CODE_FRAMEWORK.format(code), py5_ns)


def main():
    args = parser.parse_args()
    run_sketch(args.sketch_path)


if __name__ == '__main__':
    main()
