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
import os

from pathlib import Path
from typing import Any, Union, List, Dict  # noqa


import jpype


_options = []
_classpath = []


def is_jvm_running() -> bool:
    """$module_Py5Tools_is_jvm_running"""
    return jpype.isJVMStarted()


def _check_jvm_running() -> None:
    if jpype.isJVMStarted():
        raise RuntimeError("the jvm is already running")


def add_options(*options: List[str]) -> None:
    """$module_Py5Tools_add_options"""
    _check_jvm_running()
    _options.extend(options)


def get_classpath() -> str:
    """$module_Py5Tools_get_classpath"""
    return jpype.getClassPath()


def add_classpath(classpath: Union[Path, str]) -> None:
    """$module_Py5Tools_add_classpath"""
    _check_jvm_running()
    if not isinstance(classpath, Path):
        classpath = Path(classpath)
    jpype.addClassPath(classpath.absolute())


def add_jars(path: Union[Path, str]) -> None:
    """$module_Py5Tools_add_jars"""
    _check_jvm_running()
    if not isinstance(path, Path):
        path = Path(path)
    if path.exists():
        for jarfile in path.glob("**/*.[Jj][Aa][Rr]"):
            jpype.addClassPath(jarfile.absolute())


def get_jvm_debug_info() -> Dict[str, Any]:
    """$module_Py5Tools_get_jvm_debug_info"""
    out = dict()
    out['JAVA_HOME environment variable'] = os.environ.get('JAVA_HOME', '<not set>')
    out['jvm version'] = jpype.getJVMVersion()
    out['default jvm path'] = jpype.getDefaultJVMPath()
    return out


def _start_jvm() -> None:
    for c in _classpath:
        print(f'adding {c}')
        jpype.addClassPath(c)
    jpype.startJVM(*_options, convertStrings=False)


__all__ = ['is_jvm_running', 'add_options', 'get_classpath', 'add_classpath', 'add_jars', 'get_jvm_debug_info']
