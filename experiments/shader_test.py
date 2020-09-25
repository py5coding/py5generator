import numpy as np

import py5
from py5 import Sketch


class Test1(Sketch):

    def settings(self):
        self.size(640, 360, self.P3D)

    def setup(self):
        self.no_stroke()
        self.fill(204)
        self.toon = self.load_shader("frag.glsl", "vert.glsl")
        self.toon.set("fraction", 1.0)
        print(type(self.toon))

    def draw(self):
        self.shader(self.toon)
        self.background(0)
        dir_y = (self.mouse_y / self.height - 0.5) * 2
        dir_x = (self.mouse_x / self.width - 0.5) * 2
        self.directional_light(204, 0, 0, -dir_x, -dir_y, -1)
        self.translate(self.width / 2, self.height / 2)
        self.sphere(120)


class Test2(Sketch):

    def settings(self):
        self.size(640, 360, self.P2D)

    def setup(self):
        img = self.load_image('data/nyu_itp.jpg')
        self.image(img, 0, 0)

    def draw(self):
        self.apply_filter(self.BLUR, 6)


class Test3(Sketch):

    def settings(self):
        self.size(640, 360, self.P2D)

    def setup(self):
        self.point_shader = self.load_shader("spritefrag.glsl", "spritevert.glsl")
        self.point_shader.set("weight", 100)
        self.cloud1 = self.load_image("data/cloud1.png")
        self.cloud2 = self.load_image("data/cloud2.png")
        self.cloud3 = self.load_image("data/cloud3.png")
        self.cloud4 = (np.random.randint(0, 255, size=(300, 40, 4), dtype=np.uint8), "ARGB")
        self.point_shader.set("sprite", self.cloud2)

        self.stroke_weight(10)
        self.stroke_cap(self.SQUARE)
        self.stroke(255, 70)

        self.background(0)

    def draw(self):
        self.shader(self.point_shader, self.POINTS)
        if self.is_mouse_pressed():
            self.point(self.mouse_x, self.mouse_y)

    def key_pressed(self):
        if self.key == '1':
            self.point_shader.set("sprite", self.cloud1)
        elif self.key == '2':
            self.point_shader.set("sprite", self.cloud2)
        elif self.key == '3':
            self.point_shader.set("sprite", self.cloud3)


py5.prune_tracebacks(False)
test = Test3()
test.run_sketch()
