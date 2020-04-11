import py5
from py5 import autoclass

Camera3D = autoclass('camera3D.Camera3D')
camera3D = None

rotX = 0
rotY = 0
rotZ = 0


def settings():
    py5.size(500, 500, py5.P3D)
    # py5.full_screen()


def setup():
    py5.background(255)
    py5.rect_mode(py5.CENTER)
    py5.set_frame_rate(30)

    global camera3D
    camera3D = Camera3D(py5._papplet)
    camera3D.setBackgroundColor(py5.color(192))
    camera3D.renderDefaultAnaglyph().setDivergence(1)


def draw():
    if camera3D.currentActivity() == 'right':
        global rotX
        rotX += 0.5
        global rotY
        rotY += 0.1
        global rotZ
        rotZ += 0.3

    py5.strokeWeight(8)
    py5.stroke(0)
    py5.fill(255, 255, 255)
    py5.translate(py5.width / 2, py5.height / 2, -400)
    py5.rotateX(py5.radians(rotX))
    py5.rotateY(py5.radians(rotY))
    py5.rotateZ(py5.radians(rotZ))
    py5.box(250)


py5.run_sketch(settings, setup, draw)
