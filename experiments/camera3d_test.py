import numpy as np
import py5


Camera3D = py5.JClass('camera3D.Camera3D')
camera3D = None
label = None

rotX = 0
rotY = 0
rotZ = 0

coordinates = 500 * (np.random.rand(20, 3) - 0.5)


def settings():
    py5.size(500, 500, py5.P3D)
    # py5.full_screen(py5.P3D)


def setup():
    py5.background(255)
    py5.frame_rate(60)

    global camera3D
    camera3D = Camera3D(py5.get_current_sketch())
    camera3D.setBackgroundColor(py5.color(192))
    camera3D.renderDefaultAnaglyph().setDivergence(1)

    global label
    label = py5.create_graphics(140, 50)
    label.begin_draw()
    label.text_align(py5.LEFT, py5.TOP)
    label.fill(0)
    label.text_size(16)
    label.text("Rotating Cube", 0, 0)
    label.end_draw()


def pre_draw():
    global rotX
    rotX += 0.5
    global rotY
    rotY += 0.1
    global rotZ
    rotZ += 0.3


def draw():
    # print(py5.get_frame_rate())

    py5.stroke_weight(8)
    py5.stroke(0)
    py5.fill(255, 255, 255)
    py5.translate(py5.width / 2, py5.height / 2, -400)
    py5.rotate_x(np.radians(rotX))
    py5.rotate_y(np.radians(rotY))
    py5.rotate_z(np.radians(rotZ))
    # py5.box(250)

    py5.no_fill()

    # py5.begin_shape()
    # py5.vertex(0, 0, 0)
    # py5.bezier_vertices(coordinates)
    # py5.end_shape()

    py5.begin_shape()
    py5.vertex(0, 0, 0)
    py5.vertices(coordinates)
    py5.end_shape(py5.CLOSE)


def post_draw():
    py5.image(label, py5.width - label.width, py5.height - label.height)


py5.run_sketch(block=False)
