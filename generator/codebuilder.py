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
"""
Write method and field code fragments for classes based on data in csv files and
information extracted from javap.
"""
import re
import logging
from functools import lru_cache
from collections import defaultdict

from . import reference as ref
from . import templates as templ
from . import javap


logger = logging.getLogger(__name__)


###############################################################################
# REGEX
###############################################################################


CONSTANT_REGEX = re.compile(r'^\s*([A-Z_]*)\s*=\s*(.*?)\s+# CODEBUILDER INCLUDE$', re.MULTILINE)
METHOD_REGEX = re.compile(r'(@\w+)?\s*def (.*?)\((cls|self),?\s*(.*?)\)\s*-?>?\s*(.*?):\s*(# @decorator)?$', re.MULTILINE | re.DOTALL)
TYPEHINT_COMMA_REGEX = re.compile(r'(\[[\w\s,]+\])')
COMMA_REGEX = re.compile(r',\s*(?!\s*\w+\])')

SNAKE_CASE_1 = re.compile('(.)([A-Z][a-z]+)')
SNAKE_CASE_2 = re.compile('([a-z0-9])([A-Z])')

###############################################################################
# UTIL FUNCTIONS
###############################################################################


def snake_case(name):
    name = SNAKE_CASE_1.sub(r'\1_\2', name)
    name = SNAKE_CASE_2.sub(r'\1_\2', name)
    return name.lower()


@lru_cache(128)
def _convert_type(jtype: str) -> str:
    if jtype == 'void':
        return 'None'
    elif jtype in ref.TYPE_OVERRIDES:
        return ref.TYPE_OVERRIDES[jtype]
    elif jtype.endswith('[][]'):
        return f'JArray({ref.JPYPE_CONVERSIONS[jtype[:-4]]}, 2)'
    elif jtype.endswith('[]'):
        return f'JArray({ref.JPYPE_CONVERSIONS[jtype[:-2]]})'
    else:
        return ref.JTYPE_CONVERSIONS[jtype]


def _param_annotation(varname: str, jtype: str) -> str:
    if jtype.endswith('...'):
        jtype = jtype[:-3]
        varname = '*' + varname

    return f'{varname}: {_convert_type(jtype)}'


###############################################################################
# CODE BUILDER CLASS
###############################################################################


class CodeBuilder:

    def __init__(self, clsname, class_name, class_data):
        self._constant_field_data, self._field_data, self._method_data = javap.get_class_information(clsname)
        self._class_name = class_name
        self._py5_names = class_data['py5_name']
        self._py5_decorators = class_data['decorator']

        self._code_module = False
        self._instance_name = None

        self._all_known_fields_and_methods = set(class_data.index)
        self._included_fields_and_methods = set(class_data.query("implementation=='JAVA'").index)

        self.static_constant_names = set()
        self.dynamic_variable_names = set()
        self.method_names = set()
        self.extra_names = set()
        self.method_signatures = defaultdict(list)

        self.class_members = []
        self.module_members = []

    def code_module_members(self, instance_name):
        self._code_module = True
        self._instance_name = instance_name

    @property
    def all_names(self):
        return (self.static_constant_names | self.dynamic_variable_names
                | self.method_names | self.extra_names)

    def _make_param_rettype_strs(self, fname, first_param, params, paramnames, rettype):
        parameter_names = [snake_case(p) for p in paramnames]
        paramstrs = [first_param] + [_param_annotation(pn, p) for pn, p in zip(parameter_names, params)]
        rettypestr = _convert_type(rettype)

        return paramstrs, rettypestr

    def code_constant(self, name, val):
        py5_name = self._py5_names[name]

        self.class_members.append(templ.CLASS_STATIC_FIELD_TEMPLATE.format(py5_name, val))
        if self._code_module:
            self.module_members.append(templ.MODULE_STATIC_FIELD_TEMPLATE.format(py5_name, val))

        self.static_constant_names.add(py5_name)

    def code_dynamic_variable(self, name, type_name):
        py5_name = self._py5_names[name]
        decorator = self._py5_decorators[name]
        var_type = _convert_type(type_name)

        self.class_members.append(
            templ.CLASS_PROPERTY_TEMPLATE.format(self._class_name, py5_name, var_type, name, decorator)
        )
        if self._code_module:
            self.module_members.append(templ.MODULE_PROPERTY_TEMPLATE.format(py5_name, var_type))

        self.dynamic_variable_names.add(py5_name)

    def code_method(self, fname, method_data):
        py5_name = self._py5_names[fname]
        static = all([x['static'] for x in method_data.values()])
        if static:
            first_param, classobj, moduleobj, decorator = 'cls', 'cls._cls', self._class_name, '@classmethod'
            if self._py5_decorators[fname]:
                decorator = '@classmethod\n    ' + self._py5_decorators[fname]
        else:
            first_param, classobj, moduleobj, decorator = 'self', 'self._instance', self._instance_name, self._py5_decorators[fname]
        # adjust decorator if there are multiple decorators
        decorator = decorator.replace(';', '\n    ')
        # if there is only one method signature, create the real method with typehints
        if len(method_data) == 1:
            sigstr, sigdata = list(method_data.items())[0]
            params = sigstr.split(',')
            rettype = sigdata['rettype']
            paramnames = sigdata['paramnames']
            if ref.PY5_SKIP_PARAM_TYPES.intersection(params) or rettype in ref.PY5_SKIP_RETURN_TYPES:
                logger.warning(f'skipping method for {fname} {str(params)} {rettype}')
                return
            paramstrs, rettypestr = self._make_param_rettype_strs(fname, first_param, params, paramnames, rettype)
            class_arguments = ', '.join([p.split(':')[0] for p in paramstrs[1:]])
            module_arguments = class_arguments

            if len(paramstrs) > 1:
                if paramstrs[-1][0] == '*':
                    paramstrs.insert(-1, '/')
                else:
                    paramstrs.append('/')

            # create the class and module code
            signature_options = [', '.join([s for s in paramstrs[1:] if s != '/'])]
            self.class_members.append(
                templ.CLASS_METHOD_TEMPLATE_WITH_TYPEHINTS.format(
                    self._class_name, py5_name, ', '.join(paramstrs), classobj,
                    fname, decorator, rettypestr, class_arguments, signature_options
                )
            )
            self.method_signatures[(self._class_name, py5_name)].append((paramstrs[1:], rettypestr))
            if self._code_module:
                self.module_members.append(
                    templ.MODULE_FUNCTION_TEMPLATE_WITH_TYPEHINTS.format(
                        self._class_name, py5_name, ', '.join(paramstrs[1:]),
                        moduleobj, rettypestr, module_arguments
                    )
                )
        else:
            # loop through the method signatures and create the typehint methods
            skipped_all = True
            created_sigs = set()
            signature_options = []
            for sigstr, sigdata in sorted(method_data.items()):
                params = sigstr.split(',')
                rettype = sigdata['rettype']
                paramnames = sigdata['paramnames']
                if ref.PY5_SKIP_PARAM_TYPES.intersection(params) or rettype in ref.PY5_SKIP_RETURN_TYPES:
                    logger.warning(f'skipping typehint for {fname} {str(params)} {rettype}')
                    continue
                skipped_all = False
                paramstrs, rettypestr = self._make_param_rettype_strs(fname, first_param, params, paramnames, rettype)

                if len(paramstrs) > 1:
                    if paramstrs[-1][0] == '*':
                        paramstrs.insert(-1, '/')
                    else:
                        paramstrs.append('/')

                joined_paramstrs = ', '.join(paramstrs)
                # has an identical signature already been added?
                if (joined_paramstrs, rettypestr) in created_sigs:
                    continue
                # create the class and module typehints
                signature_options.append(', '.join([s for s in paramstrs[1:] if s != '/']))
                self.class_members.append(
                    templ.CLASS_METHOD_TYPEHINT_TEMPLATE.format(
                        self._class_name, py5_name, joined_paramstrs, rettypestr
                    )
                )
                self.method_signatures[(self._class_name, py5_name)].append((paramstrs[1:], rettypestr))
                if self._code_module:
                    self.module_members.append(
                        templ.MODULE_FUNCTION_TYPEHINT_TEMPLATE.format(
                            self._class_name, py5_name, ', '.join(paramstrs[1:]), rettypestr
                        )
                    )
                created_sigs.add((joined_paramstrs, rettypestr))
            if skipped_all:
                return

            # now construct the real methods
            arguments = '*args'
            module_arguments = '*args'
            self.class_members.append(
                templ.CLASS_METHOD_TEMPLATE.format(
                    self._class_name, py5_name, first_param, classobj, fname,
                    decorator, arguments, signature_options
                )
            )
            if self._code_module:
                self.module_members.append(
                    templ.MODULE_FUNCTION_TEMPLATE.format(
                        self._class_name, py5_name, moduleobj, arguments, module_arguments
                    )
                )
        self.method_names.add(py5_name)

    def code_extra(self, class_name, filename):
        if not self._code_module:
            return

        with open(filename) as f:
            code = f.read()

        for name, val in CONSTANT_REGEX.findall(code):
            self.module_members.append(templ.MODULE_STATIC_FIELD_TEMPLATE.format(name, val))
            self.static_constant_names.add(name)

        overloaded = set()
        self.module_members.append(f'\n{"#" * 78}\n# module functions from {filename.name}\n{"#" * 78}\n')
        method_code = code.split('*** BEGIN METHODS ***')[1].strip()
        for decorator, fname, arg0, args, rettypestr, fake_decorator in METHOD_REGEX.findall(method_code):
            if fname.startswith('_') and not fake_decorator:
                continue
            elif decorator == '@overload':
                overloaded.add((class_name, fname))
                self.module_members.append(
                    templ.MODULE_FUNCTION_TYPEHINT_TEMPLATE.format(self._class_name, fname, args, rettypestr)
                )
                self.method_signatures[(class_name, fname)].append((COMMA_REGEX.split(args), rettypestr))
            elif decorator == '@property':
                self.module_members.append(
                    templ.MODULE_PROPERTY_TEMPLATE.format(fname, rettypestr)
                )
                self.dynamic_variable_names.add(fname)
            elif fake_decorator == '# @decorator' and fname.startswith('_get_'):
                self.module_members.append(
                    templ.MODULE_PROPERTY_TEMPLATE.format(fname[5:], rettypestr)
                )
                self.dynamic_variable_names.add(fname[5:])
            else:
                split_args = COMMA_REGEX.split(args) if args else []
                if (class_name, fname) not in overloaded:
                    self.method_signatures[(class_name, fname)].append((split_args, rettypestr))
                moduleobj = self._class_name if arg0 == 'cls' else self._instance_name
                paramlist = []
                for arg in TYPEHINT_COMMA_REGEX.sub('', args).split(','):
                    paramname = arg.split(':')[0].strip()
                    if '=' in arg:
                        paramlist.append(f'{paramname}={paramname}')
                    else:
                        paramlist.append(paramname)

                params = ', '.join(p for p in paramlist if p != '*')
                self.module_members.append(
                    templ.MODULE_FUNCTION_TEMPLATE_WITH_TYPEHINTS.format(
                        self._class_name, fname, args, moduleobj, rettypestr, params, ''
                    )
                )
                self.extra_names.add(fname)

    def run_builder(self):

        for field_name, field_value in sorted(self._constant_field_data.items()):
            if field_name in self._included_fields_and_methods:
                self.code_constant(field_name, field_value)
            elif field_name not in self._all_known_fields_and_methods and not field_name.startswith('_'):
                logger.warning(f'detected previously unknown constant field {field_name}')

        for field_name, field_type in sorted(self._field_data.items()):
            if field_name in self._included_fields_and_methods:
                self.code_dynamic_variable(field_name, field_type)
            elif field_name not in self._all_known_fields_and_methods and not field_name.startswith('_'):
                logger.warning(f'detected previously unknown dynamic field {field_name}')

        for method_name, method_data in sorted(self._method_data.items()):
            if method_name in self._included_fields_and_methods:
                self.code_method(method_name, method_data)
            elif method_name not in self._all_known_fields_and_methods and not method_name.startswith('_'):
                logger.warning(f'detected previously unknown method {method_name}')
