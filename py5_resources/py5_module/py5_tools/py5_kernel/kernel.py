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
from IPython.core.interactiveshell import InteractiveShell
from traitlets import Type

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
    shell = None
    shell_class = Type(Py5Shell)
    help_links = [*IPythonKernel.help_links.default(), *_PY5_HELP_LINKS]
    implementation = 'py5'
    implementation_version = 'current version'
    # TODO: language_info = ???  # I can set the pygments lexer here
