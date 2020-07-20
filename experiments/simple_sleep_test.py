import time
import py5


def settings():
    py5.size(600, 800, py5.P2D)


def setup():
    py5.rect_mode(py5.CENTER)


def draw():
    py5.fill(py5.random(255), py5.random(255), py5.random(255))
    py5.rect(py5.width / 2, py5.height / 2, 50, 50)
    time.sleep(0.015)
    print(py5.get_frame_rate())


py5.run_sketch(block=True)
