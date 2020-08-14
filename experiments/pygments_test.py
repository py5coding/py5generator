from pygments import highlight
from pygments.style import Style
from pygments.lexers import PythonLexer
from pygments.filters import NameHighlightFilter, Name
from pygments.token import Token, Keyword, Name, Comment, String, Error, Number, Operator, Generic  # noqa
from pygments.formatters.img import ImageFormatter

import py5


code = """
import py5


def settings():
    py5.size(300, 200, py5.P3D)


def setup():
    py5.rect_mode(py5.CENTER)


def draw():
    for test in range(10):
        py5.rect(py5.random(py5.width), py5.random(py5.height), 10, 10)

"""

lexer = PythonLexer()
lexer.add_filter(
    NameHighlightFilter(
        names=['py5'] + dir(py5),
        tokentype=Name.Other
    )
)


class YourStyle(Style):
    default_style = ''
    styles = {
        # **styles.borland.BorlandStyle.styles,
        **{
            Token: '#000000',
            Name.Other: 'bold #ff2222',
        #    Name.Builtin: '#0f0',
           }
    }
    background_color = '#d0d0d0'


formatter = ImageFormatter(
    style=YourStyle,
    font_name="Liberation Mono",
    line_numbers=True,
    line_number_bg=None,
    line_number_fg='#888888',
    line_number_separator=False,
    font_size=20,
    hl_lines=[1, 4, 5],
    hl_color='#aaaaaa'
)

with open('/tmp/test.png', 'wb') as f:
    highlight(code, lexer, formatter, f)
