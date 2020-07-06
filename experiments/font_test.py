import py5
from py5 import Sketch


class Test(Sketch):

    def settings(self):
        self.size(600, 500, py5.P2D)

    def setup(self):
        self.font1 = self.create_font("Ubuntu", 32)
        self.font2 = self.load_font("Ubuntu-32.vlw")
        self.font3 = self.load_font("Ubuntu-BoldItalic-32.vlw")
        self.text_font(self.font3)
        self.text_align(py5.CENTER, py5.CENTER)
        self.fill(255)

    def draw(self):
        self.background(0)
        self.text("test", self.width / 2, self.height / 2)


py5_options = ['--location=400,300', '--display=1']
test = Test()
test.run_sketch(block=False, py5_options=py5_options)
