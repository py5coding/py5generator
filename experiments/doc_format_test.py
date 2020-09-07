import re


test_text = """## meta
name = noise()
category = Math
subcategory = Random
type = method

## description
this is awesome

so is this

## example
image = foo.jpg

foo = 10 # asdf
py5.size(10, 20)
py5.rect(1, 2, 3, 4)
"""

DOC_REGEX = re.compile(r'(?<=## )(\w+)\s(.*?)(?=##|$)', re.DOTALL)
META_REGEX = re.compile(r'(\w*) = (.*)')
CODE_REGEX = re.compile(r'image = ([\w\d\.]+)\s+(.*)', re.DOTALL)


class Documentation:

    def __init__(self, text):
        self.meta = dict()
        self.description = ''
        self.examples = []
        for kind, content in DOC_REGEX.findall(text):
            if kind == 'meta':
                self.meta = dict(META_REGEX.findall(content))
            elif kind == 'description':
                self.description = content.strip()
            elif kind == 'example':
                self.examples.append(CODE_REGEX.match(content.strip()).groups())


doc = Documentation(test_text)
