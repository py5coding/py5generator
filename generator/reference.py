"""
Reference and Lookups
"""

PY5_SKIP_PARAM_TYPES = {
    'processing/core/PMatrix3D', 'processing/core/PMatrix2D',
    'processing/core/PMatrix', 'java/io/File', 'processing/core/PVector'
}

PY5_SKIP_RETURN_TYPES = PY5_SKIP_PARAM_TYPES | {
    'processing/core/PImage'
}

JTYPE_CONVERSIONS = {
    'boolean': 'bool',
    'char': 'chr',
    'long': 'int',
    'java/lang/String': 'str',
    'java/lang/Object': 'Any',
    'processing/opengl/PShader': 'Py5Shader',
    'processing/core/PFont': 'Py5Font',
    'processing/core/PImage': 'Py5Image'
}

PCONSTANT_OVERRIDES = {
    'WHITESPACE': r' \t\n\r\x0c\xa0',
    'ESC': r'\x1b',
    'RETURN': r'\r',
    'ENTER': r'\n',
    'DELETE': r'\x7f',
    'BACKSPACE': r'\x08',
    'TAB': r'\t'
}

EXTRA_DIR_NAMES = {
    'run_sketch', 'get_py5applet', 'reset_py5', 'exit_sketch',
    'autoclass', 'Py5Methods', '_Py5Applet', '_py5sketch', '_py5sketch_used',
    'prune_tracebacks', 'set_stackprinter_style', 'create_font_file'
}
