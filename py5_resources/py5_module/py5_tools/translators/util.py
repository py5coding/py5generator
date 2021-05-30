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
from pathlib import Path
from typing import Union


def batch_translate_dir(translator, src: Union[str, Path], dest: Union[str, Path], ext='.pyde'):
    src = Path(src)
    dest = Path(dest)

    print('translating code in', str(src))

    count = 0
    for src_file in src.glob('**/*' + ext):
        try:
            dest_file = dest / src_file.relative_to(src).with_suffix('.py')
            translator(src_file, dest_file)
            print("translated " + str(src_file.relative_to(src)))
            count += 1
        except:
            print("error translating " + str(src_file.relative_to(src)))

    print("batch translate complete. translated", count, "files written to output directory", str(dest))
