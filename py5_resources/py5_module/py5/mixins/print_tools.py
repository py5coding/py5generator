# *****************************************************************************
#
#   Part of the py5 library
#   Copyright (C) 2020-2021 Jim Schmitz
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
import sys
from typing import Any


class _DefaultPrintStream:

    def init(self):
        pass

    def print(self, text, end='\n', stderr=False):
        print(text, end=end, file=sys.stderr if stderr else sys.stdout)


try:
    _ipython_shell = get_ipython()  # type: ignore


    class _DisplayPubPrintStream:

        def init(self):
            self.display_pub = _ipython_shell.display_pub
            self.parent_header = self.display_pub.parent_header

        def print(self, text, end='\n', stderr=False):
            name = 'stderr' if stderr else 'stdout'

            content = dict(name=name, text=text + end)
            msg = self.display_pub.session.msg('stream', content, parent=self.parent_header)
            self.display_pub.session.send(self.display_pub.pub_socket, msg, ident=b'stream')

except:
    _DisplayPubPrintStream = _DefaultPrintStream


try:
    import ipywidgets as widgets
    from IPython.display import display


    class _WidgetPrintStream:

        def init(self):
            self.out = widgets.Output(layout=dict(
                max_height='200px', overflow='auto'))
            display(self.out)

        def print(self, text, end='\n', stderr=False):
            if stderr:
                self.out.append_stderr(text + end)
            else:
                self.out.append_stdout(text + end)

except:
    _WidgetPrintStream = _DefaultPrintStream


class PrintStream:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._print_stream = None

    def _init_print_stream(self):
        self._print_stream.init()

    # *** BEGIN METHODS ***

    def set_print_stream(self, print_stream: Any) -> None:
        self._print_stream = print_stream

    def println(self, *args, end: str = '\n', stderr: bool = False) -> None:
        self._print_stream.print(' '.join(str(x)
                                 for x in args), end=end, stderr=stderr)
