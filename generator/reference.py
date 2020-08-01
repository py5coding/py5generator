"""
Reference and Lookups
"""

PY5_SKIP_PARAM_TYPES = set()

PY5_SKIP_RETURN_TYPES = PY5_SKIP_PARAM_TYPES | set()

TYPE_OVERRIDES = {
    'processing.core.PShape[]': 'List[Py5Shape]',
}


JPYPE_CONVERSIONS = {
    'boolean': 'JBoolean',
    'int': 'JInt',
    'float': 'JFloat',
    'char': 'JChar',
    'java.lang.String': 'JString',
}

JTYPE_CONVERSIONS = {
    'boolean': 'bool',
    'char': 'chr',
    'int': 'int',
    'float': 'float',
    'long': 'int',
    'java.lang.Object': 'Any',
    'java.lang.String': 'str',
    'java.io.File': 'Path',  # currently no methods use this
    'processing.opengl.PShader': 'Py5Shader',
    'processing.core.PFont': 'Py5Font',
    'processing.core.PImage': 'Py5Image',
    'processing.core.PShape': 'Py5Shape',
    'processing.core.PSurface': 'Py5Surface',
    'processing.core.PGraphics': 'Py5Graphics',
    'processing.core.PVector': 'np.ndarray',
    'processing.core.PMatrix': 'np.ndarray',
    'processing.core.PMatrix2D': 'np.ndarray',
    'processing.core.PMatrix3D': 'np.ndarray',
}

EXTRA_DIR_NAMES = {
    'run_sketch', 'get_current_sketch', 'reset_py5',
    'JClass', 'Py5Exception', 'Sketch', 'Py5Font',
    'prune_tracebacks', 'set_stackprinter_style',
    'create_font_file', 'register_image_conversion',
}
