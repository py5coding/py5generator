import re
import logging
from string import Template
import autopep8


logger = logging.getLogger(__name__)


class DocTemplate(Template):

    idpattern = r'(?a:[_a-z][_a-z0-9\|+:\*]*)'


class CodeCopier:

    def __init__(self, format_params, docstring_dict):
        self.format_params = format_params
        self.docstring_dict = docstring_dict

    def __call__(self, src, dest, *, follow_symlinks=True):
        logger.info(f'copying {src} to {dest}')

        with open(src, 'r') as f:
            content = f.read()

        if content.find('*** FORMAT PARAMS ***') > 0:
            content = re.sub(r'^.*DELETE$', '',
                             content.format(**self.format_params),
                             flags=re.MULTILINE | re.UNICODE)
        content = DocTemplate(content).substitute(self.docstring_dict)
        content = autopep8.fix_code(content, options={'aggressive': 2})

        with open(dest, 'w') as f:
            f.write(content)

        return dest
