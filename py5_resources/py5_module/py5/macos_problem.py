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

_enforce_safety_check = True
_first_renderer_opengl = None


def disable_safety_check():
    global _enforce_safety_check
    _enforce_safety_check = False


MESSAGE = """Sorry, but you can't use the OpenGL renderer here. Doing so would likely cause Python to crash.

Here's the problem: On macOS machines with Intel CPUs, py5 seems to crash when you use an OpenGL renderer in an IPython or Jupyter session if the first Sketch run in that Python session used the default renderer. Sorry if that sounds crazy. This is an unfortunate side effect of a code fix that actually solved a lot of py5 problems for all macOS users.

The root problem is somewhere in native macOS code that py5 depends on. Maybe we will find a better workaround in the future. Until then, you get this message.

If you want to use the OpenGL renderer right now, you should restart IPython or this Jupyter Notebook and run your code again. If you really need to mix Java2D and OpenGL renderers together in one Python session, you should make sure that the first Sketch executed is an OpenGL Sketch. For convenience, you use the following code to open a quick Sketch right after importing py5. This will ensure the first Sketch is always an OpenGL Sketch, eliminating the problem entirely:

    import py5

    from py5 import test
    test.test_p2d()

If you'd like to disable this safety feature, run the following code:

    from py5 import macos_problem
    macos_problem.disable_safety_check()

It actually would be helpful to the py5 maintainers if you would disable this safety feature right now and try running your code to see if Python actually does crash. If you do this test, please report your findings to the below discussion thread. Include your macOS version and CPU type (Intel or Apple Silicon). Your feedback here will help us understand the problem better and better calibrate this safety feature.

<insert link to discussion thread>

Sorry again for the weird limitation. We're doing our best to make py5 as stable as possible. Thanks for your understanding.
"""


def _macos_safety_check(f):
    @functools.wraps(f)
    def decorated(self_, *args):
        global _first_renderer_opengl
        if (
            _enforce_safety_check
            and platform.system() == "Darwin"
            and platform.processor() == "i386"
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
