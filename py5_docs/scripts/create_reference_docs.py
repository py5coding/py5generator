import re
from pathlib import Path
import textwrap

import pandas as pd

from generator.docfiles import Documentation

# TODO: Need method/attribute index pages for Sketch and other classes


# PY5_API_EN = Path('py5_docs/Reference/api_en/')
PY5_API_EN = Path('/tmp/docfiles/')
DEST_DIR = Path('/tmp/reference_docs/')

FIRST_SENTENCE_REGEX = re.compile(r'^.*?\.(?=\s)')

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

{5}
{6}
{7}
Updated on {8}

"""

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
    for docfile in sorted(PY5_API_EN.glob('*.txt')):
        doc = Documentation(docfile)
        name = doc.meta['name']
        stem = docfile.stem.lower()

        description = doc.description
        m = FIRST_SENTENCE_REGEX.match(description)
        first_sentence = m.group() if m else description

        examples = format_examples(name, doc.examples)
        signatures = format_signatures(doc.signatures)
        parameters = format_parameters(doc.variables)

        doc_rst = DOC_TEMPLATE.format(
            name, stem, now_nikola, first_sentence, examples, description,
            signatures, parameters, now_pretty)

        with open(DEST_DIR / (stem + '.rst'), 'w') as f:
            f.write(doc_rst)


if not DEST_DIR.exists():
    DEST_DIR.mkdir(parents=True)

write_doc_rst_files()
