import py5
from py5 import Sketch


class Test(Sketch):

    def settings(self):
        self.size(200, 300, py5.P2D)

    def setup(self):
        self.background(255, 0, 0)
        self.rect_mode(py5.CENTER)
        self.frame_rate(5)

    def draw(self):
        self.fill(255)
        self.rect(50, 50, 40, 40)
        self.foo = self.get_pixels()


test = Test()
test.run_sketch(block=False)
