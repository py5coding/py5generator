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
from ipykernel.kernelapp import IPKernelApp
from traitlets import Type, List, Unicode


class Py5App(IPKernelApp):
    name = 'py5-kernel'

    kernel_class = Type('py5_tools.py5_kernel.kernel.Py5Kernel',
                        klass='ipykernel.kernelbase.Kernel').tag(config=True)

    exec_lines = List(Unicode(), [
        'import py5_tools',
        'py5_tools.set_imported_mode(True)',
        'from py5 import *',
    ]).tag(config=True)

    extensions = List(Unicode(), ['py5_tools.magics']).tag(config=True)
