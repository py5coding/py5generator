"""
Py5 code, interface to the Java version of Processing using PyJNIus.

This file is created by the py5generator package. Do not edit!
"""
import time

import jnius_config
jnius_config.add_options('-Xrs', '-Xmx4096m')
jnius_config.set_classpath(
    '.', '/home/jim/Projects/git/processing/core/library/*')
from jnius import autoclass, detach  # noqa
from jnius import JavaField, JavaStaticField, JavaMethod, JavaStaticMethod  # noqa


PythonPApplet = autoclass('processing.core.PythonPApplet',
                          include_protected=False, include_private=False)
PythonPApplet._render = JavaMethod('()V')
PythonPApplet._handleSettingsPt1 = JavaMethod('()V')
PythonPApplet._handleSettingsPt2 = JavaMethod('()V')
PythonPApplet._handleDrawPt1 = JavaMethod('()V')
PythonPApplet._handleDrawPt2 = JavaMethod('()V')
PythonPApplet._handleDrawPt3 = JavaMethod('()V')
_papplet = PythonPApplet()


_target_frame_rate = 60
_frame_rate_period = 1 / _target_frame_rate


# *** PY5 GENERATED STATIC CONSTANTS ***
ADD = 2
ALPHA = 4
ALT = 18
AMBIENT = 0
ARC = 32
ARGB = 2
ARGS_DENSITY = '--density'
ARGS_DISPLAY = '--display'
ARGS_EDITOR_LOCATION = '--editor-location'
ARGS_EXTERNAL = '--external'
ARGS_HIDE_STOP = '--hide-stop'
ARGS_LOCATION = '--location'
ARGS_PRESENT = '--present'
ARGS_SKETCH_FOLDER = '--sketch-path'
ARGS_STOP_COLOR = '--stop-color'
ARGS_WINDOW_COLOR = '--window-color'
ARROW = 0
BACKSPACE = '\x08'
BASELINE = 0
BEVEL = 32
BEZIER_VERTEX = 1
BLEND = 1
BLUR = 11
BOTTOM = 102
BOX = 41
BREAK = 4
BURN = 8192
CENTER = 3
CHATTER = 0
CHORD = 2
CLAMP = 0
CLOSE = 2
CODED = 65535
COMPLAINT = 1
CONTROL = 17
CORNER = 0
CORNERS = 1
CROSS = 1
CURVE_VERTEX = 3
CUSTOM = 0
DARKEST = 16
DEFAULT_HEIGHT = 100
DEFAULT_WIDTH = 100
DEG_TO_RAD = 0.01745329238474369
DELETE = '\x7f'
DIAMETER = 3
DIFFERENCE = 32
DILATE = 18
DIRECTIONAL = 1
DISABLE_ASYNC_SAVEFRAME = 12
DISABLE_BUFFER_READING = -10
DISABLE_DEPTH_MASK = 5
DISABLE_DEPTH_SORT = -3
DISABLE_DEPTH_TEST = 2
DISABLE_KEY_REPEAT = 11
DISABLE_NATIVE_FONTS = -1
DISABLE_OPENGL_ERRORS = 4
DISABLE_OPTIMIZED_STROKE = 6
DISABLE_STROKE_PERSPECTIVE = -7
DISABLE_STROKE_PURE = -9
DISABLE_TEXTURE_MIPMAPS = 8
DODGE = 4096
DOWN = 40
DXF = 'processing.dxf.RawDXF'
ELLIPSE = 31
ENABLE_ASYNC_SAVEFRAME = -12
ENABLE_BUFFER_READING = 10
ENABLE_DEPTH_MASK = -5
ENABLE_DEPTH_SORT = 3
ENABLE_DEPTH_TEST = -2
ENABLE_KEY_REPEAT = -11
ENABLE_NATIVE_FONTS = 1
ENABLE_OPENGL_ERRORS = -4
ENABLE_OPTIMIZED_STROKE = -6
ENABLE_STROKE_PERSPECTIVE = 7
ENABLE_STROKE_PURE = 9
ENABLE_TEXTURE_MIPMAPS = -8
ENTER = '\n'
EPSILON = 9.999999747378752e-05
ERODE = 17
ESC = '\x1b'
EXCLUSION = 64
EXTERNAL_MOVE = '__MOVE__'
EXTERNAL_STOP = '__STOP__'
FX2D = 'processing.javafx.PGraphicsFX2D'
GIF = 3
GRAY = 12
GROUP = 0
HALF_PI = 1.5707963705062866
HAND = 12
HARD_LIGHT = 1024
HINT_COUNT = 13
HSB = 3
IMAGE = 2
INVERT = 13
JAVA2D = 'processing.awt.PGraphicsJava2D'
JPEG = 2
LANDSCAPE = 2
LEFT = 37
LIGHTEST = 8
LINE = 4
LINES = 5
LINE_LOOP = 51
LINE_STRIP = 50
LINUX = 3
MACOSX = 2
MAX_FLOAT = 3.4028234663852886e+38
MAX_INT = 2147483647
MIN_FLOAT = -3.4028234663852886e+38
MIN_INT = -2147483648
MITER = 8
MODEL = 4
MODELVIEW = 1
MOVE = 13
MULTIPLY = 128
NORMAL = 1
OPAQUE = 14
OPEN = 1
OPENGL = 'processing.opengl.PGraphics3D'
ORTHOGRAPHIC = 2
OTHER = 0
OVERLAY = 512
P2D = 'processing.opengl.PGraphics2D'
P3D = 'processing.opengl.PGraphics3D'
PATH = 21
PDF = 'processing.pdf.PGraphicsPDF'
PERSPECTIVE = 3
PI = 3.1415927410125732
PIE = 3
POINT = 2
POINTS = 3
POLYGON = 20
PORTRAIT = 1
POSTERIZE = 15
PROBLEM = 2
PROJECT = 4
PROJECTION = 0
QUAD = 16
QUADRATIC_VERTEX = 2
QUADS = 17
QUAD_BEZIER_VERTEX = 2
QUAD_STRIP = 18
QUARTER_PI = 0.7853981852531433
RADIUS = 2
RAD_TO_DEG = 57.2957763671875
RECT = 30
REPEAT = 1
REPLACE = 0
RETURN = '\r'
RGB = 1
RIGHT = 39
ROUND = 2
SCREEN = 256
SHAPE = 5
SHIFT = 16
SOFT_LIGHT = 2048
SPAN = 0
SPHERE = 40
SPOT = 3
SQUARE = 1
SUBTRACT = 4
SVG = 'processing.svg.PGraphicsSVG'
TAB = '\t'
TARGA = 1
TAU = 6.2831854820251465
TEXT = 2
THIRD_PI = 1.0471975803375244
THRESHOLD = 16
TIFF = 0
TOP = 101
TRIANGLE = 8
TRIANGLES = 9
TRIANGLE_FAN = 11
TRIANGLE_STRIP = 10
TWO_PI = 6.2831854820251465
UP = 38
VERTEX = 0
WAIT = 3
WHITESPACE = ' \t\n\r\x0c\xa0'
WINDOWS = 1
X = 0
Y = 1
Z = 2
javaPlatform = 8
javaVersion = 1.8
javaVersionName = '1.8.0_74'
platform = 3
platformNames = None
useNativeSelect = True


# *** PY5 GENERATED DYNAMIC VARIABLES ***
args = None
display_height = None
display_width = None
finished = None
first_mouse = None
focused = None
frame = None
frame_count = None
frame_rate = None
g = None
height = None
key = None
key_code = None
key_event = None
key_pressed = None
mouse_button = None
mouse_event = None
mouse_pressed = None
mouse_x = None
mouse_y = None
pixel_density = None
pixel_height = None
pixel_width = None
pixels = None
pmouse_x = None
pmouse_y = None
recorder = None
width = None


def _update_vars():
    global args
    args = _papplet.args
    global display_height
    display_height = _papplet.displayHeight
    global display_width
    display_width = _papplet.displayWidth
    global finished
    finished = _papplet.finished
    global first_mouse
    first_mouse = _papplet.firstMouse
    global focused
    focused = _papplet.focused
    global frame
    frame = _papplet.frame
    global frame_count
    frame_count = _papplet.frameCount
    global frame_rate
    frame_rate = _papplet.frameRate
    global g
    g = _papplet.g
    global height
    height = _papplet.height
    global key
    key = _papplet.key
    global key_code
    key_code = _papplet.keyCode
    global key_event
    key_event = _papplet.keyEvent
    global key_pressed
    key_pressed = _papplet.keyPressed
    global mouse_button
    mouse_button = _papplet.mouseButton
    global mouse_event
    mouse_event = _papplet.mouseEvent
    global mouse_pressed
    mouse_pressed = _papplet.mousePressed
    global mouse_x
    mouse_x = _papplet.mouseX
    global mouse_y
    mouse_y = _papplet.mouseY
    global pixel_density
    pixel_density = _papplet.pixelDensity
    global pixel_height
    pixel_height = _papplet.pixelHeight
    global pixel_width
    pixel_width = _papplet.pixelWidth
    global pixels
    pixels = _papplet.pixels
    global pmouse_x
    pmouse_x = _papplet.pmouseX
    global pmouse_y
    pmouse_y = _papplet.pmouseY
    global recorder
    recorder = _papplet.recorder
    global width
    width = _papplet.width


# *** PY5 GENERATED FUNCTIONS ***

def acos(*args):
    return PythonPApplet.acos(*args)


def alpha(*args):
    return _papplet.alpha(*args)


def ambient(*args):
    return _papplet.ambient(*args)


def ambient_light(*args):
    return _papplet.ambientLight(*args)


def append(*args):
    return _papplet.append(*args)


def apply_matrix(*args):
    return _papplet.applyMatrix(*args)


def arc(*args):
    return _papplet.arc(*args)


def array_copy(*args):
    return _papplet.arrayCopy(*args)


def arraycopy(*args):
    return _papplet.arraycopy(*args)


def asin(*args):
    return PythonPApplet.asin(*args)


def atan(*args):
    return PythonPApplet.atan(*args)


def atan2(*args):
    return PythonPApplet.atan2(*args)


def attrib(*args):
    return _papplet.attrib(*args)


def attrib_color(*args):
    return _papplet.attribColor(*args)


def attrib_normal(*args):
    return _papplet.attribNormal(*args)


def attrib_position(*args):
    return _papplet.attribPosition(*args)


def background(*args):
    return _papplet.background(*args)


def begin_camera(*args):
    return _papplet.beginCamera(*args)


def begin_contour(*args):
    return _papplet.beginContour(*args)


def begin_pgl(*args):
    return _papplet.beginPGL(*args)


def begin_raw(*args):
    return _papplet.beginRaw(*args)


def begin_record(*args):
    return _papplet.beginRecord(*args)


def begin_shape(*args):
    return _papplet.beginShape(*args)


def bezier(*args):
    return _papplet.bezier(*args)


def bezier_detail(*args):
    return _papplet.bezierDetail(*args)


def bezier_point(*args):
    return _papplet.bezierPoint(*args)


def bezier_tangent(*args):
    return _papplet.bezierTangent(*args)


def bezier_vertex(*args):
    return _papplet.bezierVertex(*args)


def binary(*args):
    return _papplet.binary(*args)


def blend(*args):
    return _papplet.blend(*args)


def blend_color(*args):
    return PythonPApplet.blendColor(*args)


def blend_mode(*args):
    return _papplet.blendMode(*args)


def blue(*args):
    return _papplet.blue(*args)


def box(*args):
    return _papplet.box(*args)


def brightness(*args):
    return _papplet.brightness(*args)


def camera(*args):
    return _papplet.camera(*args)


def ceil(*args):
    return PythonPApplet.ceil(*args)


def check_extension(*args):
    return PythonPApplet.checkExtension(*args)


def circle(*args):
    return _papplet.circle(*args)


def clear(*args):
    return _papplet.clear(*args)


def clip(*args):
    return _papplet.clip(*args)


def color(*args):
    return _papplet.color(*args)


def color_mode(*args):
    return _papplet.colorMode(*args)


def concat(*args):
    return _papplet.concat(*args)


def constrain(*args):
    return _papplet.constrain(*args)


def copy(*args):
    return _papplet.copy(*args)


def cos(*args):
    return PythonPApplet.cos(*args)


def create_font(*args):
    return _papplet.createFont(*args)


def create_graphics(*args):
    return _papplet.createGraphics(*args)


def create_image(*args):
    return _papplet.createImage(*args)


def create_input(*args):
    return _papplet.createInput(*args)


def create_input_raw(*args):
    return _papplet.createInputRaw(*args)


def create_output(*args):
    return _papplet.createOutput(*args)


def create_path(*args):
    return _papplet.createPath(*args)


def create_reader(*args):
    return _papplet.createReader(*args)


def create_shape(*args):
    return _papplet.createShape(*args)


def create_writer(*args):
    return _papplet.createWriter(*args)


def cursor(*args):
    return _papplet.cursor(*args)


def curve(*args):
    return _papplet.curve(*args)


def curve_detail(*args):
    return _papplet.curveDetail(*args)


def curve_point(*args):
    return _papplet.curvePoint(*args)


def curve_tangent(*args):
    return _papplet.curveTangent(*args)


def curve_tightness(*args):
    return _papplet.curveTightness(*args)


def curve_vertex(*args):
    return _papplet.curveVertex(*args)


def data_file(*args):
    return _papplet.dataFile(*args)


def data_path(*args):
    return _papplet.dataPath(*args)


def day(*args):
    return PythonPApplet.day(*args)


def debug(*args):
    return PythonPApplet.debug(*args)


def degrees(*args):
    return PythonPApplet.degrees(*args)


def delay(*args):
    return _papplet.delay(*args)


def desktop_file(*args):
    return PythonPApplet.desktopFile(*args)


def desktop_path(*args):
    return PythonPApplet.desktopPath(*args)


def die(*args):
    return _papplet.die(*args)


def directional_light(*args):
    return _papplet.directionalLight(*args)


def display_density(*args):
    return _papplet.displayDensity(*args)


def dispose(*args):
    return _papplet.dispose(*args)


def dist(*args):
    return _papplet.dist(*args)


def edge(*args):
    return _papplet.edge(*args)


def ellipse(*args):
    return _papplet.ellipse(*args)


def ellipse_mode(*args):
    return _papplet.ellipseMode(*args)


def emissive(*args):
    return _papplet.emissive(*args)


def end_camera(*args):
    return _papplet.endCamera(*args)


def end_contour(*args):
    return _papplet.endContour(*args)


def end_pgl(*args):
    return _papplet.endPGL(*args)


def end_raw(*args):
    return _papplet.endRaw(*args)


def end_record(*args):
    return _papplet.endRecord(*args)


def end_shape(*args):
    return _papplet.endShape(*args)


def equals(*args):
    return _papplet.equals(*args)


def exit_actual(*args):
    return _papplet.exitActual(*args)


def exit_called(*args):
    return _papplet.exitCalled(*args)


def exp(*args):
    return PythonPApplet.exp(*args)


def expand(*args):
    return _papplet.expand(*args)


def fill(*args):
    return _papplet.fill(*args)


def filter(*args):
    return _papplet.filter(*args)


def floor(*args):
    return PythonPApplet.floor(*args)


def flush(*args):
    return _papplet.flush(*args)


def focus_gained(*args):
    return _papplet.focusGained(*args)


def focus_lost(*args):
    return _papplet.focusLost(*args)


def frame_moved(*args):
    return _papplet.frameMoved(*args)


def frame_resized(*args):
    return _papplet.frameResized(*args)


def frustum(*args):
    return _papplet.frustum(*args)


def get(*args):
    return _papplet.get(*args)


def get_class(*args):
    return _papplet.getClass(*args)


def get_extension(*args):
    return PythonPApplet.getExtension(*args)


def get_graphics(*args):
    return _papplet.getGraphics(*args)


def get_matrix(*args):
    return _papplet.getMatrix(*args)


def get_surface(*args):
    return _papplet.getSurface(*args)


def green(*args):
    return _papplet.green(*args)


def hash_code(*args):
    return _papplet.hashCode(*args)


def hex(*args):
    return _papplet.hex(*args)


def hide_menu_bar(*args):
    return PythonPApplet.hideMenuBar(*args)


def hint(*args):
    return _papplet.hint(*args)


def hour(*args):
    return PythonPApplet.hour(*args)


def hue(*args):
    return _papplet.hue(*args)


def image(*args):
    return _papplet.image(*args)


def image_mode(*args):
    return _papplet.imageMode(*args)


def insert_frame(*args):
    return _papplet.insertFrame(*args)


def is_looping(*args):
    return _papplet.isLooping(*args)


def join(*args):
    return _papplet.join(*args)


def key_released(*args):
    return _papplet.keyReleased(*args)


def key_typed(*args):
    return _papplet.keyTyped(*args)


def launch(*args):
    return PythonPApplet.launch(*args)


def lerp(*args):
    return PythonPApplet.lerp(*args)


def lerp_color(*args):
    return _papplet.lerpColor(*args)


def light_falloff(*args):
    return _papplet.lightFalloff(*args)


def light_specular(*args):
    return _papplet.lightSpecular(*args)


def lights(*args):
    return _papplet.lights(*args)


def line(*args):
    return _papplet.line(*args)


def link(*args):
    return _papplet.link(*args)


def list_files(*args):
    return _papplet.listFiles(*args)


def list_paths(*args):
    return _papplet.listPaths(*args)


def load_bytes(*args):
    return _papplet.loadBytes(*args)


def load_font(*args):
    return _papplet.loadFont(*args)


def load_image(*args):
    return _papplet.loadImage(*args)


def load_json_array(*args):
    return _papplet.loadJSONArray(*args)


def load_json_object(*args):
    return _papplet.loadJSONObject(*args)


def load_pixels(*args):
    return _papplet.loadPixels(*args)


def load_shader(*args):
    return _papplet.loadShader(*args)


def load_shape(*args):
    return _papplet.loadShape(*args)


def load_strings(*args):
    return _papplet.loadStrings(*args)


def load_table(*args):
    return _papplet.loadTable(*args)


def load_xml(*args):
    return _papplet.loadXML(*args)


def log(*args):
    return PythonPApplet.log(*args)


def loop(*args):
    return _papplet.loop(*args)


def mag(*args):
    return _papplet.mag(*args)


def main(*args):
    return _papplet.main(*args)


def mask(*args):
    return _papplet.mask(*args)


def match(*args):
    return PythonPApplet.match(*args)


def match_all(*args):
    return PythonPApplet.matchAll(*args)


def method(*args):
    return _papplet.method(*args)


def millis(*args):
    return _papplet.millis(*args)


def minute(*args):
    return PythonPApplet.minute(*args)


def model_x(*args):
    return _papplet.modelX(*args)


def model_y(*args):
    return _papplet.modelY(*args)


def model_z(*args):
    return _papplet.modelZ(*args)


def month(*args):
    return PythonPApplet.month(*args)


def mouse_clicked(*args):
    return _papplet.mouseClicked(*args)


def mouse_dragged(*args):
    return _papplet.mouseDragged(*args)


def mouse_entered(*args):
    return _papplet.mouseEntered(*args)


def mouse_exited(*args):
    return _papplet.mouseExited(*args)


def mouse_moved(*args):
    return _papplet.mouseMoved(*args)


def mouse_released(*args):
    return _papplet.mouseReleased(*args)


def mouse_wheel(*args):
    return _papplet.mouseWheel(*args)


def nf(*args):
    return _papplet.nf(*args)


def nfc(*args):
    return _papplet.nfc(*args)


def nfp(*args):
    return _papplet.nfp(*args)


def nfs(*args):
    return _papplet.nfs(*args)


def no_clip(*args):
    return _papplet.noClip(*args)


def no_cursor(*args):
    return _papplet.noCursor(*args)


def no_fill(*args):
    return _papplet.noFill(*args)


def no_lights(*args):
    return _papplet.noLights(*args)


def no_loop(*args):
    return _papplet.noLoop(*args)


def no_smooth(*args):
    return _papplet.noSmooth(*args)


def no_stroke(*args):
    return _papplet.noStroke(*args)


def no_texture(*args):
    return _papplet.noTexture(*args)


def no_tint(*args):
    return _papplet.noTint(*args)


def noise(*args):
    return _papplet.noise(*args)


def noise_detail(*args):
    return _papplet.noiseDetail(*args)


def noise_seed(*args):
    return _papplet.noiseSeed(*args)


def norm(*args):
    return PythonPApplet.norm(*args)


def normal(*args):
    return _papplet.normal(*args)


def notify(*args):
    return _papplet.notify(*args)


def notify_all(*args):
    return _papplet.notifyAll(*args)


def orientation(*args):
    return _papplet.orientation(*args)


def ortho(*args):
    return _papplet.ortho(*args)


def parse_boolean(*args):
    return _papplet.parseBoolean(*args)


def parse_byte(*args):
    return _papplet.parseByte(*args)


def parse_char(*args):
    return _papplet.parseChar(*args)


def parse_float(*args):
    return _papplet.parseFloat(*args)


def parse_int(*args):
    return _papplet.parseInt(*args)


def parse_json_array(*args):
    return _papplet.parseJSONArray(*args)


def parse_json_object(*args):
    return _papplet.parseJSONObject(*args)


def parse_xml(*args):
    return _papplet.parseXML(*args)


def pause(*args):
    return _papplet.pause(*args)


def perspective(*args):
    return _papplet.perspective(*args)


def point(*args):
    return _papplet.point(*args)


def point_light(*args):
    return _papplet.pointLight(*args)


def pop(*args):
    return _papplet.pop(*args)


def pop_matrix(*args):
    return _papplet.popMatrix(*args)


def pop_style(*args):
    return _papplet.popStyle(*args)


def post_event(*args):
    return _papplet.postEvent(*args)


def print_array(*args):
    return PythonPApplet.printArray(*args)


def print_camera(*args):
    return _papplet.printCamera(*args)


def print_matrix(*args):
    return _papplet.printMatrix(*args)


def print_projection(*args):
    return _papplet.printProjection(*args)


def println(*args):
    return _papplet.println(*args)


def push(*args):
    return _papplet.push(*args)


def push_matrix(*args):
    return _papplet.pushMatrix(*args)


def push_style(*args):
    return _papplet.pushStyle(*args)


def quad(*args):
    return _papplet.quad(*args)


def quadratic_vertex(*args):
    return _papplet.quadraticVertex(*args)


def radians(*args):
    return PythonPApplet.radians(*args)


def random(*args):
    return _papplet.random(*args)


def random_gaussian(*args):
    return _papplet.randomGaussian(*args)


def random_seed(*args):
    return _papplet.randomSeed(*args)


def rect(*args):
    return _papplet.rect(*args)


def rect_mode(*args):
    return _papplet.rectMode(*args)


def red(*args):
    return _papplet.red(*args)


def redraw(*args):
    return _papplet.redraw(*args)


def register_method(*args):
    return _papplet.registerMethod(*args)


def request_image(*args):
    return _papplet.requestImage(*args)


def reset_matrix(*args):
    return _papplet.resetMatrix(*args)


def reset_shader(*args):
    return _papplet.resetShader(*args)


def resume(*args):
    return _papplet.resume(*args)


def reverse(*args):
    return _papplet.reverse(*args)


def rotate(*args):
    return _papplet.rotate(*args)


def rotate_x(*args):
    return _papplet.rotateX(*args)


def rotate_y(*args):
    return _papplet.rotateY(*args)


def rotate_z(*args):
    return _papplet.rotateZ(*args)


def saturation(*args):
    return _papplet.saturation(*args)


def save(*args):
    return _papplet.save(*args)


def save_bytes(*args):
    return _papplet.saveBytes(*args)


def save_file(*args):
    return _papplet.saveFile(*args)


def save_frame(*args):
    return _papplet.saveFrame(*args)


def save_json_array(*args):
    return _papplet.saveJSONArray(*args)


def save_json_object(*args):
    return _papplet.saveJSONObject(*args)


def save_path(*args):
    return _papplet.savePath(*args)


def save_stream(*args):
    return _papplet.saveStream(*args)


def save_strings(*args):
    return _papplet.saveStrings(*args)


def save_table(*args):
    return _papplet.saveTable(*args)


def save_xml(*args):
    return _papplet.saveXML(*args)


def scale(*args):
    return _papplet.scale(*args)


def screen_x(*args):
    return _papplet.screenX(*args)


def screen_y(*args):
    return _papplet.screenY(*args)


def screen_z(*args):
    return _papplet.screenZ(*args)


def second(*args):
    return PythonPApplet.second(*args)


def select_folder(*args):
    return _papplet.selectFolder(*args)


def select_input(*args):
    return _papplet.selectInput(*args)


def select_output(*args):
    return _papplet.selectOutput(*args)


def set_matrix(*args):
    return _papplet.setMatrix(*args)


def set_size(*args):
    return _papplet.setSize(*args)


def settings(*args):
    return _papplet.settings(*args)


def setup_sketch(*args):
    return PythonPApplet.setupSketch(*args)


def shader(*args):
    return _papplet.shader(*args)


def shape(*args):
    return _papplet.shape(*args)


def shape_mode(*args):
    return _papplet.shapeMode(*args)


def shear_x(*args):
    return _papplet.shearX(*args)


def shear_y(*args):
    return _papplet.shearY(*args)


def shell(*args):
    return PythonPApplet.shell(*args)


def shininess(*args):
    return _papplet.shininess(*args)


def shorten(*args):
    return _papplet.shorten(*args)


def show_depth_warning(*args):
    return PythonPApplet.showDepthWarning(*args)


def show_depth_warning_xyz(*args):
    return PythonPApplet.showDepthWarningXYZ(*args)


def show_method_warning(*args):
    return PythonPApplet.showMethodWarning(*args)


def show_missing_warning(*args):
    return PythonPApplet.showMissingWarning(*args)


def show_variation_warning(*args):
    return PythonPApplet.showVariationWarning(*args)


def sin(*args):
    return PythonPApplet.sin(*args)


def size(*args):
    return _papplet.size(*args)


def sketch_display(*args):
    return _papplet.sketchDisplay(*args)


def sketch_file(*args):
    return _papplet.sketchFile(*args)


def sketch_full_screen(*args):
    return _papplet.sketchFullScreen(*args)


def sketch_height(*args):
    return _papplet.sketchHeight(*args)


def sketch_output_path(*args):
    return _papplet.sketchOutputPath(*args)


def sketch_output_stream(*args):
    return _papplet.sketchOutputStream(*args)


def sketch_path(*args):
    return _papplet.sketchPath(*args)


def sketch_pixel_density(*args):
    return _papplet.sketchPixelDensity(*args)


def sketch_renderer(*args):
    return _papplet.sketchRenderer(*args)


def sketch_smooth(*args):
    return _papplet.sketchSmooth(*args)


def sketch_width(*args):
    return _papplet.sketchWidth(*args)


def sketch_window_color(*args):
    return _papplet.sketchWindowColor(*args)


def sort(*args):
    return _papplet.sort(*args)


def specular(*args):
    return _papplet.specular(*args)


def sphere(*args):
    return _papplet.sphere(*args)


def sphere_detail(*args):
    return _papplet.sphereDetail(*args)


def splice(*args):
    return _papplet.splice(*args)


def split(*args):
    return _papplet.split(*args)


def split_tokens(*args):
    return _papplet.splitTokens(*args)


def spot_light(*args):
    return _papplet.spotLight(*args)


def sq(*args):
    return PythonPApplet.sq(*args)


def sqrt(*args):
    return PythonPApplet.sqrt(*args)


def square(*args):
    return _papplet.square(*args)


def start(*args):
    return _papplet.start(*args)


def stop(*args):
    return _papplet.stop(*args)


def stroke(*args):
    return _papplet.stroke(*args)


def stroke_cap(*args):
    return _papplet.strokeCap(*args)


def stroke_join(*args):
    return _papplet.strokeJoin(*args)


def stroke_weight(*args):
    return _papplet.strokeWeight(*args)


def style(*args):
    return _papplet.style(*args)


def subset(*args):
    return _papplet.subset(*args)


def tan(*args):
    return PythonPApplet.tan(*args)


def text(*args):
    return _papplet.text(*args)


def text_align(*args):
    return _papplet.textAlign(*args)


def text_ascent(*args):
    return _papplet.textAscent(*args)


def text_descent(*args):
    return _papplet.textDescent(*args)


def text_font(*args):
    return _papplet.textFont(*args)


def text_leading(*args):
    return _papplet.textLeading(*args)


def text_mode(*args):
    return _papplet.textMode(*args)


def text_size(*args):
    return _papplet.textSize(*args)


def text_width(*args):
    return _papplet.textWidth(*args)


def texture(*args):
    return _papplet.texture(*args)


def texture_mode(*args):
    return _papplet.textureMode(*args)


def texture_wrap(*args):
    return _papplet.textureWrap(*args)


def thread(*args):
    return _papplet.thread(*args)


def tint(*args):
    return _papplet.tint(*args)


def to_string(*args):
    return _papplet.toString(*args)


def translate(*args):
    return _papplet.translate(*args)


def triangle(*args):
    return _papplet.triangle(*args)


def trim(*args):
    return _papplet.trim(*args)


def unbinary(*args):
    return PythonPApplet.unbinary(*args)


def unhex(*args):
    return PythonPApplet.unhex(*args)


def unregister_method(*args):
    return _papplet.unregisterMethod(*args)


def update_pixels(*args):
    return _papplet.updatePixels(*args)


def url_decode(*args):
    return PythonPApplet.urlDecode(*args)


def url_encode(*args):
    return PythonPApplet.urlEncode(*args)


def vertex(*args):
    return _papplet.vertex(*args)


def wait(*args):
    return _papplet.wait(*args)


def year(*args):
    return PythonPApplet.year(*args)


# *** PY5 USER FUNCTIONS ***
def set_frame_rate(frame_rate):
    global _target_frame_rate
    global _frame_rate_period
    _target_frame_rate = frame_rate
    _frame_rate_period = 1 / frame_rate
    # this isn't really necessary
    # _papplet.surface.setFrameRate(frame_rate)
    _papplet.getSurface().setFrameRate(frame_rate)


def run_sketch(settings, setup, draw, frameLimit=1000):
    # handle settings
    _papplet._handleSettingsPt1()
    settings()
    _papplet._handleSettingsPt2()

    PythonPApplet.setupSketch([''], _papplet)

    while frameLimit > 0:
        start = time.time()

        # handle draw
        _update_vars()
        _papplet._handleDrawPt1()
        if _papplet.frameCount == 0:
            setup()
        _papplet._handleDrawPt2()
        draw()
        _papplet._handleDrawPt3()
        _papplet._render()

        time.sleep(max(0, _frame_rate_period - (time.time() - start)))

        frameLimit -= 1

    detach()
