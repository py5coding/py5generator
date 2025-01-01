# *****************************************************************************
#
#   Part of the py5 library
#   Copyright (C) 2020-2025 Jim Schmitz
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
from .sketch import Sketch


class CreateFontTool(Sketch):
    def __init__(
        self, font_name, font_size, filename=None, characters=None, pause=True
    ):
        super().__init__()
        self.font_name = font_name
        self.font_size = font_size
        self.pause = pause
        self.filename = filename or f"{font_name}-{font_size}.vlw"
        self.characters = characters

    def __str__(self) -> str:
        return (
            f"CreateFontTool(font_name='"
            + self.font_name
            + "', font_size="
            + str(self.font_size)
            + ")"
        )

    def __repr__(self) -> str:
        return self.__str__()

    def settings(self):
        self.size(400, 100, self.P2D)

    def setup(self):
        font = self.create_font(self.font_name, self.font_size)
        self.text_align(self.CENTER)

        self.background(0)
        self.fill(0)

        self.text_font(font)
        characters = self.characters or "".join(font.CHARSET)
        self.text(characters, self.width / 2, self.height / 2)

        os = self._instance.createOutput(str(self.filename))
        font._instance.save(os)
        os.close()

        self.fill(255)
        msg = str(font.get_glyph_count()) + " glyphs written to " + self.filename
        self.translate(self.width / 2, self.height / 2)
        self.scale(0.95 * self.width / self.text_width(msg))
        self.text(msg, 0, 0)

        if not self.pause:
            self.exit_sketch()


def create_font_file(
    font_name: str,
    font_size: int,
    filename: str = None,
    characters: str = None,
    pause: bool = True,
):
    """$module_Py5Functions_create_font_file"""
    vlw_creator = CreateFontTool(
        font_name, font_size, filename=filename, characters=characters, pause=pause
    )
    vlw_creator.run_sketch(block=pause)
