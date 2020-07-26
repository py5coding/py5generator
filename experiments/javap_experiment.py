import re
import subprocess
from collections import defaultdict

classpath = "build/py5/jars/py5.jar:build/py5/jars/core.jar"

FUNCTION_REGEX = re.compile(r'[\w\s]*?\s+(static)?[\w\s]*?([\w\[\]\.]+) (\w+)\(([^\)]*)\).*;')
CLASS_REGEX = re.compile(r'.*?class ([\w\.,]+)')
EXTENDS_REGEX = re.compile(r'.*?extends ([\w\.,]+)')
IMPLEMENTS_REGEX = re.compile(r'.*?implements ([\w\.,]+)')


def process_block(block):
    data = {}
    signature = block.split('\n', maxsplit=1)[0].strip()

    m = FUNCTION_REGEX.match(signature)
    if m:
        # this is a method
        static, rettype, fname, paramtypes = m.groups()

        paramnames = []
        if 'LocalVariableTable' in block:
            var_table = block.split('LocalVariableTable:\n')[1].strip().split('\n')[1:]
            paramnames = [t[3] for t in [v.split() for v in var_table] if t[0] == '0']
            if not static:
                paramnames = paramnames[1:]

        # if fname == 'usePy5Methods':
        #     print(block)

        data['type'] = 'method'
        data['fname'] = fname
        data['static'] = static == 'static'
        data['rettype'] = rettype
        data['paramtypes'] = [p.strip() for p in paramtypes.split(',')] if paramtypes else []
        data['paramnames'] = paramnames
        assert len(data['paramnames']) == len(data['paramtypes']), (data['paramnames'], data['paramtypes'])
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

    # data['signature'] = signature

    return data


def process_class(classname, data):
    print('examining', classname)

    command = f'javap -classpath {classpath} -public -l {classname}'
    result = subprocess.run(command.split(), capture_output=True)

    if result.returncode > 0:
        error_msg = str(result.stderr, encoding='UTF8').strip()
        raise RuntimeError(f"{error_msg} while running command {command}")

    lines = str(result.stdout, encoding='UTF8')
    if lines.startswith('Compiled from'):
        _, lines = lines.split('\n', maxsplit=1)
    else:
        print(f'{classname} code is missing debug information')
    class_signature, content = lines[:-2].split('\n', maxsplit=1)

    m = IMPLEMENTS_REGEX.match(class_signature)
    if m:
        for interface in m.group(1).split(','):
            process_class(interface.strip(), data)
    m = EXTENDS_REGEX.match(class_signature)
    if m:
        process_class(m.group(1).strip(), data)

    blocks = content.split('\n\n')
    print('processing', classname)
    data.extend([process_block(b) for b in blocks if b])


classname = "py5.core.Py5Applet"
# classname = "processing.core.PApplet"
# classname = "processing.core.PGraphics"
# classname = "processing.core.PImage"
# classname = "java.lang.Cloneable"

data = []
process_class(classname, data)

static_field_data = {}
field_data = {}
method_data = defaultdict(dict)

for d in data:
    if d['type'] == 'field':
        if d['static']:
            static_field_data[d['field_name']] = d['field_type']
        else:
            field_data[d['field_name']] = d['field_type']
    elif d['type'] == 'method':
        method_data[d['fname']][','.join(d['paramtypes'])] = dict(
            static=d['static'], rettype=d['rettype'], paramnames=d['paramnames'])
