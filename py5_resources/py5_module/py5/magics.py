from IPython.display import display, SVG
from IPython.core.magic import Magics, magics_class, cell_magic
from IPython.core.magic_arguments import magic_arguments, argument, parse_argstring

import py5_tools


_unspecified = object()


@magics_class
class Py5Magics(Magics):

    @magic_arguments()
    @argument('width', type=int, help='width of SVG drawing')
    @argument('height', type=int, help='height of SVG drawing')
    @argument('--no_warnings', dest='suppress_warnings', action='store_true',
              help="suppress name conflict warnings")
    @cell_magic
    def py5drawsvg(self, line, cell):
        """Create an SVG image with py5 and embed result in the notebook.

        Code used in this cell can reference functions and variables defined in
        other cells. This will create a name conflict if your functions and
        variables overlap with py5's. The name conflict may cause an error. If
        such a conflict is detected, py5 will issue you a helpful warning to
        alert you to the potential problem. You can surpress warnings with the
        --no_warnings flag.
        """
        args = parse_argstring(self.py5drawsvg, line)
        svg = py5_tools.draw_svg(
            cell, args.width, args.height, user_ns=self.shell.user_ns,
            suppress_warnings=args.suppress_warnings)
        if svg:
            display(SVG(svg))


def load_ipython_extension(ipython):
    ipython.register_magics(Py5Magics)
