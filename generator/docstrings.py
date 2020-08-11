import re
import json
import textwrap


DOCSTRING_FILE_HEADER = re.compile(r"^# \w+$", re.UNICODE | re.MULTILINE)


class DocstringDict:

    INDENTING = {'class': 8, 'module': 4}

    def __init__(self, docstring_filename, var_desc_filename):
        super().__init__()
        self._docstrings = self._load_docstrings(docstring_filename)
        self._variable_descriptions = self._load_variable_descriptions(var_desc_filename)

    def _load_variable_descriptions(self, filename):
        with open(filename, 'r') as f:
            return json.load(f)

    def _load_docstrings(self, filename):
        with open(filename, 'r') as f:
            md_contents = f.read()
        return {k[1:].strip(): v.strip()
                for k, v in zip(DOCSTRING_FILE_HEADER.findall(md_contents),
                                DOCSTRING_FILE_HEADER.split(md_contents)[1:])}

    def __getitem__(self, item):
        try:
            dockey, params = item.replace('*', '').split('|')
            kind, name = dockey.split('_', 1)
            paramtext = ''
            if params:
                vardocs = []
                for p in params.split('+'):
                    varname, type_ = p.split(':')
                    vardesc = self._variable_descriptions[name].get(varname, '(no description)')
                    vardocs.append(f'{varname}: {type_}\n    {vardesc}')
                paramtext = '\n\n'.join(vardocs)
            doc = textwrap.indent(
                self._docstrings[name].replace('PARAMTEXT', paramtext),
                prefix=(' ' * DocstringDict.INDENTING.get(kind, 0))).strip()
            doc += '\n'
            return doc
        except KeyError:
            return 'missing docstring'
