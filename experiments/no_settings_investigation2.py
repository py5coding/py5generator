import re
from pathlib import Path
import textwrap

from generator.docfiles import Documentation


PY5_API_EN = Path('py5_docs/Reference/api_en/')


SETTINGS_REGEX = re.compile(r'^def settings\(\):', flags=re.MULTILINE)
SETUP_REGEX = re.compile(r'^def setup\(\):', flags=re.MULTILINE)
SETUP_CODE_REGEX = re.compile(r'^def setup\(\):.*?(?=^\w|\Z)', flags=re.MULTILINE | re.DOTALL)
DRAW_REGEX = re.compile(r'^def draw\(\):', flags=re.MULTILINE)
CODE_REGEXES = {f: re.compile(r'^\s*(' + f + r'\([^\)]*\))', flags=re.MULTILINE)
                for f in ['size', 'full_screen', 'smooth', 'no_smooth', 'pixel_density']}


def transform_code(code):
    "transform functionless or setttings-less py5 code into code that runs"
    if SETTINGS_REGEX.search(code):
        return code
    no_setup = SETUP_REGEX.search(code) is None
    no_draw = DRAW_REGEX.search(code) is None

    # get just the setup function if it is defined
    code2 = code if no_setup else SETUP_CODE_REGEX.search(code).group()
    # find the key lines in the relevant code
    matches = [m for m in [r.search(code2) for r in CODE_REGEXES.values()] if m]

    # if anything was found, build the settings function
    if matches:
        lines = [(m.start(), m.group(1)) for m in matches]
        settings = 'def settings():\n'
        for start, line in sorted(lines):
            settings += f'    {line}\n'
            # replace the original line so it doesn't get called in setup
            code = code.replace(line, 'pass')
    else:
        settings = ''

    if no_setup and no_draw:
        # put all of the remaining code into a setup function
        remaining_code = 'def setup():\n' + textwrap.indent(code, prefix='    ')
    else:
        # remaining code has been modified with key lines moved from setup to settings
        remaining_code = code

    return f'{settings.strip()}\n\n{remaining_code.strip()}\n'


for docfile in sorted(PY5_API_EN.glob('*.txt')):
    doc = Documentation(docfile)
    if doc.examples:
        print('*' * 20)
        print(docfile.name)
    for image_name, code in doc.examples:
        print('*' * 5, image_name)
        print(code)
        print('*' * 5)
        new_code = transform_code(code)
        print(new_code)
