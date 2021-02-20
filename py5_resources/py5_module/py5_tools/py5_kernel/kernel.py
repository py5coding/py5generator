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
from  traitlets import Type, List

from .shell import Py5Shell


class Py5Kernel(IPythonKernel):
    shell = None
    shell_class = Type(Py5Shell)
    # TODO: help_links (append my documentation)
    implementation = 'py5'
    implementation_version = 'current version'
    # TODO: language_info = ???  # I can set the pygments lexer here
