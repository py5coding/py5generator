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
from __future__ import annotations

import os
import sys
import platform
import subprocess
from pathlib import Path

from typing import Any, Union  # noqa


import jpype


_PY5_REQUIRED_JAVA_VERSION = 17

_options = []
_classpath = []


def is_jvm_running() -> bool:
    """$module_Py5Tools_is_jvm_running"""
    return jpype.isJVMStarted()


def _check_jvm_running() -> None:
    if jpype.isJVMStarted():
        raise RuntimeError("the jvm is already running")


def add_options(*options: list[str]) -> None:
    """$module_Py5Tools_add_options"""
    _check_jvm_running()
    _options.extend(options)


def get_classpath() -> str:
    """$module_Py5Tools_get_classpath"""
    if jpype.isJVMStarted():
        return jpype.getClassPath()
    else:
        return ':'.join(str(p) for p in _classpath)


def add_classpath(classpath: Union[Path, str]) -> None:
    """$module_Py5Tools_add_classpath"""
    _check_jvm_running()
    if not isinstance(classpath, Path):
        classpath = Path(classpath)
    _classpath.append(classpath.absolute())


def add_jars(path: Union[Path, str]) -> None:
    """$module_Py5Tools_add_jars"""
    _check_jvm_running()
    if not isinstance(path, Path):
        path = Path(path)
    if path.exists():
        for jarfile in path.glob("**/*.[Jj][Aa][Rr]"):
            _classpath.append(jarfile.absolute())


def get_jvm_debug_info() -> dict[str, Any]:
    """$module_Py5Tools_get_jvm_debug_info"""
    out = dict()
    out['JAVA_HOME environment variable'] = os.environ.get('JAVA_HOME', '<not set>')
    out['jvm version'] = jpype.getJVMVersion()
    out['default jvm path'] = jpype.getDefaultJVMPath()
    return out


def _evaluate_java_version(path, n=1):
    path = Path(path)
    for _ in range(n):
        try:
            if (java_path := path / 'bin' / ('java.exe' if platform.system() == 'Windows' else 'java')).exists():
                stderr = subprocess.run(
                    [str(java_path), "-XshowSettings:properties"], stderr=subprocess.PIPE
                ).stderr.decode("utf-8").splitlines()
                for l in stderr:
                    if l.find('java.version =') >= 0:
                        return int(l.split('=')[1].split('.', maxsplit=1)[0])
            path = path.parent
        except Exception:
            break

    return 0


def _start_jvm() -> None:
    jpype_exception = None
    default_jvm_path = None

    if hasattr(sys, '_MEIPASS'):
        if (pyinstaller_java_home := Path(getattr(sys, '_MEIPASS')) / 'JAVA_HOME').exists():
            os.environ['JAVA_HOME'] = str(pyinstaller_java_home)

    try:
        default_jvm_path = jpype.getDefaultJVMPath()
    except Exception as e:
        jpype_exception = e

    if 'JAVA_HOME' not in os.environ and (default_jvm_path is None or _evaluate_java_version(default_jvm_path, n=4) < _PY5_REQUIRED_JAVA_VERSION):
        possible_jdks = []
        if (dot_jdk := Path(Path.home(), '.jdk')).exists():
            possible_jdks.extend(dot_jdk.glob('*/Contents/Home/' if platform.system() == 'Darwin' else '*'))
        if (dot_jre := Path(Path.home(), '.jre')).exists():
            possible_jdks.extend(dot_jre.glob('*/Contents/Home/' if platform.system() == 'Darwin' else '*'))

        for d in possible_jdks:
            if _evaluate_java_version(d) >= _PY5_REQUIRED_JAVA_VERSION:
                os.environ['JAVA_HOME'] = str(d)
                try:
                    default_jvm_path = jpype.getDefaultJVMPath()
                    jpype_exception = None
                except Exception as e:
                    jpype_exception = e
                break

    for c in _classpath:
        jpype.addClassPath(c)

    if jpype_exception is not None:
        raise jpype_exception

    jpype.startJVM(default_jvm_path, *_options, convertStrings=False)


__all__ = ['is_jvm_running', 'add_options', 'get_classpath',
           'add_classpath', 'add_jars', 'get_jvm_debug_info']
