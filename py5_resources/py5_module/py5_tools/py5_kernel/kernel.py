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
from ipykernel.ipkernel import IPythonKernel
from traitlets import Type, Instance, List

from .shell import Py5Shell

_PY5_HELP_LINKS = [
    {
        'text': 'py5 Reference',
        'url': 'http://py5.ixora.io/reference/'
    },
    {
        'text': 'py5 Tutorials',
        'url': 'http://py5.ixora.io/tutorials/'
    },
]


class Py5Kernel(IPythonKernel):
    shell = Instance('IPython.core.interactiveshell.InteractiveShellABC',
                     allow_none=True)
    shell_class = Type(Py5Shell)

    help_links = List([*IPythonKernel.help_links.default(),
                       *_PY5_HELP_LINKS]).tag(config=True)

    implementation = 'py5'
    implementation_version = '0.3a6.dev0'
    # TODO: set this to modify the 'pygments_lexer' key
    # language_info = {}
