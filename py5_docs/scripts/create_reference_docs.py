import re
from pathlib import Path
import textwrap
from collections import defaultdict

import requests
import pandas as pd

from generator.docfiles import Documentation

# PY5_API_EN = Path('py5_docs/Reference/api_en/')
PY5_API_EN = Path('/tmp/docfiles/')
DEST_DIR = Path('/tmp/reference_docs/')

FIRST_SENTENCE_REGEX = re.compile(r'^.*?\.(?=\s)')

PROCESSING_CLASSNAME_LOOKUP = {
    'Py5Graphics': 'PGraphics',
    'Py5Image': 'PImage',
    'Py5Shape': 'PShape',
    'Py5Shader': 'PShader',
    'Py5Font': 'PFont'
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

def format_underlying_java_ref(stem, doc_type, processing_name):
    out = ''

    if processing_name:
        text = ''
        link = processing_name

        processing_classname = PROCESSING_CLASSNAME_LOOKUP.get(stem.split('_')[0])
        if processing_classname:
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


def write_doc_rst_files():
    now = pd.Timestamp.now(tz='UTC')
    now_nikola = now.strftime('%Y-%m-%d %H:%M:%S %Z%z')[:-2] + ':00'
    now_pretty = now.strftime('%B %d, %Y %H:%M:%S%P %Z')
    rstfiles = defaultdict(set)
    docfiles = sorted(PY5_API_EN.glob('*.txt'))
    for num, docfile in enumerate(docfiles):
        doc = Documentation(docfile)
        name = doc.meta['name']
        doc_type = doc.meta['type']
        stem = docfile.stem

        print(f'{num + 1} / {len(docfiles)} creating rst doc for {stem}')

        description = doc.description
        m = FIRST_SENTENCE_REGEX.match(description)
        first_sentence = m.group() if m else description

        underlying_java_ref = format_underlying_java_ref(
            stem, doc_type, doc.meta.get('processing_name'))
        examples = format_examples(name, doc.examples)
        signatures = format_signatures(doc.signatures)
        parameters = format_parameters(doc.variables)

        doc_rst = DOC_TEMPLATE.format(
            name, stem.lower(), now_nikola, first_sentence, examples,
            description, underlying_java_ref, signatures, parameters, now_pretty)

        with open(DEST_DIR / (stem.lower() + '.rst'), 'w') as f:
            f.write(doc_rst)
        rstfiles[stem.split('_', 1)[0].lower()].add((name, stem.lower(), first_sentence))

    # TODO: why don't the classes have their own docstrings that are also included in the reference documentation?
    for group, data in rstfiles.items():
        # TODO: need to use categories and subcategories for main doc page
        # if group == 'sketch':
        #     pass
        # else:
        with open(DEST_DIR / f'{group}_include.rst', 'w') as f:
            for name, stem, first_sentence in sorted(data):
                if group == 'sketch':
                    f.write(f'* `{name} <{stem}/>`_: {first_sentence}\n')
                else:
                    f.write(f'* `{name} <../{stem}/>`_: {first_sentence}\n')


if not DEST_DIR.exists():
    DEST_DIR.mkdir(parents=True)

write_doc_rst_files()
