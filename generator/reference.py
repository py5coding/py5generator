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
Reference and Lookups
"""

PY5_SKIP_PARAM_TYPES = {"processing.core.PMatrix"}

PY5_SKIP_RETURN_TYPES = set()

PARAM_TYPE_OVERRIDES = {
    "boolean[]": "Iterator[bool]",
    "char[]": "Iterator[chr]",
    "float[]": "Iterator[float]",
    "float[][]": "Iterator[Iterator[float]]",
    "int[]": "Iterator[int]",
}

RETURN_TYPE_OVERRIDES = {
    # this is correct, see _return_list_py5shapes
    "processing.core.PShape[]": "list[Py5Shape]",
    "java.lang.String[]": "list[str]",
    "int[]": "npt.NDArray[np.integer]",
}

JPYPE_CONVERSIONS = {
    "boolean": "JBoolean",
    "int": "JInt",
    "float": "JFloat",
    "char": "JChar",
    "java.lang.String": "JString",
}

JTYPE_CONVERSIONS = {
    "boolean": "bool",
    "char": "chr",
    "int": "int",
    "float": "float",
    "long": "int",
    "java.lang.Object": "Any",
    "java.lang.String": "str",
    "java.io.File": "Path",  # currently no methods use this
    "processing.opengl.PShader": "Py5Shader",
    "processing.core.PFont": "Py5Font",
    "processing.core.PImage": "Py5Image",
    "processing.core.PShape": "Py5Shape",
    "processing.core.PSurface": "Py5Surface",
    "processing.core.PGraphics": "Py5Graphics",
    "processing.core.PVector": "Py5Vector",
    "processing.core.PMatrix": "npt.NDArray[np.floating]",
    "processing.core.PMatrix2D": "npt.NDArray[np.floating]",
    "processing.core.PMatrix3D": "npt.NDArray[np.floating]",
}

EXTRA_DIR_NAMES = {
    "run_sketch",
    "get_current_sketch",
    "reset_py5",
    "JClass",
    "Sketch",
    "Py5Color",
    "Py5Font",
    "Py5Graphics",
    "Py5Image",
    "Py5Surface",
    "Py5Shader",
    "Py5Shape",
    "Py5KeyEvent",
    "Py5MouseEvent",
    "prune_tracebacks",
    "set_stackprinter_style",
    "create_font_file",
    "register_exception_msg",
    "register_image_conversion",
    "register_shape_conversion",
    "NumpyImageArray",
    "__version__",
    "utils",
    "render_frame",
    "render_frame_sequence",
    "render",
    "render_sequence",
    "Py5Vector",
    "Py5Vector2D",
    "Py5Vector3D",
    "Py5Vector4D",
    "xkcd_colors",
    "css4_colors",
    "mpl_cmaps",
}

SKIP_METHOD_SIGNATURES = {
    "py5.core.Sketch": [("vertex", "float[]")],
    "py5.core.Py5Graphics": [("vertex", "float[]")],
}

EXTRA_METHOD_SIGNATURES = {
    ("Sketch", "run_sketch"): [
        (
            [
                "block: bool = None",
                "*",
                "py5_options: list[str] = None",
                "sketch_args: list[str] = None",
                "sketch_functions: dict[str, Callable] = None",
                "jclassname: str = None",
                "jclass_params: tuple[Any] = ()",
            ],
            "None",
        )
    ],
    ("Py5Functions", "create_font_file"): [
        (
            [
                "font_name: str",
                "font_size: int",
                "filename: str = None",
                "characters: str = None",
                "pause: bool = True",
            ],
            "None",
        )
    ],
    ("Py5Functions", "get_current_sketch"): [([], "Sketch")],
    ("Py5Functions", "reset_py5"): [(["jclassname: str = None"], "bool")],
    ("Py5Functions", "prune_tracebacks"): [(["prune: bool"], "None")],
    ("Py5Functions", "set_stackprinter_style"): [(["style: str"], "None")],
    ("Py5Functions", "render_frame"): [
        (
            [
                "draw: Callable",
                "width: int",
                "height: int",
                "renderer: str = Sketch.HIDDEN",
                "*",
                "draw_args: tuple = None",
                "draw_kwargs: dict = None",
                "use_py5graphics: bool = False",
            ],
            "Image",
        )
    ],
    ("Py5Functions", "render"): [
        (
            [
                "width: int",
                "height: int",
                "renderer: str = Sketch.HIDDEN",
                "use_py5graphics: bool = False",
            ],
            "Image",
        )
    ],
    ("Py5Functions", "render_frame_sequence"): [
        (
            [
                "draw: Callable",
                "width: int",
                "height: int",
                "renderer: str = Sketch.HIDDEN",
                "*",
                "limit: int = 1",
                "setup: Callable = None",
                "setup_args: tuple = None",
                "setup_kwargs: dict = None",
                "draw_args: tuple = None",
                "draw_kwargs: dict = None",
                "use_py5graphics: bool = False",
            ],
            "list[PIL_Image]",
        )
    ],
    ("Py5Functions", "render_sequence"): [
        (
            [
                "width: int",
                "height: int",
                "renderer: str = Sketch.HIDDEN",
                "*",
                "limit: int = 1",
                "setup: Callable = None",
                "setup_args: tuple = None",
                "setup_kwargs: dict = None",
                "use_py5graphics: bool = False",
            ],
            "list[PIL_Image]",
        )
    ],
    ("Py5Functions", "register_image_conversion"): [
        (["precondition: Callable", "convert_function: Callable"], "None")
    ],
    ("Py5Functions", "register_shape_conversion"): [
        (["precondition: Callable", "convert_function: Callable"], "None")
    ],
    ("Py5Tools", "is_jvm_running"): [([], "bool")],
    ("Py5Tools", "add_options"): [(["*options: list[str]"], "None")],
    ("Py5Tools", "get_classpath"): [([], "str")],
    ("Py5Tools", "add_classpath"): [(["classpath: Union[Path, str]"], "None")],
    ("Py5Tools", "add_jars"): [(["path: Union[Path, str]"], "None")],
    ("Py5Tools", "register_processing_mode_key"): [
        (
            [
                "key: str",
                "value: Union[Callable, ModuleType]",
                "*",
                "callback_once: bool = False",
            ],
            "None",
        )
    ],
    ("Py5Tools", "get_jvm_debug_info"): [([], "dict[str, Any]")],
    ("Py5Tools", "screenshot"): [
        (["*", "sketch: Sketch = None", "hook_post_draw: bool = False"], "PIL_Image")
    ],
    ("Py5Tools", "save_frames"): [
        (
            [
                "dirname: str",
                "*",
                'filename: str = "frame_####.png"',
                "period: float = 0.0",
                "start: int = None",
                "limit: int = 0",
                "sketch: Sketch = None",
                "hook_post_draw: bool = False",
                "block: bool = False",
                "display_progress: bool = True",
            ],
            "None",
        )
    ],
    ("Py5Tools", "animated_gif"): [
        (
            [
                "filename: str",
                "*",
                "count: int = 0",
                "period: float = 0.0",
                "frame_numbers: Iterable = None",
                "duration: float = 0.0",
                "loop: int = 0",
                "optimize: bool = True",
                "sketch: Sketch = None",
                "hook_post_draw: bool = False",
                "block: bool = False",
            ],
            "None",
        )
    ],
    ("Py5Tools", "offline_frame_processing"): [
        (
            [
                "func: Callable[[npt.NDArray[np.uint8]], None]",
                "*",
                "limit: int = 0",
                "period: float = 0.0",
                "batch_size: int = 1",
                "complete_func: Callable[[], None] = None",
                "stop_processing_func: Callable[[], bool] = None",
                "sketch: Sketch = None",
                "hook_post_draw: bool = False",
                "queue_limit: int = None",
                "block: bool = False",
                "display_progress: bool = True",
            ],
            "None",
        )
    ],
    ("Py5Tools", "capture_frames"): [
        (
            [
                "*",
                "count: float = 0",
                "period: float = 0.0",
                "frame_numbers: Iterable = None",
                "sketch: Sketch = None",
                "hook_post_draw: bool = False",
                "block: bool = False",
            ],
            "list[PIL_Image]",
        )
    ],
    ("Py5Tools", "sketch_portal"): [
        (
            [
                "*",
                "time_limit: float = 0.0",
                "throttle_frame_rate: float = 30",
                "scale: float = 1.0",
                "quality: int = 75",
                "portal_widget: Py5SketchPortal = None",
                "sketch: Sketch = None",
                "hook_post_draw: bool = False",
            ],
            "None",
        )
    ],
    ("Py5Tools", "live_coding_screenshot"): [
        (
            [
                "screenshot_name: str = None",
            ],
            "None",
        )
    ],
    ("Py5Tools", "live_coding_copy_code"): [
        (
            [
                "copy_name: str = None",
            ],
            "None",
        )
    ],
    ("Py5Tools", "live_coding_snapshot"): [
        (
            [
                "snapshot_name: str = None",
            ],
            "None",
        )
    ],
    ("Py5Tools", "live_coding_count"): [
        (
            [],
            "int",
        )
    ],
    ("Py5Tools", "live_coding_activate"): [
        (
            [
                "*",
                "always_rerun_setup: bool = True",
                "always_on_top: bool = True",
                "activate_keyboard_shortcuts: bool = False",
                "archive_dir: str = 'archive'",
            ],
            "None",
        )
    ],
}

OPTIONAL_METHOD_SIGNATURES = {
    ("Py5Graphics", "nextPage"): {
        "": {"static": False, "rettype": "void", "paramnames": []}
    },
}

PY5_PYTHON_DYNAMIC_VARIABLES = {
    "pixels",
}
