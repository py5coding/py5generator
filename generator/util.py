# *****************************************************************************
#
#   Part of the py5generator project; generator of the py5 library
#   Copyright (C) 2020-2023 Jim Schmitz
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
import logging
import re
import shutil
from pathlib import Path
from string import Template

import autopep8

logger = logging.getLogger(__name__)


class CodeCopier:

    def __init__(self, format_params, docstring_dict, skip_autopep8=False):
        self.format_params = format_params
        self.docstring_dict = docstring_dict
        self.skip_autopep8 = skip_autopep8

    def __call__(self, src, dest, *, follow_symlinks=True):
        logger.info(f'copying {src} to {dest}')

        if Path(src).suffix != '.py':
            shutil.copy(src, dest)
        else:
            with open(src, 'r') as f:
                content = f.read()

            if content.find('# *** FORMAT PARAMS ***') >= 0:
                content = content.replace('# *** FORMAT PARAMS ***\n', '')
                content = content.format(**self.format_params)

            content = re.sub(r'^.*DELETE$', '', content, flags=re.MULTILINE)
            content = re.sub(r'\s*# @decorator$', '',
                             content, flags=re.MULTILINE)
            content = Template(content).substitute(self.docstring_dict)
            if self.skip_autopep8 or content.find('# *** SKIP AUTOPEP8 ***') >= 0:
                content = content.replace('# *** SKIP AUTOPEP8 ***\n', '')
            else:
                content = autopep8.fix_code(content, options={'aggressive': 2})

            with open(dest, 'w') as f:
                f.write(content)

        return dest
