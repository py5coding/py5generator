# *****************************************************************************
#
#   Part of the py5generator project; generator of the py5 library
#   Copyright (C) 2020-2025 Jim Schmitz
#
#   This project is free software: you can redistribute it and/or modify it
#   under the terms of the GNU General Public License as published by the
#   Free Software Foundation, either version 3 of the License, or (at your
#   option) any later version.
#
#   This project is distributed in the hope that it will be useful, but
#   WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
#   Public License for more details.
#
#   You should have received a copy of the GNU General Public License along
#   with this program. If not, see <https://www.gnu.org/licenses/>.
#
# *****************************************************************************
"""
This code is no longer used but might be pillaged one day to help work with
the documentation example code.

This code was used once to change the doc links when converting from the old
nikola website to the jupyter book website.
"""
import re
from pathlib import Path

from generator.docfiles import Documentation


PY5_API_EN = Path("py5_docs/Reference/api_en/")

DOC_REF_REGEX = re.compile(r":doc:`([^`]*)`", flags=re.MULTILINE | re.DOTALL)

PY5_MAGICS = {"py5drawpdf", "py5drawdxf", "py5drawsvg", "py5draw", "py5bot"}
PY5_TOOLS = {
    "is_jvm_running",
    "add_options",
    "get_classpath",
    "add_classpath",
    "add_jars",
    "screenshot",
    "save_frames",
    "animated_gif",
    "capture_frames",
    "sketch_portal",
    "get_jvm_debug_info",
}
PY5_FUNCTIONS = {
    "get_current_sketch",
    "reset_py5",
    "prune_tracebacks",
    "set_stackprinter_style",
    "create_font_file",
    "render_frame",
    "render_frame_sequence",
    "render",
    "render_sequence",
    "register_image_conversion",
}


problem_files = 0
for docfile in sorted(PY5_API_EN.glob("*.txt")):
    doc = Documentation(docfile)

    changes = set()
    for m in DOC_REF_REGEX.finditer(doc.description):
        restlink = m.group(0)
        ref = m.group(1)

        if (
            ref.startswith("py5font")
            or ref.startswith("py5graphics")
            or ref.startswith("py5image")
            or ref.startswith("py5surface")
            or ref.startswith("py5shader")
            or ref.startswith("py5shape")
        ):
            continue

        if ref in PY5_MAGICS:
            new_ref = f"py5magics_{ref}"
        elif ref in PY5_TOOLS:
            new_ref = f"py5tools_{ref}"
        elif ref in PY5_FUNCTIONS:
            new_ref = f"py5functions_{ref}"
        else:
            new_ref = f"sketch_{ref}"

        new_restlink = f":doc:`{new_ref}`"

        changes.add((restlink, new_restlink))

    if changes:
        print(f"altering {docfile}")
        new_description = doc.description
        for old, new in changes:
            print(old, new)
            new_description = new_description.replace(old, new)
        doc.description = new_description

        doc.write(docfile)
