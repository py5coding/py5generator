import cmd
import argparse
from pathlib import Path

import py5_tools


parser = argparse.ArgumentParser(description="py5 command tool",
                                 epilog="this is the epilog")


class Py5Cmd(cmd.Cmd):

    def __init__(self):
        super().__init__()
        self._libraries = py5_tools.ProcessingLibraryInfo()

    prompt = 'py5: '
    intro = "Welcome to the py5 command tool."

    def do_run_sketch(self, line):
        if line:
            try:
                py5_tools.run.run_sketch(line)
            except Exception as e:
                print(e)

    def do_get_library(self, line):
        try:
            self._libraries.download_zip('jars', library_name=line)
        except Exception as e:
            print(e)

    def do_EOF(self, line):
        return True


def main():
    # args = parser.parse_args()
    py5cmd = Py5Cmd()
    py5cmd.cmdloop()


if __name__ == '__main__':
    main()
