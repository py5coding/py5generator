# *****************************************************************************
#
#   Part of the py5 library
#   Copyright (C) 2020-2024 Jim Schmitz
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
import functools
import platform

_enforce_macos_renderer_problem = True
_first_renderer_opengl = None


def disable_macos_renderer_problem():
    global _enforce_macos_renderer_problem
    _enforce_macos_renderer_problem = False


MESSAGE = """Sorry, but you can't use the OpenGL renderer here. Doing so would likely cause Python to crash.

Here's the problem: On macOS on Intel CPU machines, py5 seems to crash when you use an OpenGL renderer in an IPython or Jupyter session if the first Sketch used the default renderer. Sorry if that sounds crazy, but it's true. This is caused by problems in native macOS code.

If you want to use the OpenGL renderer here, you should restart IPython or this Jupyter Notebook and run the code again. If you really need to mix Java2D and OpenGL renderers together, you should make sure the first Sketch executed is an OpenGL Sketch. For convenience, you use the following code to open a quick Sketch right after importing py5. This will ensure the first Sketch is an OpenGL Sketch, eliminating the problem entirely:

    import py5

    from py5 import test
    test.test_p2d()

If you'd like to disable this safety feature, run the following code:

    from py5 import macos_renderer_problem
    disable_macos_renderer_problem()

It actually would be helpful to the py5 maintainers if you would disable this safety feature and try running your code to see if it actually does crash. If you do that, please report your findings to the below discussion thread. Include your macOS version and CPU type (Intel or Apple Silicon). Your feedback here will help us understand the problem better and better calibrate this safety feature.

<insert link to discussion thread>
"""


def _macos_renderer_problem(f):
    @functools.wraps(f)
    def decorated(self_, *args):
        global _first_renderer_opengl
        if (
            _enforce_macos_renderer_problem
            and platform.system() == "Darwin"
            and self_._environ.in_ipython_session
        ):
            if _first_renderer_opengl is None:
                # This is the first Sketch. Record if the renderer is OpenGL
                if len(args) >= 2 and args[2] in [
                    "processing.opengl.PGraphics2D",
                    "processing.opengl.PGraphics3D",
                ]:
                    _first_renderer_opengl = True
                else:
                    _first_renderer_opengl = False
            elif _first_renderer_opengl is False:
                # The first Sketch was not OpenGL. OpenGL is not allowed now.
                if len(args) >= 2 and args[2] in [
                    "processing.opengl.PGraphics2D",
                    "processing.opengl.PGraphics3D",
                ]:
                    raise RuntimeError(MESSAGE)

        f(self_, *args)

    return decorated
