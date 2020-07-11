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
# CODE BUILDER CLASS
###############################################################################


class CodeBuilder:

    def __init__(self, method_parameter_names_data,
                 py5_names, py5_decorators, py5_special_kwargs):
        self.method_parameter_names_data = method_parameter_names_data
        self.py5_names = py5_names
        self.py5_decorators = py5_decorators
        self.py5_special_kwargs = py5_special_kwargs

        self.class_members = []
        self.module_members = []
        self.py5_dir = []

    def snake_case(self, name):
        name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name)
        return name.lower()

    @lru_cache(128)
    def convert_type(self, jtype: str) -> str:
        if jtype == 'void':
            return 'None'

        isarray = jtype.endswith('[]')
        jtype = jtype[:-2] if isarray else jtype
        out = ref.JTYPE_CONVERSIONS.get(jtype, jtype.split('/')[-1])

        return f'List[{out}]' if isarray else out

    def param_annotation(self, varname: str, jtype: str) -> str:
        if jtype.endswith('...'):
            jtype = jtype[:-3]
            varname = '*' + varname

        return f'{varname}: {self.convert_type(jtype)}'

    def make_param_rettype_strs(self, fname, first_param, params, rettype):
        try:
            parameter_name_key = ','.join([p.split('/')[-1].replace('...', '[]') for p in params])
            parameter_names, _ = self.method_parameter_names_data['PApplet'][fname][parameter_name_key]
            parameter_names = [self.snake_case(p) for p in parameter_names.split(',')]
            paramstrs = [first_param] + [self.param_annotation(pn, p) for pn, p in zip(parameter_names, params)]
        except Exception:
            logger.warning(f'missing parameter names for {fname} {params}')
            paramstrs = [first_param] + [self.param_annotation(f'arg{i}', p) for i, p in enumerate(params)]
        rettypestr = self.convert_type(rettype)

        return paramstrs, rettypestr

    def code_static_constants(self, static_fields, Py5Applet):
        for name in sorted(static_fields):
            if name in ref.PCONSTANT_OVERRIDES:
                self.module_members.append(f'\n{name} = {shlex.quote(ref.PCONSTANT_OVERRIDES[name])}')
            else:
                val = getattr(Py5Applet, name)
                if isinstance(val, str):
                    val = f"'{val}'"
                if name == 'javaVersion':
                    val = round(val, 2)
                self.module_members.append(templ.MODULE_STATIC_FIELD_TEMPLATE.format(name, val))
                self.class_members.append(templ.CLASS_STATIC_FIELD_TEMPLATE.format(name, val))
            self.py5_dir.append(name)

    def code_dynamic_variables(self, fields, py5applet):
        py5_dynamic_vars = []
        run_sketch_pre_run_steps = []
        for name in sorted(fields):
            snake_name = self.py5_names[name]
            var_type = (
                {'args': 'List[str]', 'g': 'PGraphics', 'recorder': 'PGraphics', 'pixels': 'List[int]'}
            ).get(name, type(getattr(py5applet, name)).__name__)
            self.class_members.append(templ.CLASS_PROPERTY_TEMPLATE.format(snake_name, var_type, name))
            self.module_members.append(templ.MODULE_PROPERTY_TEMPLATE.format(snake_name, var_type))
            run_sketch_pre_run_steps.append(templ.MODULE_PROPERTY_PRE_RUN_TEMPLATE.format(snake_name))
            py5_dynamic_vars.append(snake_name)
            self.py5_dir.append(snake_name)
        return py5_dynamic_vars, run_sketch_pre_run_steps

    def code_methods(self, methods, static):
        for fname, method in sorted(methods, key=lambda x: x[0]):
            snake_name = self.py5_names[fname]
            kwargs = self.py5_special_kwargs[fname]
            if kwargs:
                kwargs_precondition, kwargs = kwargs.split('|')
            if static:
                first_param, classobj, moduleobj, decorator = 'cls', '_Py5Applet', 'Sketch', '@classmethod'
            else:
                first_param, classobj, moduleobj, decorator = 'self', 'self._py5applet', '_py5sketch', self.py5_decorators[fname]
            # if there is only one method signature, create the real method with typehints
            if len(method.signatures()) == 1:
                params, rettype = method.signatures()[0]
                if ref.PAPPLET_SKIP_PARAM_TYPES.intersection(params) or rettype in ref.PAPPLET_SKIP_RETURN_TYPES:
                    continue
                paramstrs, rettypestr = self.make_param_rettype_strs(fname, first_param, params, rettype)
                class_arguments = ', '.join([p.split(':')[0] for p in paramstrs[1:]])
                module_arguments = class_arguments
                if kwargs and any([kwargs_precondition in p for p in paramstrs]):
                    paramstrs.append(kwargs)
                    kw_param = kwargs.split(':')[0]
                    module_arguments += f', {kw_param}={kw_param}'
                # create the class and module code
                self.class_members.append(templ.CLASS_METHOD_TEMPLATE_WITH_TYPEHINTS.format(
                    snake_name, ', '.join(paramstrs), classobj, fname, decorator, rettypestr, class_arguments))
                self.module_members.append(templ.MODULE_FUNCTION_TEMPLATE_WITH_TYPEHINTS.format(
                    snake_name, ', '.join(paramstrs[1:]), moduleobj, rettypestr, module_arguments))
            else:
                # loop through the method signatures and create the typehint methods
                skipped_all = True
                for params, rettype in sorted(method.signatures(), key=lambda x: len(x[0])):
                    if ref.PAPPLET_SKIP_PARAM_TYPES.intersection(params) or rettype in ref.PAPPLET_SKIP_RETURN_TYPES:
                        continue
                    skipped_all = False
                    paramstrs, rettypestr = self.make_param_rettype_strs(fname, first_param, params, rettype)
                    if kwargs and any([kwargs_precondition in p for p in paramstrs]):
                        paramstrs.append(kwargs)
                    # create the class and module typehints
                    self.class_members.append(templ.CLASS_METHOD_TYPEHINT_TEMPLATE.format(snake_name, ', '.join(paramstrs), rettypestr))
                    self.module_members.append(templ.MODULE_FUNCTION_TYPEHINT_TEMPLATE.format(snake_name, ', '.join(paramstrs[1:]), rettypestr))
                if skipped_all:
                    continue
                # now construct the real methods
                arguments = '*args'
                module_arguments = '*args'
                if kwargs:
                    arguments += f', {kwargs}'
                    kw_param = kwargs.split(':')[0]
                    module_arguments += f', {kw_param}={kw_param}'
                self.class_members.append(templ.CLASS_METHOD_TEMPLATE.format(snake_name, first_param, classobj, fname, decorator, arguments))
                self.module_members.append(templ.MODULE_FUNCTION_TEMPLATE.format(snake_name, moduleobj, arguments, module_arguments))
            self.py5_dir.append(snake_name)

    def code_mixin(self, filename):
        with open(filename) as f:
            code = f.read()
            code = code.split('*** BEGIN METHODS ***')[1].strip()

        self.module_members.append(f'\n{"#" * 78}\n# module functions from {filename.name}\n{"#" * 78}\n')
        for decorator, fname, arg0, args, rettypestr in METHOD_REGEX.findall(code):
            if fname.startswith('_'):
                continue
            elif decorator == '@overload':
                self.module_members.append(templ.MODULE_FUNCTION_TYPEHINT_TEMPLATE.format(fname, args, rettypestr))
            else:
                moduleobj = 'Sketch' if arg0 == 'cls' else '_py5sketch'
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
                self.py5_dir.append(fname)
