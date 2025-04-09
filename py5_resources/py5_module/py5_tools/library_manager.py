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

from .libraries import ProcessingLibraryInfo

# TODO: change this to someplace more suitable
STORAGE_DIR = Path("/tmp/py5-library-storage")
STORAGE_DIR.mkdir(exist_ok=True)

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

    def get_library(self, library_name):
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


def download_processing_library(library_name: str) -> bool:
    # TODO: add to reference docs
    """module_Py5Tools_download_processing_library"""
    global _library_manager
    if _library_manager is None:
        _library_manager = ProcessingLibraryManager()

    return _library_manager.get_library(library_name)


__all__ = ["download_processing_library"]
