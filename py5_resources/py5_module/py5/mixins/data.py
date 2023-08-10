# *****************************************************************************
#
#   Part of the py5 library
#   Copyright (C) 2020-2023 Jim Schmitz
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

import json
import pickle
import re
from pathlib import Path
from typing import Any, Union

import requests


class DataMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # *** BEGIN METHODS ***
    def load_json(self, json_path: Union[str, Path], **kwargs: dict[str, Any]) -> Any:
        """$class_Sketch_load_json"""
        if isinstance(json_path, str) and re.match(r'https?://', json_path.lower()):
            response = requests.get(json_path, **kwargs)
            if response.status_code == 200:
                return response.json()
            else:
                raise RuntimeError(
                    'Unable to download JSON URL: ' + response.reason)
        else:
            path = Path(json_path)
            if not path.is_absolute():
                cwd = self.sketch_path()
                if (cwd / 'data' / json_path).exists():
                    path = cwd / 'data' / json_path
                else:
                    path = cwd / json_path
            if path.exists():
                with open(path, 'r', encoding='utf8') as f:
                    return json.load(f, **kwargs)
            else:
                raise RuntimeError(
                    'Unable to find JSON file ' + str(json_path))

    def save_json(self, json_data: Any, filename: Union[str, Path], **kwargs: dict[str, Any]) -> None:
        """$class_Sketch_save_json"""
        path = Path(filename)
        if not path.is_absolute():
            cwd = self.sketch_path()
            path = cwd / filename
        if not path.parent.exists():
            path.parent.mkdir(parents=True)
        with open(path, 'w') as f:
            json.dump(json_data, f, **kwargs)

    @classmethod
    def parse_json(cls, serialized_json: Any, **kwargs: dict[str, Any]) -> Any:
        """$class_Sketch_parse_json"""
        return json.loads(serialized_json, **kwargs)

    def load_strings(self, string_path: Union[str, Path], **kwargs: dict[str, Any]) -> list[str]:
        """$class_Sketch_load_strings"""
        if isinstance(string_path, str) and re.match(r'https?://', string_path.lower()):
            response = requests.get(string_path, **kwargs)
            if response.status_code == 200:
                return response.text.splitlines()
            else:
                raise RuntimeError(
                    'Unable to download URL: ' + response.reason)
        else:
            path = Path(string_path)
            if not path.is_absolute():
                cwd = self.sketch_path()
                if (cwd / 'data' / string_path).exists():
                    path = cwd / 'data' / string_path
                else:
                    path = cwd / string_path
            if path.exists():
                with open(path, 'r', encoding='utf8') as f:
                    return f.read().splitlines()
            else:
                raise RuntimeError('Unable to find file ' + str(string_path))

    def save_strings(self, string_data: list[str], filename: Union[str, Path], *, end: str = '\n') -> None:
        """$class_Sketch_save_strings"""
        path = Path(filename)
        if not path.is_absolute():
            path = self.sketch_path() / filename
        if not path.parent.exists():
            path.parent.mkdir(parents=True)
        with open(path, 'w') as f:
            f.write(end.join(str(s) for s in string_data))

    def load_bytes(self, bytes_path: Union[str, Path], **kwargs: dict[str, Any]) -> bytearray:
        """$class_Sketch_load_bytes"""
        if isinstance(bytes_path, str) and re.match(r'https?://', bytes_path.lower()):
            response = requests.get(bytes_path, **kwargs)
            if response.status_code == 200:
                return bytearray(response.content)
            else:
                raise RuntimeError(
                    'Unable to download URL: ' + response.reason)
        else:
            path = Path(bytes_path)
            if not path.is_absolute():
                cwd = self.sketch_path()
                if (cwd / 'data' / bytes_path).exists():
                    path = cwd / 'data' / bytes_path
                else:
                    path = cwd / bytes_path
            if path.exists():
                with open(path, 'rb') as f:
                    return bytearray(f.read())
            else:
                raise RuntimeError('Unable to find file ' + str(bytes_path))

    def save_bytes(self, bytes_data: Union[bytes, bytearray], filename: Union[str, Path]) -> None:
        """$class_Sketch_save_bytes"""
        path = Path(filename)
        if not path.is_absolute():
            path = self.sketch_path() / filename
        if not path.parent.exists():
            path.parent.mkdir(parents=True)
        with open(path, 'wb') as f:
            f.write(bytes_data)

    def load_pickle(self, pickle_path: Union[str, Path]) -> Any:
        """$class_Sketch_load_pickle"""
        path = Path(pickle_path)
        if not path.is_absolute():
            cwd = self.sketch_path()
            if (cwd / 'data' / pickle_path).exists():
                path = cwd / 'data' / pickle_path
            else:
                path = cwd / pickle_path
        if path.exists():
            with open(path, 'rb') as f:
                return pickle.load(f)
        else:
            raise RuntimeError('Unable to find file ' + str(pickle_path))

    def save_pickle(self, obj: Any, filename: Union[str, Path]) -> None:
        """$class_Sketch_save_pickle"""
        path = Path(filename)
        if not path.is_absolute():
            path = self.sketch_path() / filename
        if not path.parent.exists():
            path.parent.mkdir(parents=True)
        with open(path, 'wb') as f:
            pickle.dump(obj, f)
