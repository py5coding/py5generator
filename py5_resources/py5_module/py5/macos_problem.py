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

from py5_tools.environ import Environment

_environ = Environment()

_enforce_safety_check = (
    platform.system() == "Darwin"
    and platform.processor() == "i386"
    and _environ.in_ipython_session
)
_first_renderer_opengl = None


def disable_safety_check():
    global _enforce_safety_check
    _enforce_safety_check = False


def enable_safety_check():
    global _enforce_safety_check
    _enforce_safety_check = True


OPENGL_RENDERERS = [
    "processing.opengl.PGraphics2D",
    "processing.opengl.PGraphics3D",
]

MESSAGE = """Sorry, but you can't use an OpenGL renderer in your Sketch right now. Doing so might cause Python to crash.

Here's the problem: On macOS machines with Intel CPUs, py5 seems to crash when you use an OpenGL renderer in an IPython or Jupyter session if the first Sketch run in that Python session used the default (JAVA2D) renderer. Sorry if that sounds crazy. This is an unfortunate side effect of an important code change that actually significantly improved py5 for all macOS users.

The root issue is somewhere in native macOS code that py5 depends on. Hopefully in the future we will find a real fix or a better workaround.

If you want to use the OpenGL renderer right now, you should restart IPython or this Jupyter Notebook and run your code again. If you really need to mix Java2D and OpenGL renderers together in one Python session, you should make sure that the first Sketch executed is always an OpenGL Sketch. For convenience, you can use the following code to open a quick Sketch right after importing py5. This will ensure the first Sketch is always an OpenGL Sketch, eliminating the problem (and this warning) entirely:

    import py5

    from py5 import test
    test.test_p2d()

If you'd like to disable this safety feature (and risk Python crashing), use the following code:

    import py5

    from py5 import macos_problem
    macos_problem.disable_safety_check()

It actually would be helpful to the py5 maintainers if you would disable the safety feature just once to test if the problematic sequence of events does in fact cause Python to crash on your machine. To run this test, use the following code in Jupyter, with each line of code in a separate cell:

    from py5 import macos_problem, test

    macos_problem.disable_safety_check()

    # open a Sketch with the default renderer
    test.test_java2d()

    # does this cell cause a crash?
    test.test_p2d()

If you do this test, please report your findings in the below discussion thread. Include your macOS version and CPU type. (For your convenience, this information will be displayed at the end of this message.) Your feedback will help us understand the problem better and more accurately calibrate this crash protection feature.

<insert link to discussion thread>

Sorry again for the weird limitation. We're doing our best to make py5 as stable as possible. Thank you for your understanding.
"""


def _macos_safety_check(f):
    @functools.wraps(f)
    def decorated(self_, *args):
        global _first_renderer_opengl
        if _enforce_safety_check:
            if _first_renderer_opengl is None:
                # This is the first Sketch. Record if the renderer is OpenGL.
                if len(args) >= 2 and args[2] in OPENGL_RENDERERS:
                    _first_renderer_opengl = True
                else:
                    _first_renderer_opengl = False

            elif _first_renderer_opengl is False:
                # The first Sketch was not OpenGL. OpenGL is not allowed now.
                if len(args) >= 2 and args[2] in OPENGL_RENDERERS:
                    self_.println(MESSAGE)
                    self_.println("macOS version:", platform.mac_ver()[0])
                    self_.println("macOS CPU type:", platform.processor())
                    raise RuntimeError(
                        "Halting Sketch startup to prevent Python from crashing"
                    )

        f(self_, *args)

    return decorated
