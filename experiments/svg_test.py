import numpy as np
import py5


def settings():
    py5.size(400, 400, py5.SVG, "/tmp/test.svg")


def setup():
    # py5.begin_record(py5.SVG, "/tmp/test2.svg")
    width = py5.width
    height = py5.height

    for _ in range(20):
        py5.fill(255 * np.random.rand(), 255 * np.random.rand(), 255 * np.random.rand())
        py5.ellipse(width * np.random.rand(), height * np.random.rand(), 20, 20)
    # py5.end_record()
    py5.exit_sketch()


py5.run_sketch(block=True)
