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
from pathlib import Path

from .constants import PY5_HOME
from .libraries import ProcessingLibraryInfo

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
            f.write(f"dir={info['dir']}\n")

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

    def installed_libraries(self):
        return [f.stem for f in STORAGE_DIR.glob("*.txt")]

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
            print(f"Library {library_name} not found")
            return
        if len(info) > 1:
            print(f"Library {library_name} is ambiguous")
            return

        info = info[0]

        stored_info = self._load_library_info(library_name)
        if stored_info:
            if stored_info["version"] == info["version"]:
                return
            print(f"Library {library_name} is outdated. Updating...")

        try:
            parts0 = self._libraries.download_zip(
                STORAGE_DIR, library_name=library_name
            )
            info["dir"] = parts0
            self._store_library_info(library_name, info)
            return self._load_library_info(library_name)
        except Exception as e:
            print(f"Failed to download library {library_name}: {e}")
            return


def library_storage_dir() -> Path:
    """module_Py5Tools_processing_library_storage_dir"""
    return STORAGE_DIR


def installed_libraries() -> list[str]:
    # TODO: add to reference docs
    """module_Py5Tools_processing_installed_libraries"""
    global _library_manager
    if _library_manager is None:
        _library_manager = ProcessingLibraryManager()

    return _library_manager.installed_libraries()


def check_library(library_name: str) -> bool:
    # TODO: add to reference docs
    """module_Py5Tools_processing_check_library"""
    global _library_manager
    if _library_manager is None:
        _library_manager = ProcessingLibraryManager()

    return _library_manager.check_library(library_name)


def download_library(library_name: str) -> bool:
    # TODO: add to reference docs
    """module_Py5Tools_processing_download_library"""
    global _library_manager
    if _library_manager is None:
        _library_manager = ProcessingLibraryManager()

    return _library_manager.get_library(library_name)


__all__ = [
    "check_library",
    "download_library",
    "installed_libraries",
    "library_storage_dir",
]


def __dir__():
    return __all__
