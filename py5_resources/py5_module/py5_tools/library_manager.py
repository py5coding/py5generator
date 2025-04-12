# *****************************************************************************
#
#   Part of the py5 library
#   Copyright (C) 2020-2025 Jim Schmitz
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
import datetime as dt
import os
import platform
from pathlib import Path

from .libraries import ProcessingLibraryInfo

if not (PY5_HOME := os.environ.get("PY5_HOME")):
    if platform.system() == "Windows":
        PY5_HOME = Path.home() / "AppData" / "Local" / "py5"
    else:
        PY5_HOME = Path.home() / ".cache" / "py5"

STORAGE_DIR = Path(PY5_HOME) / "processing-libraries"
STORAGE_DIR.mkdir(parents=True, exist_ok=True)

_library_manager = None


class ProcessingLibraryManager:

    def __init__(self):
        self._libraries = ProcessingLibraryInfo()

    def _store_library_info(self, library_name, info):
        info_file = STORAGE_DIR / f"{library_name}.txt"
        current_date = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(info_file, "w") as f:
            f.write(f"name={info['name']}\n")
            f.write(f"version={info['version']}\n")
            f.write(f"prettyVersion={info['prettyVersion']}\n")
            f.write(f"downloadDate={current_date}\n")

    def _load_library_info(self, library_name):
        info_file = STORAGE_DIR / f"{library_name}.txt"
        if not info_file.exists():
            return None

        with open(info_file, "r") as f:
            lines = f.readlines()

        info = {}
        for line in lines:
            key, value = line.strip().split("=", maxsplit=1)
            if key == "version":
                info[key] = int(value)
            if key == "downloadDate":
                info[key] = dt.datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
            else:
                info[key] = value

        return info

    def check_library(self, library_name):
        """Check if a library is available and up to date.

        Args:
            library_name (str): The name of the library to check.

        Returns:
            bool: True if the library is available and up to date, False otherwise.
        """
        info = self._libraries.get_library_info(library_name=library_name)

        if len(info) == 0:
            return False
        if len(info) > 1:
            raise ValueError(f"Library {library_name} is ambiguous")

        info = info[0]

        stored_info = self._load_library_info(library_name)
        if stored_info and stored_info["version"] == info["version"]:
            return True
        else:
            return False

    def get_library(self, library_name):
        """Download a library if it is not already downloaded or is outdated.

        Args:
            library_name (str): The name of the library to download.

        Returns:
            dict: Information about the downloaded library.
        """
        info = self._libraries.get_library_info(library_name=library_name)

        if len(info) == 0:
            raise ValueError(f"Library {library_name} not found")
        if len(info) > 1:
            raise ValueError(f"Library {library_name} is ambiguous")

        info = info[0]

        stored_info = self._load_library_info(library_name)
        if stored_info:
            if stored_info["version"] == info["version"]:
                return
            print(f"Library {library_name} is outdated. Updating...")

        try:
            self._libraries.download_zip(STORAGE_DIR, library_name=library_name)
        except Exception as e:
            raise RuntimeError(f"Failed to download library {library_name}: {e}")
        finally:
            self._store_library_info(library_name, info)
            return self._load_library_info(library_name)


def get_processing_library_storage_dir() -> Path:
    return STORAGE_DIR


def check_processing_library(library_name: str) -> bool:
    # TODO: add to reference docs
    """module_Py5Tools_check_processing_library"""
    global _library_manager
    if _library_manager is None:
        _library_manager = ProcessingLibraryManager()

    return _library_manager.check_library(library_name)


def download_processing_library(library_name: str) -> bool:
    # TODO: add to reference docs
    """module_Py5Tools_download_processing_library"""
    global _library_manager
    if _library_manager is None:
        _library_manager = ProcessingLibraryManager()

    return _library_manager.get_library(library_name)


__all__ = [
    "check_processing_library",
    "download_processing_library",
    "get_processing_library_storage_dir",
]
