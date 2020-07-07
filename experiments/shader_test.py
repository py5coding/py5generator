from py5 import Sketch


class Test(Sketch):

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


test = Test2()
test.run_sketch(block=True)
