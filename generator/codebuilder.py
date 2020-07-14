import re
import logging
import shlex
from functools import lru_cache

from . import reference as ref
from . import templates as templ


logger = logging.getLogger(__name__)


###############################################################################
# REGEX
###############################################################################


METHOD_REGEX = re.compile(r'(@\w+)?\s*def (.*?)\((cls|self),?\s*(.*?)\)\s*-?>?\s*(.*?):$', re.MULTILINE | re.DOTALL)
TYPEHINT_COMMA_REGEX = re.compile(r'(\[[\w\s,]+\])')


###############################################################################
# UTIL FUNCTIONS
###############################################################################


def snake_case(name):
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name)
    return name.lower()


@lru_cache(128)
def _convert_type(jtype: str) -> str:
    if jtype == 'void':
        return 'None'

    isarray = jtype.endswith('[]')
    jtype = jtype[:-2] if isarray else jtype
    out = ref.JTYPE_CONVERSIONS.get(jtype, jtype.split('/')[-1])

    return f'List[{out}]' if isarray else out


def _param_annotation(varname: str, jtype: str) -> str:
    if jtype.endswith('...'):
        jtype = jtype[:-3]
        varname = '*' + varname

    return f'{varname}: {_convert_type(jtype)}'


###############################################################################
# CODE BUILDER CLASS
###############################################################################


class CodeBuilder:

    def __init__(self, method_parameter_names_data, class_data):
        self._method_parameter_names_data = method_parameter_names_data
        self._py5_names = class_data['py5_name']
        self._py5_decorators = class_data['decorator']
        self._py5_special_kwargs = class_data['special_kwargs']

        self._code_module = False
        self._class_name = None
        self._instance_name = None

        self._all_known_fields_and_methods = set(class_data.index)
        self._included_fields_and_methods = set(class_data.query("implementation_from_processing==True").index)

        self.static_constant_names = set()
        self.dynamic_variable_names = set()
        self.method_names = set()
        self.extra_names = set()

        self.class_members = []
        self.module_members = []

    def code_module_members(self, class_name, instance_name):
        self._code_module = True
        self._class_name = class_name
        self._instance_name = instance_name

    @property
    def all_names(self):
        return (self.static_constant_names | self.dynamic_variable_names
                | self.method_names | self.extra_names)

    def _make_param_rettype_strs(self, fname, first_param, params, rettype):
        try:
            parameter_name_key = ','.join([p.split('/')[-1].replace('...', '[]') for p in params])
            parameter_names, _ = self._method_parameter_names_data[fname][parameter_name_key]
            parameter_names = [snake_case(p) for p in parameter_names.split(',')]
            paramstrs = [first_param] + [_param_annotation(pn, p) for pn, p in zip(parameter_names, params)]
        except Exception:
            logger.warning(f'missing parameter names for {fname} {params}')
            paramstrs = [first_param] + [_param_annotation(f'arg{i}', p) for i, p in enumerate(params)]
        rettypestr = _convert_type(rettype)

        return paramstrs, rettypestr

    def code_static_constant(self, name, val):
        if name in ref.PCONSTANT_OVERRIDES:
            val = shlex.quote(ref.PCONSTANT_OVERRIDES[name])
        else:
            if isinstance(val, str):
                val = f"'{val}'"
            if name == 'javaVersion':
                val = round(val, 2)

        self.class_members.append(templ.CLASS_STATIC_FIELD_TEMPLATE.format(name, val))
        if self._code_module:
            self.module_members.append(templ.MODULE_STATIC_FIELD_TEMPLATE.format(name, val))

        self.static_constant_names.add(name)

    def code_dynamic_variable(self, name, type_name):
        snake_name = self._py5_names[name]
        var_type = (
            {'args': 'List[str]', 'g': 'PGraphics', 'recorder': 'PGraphics', 'pixels': 'List[int]'}
        ).get(name, type_name)

        self.class_members.append(templ.CLASS_PROPERTY_TEMPLATE.format(snake_name, var_type, name))
        if self._code_module:
            self.module_members.append(templ.MODULE_PROPERTY_TEMPLATE.format(snake_name, var_type))

        self.dynamic_variable_names.add(snake_name)

    def code_method(self, fname, method, static):
        snake_name = self._py5_names[fname]
        kwargs = self._py5_special_kwargs[fname]
        if kwargs:
            kwargs_precondition, kwargs = kwargs.split('|')
        if static:
            first_param, classobj, moduleobj, decorator = 'cls', 'cls._cls', self._class_name, '@classmethod'
        else:
            first_param, classobj, moduleobj, decorator = 'self', 'self._instance', self._instance_name, self._py5_decorators[fname]
        # if there is only one method signature, create the real method with typehints
        if len(method.signatures()) == 1:
            params, rettype = method.signatures()[0]
            if ref.PY5_SKIP_PARAM_TYPES.intersection(params) or rettype in ref.PY5_SKIP_RETURN_TYPES:
                return
            paramstrs, rettypestr = self._make_param_rettype_strs(fname, first_param, params, rettype)
            class_arguments = ', '.join([p.split(':')[0] for p in paramstrs[1:]])
            module_arguments = class_arguments
            if kwargs and any([kwargs_precondition in p for p in paramstrs]):
                paramstrs.append(kwargs)
                kw_param = kwargs.split(':')[0]
                module_arguments += f', {kw_param}={kw_param}'

            # create the class and module code
            self.class_members.append(templ.CLASS_METHOD_TEMPLATE_WITH_TYPEHINTS.format(
                snake_name, ', '.join(paramstrs), classobj, fname, decorator, rettypestr, class_arguments))
            if self._code_module:
                self.module_members.append(templ.MODULE_FUNCTION_TEMPLATE_WITH_TYPEHINTS.format(
                    snake_name, ', '.join(paramstrs[1:]), moduleobj, rettypestr, module_arguments))
        else:
            # loop through the method signatures and create the typehint methods
            skipped_all = True
            for params, rettype in sorted(method.signatures(), key=lambda x: str(x[0])):
                if ref.PY5_SKIP_PARAM_TYPES.intersection(params) or rettype in ref.PY5_SKIP_RETURN_TYPES:
                    continue
                skipped_all = False
                paramstrs, rettypestr = self._make_param_rettype_strs(fname, first_param, params, rettype)
                if kwargs and any([kwargs_precondition in p for p in paramstrs]):
                    paramstrs.append(kwargs)

                # create the class and module typehints
                self.class_members.append(templ.CLASS_METHOD_TYPEHINT_TEMPLATE.format(snake_name, ', '.join(paramstrs), rettypestr))
                if self._code_module:
                    self.module_members.append(templ.MODULE_FUNCTION_TYPEHINT_TEMPLATE.format(snake_name, ', '.join(paramstrs[1:]), rettypestr))
            if skipped_all:
                return
            # now construct the real methods
            arguments = '*args'
            module_arguments = '*args'
            if kwargs:
                arguments += f', {kwargs}'
                kw_param = kwargs.split(':')[0]
                module_arguments += f', {kw_param}={kw_param}'

            self.class_members.append(templ.CLASS_METHOD_TEMPLATE.format(snake_name, first_param, classobj, fname, decorator, arguments))
            if self._code_module:
                self.module_members.append(templ.MODULE_FUNCTION_TEMPLATE.format(snake_name, moduleobj, arguments, module_arguments))
        self.method_names.add(snake_name)

    def code_extra(self, filename):
        with open(filename) as f:
            code = f.read()
            code = code.split('*** BEGIN METHODS ***')[1].strip()

        if not self._code_module:
            return

        self.module_members.append(f'\n{"#" * 78}\n# module functions from {filename.name}\n{"#" * 78}\n')
        for decorator, fname, arg0, args, rettypestr in METHOD_REGEX.findall(code):
            if fname.startswith('_'):
                continue
            elif decorator == '@overload':
                self.module_members.append(templ.MODULE_FUNCTION_TYPEHINT_TEMPLATE.format(fname, args, rettypestr))
            else:
                moduleobj = self._class_name if arg0 == 'cls' else self._instance_name
                paramlist = []
                for arg in TYPEHINT_COMMA_REGEX.sub('', args).split(','):
                    paramname = arg.split(':')[0].strip()
                    if '=' in arg:
                        paramlist.append(f'{paramname}={paramname}')
                    else:
                        paramlist.append(paramname)

                params = ', '.join(paramlist)
                self.module_members.append(templ.MODULE_FUNCTION_TEMPLATE_WITH_TYPEHINTS.format(
                    fname, args, moduleobj, rettypestr, params))
                self.extra_names.add(fname)

    def run_builder(self, cls_, instance):
        from jnius import JavaStaticMethod, JavaMethod, JavaMultipleMethod, JavaStaticField, JavaField

        ordering = {JavaStaticField: 0, JavaField: 1}
        for k, v in sorted(cls_.__dict__.items(), key=lambda x: (ordering.get(type(x[1]), 2), x[0])):
            if isinstance(v, JavaStaticMethod) and k in self._included_fields_and_methods:
                self.code_method(k, v, True)
            elif isinstance(v, (JavaMethod, JavaMultipleMethod)) and k in self._included_fields_and_methods:
                self.code_method(k, v, False)
            elif isinstance(v, JavaStaticField) and k in self._included_fields_and_methods:
                self.code_static_constant(k, getattr(cls_, k))
            elif isinstance(v, JavaField) and k in self._included_fields_and_methods:
                self.code_dynamic_variable(k, type(getattr(instance, k)).__name__)
            if k not in self._all_known_fields_and_methods and not k.startswith('_'):
                logger.warning(f'detected previously unknown {type(v).__name__} {k}')
