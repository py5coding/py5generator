import numpy as np

import py5

tile_texture = None
tile_shader = None


def settings():
    py5.size(640, 480, py5.P2D)


def setup():
    global tile_texture
    py5.texture_wrap(py5.REPEAT)
    tile_texture = py5.load_image("data/penrose.jpg")
    load_tile_shader()


def load_tile_shader():
    global tile_texture
    global tile_shader
    tile_shader = py5.load_shader("scroller.glsl")
    tile_shader.set("resolution", py5.width, py5.height)
    tile_shader.set("tileImage", tile_texture)
    tile_shader.set("test", np.array([-50, 20, 0.]))


def draw():
    tile_shader.set("time", py5.millis() / 1000.0)
    py5.shader(tile_shader)
    py5.rect(0, 0, py5.width, py5.height)


py5.run_sketch(block=True)
