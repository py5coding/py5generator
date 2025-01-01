# *****************************************************************************
#
#   Part of the py5generator project; generator of the py5 library
#   Copyright (C) 2020-2025 Jim Schmitz
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
This code is no longer used but might be pillaged one day to help convert Java example code.

It was written to convert Processing's XML documentation data to py5's.
"""
import re
from pathlib import Path
from io import StringIO
import string
import shlex
from html.parser import HTMLParser

import autopep8

import pandas as pd

from generator.docfiles import Documentation


NEW_TEMPLATE = """@@ meta
name = {0}
type = {1}
{2}
@@ description
The documentation for this field or method has not yet been written. If you know what it does, please help out with a pull request to the relevant file in https://github.com/py5coding/py5generator/tree/master/py5_docs/Reference/api_en/.

"""

PROCESSING_API_EN = Path("../processing-docs/content/api_en/")
PY5_API_EN = Path("py5_docs/Reference/api_en/")

PY5_CLASS_LOOKUP = {
    "PApplet": "Sketch",
    "PFont": "Py5Font",
    "PGraphics": "Py5Graphics",
    "PImage": "Py5Image",
    "PShader": "Py5Shader",
    "PShape": "Py5Shape",
    "PSurface": "Py5Surface",
}

SNAKE_CASE_OVERRIDE = {
    "null": "None",
    "true": "True",
    "false": "False",
}

CODE_REPLACEMENTS = {
    "&0x92": "\\",
    "filter(": "apply_filter(",
    "(mouse_pressed)": "(is_mouse_pressed())",
    "Py5Image img1, img2": "Py5Image img1\nPy5Image img2",
    "Py5Image photo, mask_image": "Py5Image photo\nPy5Image mask_image",
    "distribution = new float[360]": "distribution = [0] * 360",
    "(float y)": "(y)",
    "width/2": "width//2",
    "height/2": "height//2",
    "from": "from_",
}

CONSTANT_CHARACTERS = string.ascii_uppercase + string.digits + "_"


def snake_case(name):
    if all([c in CONSTANT_CHARACTERS for c in list(name)]):
        return name
    if re.match(r"0x[\da-fA-F]{2,}", name):
        return name
    elif (stem := name.replace("()", "")) in PY5_CLASS_LOOKUP:
        return name.replace(stem, PY5_CLASS_LOOKUP[stem])
    elif name in SNAKE_CASE_OVERRIDE:
        return SNAKE_CASE_OVERRIDE[name]
    else:
        name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
        name = re.sub("([a-z0-9])([A-Z])", r"\1_\2", name)
        return name.lower()


def convert_to_python(code):
    code = code.replace("println", "print")
    code = code.replace("//", "#")

    # minor issues
    for k, v in CODE_REPLACEMENTS.items():
        code = code.replace(k, v)

    # convert function declarations
    code = re.sub(r"void\s+(\w+)\(([\w\s]*)\)\s*{", r"def \1(\2):", code)

    # convert if statements
    code = re.sub(r"if\s+\((.+?)\)\s*{", r"if \1:", code)
    code = code.replace("} else if", "elif")
    code = code.replace("} else {", "else:")

    # convert for loops to range iteration
    while m := re.search(
        r"for \(\w+\s+(\w+)\s*=\s*(\d+); \1\s*([<=>]+)\s*([^;]+);\s*\1\s*([^\)]*)\)\s*{",
        code,
    ):
        end = m.group(4) + ("" if m.group(3) == "<" else " + 1")
        step = "" if (step := m.group(5)) == "++" else f",{step.split('=')[1]}"
        code = code.replace(
            m.group(), f"for {m.group(1)} in range({m.group(2)}, {end}{step}):"
        )

    # convert variable declarations
    # this converts declarations with assignments
    for m in re.finditer(r"^(\s*)([\w\[\]]+) +(\w+)\s*=", code, flags=re.MULTILINE):
        if m.group(2) in {"for", "if"}:
            continue
        else:
            code = code.replace(m.group(), f"{m.group(1)}{m.group(3)} =")

    # this removes declarations without assignments but adds global statement to setup if it is present
    global_vars = []
    while m := re.search(r"^[\w\[\]]+ +([\w #\d;]+)$", code, flags=re.MULTILINE):
        global_vars.append(m.group(1))
        code = code.replace(m.group(), "")

    if global_vars:
        replacement = "\n".join([f"  global {g}" for g in global_vars])
        code = code.replace("def setup():", f"def setup():\n{replacement}")

    # convert x.length to len(x)
    code = re.sub(r"([\w\.]+)\.length", r"len(\1)", code)

    # get rid of the closing braces
    code = re.sub(r"^\s*}", "", code, flags=re.MULTILINE)

    # remove import statements
    code = re.sub(r"^import .*$", "", code, flags=re.MULTILINE)

    # indenting spacing == 4
    code = re.sub(r"^( +)(?!$)", r"\1\1", code, flags=re.MULTILINE)

    # because of course ;)
    code = code.replace(";", "")

    return code


def adjust_code(code, use_autopep8=False):
    if code == "#":
        return code
    code = re.sub(r"#(?=[\da-fA-F]{2,})", "0x", code)
    tokens = shlex.shlex(code)
    tokens.whitespace = ""
    new_code = StringIO()
    for token in tokens:
        if token[0] in {'"'}:
            new_code.write(token)
        else:
            new_code.write(snake_case(token))

    code = new_code.getvalue()
    code = convert_to_python(code)

    if use_autopep8:
        code = autopep8.fix_code(code, options={"aggressive": 2})

    return code


class TagRemover(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = StringIO()
        self._in_code_block = False
        self._tag_list = set()

    def handle_starttag(self, tag, attrs):
        if tag in {"b", "tt", "strong", "pre"}:
            self.text.write("``")
            self._in_code_block = True
        elif tag in {"i", "em"}:
            self.text.write("*")
        elif tag in {"a", "br"}:
            pass
        else:
            self._tag_list.add(tag)

    def handle_endtag(self, tag):
        # documentation erroniously uses </s> to end some <b> tags
        if tag in {"b", "s", "tt", "strong", "pre"}:
            self.text.write("``")
            self._in_code_block = False
        elif tag in {"i", "em"}:
            self.text.write("*")
        elif tag in {"br", "a"}:
            pass
        else:
            self._tag_list.add(tag)

    def handle_data(self, d):
        if self._in_code_block:
            self.text.write(adjust_code(d))
        else:
            self.text.write(d)

    def get_data(self):
        if self._tag_list:
            print(self._tag_list)
        return self.text.getvalue()


def remove_html(html):
    # remove html tags and do some conversions
    tr = TagRemover()
    tr.feed(html)
    text = tr.get_data()
    # find text that looks like a function reference
    while m := re.search(r"(?<!`)(\w+\(\))(?!`)", text):
        text = text[: m.start()] + f"``{snake_case(m.group())}``" + text[m.end() :]

    return text


# read the class datafiles so I know what methods and fields are relevant
class_data_info = dict()
class_resource_data = Path("py5_resources", "data")
papplet_category_data = None
for pclass in PY5_CLASS_LOOKUP.keys():
    filename = "py5applet.csv" if pclass == "PApplet" else pclass.lower() + ".csv"
    class_data = pd.read_csv(class_resource_data / filename)
    class_data = class_data.fillna("").set_index("processing_name")
    class_data_info[pclass] = class_data.query("available_in_py5==True")
    if pclass == "PApplet":
        papplet_category_data = class_data_info[pclass].set_index("py5_name")[
            ["category", "subcategory"]
        ]


# go through the class data info and for each relevant method and field
# for each find the xml documentation file or note new files that must be created
xml_files = []
new_xml_files = []
for pclass, class_data in class_data_info.items():
    for processing_name, data in class_data.iterrows():
        item_type = data["type"]
        implementation_from_processing = data["implementation_from_processing"]
        if item_type in ["static field", "unknown"]:
            # skip, we don't care
            continue
        py5_name = data["py5_name"]
        if not implementation_from_processing:
            if pclass == "PApplet":
                # definitely a new function I need to document
                new_xml_files.append((pclass, py5_name, item_type, None))
            continue

        # first try the correct documentation filename
        if processing_name:
            if pclass == "PApplet":
                name = f"{processing_name}.xml"
            else:
                name = f"{pclass}_{processing_name}.xml"
            if processing_name == "hint":
                xml_file = PROCESSING_API_EN / "include" / name
            else:
                xml_file = PROCESSING_API_EN / name
            if xml_file.exists():
                # documentation exists, copy
                xml_files.append((xml_file, (pclass, py5_name, processing_name)))
                continue

            # usable documentation might be in a different file because of inheritance
            if pclass in ["PApplet", "PGraphics", "PImage"]:
                for prefix in ["", "PGraphics_", "PImage_"]:
                    if processing_name == "hint":
                        xml_file = (
                            PROCESSING_API_EN
                            / "include"
                            / f"{prefix}{processing_name}.xml"
                        )
                    else:
                        xml_file = PROCESSING_API_EN / f"{prefix}{processing_name}.xml"
                    if xml_file.exists():
                        break
            if xml_file.exists():
                # documentation exists, and should have already been copied
                continue

        # new documentation that I must write. skip pgraphics so I don't duplicate work
        if pclass not in ["PGraphics", "PImage"]:
            new_xml_files.append((pclass, py5_name, item_type, processing_name))

# add in the class documentation files
for pclass, py5class in PY5_CLASS_LOOKUP.items():
    xml_file = PROCESSING_API_EN / f"{pclass}.xml"
    if xml_file.exists():
        xml_files.append((xml_file, (pclass, py5class, pclass)))
    else:
        new_xml_files.append((pclass, py5class, "class", pclass))

# copy the relevant xml files to the py5 directory
print("read and translate Processing's xml documentation files")
for num, (xml_file, file_data) in enumerate(xml_files):
    print(f"{num + 1} / {len(xml_files)} {xml_file.name}")
    pclass, py5_name, processing_name = file_data
    doc = Documentation(xml_file)
    # hack to fix bad data
    if xml_file.stem == "PShader_set":
        doc.meta["name"] = "set()"
        doc.meta["type"] = "method"
    if doc.meta["type"] == "class":
        new_filename_base = f"{PY5_CLASS_LOOKUP[pclass]}"
    else:
        new_filename_base = f"{PY5_CLASS_LOOKUP[pclass]}_{py5_name}"
    doc.description = remove_html(doc.description)
    doc.meta["pclass"] = pclass
    doc.meta["processing_name"] = processing_name
    doc.meta["name"] = doc.meta["name"].replace(processing_name, py5_name)
    if pclass == "PApplet":
        doc.meta["category"] = papplet_category_data.loc[py5_name, "category"] or "None"
        doc.meta["subcategory"] = (
            papplet_category_data.loc[py5_name, "subcategory"] or "None"
        )

    new_examples = []
    for num, (image_name, code) in enumerate(doc.examples):
        # this makes sure the image names are all unique
        if image_name:
            image_name = f"{new_filename_base}_{num}.png"
        new_examples.append((image_name, adjust_code(code, use_autopep8=True)))
    doc.examples = new_examples
    doc.write(PY5_API_EN / (new_filename_base + ".txt"))

print(f"create {len(new_xml_files)} new documentation files")
for num, new_file_data in enumerate(new_xml_files):
    pclass, py5_name, item_type, processing_name = new_file_data
    if item_type == "dynamic variable":
        doc_type = "field"
        name = py5_name
        new_filename_base = f"{PY5_CLASS_LOOKUP[pclass]}_{py5_name}"
    elif item_type == "class":
        doc_type = "class"
        name = py5_name
        new_filename_base = f"{PY5_CLASS_LOOKUP[pclass]}"
    else:
        doc_type = "method"
        name = py5_name + "()"
        new_filename_base = f"{PY5_CLASS_LOOKUP[pclass]}_{py5_name}"

    with open(PY5_API_EN / f"{new_filename_base}.txt", "w") as f:
        extra = (
            f"pclass = {pclass}\nprocessing_name = {processing_name}\n"
            if processing_name
            else ""
        )
        if pclass == "PApplet" and py5_name in papplet_category_data.index:
            category = papplet_category_data.loc[py5_name, "category"] or "None"
            subcategory = papplet_category_data.loc[py5_name, "subcategory"] or "None"
            extra += f"category = {category}\nsubcategory = {subcategory}\n"
        f.write(NEW_TEMPLATE.format(name, doc_type, extra))

print(f"copied {len(xml_files)} files and created {len(new_xml_files)} new files.")
