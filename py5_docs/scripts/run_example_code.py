# *****************************************************************************
#
#   Part of the py5generator project; generator of the py5 library
#   Copyright (C) 2020-2021 Jim Schmitz
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
import os
import io
import shutil
from pathlib import Path

from PIL import Image

import py5_tools

from generator.docfiles import Documentation

PY5_API_EN = Path('py5_docs/Reference/api_en/').absolute()
DOC_DATA = Path('py5_docs/Reference/data')
DEST_DIR = Path('/tmp/examples/')

ONLY_RUN_EXAMPLES_WITH_IMAGES = False

MAGIC_RENDERER_MAP = {
    'py5drawdxf': 'DXF',
    'py5drawpdf': 'PDF',
    'py5drawsvg': 'SVG', 
}

# set the current working dir and put supporting files in data subdirectory
cwd = os.getcwd()
if DEST_DIR.exists():
    shutil.rmtree(DEST_DIR)
DEST_DIR.mkdir(exist_ok=True)
shutil.copytree(DOC_DATA, DEST_DIR / 'data')
os.chdir(DEST_DIR)


try:
    for docfile in sorted(PY5_API_EN.glob('*.txt')):
        doc = Documentation(docfile)
        if doc.meta['type'] in ['function', 'line magic']:
            # skip these for now, but I should probably include them later
            continue

        # if doc.meta.get('pclass') != 'PShape':  #
        # if doc.meta.get('category') != 'typography':
        # if doc.meta.get('category') != 'image' or doc.meta.get('subcategory') != 'loading_displaying':
        if doc.meta.get('pclass') != 'PShape' or doc.meta.get('name') not in ['begin_contour()', 'end_contour()', 'stroke_join()', 'stroke_cap()', 'stroke_weight()', 'no_fill()', 'fill()', 'no_stroke()', 'stroke()', 'bezier_vertex()', 'bezier_detail()']:
            continue

        for image, code in doc.examples:
            if ONLY_RUN_EXAMPLES_WITH_IMAGES and image is None:
                continue

            print(docfile.name, image)

            if doc.meta['type'] == 'cell magic':
                magic_line, magic_cell = code.split('\n', maxsplit=1)
                magic, line = magic_line.split(' ', maxsplit=1)
                renderer = MAGIC_RENDERER_MAP.get(magic[2:], 'JAVA2D')
                # TODO: what if the -r parameter is used? could want P2D or P3D renderers
                width, height = (int(x) for x in line.split(maxsplit=2)[:2])
                result = py5_tools.magics.drawing._run_sketch(renderer, magic_cell, width, height, dict(), True)
                if image:
                    Image.open(io.BytesIO(result)).convert(mode='RGB').save(DEST_DIR / image)
            else:
                save_path = DEST_DIR / image if image else None
                success = py5_tools.testing.run_code(code, save_path)
                if success:
                    if save_path:
                        img = Image.open(save_path)
                        if img.size != (100, 100):
                            img.crop((0, 0, 100, 100)).save(save_path)
                else:
                    print('-' * 20)
                    print(f'error in file: {docfile.name} output: {image}')
                    print('-' * 20)
                    print(code)
                    print('=' * 60)
                    break
finally:
    os.chdir(cwd)
