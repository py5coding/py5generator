"""
Reference and Lookups
"""

PY5_SKIP_PARAM_TYPES = {
    'processing.core.PMatrix'
}

PY5_SKIP_RETURN_TYPES = set()

TYPE_OVERRIDES = {
    'processing.core.PShape[]': 'List[Py5Shape]',  # this is correct, see _return_list_py5shapes
    'char[]': 'List[chr]',
    'java.lang.String[]': 'List[str]',
    'float[]': 'NDArray[(Any,), Float]',
    'float[][]': 'NDArray[(Any, Any), Float]',
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
    'processing.core.PVector': 'NDArray[(Any,), Float]',
    'processing.core.PMatrix': 'NDArray[(Any, Any), Float]',
    'processing.core.PMatrix2D': 'NDArray[(2, 3), Float]',
    'processing.core.PMatrix3D': 'NDArray[(4, 4), Float]',
}

EXTRA_DIR_NAMES = {
    'run_sketch', 'get_current_sketch', 'reset_py5',
    'JClass', 'Sketch', 'Py5Font', 'Py5Graphics', 'Py5Image',
    'Py5Surface', 'Py5Shader', 'Py5Shape',
    'prune_tracebacks', 'set_stackprinter_style',
    'create_font_file', 'register_image_conversion',
    'register_exception_msg', '__version__', 'utils'
}

EXTRA_METHOD_SIGNATURES = {
    ('Sketch', 'run_sketch'): [(['block: bool = None', 'py5_options: List = None', 'sketch_args: List = None'], 'None')]
}
