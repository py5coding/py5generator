import re
from pathlib import Path


METHOD_REGEX = re.compile(r'(@\w+)?\s*def (.*?)\((cls|self),?\s*(.*?)\)(\s*-?>?\s*.*?):$', re.MULTILINE | re.DOTALL)
TYPEHINT_COMMA_REGEX = re.compile(r'(\[[\w\s,]+\])')


MODULE_FUNCTION_TYPEHINT_TEMPLATE = """
@overload
def {0}({1}){2}:
    \"\"\"$module_{0}\"\"\"
    pass
"""

MODULE_FUNCTION_TEMPLATE_WITH_TYPEHINTS = """
def {0}({1}){3}:
    \"\"\"$module_{0}\"\"\"
    return {2}.{0}({4})
"""


mixin_dir = Path('py5_resources/py5_module/py5/mixins/')
for filename in mixin_dir.glob('*.py'):
    if filename.stem == '__init__':
        continue

    print(f'\n{"#" * 78}\n# module functions from {filename.name}\n{"#" * 78}\n')

    with open(filename) as f:
        code = f.read()
        code = code.split('*** BEGIN METHODS ***')[1].strip()

    for decorator, fname, arg0, args, return_typehint in METHOD_REGEX.findall(code):
        if fname.startswith('_'):
            continue
        elif decorator == '@overload':
            print(MODULE_FUNCTION_TYPEHINT_TEMPLATE.format(fname, args, return_typehint))
        else:
            if arg0 == 'cls':
                moduleobj = 'Sketch'
            else:
                moduleobj = '_py5sketch'

            paramlist = []
            for arg in TYPEHINT_COMMA_REGEX.sub('', args).split(','):
                paramname = arg.split(':')[0].strip()
                if '=' in arg:
                    paramlist.append(f'{paramname}={paramname}')
                else:
                    paramlist.append(paramname)

            params = ', '.join(paramlist)
            print(MODULE_FUNCTION_TEMPLATE_WITH_TYPEHINTS.format(
                fname, args, moduleobj, return_typehint, params))
