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
import re
from pathlib import Path
import argparse
import textwrap
from io import StringIO
from itertools import groupby
from collections import defaultdict

import requests
import pandas as pd

from generator.docfiles import Documentation

###############################################################################
# ARGUMENT PARSING
###############################################################################


parser = argparse.ArgumentParser(description="Generate py5 library reference documentation")
parser.add_argument('dest_dir', action='store', help='location to write documentation files to')
parser.add_argument('py5_doc_ref_dir', action='store', help='location to write py5 documenation rst files')


###############################################################################
# REFERENCE AND LOOKUPS
###############################################################################


FIRST_SENTENCE_REGEX = re.compile(r'^.*?\.(?=\s)')

MAIN_REF_COLUMN_STARTS = [('lights_camera', 'camera'), ('shape', '')]

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

DOC_TEMPLATE = """.. title: {0}
.. slug: {1}
.. date: {2}
.. tags:
.. category:
.. link:
.. description: py5 {0} documentation
.. type: text

{3}
{4}
Description
===========

{5}{6}
{7}
{8}
Updated on {9}

"""

MAGIC_TEMPLATE = """.. title: {0}
.. slug: {1}
.. date: {2}
.. tags:
.. category:
.. link:
.. description: py5 {0} documentation
.. type: text

{3}
{4}
Description
===========

{5}

Usage
=====

.. code::

    {6}
Arguments
=========

.. code::

{7}

Updated on {8}

"""

CLASS_DOC_TEMPLATE = """.. title: {0}
.. slug: {1}
.. date: {2}
.. tags:
.. category:
.. link:
.. description: py5 {0} documentation
.. type: text

{3}
{4}
Description
===========

{5}{6}

This class provides the following methods and fields:

.. include:: include/{7}_include.rst

Updated on {8}

"""


###############################################################################
# HELPER FUNCTIONS
###############################################################################


def format_underlying_java_ref(stem, doc_type, processing_name):
    out = ''

    if processing_name:
        text = ''
        link = processing_name

        processing_classname = PROCESSING_CLASSNAME_LOOKUP.get(stem.split('_')[0])
        if doc_type != 'class' and processing_classname:
            text = processing_classname + '.'
            link = f'{processing_classname}_{link}'
        text += processing_name
        if doc_type == 'method':
            link += '_'
        link = f'https://processing.org/reference/{link}.html'

        # test the link to make sure it is valid
        out = f'\n\nUnderlying Java {doc_type}: '
        if requests.get(link).status_code == 200:
            out += f'`{text} <{link}>`_'
        else:
            out += f'{text}'

    return out


def format_examples(name, examples):
    out = ''

    if examples:
        out += '\nExamples\n========\n\n'
        out += '.. raw:: html\n\n    <div class="example-table">\n\n'
        for img, code in examples:
            out += '.. raw:: html\n\n    <div class="example-row"><div class="example-cell-image">\n\n'
            if img:
                out += f'.. image:: /images/reference/{img}\n    :alt: example picture for {name}\n\n'
            out += '.. raw:: html\n\n    </div><div class="example-cell-code">\n\n'
            out += f'.. code:: python\n    :number-lines:\n\n{textwrap.indent(code, "    ")}\n\n'
            out += '.. raw:: html\n\n    </div></div>\n\n'
        out += '.. raw:: html\n\n    </div>\n'

    return out


def format_signatures(signatures):
    out = ''

    if signatures:
        out += '\nSyntax\n======\n\n.. code:: python\n\n'
        out += textwrap.indent('\n'.join(signatures), '    ')

    return out


def format_parameters(variables):
    out = ''

    if variables:
        out += '\nParameters\n==========\n\n'
        for var, desc in variables.items():
            if ':' in var:
                varname, vartype = var.split(':')
                out += f'* **{varname}**: `{vartype.strip()}` - {desc}\n'
            else:
                out += f'* **{var}**: - {desc}\n'
        out += '\n'

    return out


def write_main_ref_columns(filename, columns):
    with open(filename, 'w') as f:
        f.write('.. raw:: html\n\n    <table style="width:100%"><tr><td style="vertical-align:top">\n\n')
        f.write(columns[0].getvalue())
        f.write('\n\n.. raw:: html\n\n    </td><td style="vertical-align:top">\n\n')
        f.write(columns[1].getvalue())
        f.write('\n\n.. raw:: html\n\n    </td><td style="vertical-align:top">\n\n')
        f.write(columns[2].getvalue())
        f.write('\n\n.. raw:: html\n\n    </td></tr></table>\n\n')


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
    char = '-' if subcategory else '='
    f.write(f'\n{catname}\n{char * len(catname)}\n')


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


def write_doc_rst_files(dest_dir, py5_doc_ref_dir):
    now = pd.Timestamp.now(tz='UTC')
    now_nikola = now.strftime('%Y-%m-%d %H:%M:%S %Z%z')[:-2] + ':00'
    now_pretty = now.strftime('%B %d, %Y %H:%M:%S%P %Z')

    # create the destination directories
    (dest_dir / 'reference').mkdir(parents=True, exist_ok=True)
    (dest_dir / 'include').mkdir(parents=True, exist_ok=True)

    rstfiles = defaultdict(set)
    docfiles = sorted(py5_doc_ref_dir.glob('*.txt'))
    for num, docfile in enumerate(docfiles):
        doc = Documentation(docfile)
        name = doc.meta['name']
        item_type = doc.meta['type']
        stem = docfile.stem
        if stem == 'Sketch':
            continue
        group = stem.split('_', 1)[0]
        if group in ['Sketch', 'Py5Functions', 'Py5Tools', 'Py5Magics']:
            slug = stem[len(group)+1:].lower()
        else:
            slug = stem.lower()

        print(f'{num + 1} / {len(docfiles)} generating rst doc for {stem}')

        description = doc.description
        m = FIRST_SENTENCE_REGEX.match(description)
        first_sentence = m.group() if m else description

        underlying_java_ref = format_underlying_java_ref(
            stem, item_type, doc.meta.get('processing_name'))
        examples = format_examples(name, doc.examples)

        if item_type == 'class':
            doc_rst = CLASS_DOC_TEMPLATE.format(
                name, slug, now_nikola, first_sentence, examples,
                description, underlying_java_ref, stem.lower(), now_pretty)
        elif item_type in ['line magic', 'cell magic']:
            usage, arguments = magic_help_strings(name, doc.arguments)
            arguments = textwrap.indent(arguments, prefix='    ')
            doc_rst = MAGIC_TEMPLATE.format(
                name, slug, now_nikola, first_sentence, examples,
                description, usage, arguments, now_pretty)
        else:
            signatures = format_signatures(doc.signatures)
            parameters = format_parameters(doc.variables)

            doc_rst = DOC_TEMPLATE.format(
                name, slug, now_nikola, first_sentence, examples,
                description, underlying_java_ref, signatures, parameters, now_pretty)

        # only write new file if more changed than the timestamp
        dest_filename = dest_dir / 'reference' / f'{stem.lower()}.rst'
        if not compare_files(dest_filename, doc_rst):
            print('writing file', dest_filename)
            with open(dest_filename, 'w') as f:
                f.write(doc_rst)
        if item_type == 'class':
            if stem != 'Sketch':
                rstfiles['Sketch'].add((name, slug, first_sentence, CLASS_CATEGORY_LOOKUP[name]))
        else:
            if group in ['Sketch', 'Py5Functions', 'Py5Tools', 'Py5Magics']:
                rstfiles['Sketch'].add(
                    (name, slug, first_sentence,
                     (doc.meta['category'].replace('None', ''), doc.meta['subcategory'].replace('None', ''))
                    )
                )
            else:
                rstfiles[group].add((name, slug, first_sentence))

    for group, data in rstfiles.items():
        if group == 'Sketch':
            organized_data = groupby(sorted(data, key=lambda x: x[3]), key=lambda x: x[3])
            prev_category = ('_', '_')
            columns = [StringIO() for _ in range(3)]
            column_num = 0
            for category, contents in organized_data:
                if category in MAIN_REF_COLUMN_STARTS:
                    column_num += 1
                if category[0] != prev_category[0]:
                    write_category_heading(columns[column_num], category[0])
                if category[1] != prev_category[1] and category[1] != '':
                    write_category_heading(columns[column_num], category[1], subcategory=True)
                prev_category = category
                columns[column_num].write('\n')
                for (name, stem, first_sentence, _) in sorted(contents):
                    columns[column_num].write(f'* `{name} <{stem}/>`_\n')
            write_main_ref_columns(dest_dir / 'include' / f'{group.lower()}_include.rst', columns)
        else:
            with open(dest_dir / 'include' / f'{group.lower()}_include.rst', 'w') as f:
                for name, stem, first_sentence in sorted(data):
                    f.write(f'* `{name} <../{stem}/>`_: {first_sentence}\n')



def main():
    args = parser.parse_args()
    write_doc_rst_files(Path(args.dest_dir), Path(args.py5_doc_ref_dir))


if __name__ == '__main__':
    main()
