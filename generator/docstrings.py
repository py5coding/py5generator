import re
from string import Template
import json
import textwrap


DOCSTRING_FILE_HEADER = re.compile(r"^# \w+$", re.UNICODE | re.MULTILINE)


class MethodParamsDict:

    def __init__(self, method_signatures_lookup, var_desc_filename):
        self._method_signatures_lookup = method_signatures_lookup
        self._variable_descriptions = self._load_variable_descriptions(var_desc_filename)

    def _load_variable_descriptions(self, filename):
        with open(filename, 'r') as f:
            return json.load(f)

    def __getitem__(self, item):
        try:
            class_method = item[:-11]
            class_name, method_name = class_method.split('_', 1)
            signature_info = self._method_signatures_lookup[class_name, method_name]
            var_descriptions = self._variable_descriptions[class_method]
            return 'it works: ' + str(signature_info) + ' ' + str(var_descriptions)
        except KeyError:
            return f'missing param information for {item}'


class DocstringDict:

    INDENTING = {'class': 8, 'module': 4}

    def __init__(self, docstring_filename, method_params_dict):
        self._docstrings = self._load_docstrings(docstring_filename, method_params_dict)

    def _load_docstrings(self, filename, method_params_dict):
        with open(filename, 'r') as f:
            md_contents = f.read()
        md_contents = Template(md_contents).substitute(method_params_dict)
        return {k[1:].strip(): v.strip()
                for k, v in zip(DOCSTRING_FILE_HEADER.findall(md_contents),
                                DOCSTRING_FILE_HEADER.split(md_contents)[1:])}

    def __getitem__(self, item):
        try:
            kind, name = item.split('_', 1)
            doc = textwrap.indent(
                self._docstrings[name],
                prefix=(' ' * DocstringDict.INDENTING.get(kind, 0))).strip()
            doc += '\n'
            return doc
        except KeyError:
            return 'missing docstring'
