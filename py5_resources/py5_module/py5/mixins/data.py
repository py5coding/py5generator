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

import json
import re
from pathlib import Path
from typing import Any, Union, overload
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
                raise RuntimeError('Unable to download JSON URL: ' + response.reason)
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
                raise RuntimeError('Unable to find JSON file ' + str(json_path))

    def save_json(self, json_data: Any, filename: Union[str, Path], **kwargs: dict[str, Any]) -> None:
        """$class_Sketch_save_json"""
        path = Path(filename)
        if not path.is_absolute():
            cwd = self.sketch_path()
            path = cwd / filename
        with open(path, 'w') as f:
            json.dump(json_data, f, **kwargs)

    @classmethod
    def parse_json(cls, serialized_json: Any, **kwargs: dict[str, Any]) -> Any:
        """$class_Sketch_parse_json"""
        return json.loads(serialized_json, **kwargs)
