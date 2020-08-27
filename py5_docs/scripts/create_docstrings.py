from io import StringIO
import pickle
from html.parser import HTMLParser
from pathlib import Path

import xmltodict


DOC_TEMPLATE = """
{0}.

Parameters
----------

list params

Notes
-----

{1}
"""


PY5_API_EN = Path('py5_docs/Reference/api_en/')


class TagRemover(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = StringIO()

    def handle_data(self, d):
        self.text.write(d)

    def get_data(self):
        return self.text.getvalue()


def remove_html(html):
    tr = TagRemover()
    tr.feed(html)
    return tr.get_data()


docstrings = {}
for xml_file in PY5_API_EN.glob('*.xml'):
    print(xml_file)
    key = tuple(xml_file.stem.split('_', maxsplit=1))
    with open(xml_file, 'r') as f:
        data = xmltodict.parse(f.read())
        # TODO: I don't want to remove all html, I want to replace the <b> tags with backticks, for example
        description = remove_html(data['root']['description']).strip()
        first_sentence = description.split('. ', maxsplit=1)[0]
        docstring = DOC_TEMPLATE.format(first_sentence, description)
        docstrings[key] = docstring


with open('/tmp/docstrings.p', 'wb') as f:
    pickle.dump(docstrings, f)
