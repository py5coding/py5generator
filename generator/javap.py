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
Parse the output of `javap` to get info on a class's methods and fields.

Java classes need to have been compiled with debug information for this to work.
"""
import re
import subprocess
from collections import defaultdict

classpath = ''

FUNCTION_REGEX = re.compile(r'[\w\s]*?\s+(static)?[\w\s]*?([\w\[\]\.]+) (\w+)\(([^\)]*)\).*;')
CLASS_REGEX = re.compile(r'.*?class ([\w\.,]+)')
EXTENDS_REGEX = re.compile(r'.*?extends ([\w\.,]+)')
IMPLEMENTS_REGEX = re.compile(r'.*?implements ([\w\.,]+)')


def process_block(block, is_interface):
    data = {}
    signature = block.split('\n', maxsplit=1)[0].strip()

    m = FUNCTION_REGEX.match(signature)
    if m and not is_interface:
        # this is a method
        static, rettype, fname, paramtypes = m.groups()

        paramnames = []
        if 'LocalVariableTable' in block:
            var_table = block.split('LocalVariableTable:\n')[1].strip().splitlines()[1:]
            paramnames = [t[3] for t in [v.split() for v in var_table] if t[0] == '0']
            if not static:
                paramnames = paramnames[1:]

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
        data['type'] = 'field'
        if '=' in signature:
            tokens = signature.split('=')
            data['constant'] = True
            data['field_value'] = tokens[1][:-1].strip()
            signature = tokens[0].strip()
        else:
            data['constant'] = False
            signature = signature[:-1]  # remove ;
        tokens = signature.split()
        data['field_name'] = tokens[-1]
        data['field_type'] = tokens[-2]

        if data['field_type'] == 'float' and data.get('field_value', 'X')[-1] == 'f':
            data['field_value'] = data['field_value'][:-1]

    return data


def process_class(classname, data):
    command = f'javap -classpath {classpath} -constants -public -l {classname}'
    result = subprocess.run(command.split(), capture_output=True)

    if result.returncode > 0:
        error_msg = str(result.stderr, encoding='UTF8').strip()
        raise RuntimeError(f"{error_msg} while running command {command}")

    lines = str(result.stdout, encoding='UTF8')
    if lines.startswith('Compiled from'):
        _, lines = lines.split('\n', maxsplit=1)
    else:
        raise RuntimeError(f'{classname} code is missing debug information')
    class_signature, content = lines[:-2].split('\n', maxsplit=1)

    is_interface = 'interface' in class_signature

    m = IMPLEMENTS_REGEX.match(class_signature)
    if m:
        for interface in m.group(1).split(','):
            process_class(interface.strip(), data)
    m = EXTENDS_REGEX.match(class_signature)
    if m:
        process_class(m.group(1).strip(), data)

    blocks = content.split('\n\n')
    data.extend([process_block(b, is_interface) for b in blocks if b])


def get_class_information(classname):
    """parse the output of `javap` to get info on a class's methods and fields

    Java classes need to have been compiled with debug information for this to
    work.
    """
    data = []
    process_class(classname, data)

    constant_field_data = {}
    field_data = {}
    method_data = defaultdict(dict)

    for d in data:
        if d['type'] == 'field':
            if d['constant']:
                constant_field_data[d['field_name']] = d['field_value']
            else:
                field_data[d['field_name']] = d['field_type']
        elif d['type'] == 'method':
            method_data[d['fname']][','.join(d['paramtypes'])] = dict(
                static=d['static'], rettype=d['rettype'], paramnames=d['paramnames'])

    # cannot have a method and field with the same name. drop the field if there
    # is a collision.
    for key in list(field_data.keys()):
        if key in method_data:
            del field_data[key]
    for key in list(constant_field_data.keys()):
        if key in method_data:
            del constant_field_data[key]

    return constant_field_data, field_data, method_data
