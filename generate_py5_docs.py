# *****************************************************************************
#
#   Part of the py5generator project; generator of the py5 library
#   Copyright (C) 2020-2023 Jim Schmitz
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
import re
from pathlib import Path
import argparse
import textwrap
from io import StringIO
from itertools import groupby
from collections import defaultdict
import json

import requests
import pandas as pd
import black

from generator.docfiles import Documentation

###############################################################################
# ARGUMENT PARSING
###############################################################################


parser = argparse.ArgumentParser(description="Generate py5 library reference documentation")
parser.add_argument('dest_dir', action='store', help='location to write documentation files to')
parser.add_argument('py5_doc_ref_dir', action='store', help='location to write py5 documenation md files')


###############################################################################
# REFERENCE AND LOOKUPS
###############################################################################


FIRST_SENTENCE_REGEX = re.compile(r'^.*?\.(?=\s)')
PARTITION_SIG_REGEX = re.compile(r'(\w*)\((.*?)\)( ->.*)')

REF_COLUMN_STARTS = {
    'Sketch': [('lights_camera', 'camera'), ('shape', '')],
    'Py5Shape': [('object', 'organization'), ('transform', '')],
    'Py5Graphics': [('lights_camera', 'camera'), ('shape', '')],
}

CLASS_CATEGORY_LOOKUP = {
    'Py5Graphics': ('rendering', ''),
    'Py5Image': ('image', ''),
    'Py5Shape': ('shape', ''),
    'Py5Shader': ('rendering', 'shaders'),
    'Py5Font': ('typography', ''),
    'Py5Surface': ('environment', ''),
}

PROCESSING_CLASSNAME_LOOKUP = {
    'Py5Graphics': 'PGraphics',
    'Py5Image': 'PImage',
    'Py5Shape': 'PShape',
    'Py5Shader': 'PShader',
    'Py5Font': 'PFont',
    'Py5Surface': 'PSurface',
}

CATEGORY_LOOKUP = {
    '': 'Unknown',
    'lights_camera': 'Lights & Camera',
    'loading_displaying': 'Loading / Displaying',
    '2d_primitives': '2D Primitives',
    '3d_primitives': '3D Primitives',
    'time_date': 'Time & Date',
    'creating_reading': 'Creating / Reading',
}

DOC_TEMPLATE = """{0}

{1}
{2}
## Description

{3}{4}
{5}
Updated on {6}
"""

MAGIC_TEMPLATE = """{0}

{1}
{2}
## Description

{3}

## Usage

```python

    {4}
```

## Arguments

```python

{5}
```

Updated on {6}
"""

CLASS_DOC_TEMPLATE = """{0}

{1}
{2}
## Description

{3}{4}

The following {5} are provided:

```{{include}} include_{6}.md
```

Updated on {7}
"""


###############################################################################
# HELPER FUNCTIONS
###############################################################################


def format_underlying_java_ref(stem, doc_type, processing_name, valid_link_cache):
    out = ''

    if processing_name:
        text = ''
        link = processing_name

        processing_classname = PROCESSING_CLASSNAME_LOOKUP.get(stem.split('_')[0])
        if doc_type not in ['class', 'pseudoclass'] and processing_classname:
            text = processing_classname + '.'
            link = f'{processing_classname}_{link}'
        text += processing_name
        if doc_type == 'method':
            link += '_'
        link = f'https://processing.org/reference/{link}.html'

        if link in valid_link_cache:
            valid = valid_link_cache[link]
        else:
            valid = requests.get(link).status_code == 200
            valid_link_cache[link] = valid

        out = f'\n\nUnderlying Processing {doc_type}: '
        if valid:
            out += f'[{text}]({link})'
        else:
            out += f'{text}'

    return out


def format_examples(name, examples):
    out = ''

    if examples:
        out += '\n## Examples\n\n'
        out += '<div class="example-table">\n\n'
        for img, code in examples:
            out += '<div class="example-row"><div class="example-cell-image">\n\n'
            if img:
                out += f'![example picture for {name}](/images/reference/{img})\n\n'
            out += '</div><div class="example-cell-code">\n\n'
            out += f'```python\n\n{textwrap.indent(code, "    ")}\n```\n\n'
            out += '</div></div>\n\n'
        out += '</div>\n'

    return out


def tokenize_params(params):
    bracket_count = 0
    out = ''
    for c in params:
        if c == ',' and bracket_count == 0:
            yield out.strip()
            out = ''
        else:
            out += c
        if c == '[':
            bracket_count += 1
        if c == ']':
            bracket_count -= 1
    yield out.strip()


def format_signatures_variables(signatures, variables):
    out = ''

    if signatures:
        new_signatures = []
        for s in signatures:
            name, params, ret = PARTITION_SIG_REGEX.match(s).groups()

            if params:
                new_params = []
                for param in tokenize_params(params):
                    if param in variables:
                        new_params.append((param, variables[param.replace('*', '')]))
                    else:
                        new_params.append((param, ''))

                new_params2 = []
                for i, (param, vardesc) in enumerate(new_params):
                    maybe_comma = ',' if i < len(new_params) - 1 else ''
                    new_params2.append(f"{param}{maybe_comma}  # {vardesc}" if vardesc else f"{param}{maybe_comma}")

                params = '\n'.join(new_params2) + '\n'
                line_length = max([len(l) for l in new_params2]) + 5
            else:
                line_length = 120

            new_signatures.append(black.format_str(f"def {name}({params}){ret}: pass", mode=black.Mode(line_length=line_length))[4:-11])

        out += '\n## Signatures\n\n```python\n\n'
        has_multi_line_signature = max(len(s.strip().split('\n')) for s in new_signatures) > 1
        out += textwrap.indent(('\n\n' if has_multi_line_signature else '\n').join(new_signatures), '    ')
        out += '\n```\n'

    return out


def write_main_ref_columns(filename, columns):
    with open(filename, 'w') as f:
        f.write('<table style="width:100%"><tr><td style="vertical-align:top">\n\n')
        f.write(columns[0].getvalue())
        f.write('\n\n    </td><td style="vertical-align:top">\n\n')
        f.write(columns[1].getvalue())
        f.write('\n\n    </td><td style="vertical-align:top">\n\n')
        f.write(columns[2].getvalue())
        f.write('\n\n    </td></tr></table>\n\n')


def compare_files(old_filename, new_content):
    try:
        with open(old_filename, 'r') as f:
            old_content = f.read()
        old_content = re.sub(r'^\.\. date: .*$', '', old_content, flags=re.MULTILINE)
        old_content = re.sub(r'^Updated on .*$', '', old_content, flags=re.MULTILINE)
        new_content = re.sub(r'^\.\. date: .*$', '', new_content, flags=re.MULTILINE)
        new_content = re.sub(r'^Updated on .*$', '', new_content, flags=re.MULTILINE)
        return old_content == new_content
    except FileNotFoundError:
        return False


def write_category_heading(f, catname, subcategory=False):
    if catname in CATEGORY_LOOKUP:
        catname = CATEGORY_LOOKUP[catname]
    else:
        catname = ' '.join([w.capitalize() for w in catname.split('_')])
    prefix = '#' * (4 if subcategory else 3)
    f.write(f'\n{prefix} {catname}\n')


def magic_help_strings(program_name, argument_data):
    argument_args = []
    for datum in argument_data:
        arg_str, *help = datum.split('\n', maxsplit=1)
        args, kwargs = eval(f"(lambda *args, **kwargs: (args, kwargs))({arg_str})")
        if help:
            kwargs['help'] = help[0]
        argument_args.append((args, kwargs))

    parser = argparse.ArgumentParser(prog=program_name, add_help=False)
    for args, kwargs in argument_args:
        parser.add_argument(*args, **kwargs)

    usage = parser.format_usage()
    arguments = parser.format_help()[len(usage):].strip()
    usage = usage[7:]

    return usage, arguments


###############################################################################
# MAIN
###############################################################################


def write_doc_md_files(dest_dir, py5_doc_ref_dir):
    now = pd.Timestamp.now(tz='UTC')
    now_pretty = now.strftime('%B %d, %Y %H:%M:%S%P %Z')

    # create the destination directories
    (dest_dir / 'reference').mkdir(parents=True, exist_ok=True)

    # load valid link cache if it exists
    valid_link_cache = dict()
    valid_link_cache_file = py5_doc_ref_dir / 'valid_link_cache.json'
    if valid_link_cache_file.exists():
        with open(valid_link_cache_file, 'r') as f:
            valid_link_cache = json.load(f)

    mdfiles = defaultdict(set)
    docfiles = sorted(py5_doc_ref_dir.glob('*.txt'))
    for num, docfile in enumerate(docfiles):
        doc = Documentation(docfile)
        name = doc.meta['name']
        item_type = doc.meta['type']
        stem = docfile.stem
        group = stem.split('_', 1)[0]
        slug = stem.lower()

        print(f'{num + 1} / {len(docfiles)} generating md doc for {stem}')

        description = doc.description
        m = FIRST_SENTENCE_REGEX.match(description)
        first_sentence = m.group() if m else description

        underlying_java_ref = format_underlying_java_ref(
            stem, item_type, doc.meta.get('processing_name'), valid_link_cache)
        examples = format_examples(name, doc.examples)

        if item_type in ['class', 'pseudoclass']:
            title = f'# {name}'
            provides_description = doc.meta.get('provides_description', 'methods and fields')
            doc_md = CLASS_DOC_TEMPLATE.format(
                title, first_sentence, examples,
                description, underlying_java_ref, provides_description,
                stem.lower(), now_pretty)
        elif item_type in ['line magic', 'cell magic']:
            usage, arguments = magic_help_strings(name, doc.arguments)
            arguments = textwrap.indent(arguments, prefix='    ')
            title = f'# {name}'
            doc_md = MAGIC_TEMPLATE.format(
                title, first_sentence, examples,
                description, usage, arguments, now_pretty)
        else:
            signatures = format_signatures_variables(doc.signatures, doc.variables)
            if group in ['Sketch', 'Py5Functions', 'Py5Magics']:
                title = name
            elif group == 'Py5Tools':
                title = f"py5_tools.{name}"
            else:
                title = f"{group}.{name}"

            title = f'# {title}'
            doc_md = DOC_TEMPLATE.format(
                title, first_sentence, examples,
                description, underlying_java_ref, signatures, now_pretty)

        # only write new file if more changed than the timestamp
        dest_filename = dest_dir / 'reference' / f'{stem.lower()}.md'
        if not compare_files(dest_filename, doc_md):
            print('writing file', dest_filename)
            with open(dest_filename, 'w') as f:
                f.write(doc_md)

        # collect data for the include files
        if item_type not in ['class', 'pseudoclass']:
            if group in ['Sketch']:
                mdfiles['Sketch'].add(
                    (name, slug, first_sentence,
                     (doc.meta['category'].replace('None', ''), doc.meta['subcategory'].replace('None', ''))
                    )
                )
            elif group in ['Py5Shape', 'Py5Graphics']:
                mdfiles[group].add(
                    (name, slug, first_sentence,
                     (doc.meta['category'].replace('None', ''), doc.meta['subcategory'].replace('None', ''))
                    )
                )
            else:
                mdfiles[group].add((name, slug, first_sentence))

    for group, data in mdfiles.items():
        if group in ['Sketch', 'Py5Shape', 'Py5Graphics']:
            organized_data = groupby(sorted(data, key=lambda x: x[3]), key=lambda x: x[3])
            prev_category = ('_', '_')
            columns = [StringIO() for _ in range(3)]
            column_num = 0
            for category, contents in organized_data:
                if category in REF_COLUMN_STARTS[group]:
                    column_num += 1
                if category[0] != prev_category[0]:
                    write_category_heading(columns[column_num], category[0])
                if category[1] != prev_category[1] and category[1] != '':
                    write_category_heading(columns[column_num], category[1], subcategory=True)
                prev_category = category
                columns[column_num].write('\n')
                for (name, stem, first_sentence, _) in sorted(contents):
                    columns[column_num].write(f'* [{name}]({stem})\n')
            write_main_ref_columns(dest_dir / 'reference' / f'include_{group.lower()}.md', columns)
        else:
            with open(dest_dir / 'reference' / f'include_{group.lower()}.md', 'w') as f:
                for name, stem, first_sentence in sorted(data):
                    f.write(f'* [{name}]({stem}): {first_sentence}\n')

    # save the valid link cache
    with open(valid_link_cache_file, 'w') as f:
        json.dump(valid_link_cache, f, indent=2)


def main():
    args = parser.parse_args()
    write_doc_md_files(Path(args.dest_dir), Path(args.py5_doc_ref_dir))


if __name__ == '__main__':
    main()
