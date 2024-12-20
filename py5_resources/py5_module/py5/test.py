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
from pathlib import Path

from .sketch import Sketch


class Test(Sketch):

    def __init__(self, renderer, renderer_name):
        super().__init__()
        self.renderer = renderer
        self.renderer_name = renderer_name

    def settings(self):
        self.size(150, 150, self.renderer)

    def setup(self):
        self.text_align(self.CENTER, self.CENTER)
        self.text_size(20)
        self.image_mode(self.CENTER)
        self.fill(24)

        self.logo = self.load_image(
            Path(__file__).parent.parent / "py5_tools/resources/logo-64x64.png"
        )

    def draw(self):
        self.background(240)
        self.image(self.logo, self.width / 2, 50)
        self.text("testing " + self.renderer_name, self.width / 2, 125)

        if self.frame_count == 60:
            self.exit_sketch()


def test_java2d():
    test = Test(Sketch.JAVA2D, "JAVA2D")
    test.run_sketch()


def test_p2d():
    test = Test(Sketch.P2D, "P2D")
    test.run_sketch()


def test_p3d():
    test = Test(Sketch.P3D, "P3D")
    test.run_sketch()
