import re
import subprocess

classpath = "build/py5/jars/py5.jar:build/py5/jars/core.jar"
classname = "processing.core.PApplet"

FUNCTION_REGEX = re.compile(r'[\w\s]*?\s+(static)?[\w\s]*?([\w\[\]\.]+) (\w+)\(([^\)]*)\).*;')


# use -constants to get the value of the final constants
command = f'javap -classpath {classpath} -public -l {classname}'

result = subprocess.run(command.split(), capture_output=True)

if result.returncode > 0:
    error_msg = str(result.stderr, encoding='UTF8').strip()
    print(f"{error_msg} while running command {command}")
else:
    lines = str(result.stdout, encoding='UTF8')
    _, class_signature, content = lines[:-3].split('\n', maxsplit=2)
    blocks = content.split('\n\n')


def process_block(block):
    data = {}
    signature = block.split('\n', maxsplit=1)[0].strip()

    m = FUNCTION_REGEX.match(signature)
    if m:
        # this is a method
        static, rettype, fname, paramtypes = m.groups()

        variables = []
        if 'LocalVariableTable' in block:
            var_table = block.split('LocalVariableTable:\n')[1].split('\n')[1:]
            variables = [t[3] for t in [v.split() for v in var_table] if t[0] == '0']
            if not static:
                variables = variables[1:]

        data['type'] = 'method'
        data['fname'] = fname
        data['static'] = static == 'static'
        data['rettype'] = rettype
        data['paramtypes'] = [p.strip() for p in paramtypes.split(',')] if paramtypes else []
        data['variables'] = variables
        assert len(data['variables']) == len(data['paramtypes']), (data['variables'], data['paramtypes'])
    elif '(' in signature:
        # this is a constructor
        data['type'] = 'constructor'
    else:
        # this is a field
        tokens = signature[:-1].split()
        data['type'] = 'field'
        data['field_name'] = tokens[-1]
        data['field_type'] = tokens[-2]
        data['static'] = 'static' in signature

    data['signature'] = signature

    return data


for b in blocks:
    data = process_block(b)
    if data['type'] == 'method':
        print(data)
