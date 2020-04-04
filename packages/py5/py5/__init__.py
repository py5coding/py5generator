import time

import jnius_config
jnius_config.set_classpath('.', '/home/jim/Projects/git/processing/core/library/*')
from jnius import autoclass  # noqa

PythonPApplet = autoclass('processing.core.PythonPApplet')
PConstants = autoclass('processing.core.PConstants')

_papplet = PythonPApplet()

# *** PY5 GENERATED CONSTANTS ***
ADD = 2
ALPHA = 4
ALT = 18
AMBIENT = 0
ARC = 32
ARGB = 2
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


# *** PY5 GENERATED FUNCTIONS ***
def abs(*args):
    return _papplet.abs(*args)


def acos(*args):
    return _papplet.acos(*args)


def alpha(*args):
    return _papplet.alpha(*args)


def ambient(*args):
    return _papplet.ambient(*args)


def ambientLight(*args):
    return _papplet.ambientLight(*args)


def append(*args):
    return _papplet.append(*args)


def applyMatrix(*args):
    return _papplet.applyMatrix(*args)


def arc(*args):
    return _papplet.arc(*args)


def args(*args):
    return _papplet.args(*args)


def arrayCopy(*args):
    return _papplet.arrayCopy(*args)


def arraycopy(*args):
    return _papplet.arraycopy(*args)


def asin(*args):
    return _papplet.asin(*args)


def atan(*args):
    return _papplet.atan(*args)


def atan2(*args):
    return _papplet.atan2(*args)


def attrib(*args):
    return _papplet.attrib(*args)


def attribColor(*args):
    return _papplet.attribColor(*args)


def attribNormal(*args):
    return _papplet.attribNormal(*args)


def attribPosition(*args):
    return _papplet.attribPosition(*args)


def background(*args):
    return _papplet.background(*args)


def beginCamera(*args):
    return _papplet.beginCamera(*args)


def beginContour(*args):
    return _papplet.beginContour(*args)


def beginPGL(*args):
    return _papplet.beginPGL(*args)


def beginRaw(*args):
    return _papplet.beginRaw(*args)


def beginRecord(*args):
    return _papplet.beginRecord(*args)


def beginShape(*args):
    return _papplet.beginShape(*args)


def bezier(*args):
    return _papplet.bezier(*args)


def bezierDetail(*args):
    return _papplet.bezierDetail(*args)


def bezierPoint(*args):
    return _papplet.bezierPoint(*args)


def bezierTangent(*args):
    return _papplet.bezierTangent(*args)


def bezierVertex(*args):
    return _papplet.bezierVertex(*args)


def binary(*args):
    return _papplet.binary(*args)


def blend(*args):
    return _papplet.blend(*args)


def blendColor(*args):
    return _papplet.blendColor(*args)


def blendMode(*args):
    return _papplet.blendMode(*args)


def blue(*args):
    return _papplet.blue(*args)


def box(*args):
    return _papplet.box(*args)


def brightness(*args):
    return _papplet.brightness(*args)


def calcSketchPath(*args):
    return _papplet.calcSketchPath(*args)


def camera(*args):
    return _papplet.camera(*args)


def ceil(*args):
    return _papplet.ceil(*args)


def checkExtension(*args):
    return _papplet.checkExtension(*args)


def checkLookAndFeel(*args):
    return _papplet.checkLookAndFeel(*args)


def circle(*args):
    return _papplet.circle(*args)


def clear(*args):
    return _papplet.clear(*args)


def clip(*args):
    return _papplet.clip(*args)


def clone(*args):
    return _papplet.clone(*args)


def color(*args):
    return _papplet.color(*args)


def colorMode(*args):
    return _papplet.colorMode(*args)


def concat(*args):
    return _papplet.concat(*args)


def constrain(*args):
    return _papplet.constrain(*args)


def copy(*args):
    return _papplet.copy(*args)


def cos(*args):
    return _papplet.cos(*args)


def createFont(*args):
    return _papplet.createFont(*args)


def createGraphics(*args):
    return _papplet.createGraphics(*args)


def createImage(*args):
    return _papplet.createImage(*args)


def createInput(*args):
    return _papplet.createInput(*args)


def createInputRaw(*args):
    return _papplet.createInputRaw(*args)


def createOutput(*args):
    return _papplet.createOutput(*args)


def createPath(*args):
    return _papplet.createPath(*args)


def createPrimaryGraphics(*args):
    return _papplet.createPrimaryGraphics(*args)


def createReader(*args):
    return _papplet.createReader(*args)


def createShape(*args):
    return _papplet.createShape(*args)


def createTempFile(*args):
    return _papplet.createTempFile(*args)


def createWriter(*args):
    return _papplet.createWriter(*args)


def cursor(*args):
    return _papplet.cursor(*args)


def curve(*args):
    return _papplet.curve(*args)


def curveDetail(*args):
    return _papplet.curveDetail(*args)


def curvePoint(*args):
    return _papplet.curvePoint(*args)


def curveTangent(*args):
    return _papplet.curveTangent(*args)


def curveTightness(*args):
    return _papplet.curveTightness(*args)


def curveVertex(*args):
    return _papplet.curveVertex(*args)


def dataFile(*args):
    return _papplet.dataFile(*args)


def dataPath(*args):
    return _papplet.dataPath(*args)


def day(*args):
    return _papplet.day(*args)


def debug(*args):
    return _papplet.debug(*args)


def degrees(*args):
    return _papplet.degrees(*args)


def delay(*args):
    return _papplet.delay(*args)


def dequeueEvents(*args):
    return _papplet.dequeueEvents(*args)


def desktopFile(*args):
    return _papplet.desktopFile(*args)


def desktopPath(*args):
    return _papplet.desktopPath(*args)


def die(*args):
    return _papplet.die(*args)


def directionalLight(*args):
    return _papplet.directionalLight(*args)


def displayDensity(*args):
    return _papplet.displayDensity(*args)


def displayHeight(*args):
    return _papplet.displayHeight(*args)


def displayWidth(*args):
    return _papplet.displayWidth(*args)


def dispose(*args):
    return _papplet.dispose(*args)


def dist(*args):
    return _papplet.dist(*args)


def edge(*args):
    return _papplet.edge(*args)


def ellipse(*args):
    return _papplet.ellipse(*args)


def ellipseMode(*args):
    return _papplet.ellipseMode(*args)


def emissive(*args):
    return _papplet.emissive(*args)


def endCamera(*args):
    return _papplet.endCamera(*args)


def endContour(*args):
    return _papplet.endContour(*args)


def endPGL(*args):
    return _papplet.endPGL(*args)


def endRaw(*args):
    return _papplet.endRaw(*args)


def endRecord(*args):
    return _papplet.endRecord(*args)


def endShape(*args):
    return _papplet.endShape(*args)


def equals(*args):
    return _papplet.equals(*args)


def exit(*args):
    return _papplet.exit(*args)


def exitActual(*args):
    return _papplet.exitActual(*args)


def exitCalled(*args):
    return _papplet.exitCalled(*args)


def exp(*args):
    return _papplet.exp(*args)


def expand(*args):
    return _papplet.expand(*args)


def fill(*args):
    return _papplet.fill(*args)


def filter(*args):
    return _papplet.filter(*args)


def finalize(*args):
    return _papplet.finalize(*args)


def finished(*args):
    return _papplet.finished(*args)


def firstMouse(*args):
    return _papplet.firstMouse(*args)


def floor(*args):
    return _papplet.floor(*args)


def flush(*args):
    return _papplet.flush(*args)


def focusGained(*args):
    return _papplet.focusGained(*args)


def focusLost(*args):
    return _papplet.focusLost(*args)


def focused(*args):
    return _papplet.focused(*args)


def frame(*args):
    return _papplet.frame(*args)


def frameCount(*args):
    return _papplet.frameCount(*args)


def frameMoved(*args):
    return _papplet.frameMoved(*args)


def frameRate(*args):
    return _papplet.frameRate(*args)


def frameResized(*args):
    return _papplet.frameResized(*args)


def frustum(*args):
    return _papplet.frustum(*args)


def fullScreen(*args):
    return _papplet.fullScreen(*args)


def g(*args):
    return _papplet.g(*args)


def get(*args):
    return _papplet.get(*args)


def getClass(*args):
    return _papplet.getClass(*args)


def getExtension(*args):
    return _papplet.getExtension(*args)


def getGraphics(*args):
    return _papplet.getGraphics(*args)


def getMatrix(*args):
    return _papplet.getMatrix(*args)


def getSurface(*args):
    return _papplet.getSurface(*args)


def graphics(*args):
    return _papplet.graphics(*args)


def green(*args):
    return _papplet.green(*args)


def handleDraw(*args):
    return _papplet.handleDraw(*args)


def handleDrawPt1(*args):
    return _papplet.handleDrawPt1(*args)


def handleDrawPt2(*args):
    return _papplet.handleDrawPt2(*args)


def handleDrawPt3(*args):
    return _papplet.handleDrawPt3(*args)


def handleKeyEvent(*args):
    return _papplet.handleKeyEvent(*args)


def handleMethods(*args):
    return _papplet.handleMethods(*args)


def handleMouseEvent(*args):
    return _papplet.handleMouseEvent(*args)


def handleSettings(*args):
    return _papplet.handleSettings(*args)


def handleSettingsPt1(*args):
    return _papplet.handleSettingsPt1(*args)


def handleSettingsPt2(*args):
    return _papplet.handleSettingsPt2(*args)


def hashCode(*args):
    return _papplet.hashCode(*args)


def height(*args):
    return _papplet.height(*args)


def hex(*args):
    return _papplet.hex(*args)


def hideMenuBar(*args):
    return _papplet.hideMenuBar(*args)


def hint(*args):
    return _papplet.hint(*args)


def hour(*args):
    return _papplet.hour(*args)


def hue(*args):
    return _papplet.hue(*args)


def image(*args):
    return _papplet.image(*args)


def imageMode(*args):
    return _papplet.imageMode(*args)


def initSurface(*args):
    return _papplet.initSurface(*args)


def insertFrame(*args):
    return _papplet.insertFrame(*args)


def insideSettings(*args):
    return _papplet.insideSettings(*args)


def isLooping(*args):
    return _papplet.isLooping(*args)


def javaPlatform(*args):
    return _papplet.javaPlatform(*args)


def javaVersion(*args):
    return _papplet.javaVersion(*args)


def javaVersionName(*args):
    return _papplet.javaVersionName(*args)


def join(*args):
    return _papplet.join(*args)


def key(*args):
    return _papplet.key(*args)


def keyCode(*args):
    return _papplet.keyCode(*args)


def keyEvent(*args):
    return _papplet.keyEvent(*args)


def keyPressed(*args):
    return _papplet.keyPressed(*args)


def keyReleased(*args):
    return _papplet.keyReleased(*args)


def keyTyped(*args):
    return _papplet.keyTyped(*args)


def launch(*args):
    return _papplet.launch(*args)


def lerp(*args):
    return _papplet.lerp(*args)


def lerpColor(*args):
    return _papplet.lerpColor(*args)


def lightFalloff(*args):
    return _papplet.lightFalloff(*args)


def lightSpecular(*args):
    return _papplet.lightSpecular(*args)


def lights(*args):
    return _papplet.lights(*args)


def line(*args):
    return _papplet.line(*args)


def link(*args):
    return _papplet.link(*args)


def listFiles(*args):
    return _papplet.listFiles(*args)


def listFilesImpl(*args):
    return _papplet.listFilesImpl(*args)


def listPaths(*args):
    return _papplet.listPaths(*args)


def loadBytes(*args):
    return _papplet.loadBytes(*args)


def loadFont(*args):
    return _papplet.loadFont(*args)


def loadImage(*args):
    return _papplet.loadImage(*args)


def loadImageIO(*args):
    return _papplet.loadImageIO(*args)


def loadImageTGA(*args):
    return _papplet.loadImageTGA(*args)


def loadJSONArray(*args):
    return _papplet.loadJSONArray(*args)


def loadJSONObject(*args):
    return _papplet.loadJSONObject(*args)


def loadPixels(*args):
    return _papplet.loadPixels(*args)


def loadShader(*args):
    return _papplet.loadShader(*args)


def loadShape(*args):
    return _papplet.loadShape(*args)


def loadStrings(*args):
    return _papplet.loadStrings(*args)


def loadTable(*args):
    return _papplet.loadTable(*args)


def loadXML(*args):
    return _papplet.loadXML(*args)


def log(*args):
    return _papplet.log(*args)


def loop(*args):
    return _papplet.loop(*args)


def looping(*args):
    return _papplet.looping(*args)


def mag(*args):
    return _papplet.mag(*args)


def main(*args):
    return _papplet.main(*args)


def makeGraphics(*args):
    return _papplet.makeGraphics(*args)


def map(*args):
    return _papplet.map(*args)


def mask(*args):
    return _papplet.mask(*args)


def match(*args):
    return _papplet.match(*args)


def matchAll(*args):
    return _papplet.matchAll(*args)


def matchPattern(*args):
    return _papplet.matchPattern(*args)


def max(*args):
    return _papplet.max(*args)


def method(*args):
    return _papplet.method(*args)


def millis(*args):
    return _papplet.millis(*args)


def min(*args):
    return _papplet.min(*args)


def minute(*args):
    return _papplet.minute(*args)


def modelX(*args):
    return _papplet.modelX(*args)


def modelY(*args):
    return _papplet.modelY(*args)


def modelZ(*args):
    return _papplet.modelZ(*args)


def month(*args):
    return _papplet.month(*args)


def mouseButton(*args):
    return _papplet.mouseButton(*args)


def mouseClicked(*args):
    return _papplet.mouseClicked(*args)


def mouseDragged(*args):
    return _papplet.mouseDragged(*args)


def mouseEntered(*args):
    return _papplet.mouseEntered(*args)


def mouseEvent(*args):
    return _papplet.mouseEvent(*args)


def mouseExited(*args):
    return _papplet.mouseExited(*args)


def mouseMoved(*args):
    return _papplet.mouseMoved(*args)


def mousePressed(*args):
    return _papplet.mousePressed(*args)


def mouseReleased(*args):
    return _papplet.mouseReleased(*args)


def mouseWheel(*args):
    return _papplet.mouseWheel(*args)


def mouseX(*args):
    return _papplet.mouseX(*args)


def mouseY(*args):
    return _papplet.mouseY(*args)


def nf(*args):
    return _papplet.nf(*args)


def nfc(*args):
    return _papplet.nfc(*args)


def nfp(*args):
    return _papplet.nfp(*args)


def nfs(*args):
    return _papplet.nfs(*args)


def noClip(*args):
    return _papplet.noClip(*args)


def noCursor(*args):
    return _papplet.noCursor(*args)


def noFill(*args):
    return _papplet.noFill(*args)


def noLights(*args):
    return _papplet.noLights(*args)


def noLoop(*args):
    return _papplet.noLoop(*args)


def noSmooth(*args):
    return _papplet.noSmooth(*args)


def noStroke(*args):
    return _papplet.noStroke(*args)


def noTexture(*args):
    return _papplet.noTexture(*args)


def noTint(*args):
    return _papplet.noTint(*args)


def noise(*args):
    return _papplet.noise(*args)


def noiseDetail(*args):
    return _papplet.noiseDetail(*args)


def noiseSeed(*args):
    return _papplet.noiseSeed(*args)


def noise_fsc(*args):
    return _papplet.noise_fsc(*args)


def norm(*args):
    return _papplet.norm(*args)


def normal(*args):
    return _papplet.normal(*args)


def notify(*args):
    return _papplet.notify(*args)


def notifyAll(*args):
    return _papplet.notifyAll(*args)


def orientation(*args):
    return _papplet.orientation(*args)


def ortho(*args):
    return _papplet.ortho(*args)


def parseBoolean(*args):
    return _papplet.parseBoolean(*args)


def parseByte(*args):
    return _papplet.parseByte(*args)


def parseChar(*args):
    return _papplet.parseChar(*args)


def parseFloat(*args):
    return _papplet.parseFloat(*args)


def parseInt(*args):
    return _papplet.parseInt(*args)


def parseJSONArray(*args):
    return _papplet.parseJSONArray(*args)


def parseJSONObject(*args):
    return _papplet.parseJSONObject(*args)


def parseXML(*args):
    return _papplet.parseXML(*args)


def pause(*args):
    return _papplet.pause(*args)


def perspective(*args):
    return _papplet.perspective(*args)


def pixelDensity(*args):
    return _papplet.pixelDensity(*args)


def pixelHeight(*args):
    return _papplet.pixelHeight(*args)


def pixelWidth(*args):
    return _papplet.pixelWidth(*args)


def pixels(*args):
    return _papplet.pixels(*args)


def platform(*args):
    return _papplet.platform(*args)


def platformNames(*args):
    return _papplet.platformNames(*args)


def pmouseX(*args):
    return _papplet.pmouseX(*args)


def pmouseY(*args):
    return _papplet.pmouseY(*args)


def point(*args):
    return _papplet.point(*args)


def pointLight(*args):
    return _papplet.pointLight(*args)


def pop(*args):
    return _papplet.pop(*args)


def popMatrix(*args):
    return _papplet.popMatrix(*args)


def popStyle(*args):
    return _papplet.popStyle(*args)


def postEvent(*args):
    return _papplet.postEvent(*args)


def pow(*args):
    return _papplet.pow(*args)


def printArray(*args):
    return _papplet.printArray(*args)


def printCamera(*args):
    return _papplet.printCamera(*args)


def printMatrix(*args):
    return _papplet.printMatrix(*args)


def printProjection(*args):
    return _papplet.printProjection(*args)


def printStackTrace(*args):
    return _papplet.printStackTrace(*args)


def println(*args):
    return _papplet.println(*args)


def push(*args):
    return _papplet.push(*args)


def pushMatrix(*args):
    return _papplet.pushMatrix(*args)


def pushStyle(*args):
    return _papplet.pushStyle(*args)


def quad(*args):
    return _papplet.quad(*args)


def quadraticVertex(*args):
    return _papplet.quadraticVertex(*args)


def radians(*args):
    return _papplet.radians(*args)


def random(*args):
    return _papplet.random(*args)


def randomGaussian(*args):
    return _papplet.randomGaussian(*args)


def randomSeed(*args):
    return _papplet.randomSeed(*args)


def recorder(*args):
    return _papplet.recorder(*args)


def rect(*args):
    return _papplet.rect(*args)


def rectMode(*args):
    return _papplet.rectMode(*args)


def red(*args):
    return _papplet.red(*args)


def redraw(*args):
    return _papplet.redraw(*args)


def registerMethod(*args):
    return _papplet.registerMethod(*args)


def registerNatives(*args):
    return _papplet.registerNatives(*args)


def registerNoArgs(*args):
    return _papplet.registerNoArgs(*args)


def registerWithArgs(*args):
    return _papplet.registerWithArgs(*args)


def render(*args):
    return _papplet.render(*args)


def requestImage(*args):
    return _papplet.requestImage(*args)


def resetMatrix(*args):
    return _papplet.resetMatrix(*args)


def resetShader(*args):
    return _papplet.resetShader(*args)


def resume(*args):
    return _papplet.resume(*args)


def reverse(*args):
    return _papplet.reverse(*args)


def rotate(*args):
    return _papplet.rotate(*args)


def rotateX(*args):
    return _papplet.rotateX(*args)


def rotateY(*args):
    return _papplet.rotateY(*args)


def rotateZ(*args):
    return _papplet.rotateZ(*args)


def round(*args):
    return _papplet.round(*args)


def runSketch(*args):
    return _papplet.runSketch(*args)


def saturation(*args):
    return _papplet.saturation(*args)


def save(*args):
    return _papplet.save(*args)


def saveBytes(*args):
    return _papplet.saveBytes(*args)


def saveFile(*args):
    return _papplet.saveFile(*args)


def saveFrame(*args):
    return _papplet.saveFrame(*args)


def saveJSONArray(*args):
    return _papplet.saveJSONArray(*args)


def saveJSONObject(*args):
    return _papplet.saveJSONObject(*args)


def savePath(*args):
    return _papplet.savePath(*args)


def saveStream(*args):
    return _papplet.saveStream(*args)


def saveStrings(*args):
    return _papplet.saveStrings(*args)


def saveTable(*args):
    return _papplet.saveTable(*args)


def saveXML(*args):
    return _papplet.saveXML(*args)


def scale(*args):
    return _papplet.scale(*args)


def screenX(*args):
    return _papplet.screenX(*args)


def screenY(*args):
    return _papplet.screenY(*args)


def screenZ(*args):
    return _papplet.screenZ(*args)


def second(*args):
    return _papplet.second(*args)


def selectCallback(*args):
    return _papplet.selectCallback(*args)


def selectFolder(*args):
    return _papplet.selectFolder(*args)


def selectImpl(*args):
    return _papplet.selectImpl(*args)


def selectInput(*args):
    return _papplet.selectInput(*args)


def selectOutput(*args):
    return _papplet.selectOutput(*args)


def set(*args):
    return _papplet.set(*args)


def setMatrix(*args):
    return _papplet.setMatrix(*args)


def setSize(*args):
    return _papplet.setSize(*args)


def settings(*args):
    return _papplet.settings(*args)


def setupSketch(*args):
    return _papplet.setupSketch(*args)


def shader(*args):
    return _papplet.shader(*args)


def shape(*args):
    return _papplet.shape(*args)


def shapeMode(*args):
    return _papplet.shapeMode(*args)


def shearX(*args):
    return _papplet.shearX(*args)


def shearY(*args):
    return _papplet.shearY(*args)


def shell(*args):
    return _papplet.shell(*args)


def shininess(*args):
    return _papplet.shininess(*args)


def shorten(*args):
    return _papplet.shorten(*args)


def showDepthWarning(*args):
    return _papplet.showDepthWarning(*args)


def showDepthWarningXYZ(*args):
    return _papplet.showDepthWarningXYZ(*args)


def showMethodWarning(*args):
    return _papplet.showMethodWarning(*args)


def showMissingWarning(*args):
    return _papplet.showMissingWarning(*args)


def showSurface(*args):
    return _papplet.showSurface(*args)


def showVariationWarning(*args):
    return _papplet.showVariationWarning(*args)


def sin(*args):
    return _papplet.sin(*args)


def size(*args):
    return _papplet.size(*args)


def sketchDisplay(*args):
    return _papplet.sketchDisplay(*args)


def sketchFile(*args):
    return _papplet.sketchFile(*args)


def sketchFullScreen(*args):
    return _papplet.sketchFullScreen(*args)


def sketchHeight(*args):
    return _papplet.sketchHeight(*args)


def sketchOutputPath(*args):
    return _papplet.sketchOutputPath(*args)


def sketchOutputStream(*args):
    return _papplet.sketchOutputStream(*args)


def sketchPath(*args):
    return _papplet.sketchPath(*args)


def sketchPixelDensity(*args):
    return _papplet.sketchPixelDensity(*args)


def sketchRenderer(*args):
    return _papplet.sketchRenderer(*args)


def sketchSmooth(*args):
    return _papplet.sketchSmooth(*args)


def sketchWidth(*args):
    return _papplet.sketchWidth(*args)


def sketchWindowColor(*args):
    return _papplet.sketchWindowColor(*args)


def smooth(*args):
    return _papplet.smooth(*args)


def smoothWarning(*args):
    return _papplet.smoothWarning(*args)


def sort(*args):
    return _papplet.sort(*args)


def specular(*args):
    return _papplet.specular(*args)


def sphere(*args):
    return _papplet.sphere(*args)


def sphereDetail(*args):
    return _papplet.sphereDetail(*args)


def splice(*args):
    return _papplet.splice(*args)


def split(*args):
    return _papplet.split(*args)


def splitTokens(*args):
    return _papplet.splitTokens(*args)


def spotLight(*args):
    return _papplet.spotLight(*args)


def sq(*args):
    return _papplet.sq(*args)


def sqrt(*args):
    return _papplet.sqrt(*args)


def square(*args):
    return _papplet.square(*args)


def start(*args):
    return _papplet.start(*args)


def startSurface(*args):
    return _papplet.startSurface(*args)


def stop(*args):
    return _papplet.stop(*args)


def str(*args):
    return _papplet.str(*args)


def stroke(*args):
    return _papplet.stroke(*args)


def strokeCap(*args):
    return _papplet.strokeCap(*args)


def strokeJoin(*args):
    return _papplet.strokeJoin(*args)


def strokeWeight(*args):
    return _papplet.strokeWeight(*args)


def style(*args):
    return _papplet.style(*args)


def subset(*args):
    return _papplet.subset(*args)


def surface(*args):
    return _papplet.surface(*args)


def tan(*args):
    return _papplet.tan(*args)


def text(*args):
    return _papplet.text(*args)


def textAlign(*args):
    return _papplet.textAlign(*args)


def textAscent(*args):
    return _papplet.textAscent(*args)


def textDescent(*args):
    return _papplet.textDescent(*args)


def textFont(*args):
    return _papplet.textFont(*args)


def textLeading(*args):
    return _papplet.textLeading(*args)


def textMode(*args):
    return _papplet.textMode(*args)


def textSize(*args):
    return _papplet.textSize(*args)


def textWidth(*args):
    return _papplet.textWidth(*args)


def texture(*args):
    return _papplet.texture(*args)


def textureMode(*args):
    return _papplet.textureMode(*args)


def textureWrap(*args):
    return _papplet.textureWrap(*args)


def thread(*args):
    return _papplet.thread(*args)


def tint(*args):
    return _papplet.tint(*args)


def toString(*args):
    return _papplet.toString(*args)


def translate(*args):
    return _papplet.translate(*args)


def triangle(*args):
    return _papplet.triangle(*args)


def trim(*args):
    return _papplet.trim(*args)


def unbinary(*args):
    return _papplet.unbinary(*args)


def unhex(*args):
    return _papplet.unhex(*args)


def unregisterMethod(*args):
    return _papplet.unregisterMethod(*args)


def updatePixels(*args):
    return _papplet.updatePixels(*args)


def urlDecode(*args):
    return _papplet.urlDecode(*args)


def urlEncode(*args):
    return _papplet.urlEncode(*args)


def useNativeSelect(*args):
    return _papplet.useNativeSelect(*args)


def vertex(*args):
    return _papplet.vertex(*args)


def wait(*args):
    return _papplet.wait(*args)


def width(*args):
    return _papplet.width(*args)


def year(*args):
    return _papplet.year(*args)




frame_rate = 0
mouse_x = 0
mouse_y = 0


def _handle_settings(settings):
    _papplet.handleSettingsPt1()
    settings()
    _papplet.handleSettingsPt2()


def _update_vars():
    global frame_rate
    frame_rate = _papplet.frameRate
    global mouse_x
    mouse_x = _papplet.mouseX
    global mouse_y
    mouse_y = _papplet.mouseY


def _handle_draw(setup, draw):
    _update_vars()
    _papplet.handleDrawPt1()
    if _papplet.frameCount == 0:
        setup()
    _papplet.handleDrawPt2()
    draw()
    _papplet.handleDrawPt3()

    _papplet.render()


def run_sketch(settings, setup, draw, frameLimit=1000):
    _handle_settings(settings)
    PythonPApplet.setupSketch(['py5 sketch'], _papplet)

    while frameLimit > 0:
        _handle_draw(setup, draw)
        time.sleep(1 / 60)

        frameLimit -= 1
