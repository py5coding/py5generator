from io import BytesIO

from PIL import Image

from pygments import highlight
from pygments.style import Style
from pygments.lexers import PythonLexer
from pygments.filters import NameHighlightFilter, Name
from pygments.token import Token, Keyword, Name, Comment, String, Error, Number, Operator, Generic  # noqa
from pygments.formatters.img import ImageFormatter


class HighlightPy5Style(Style):
    default_style = ''
    styles = {
        # **styles.borland.BorlandStyle.styles,
        **{
            Token: '#000000',
            Name.Other: 'bold #ff2222',
            # Name.Builtin: '#0f0',
        }
    }
    background_color = '#d0d0d0'


class CodeConverter:

    def __init__(self):
        self.lexer = self._create_lexer()

    def _create_lexer(self):
        lexer = PythonLexer()
        import py5  # noqa
        lexer.add_filter(
            NameHighlightFilter(
                names=['py5'] + dir(py5),
                tokentype=Name.Other
            )
        )
        return lexer

    def _create_formatter(self, hl_lines=None):
        formatter = ImageFormatter(
            style=HighlightPy5Style,
            font_name="Liberation Mono",
            line_numbers=True,
            line_number_bg=None,
            line_number_fg='#888888',
            line_number_separator=False,
            font_size=25,
            hl_lines=hl_lines,
            hl_color='#aaaaaa'
        )
        return formatter

    def convert(self, code, hl_lines=None, filename=None):
        hl_lines = hl_lines or []
        formatter = self._create_formatter(hl_lines)
        result = highlight(code, self.lexer, formatter)
        if filename:
            with open(filename, 'wb') as f:
                f.write(result)
            return filename
        else:
            return Image.open(BytesIO(result))


code = """
import py5


def settings():
    py5.size(300, 200, py5.P3D)


def setup():
    py5.rect_mode(py5.CENTER)


def draw():
    for _ in range(10):
        x = py5.random(py5.width)
        y = py5.random(py5.height)
        py5.rect(x, y, 10, 10)

############################################################
"""


converter = CodeConverter()
