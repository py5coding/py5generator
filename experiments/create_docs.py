import re
from collections import defaultdict
import xmltodict


DOC_TEMPLATE = """
# {0}_{1}

{2}

Parameters
----------

$params_{0}_{1}

Notes
-----

{3}

"""


SEE_ALSO_TEMPLATE = """
See Also
--------

{0}

"""


AUTOGEN_REGEX = re.compile(r'\( begin auto-generated from .*?xml \) ')
CODE_REGEX = re.compile(r'(`[^`]*`)')

PY5_CLASS_LOOKUP = {
    'PApplet': 'Sketch',
    'PFont': 'Py5Font',
    'PGraphics': 'Py5Graphics',
    'PImage': 'Py5Image',
    'PShader': 'Py5Shader',
    'PShape': 'Py5Shape',
    'PSurface': 'Py5Surface',
}


def snake_case(name):
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name)
    return name.lower()


class FunctionDocData:

    def __init__(self):
        self.first = ''
        self.full = ''
        self.vars = dict()
        self.see_also = []

    def _text_cleanup(self, text):
        for c in CODE_REGEX.findall(text):
            text = text.replace(c, snake_case(c))
        for pname, py5name in PY5_CLASS_LOOKUP.items():
            text = text.replace(pname, py5name)
        return text

    def report_first(self, first):
        first = re.sub(AUTOGEN_REGEX, '', first or '')
        if first and len(first) > len(self.first):
            self.first = first

    def get_first(self):
        return self._text_cleanup(self.first)

    def report_full(self, full):
        if full and len(full) > len(self.full):
            self.full = full

    def get_full(self):
        return self._text_cleanup(self.full)

    def report_param(self, varname, vardesc):
        self.vars[varname] = vardesc

    def report_see_also(self, classname, call):
        self.see_also.append((classname, snake_case(call)))

    def get_see(self, docdata):
        out = []
        for classname, call in self.see_also:
            see = f'{classname}.{call}'
            key = (classname, call.split('(', 1)[0])
            if key in docdata:
                see += ' : ' + docdata[key].get_first()
            out.append(see)
        return '\n\n'.join(out)


docdata = defaultdict(FunctionDocData)

filename = 'py5_docs/docfiles/javadocs.xml'
with open(filename, 'r') as f:
    root = xmltodict.parse(f.read())
for commenttree in root['commenttrees']['commenttree']:
    pclass = commenttree['@class'].split('.')[-1]
    if pclass not in PY5_CLASS_LOOKUP.keys():
        continue
    py5class = PY5_CLASS_LOOKUP[pclass]
    py5name = snake_case(commenttree['@name'])
    body = commenttree['body']

    fdata = docdata[(py5class, py5name)]
    fdata.report_first(body['first'])
    fdata.report_full(body['full'])

    blocktags = commenttree['blocktags']
    if blocktags:
        tags = blocktags['blocktag']
        if isinstance(tags, str):
            tags = [tags]
        for tag in [t[7:] for t in tags if t.startswith('@param ')]:
            tokens = tag.split(' ', 1)
            if len(tokens) == 2:
                fdata.report_param(*tokens)
        for tag in [t[5:] for t in tags if t.startswith('@see ')]:
            tokens = tag.split('#', 1)
            if len(tokens) == 2:
                fdata.report_see_also(PY5_CLASS_LOOKUP.get(tokens[0], py5class), tokens[1])


with open('/tmp/en.md', 'w') as f:
    for (py5class, py5name), fdata in sorted(docdata.items()):
        doc = DOC_TEMPLATE.format(py5class, py5name, fdata.get_first(), fdata.get_full())
        see_also = fdata.get_see(docdata)
        if see_also:
            doc += SEE_ALSO_TEMPLATE.format(see_also)
        f.write(doc)
    # print('VARS', fdata.vars)
