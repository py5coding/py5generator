import py5


rocket = None
ry = 0


def settings():
    py5.size(640, 360, py5.P3D)


def setup():
    global rocket
    rocket = py5.load_shape('rocket.obj')


def draw():
    global ry
    py5.background(0)
    py5.lights()

    py5.translate(py5.width / 2, py5.height / 2 + 100, -200)
    py5.rotate_z(py5.PI)
    py5.rotate_y(ry)
    py5.shape(rocket)

    ry += 0.02


py5.run_sketch()
