import numpy as np

import jnius_config
if not jnius_config.vm_running:
    jnius_config.add_options('-Xrs', '-Xmx4096m')
    jnius_config.add_classpath('/home/jim/Projects/ITP/pythonprocessing/py5development/experiments/libraries/*')
import py5  # noqa


Camera3D = py5.autoclass('camera3D.Camera3D')
camera3D = None


rotX = 0
rotY = 0
rotZ = 0


def settings():
    # py5.size(500, 500, py5.P3D)
    py5.full_screen(py5.P3D)


def setup():
    py5.background(255)
    py5.frame_rate(60)

    global camera3D
    camera3D = Camera3D(py5.get_py5applet())
    camera3D.setBackgroundColor(py5.color(192))
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

    py5.stroke_weight(8)
    py5.stroke(0)
    py5.fill(255, 255, 255)
    py5.translate(py5.width / 2, py5.height / 2, -400)
    py5.rotate_x(np.radians(rotX))
    py5.rotate_y(np.radians(rotY))
    py5.rotate_z(np.radians(rotZ))
    py5.box(250)


py5_methods = py5.Py5Methods(settings, setup, draw)
py5.run_sketch(py5_methods, block=False)
