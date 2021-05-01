# *****************************************************************************
#
#   Part of the py5generator project; generator of the py5 library
#   Copyright (C) 2020-2021 Jim Schmitz
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
Reference and Lookups
"""

PY5_SKIP_PARAM_TYPES = {
    'processing.core.PMatrix'
}

PY5_SKIP_RETURN_TYPES = set()

TYPE_OVERRIDES = {
    # this is correct, see _return_list_py5shapes
    'processing.core.PShape[]': 'List[Py5Shape]',
    'char[]': 'List[chr]',
    'java.lang.String[]': 'List[str]',
    'float[]': 'NDArray[(Any,), Float]',
    'float[][]': 'NDArray[(Any, Any), Float]',
    'int[]': 'NDArray[(Any,), Int]',
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
    'create_font_file', 'register_exception_msg',
    'register_image_conversion', 'NumpyImageArray',
    '__version__', 'utils',
    'render_frame', 'render_frame_sequence', 'render', 'render_sequence',
}

EXTRA_METHOD_SIGNATURES = {
    ('Sketch', 'run_sketch'): [
        (['block: bool = None', '*',
          'py5_options: List[str] = None', 'sketch_args: List[str] = None',
          'sketch_functions: Dict[str, Callable] = None'], 'None')
    ],
    ('Py5Functions', 'create_font_file'): [
        (['font_name: str', 'font_size: int', 'filename: str = None',
          'characters: str = None', 'pause: bool = True'], 'None')
    ],
    ('Py5Functions', 'get_current_sketch'): [([], 'Sketch')],
    ('Py5Functions', 'reset_py5'): [([], 'bool')],
    ('Py5Functions', 'prune_tracebacks'): [(['prune: bool'], 'None')],
    ('Py5Functions', 'set_stackprinter_style'): [(['style: str'], 'None')],
    ('Py5Functions', 'render_frame'): [
        (['draw: Callable', 'width: int', 'height: int', 'renderer: str = Sketch.HIDDEN', '*',
          'draw_args: Tuple = None', 'draw_kwargs: Dict = None', 'use_py5graphics: bool = False'], 'Image')
    ],
    ('Py5Functions', 'render'): [
        (['width: int', 'height: int', 'renderer: str = Sketch.HIDDEN', 'use_py5graphics: bool = False'], 'Image')
    ],
    ('Py5Functions', 'render_frame_sequence'): [
        (['draw: Callable', 'width: int', 'height: int', 'renderer: str = Sketch.HIDDEN', '*',
          'limit: int = 1', 'setup: Callable = None', 'setup_args: Tuple = None',
          'setup_kwargs: Dict = None', 'draw_args: Tuple = None',
          'draw_kwargs: Dict = None', 'use_py5graphics: bool = False'], 'List[PIL_Image]')
    ],
    ('Py5Functions', 'render_sequence'): [
        (['width: int', 'height: int', 'renderer: str = Sketch.HIDDEN', '*', 'limit: int = 1',
          'setup: Callable = None', 'setup_args: Tuple = None',
          'setup_kwargs: Dict = None', 'use_py5graphics: bool = False'], 'List[PIL_Image]')
    ],
    ('Py5Functions', 'register_image_conversion'): [
        (['precondition: Callable', 'convert_function: Callable'], 'None')
    ],
    ('Py5Tools', 'is_jvm_running'): [
        ([], 'bool')
    ],
    ('Py5Tools', 'add_options'): [
        (['*options: List[str]'], 'None')
    ],
    ('Py5Tools', 'get_classpath'): [
        ([], 'str')
    ],
    ('Py5Tools', 'add_classpath'): [
        (['classpath: Union[Path, str]'], 'None')
    ],
    ('Py5Tools', 'add_jars'): [
        (['path: Union[Path, str]'], 'None')
    ],
}
