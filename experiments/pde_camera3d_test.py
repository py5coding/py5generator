import numpy as np

rotX = 0
rotY = 0
rotZ = 0

Camera3D = autoclass('camera3D.Camera3D')
camera3D = None


def settings():
    # py5.size(500, 500, py5.P3D)
    full_screen(P3D)


def setup():
    background(255)
    frame_rate(60)

    global camera3D
    camera3D = Camera3D(get_py5applet())
    camera3D.setBackgroundColor(color(192))
    camera3D.renderDefaultAnaglyph().setDivergence(1)


def draw():
    # print(py5.get_frame_rate())
    if camera3D.currentActivity() == 'right':
        global rotX
        rotX += 0.5
        global rotY
        rotY += 0.1
        global rotZ
        rotZ += 0.3

    stroke_weight(8)
    stroke(0)
    fill(255, 255, 255)
    translate(width / 2, height / 2, -400)
    rotate_x(np.radians(rotX))
    rotate_y(np.radians(rotY))
    rotate_z(np.radians(rotZ))
    box(250)
