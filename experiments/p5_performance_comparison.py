import numpy as np
import py5

start_time = 0


def settings():
    py5.size(800, 800, py5.P2D)


def setup():
    py5.rect_mode(py5.CENTER)
    py5.frame_rate(1000)


def random(x):
    return x * np.random.rand()


def draw():
    global start_time
    width = py5.width
    height = py5.height

    py5.background(220)
    for _ in range(2000):
        # py5.fill(py5.random(255), py5.random(255), py5.random(255), 100)
        # py5.rect(py5.random(width), py5.random(height), 50, 50)
        py5.fill(random(255), random(255), random(255), 100)
        py5.rect(random(width), random(height), 50, 50)

    if py5.frame_count == 1000:
        start_time = py5.millis()
    if py5.frame_count % 1000 == 0:
        print(py5.frame_count, py5.get_frame_rate(),
              (py5.millis() - start_time) / 1000)


py5.run_sketch(block=False)
