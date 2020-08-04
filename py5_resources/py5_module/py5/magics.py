# TODO: IPython might not be installed
from IPython.display import display, SVG
from IPython.core.magic import Magics, magics_class, cell_magic
from IPython.core import magic_arguments

import py5_tools


@magics_class
class Py5Magics(Magics):

    @cell_magic
    def py5drawsvg(self, line, cell):
        # filename = line.strip()
        # with open(filename, 'r') as f:
        #     svg = f.read()

        # display(SVG(svg))

        width, height = [int(x) for x in line.strip().split()]
        svg = py5_tools.draw_svg(cell, width, height)
        display(SVG(svg))


def load_ipython_extension(ipython):
    # activate with `%load_ext py5.magics`
    ipython.register_magics(Py5Magics)
