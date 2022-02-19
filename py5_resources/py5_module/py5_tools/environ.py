# *****************************************************************************
#
#   Part of the py5 library
#   Copyright (C) 2020-2022 Jim Schmitz
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


in_ipython_session = None
ipython_shell = None
in_jupyter_zmq_shell = None


# this examine() function delays the execution of this code until when
# sketch.py gets imported, which for some reason is necessary to get the py5
# kernel to work correctly

def examine():
    global in_ipython_session, ipython_shell, in_jupyter_zmq_shell

    try:
        __IPYTHON__  # type: ignore
        in_ipython_session = True
        from ipykernel.zmqshell import ZMQInteractiveShell
        ipython_shell = get_ipython()  # type: ignore
        in_jupyter_zmq_shell = isinstance(ipython_shell, ZMQInteractiveShell)
    except NameError:
        in_ipython_session = False
        ipython_shell = None
        in_jupyter_zmq_shell = False
