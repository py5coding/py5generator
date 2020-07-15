import py5
from py5 import Sketch


class Test(Sketch):

    def settings(self):
        self.size(600, 500, py5.P2D)

    def setup(self):
        self.font = self.create_font("Ubuntu", 32)
        shape = self.font.get_shape('a')
        print(type(shape))
        # self.font = self.load_font("Ubuntu-32.vlw")
        self.text_align(py5.CENTER, py5.CENTER)
        self.fill(255)
        print('glyph count', self.font.get_glyph_count())
        print(self.font.get_name(), self.font.get_default_size(), self.font.get_size())
        self.no_loop()

    def draw(self):
        self.background(0)
        self.text_font(self.font)
        letters = 'test message'
        self.text(letters, self.width / 2, self.height / 2)


test = Test()
test.run_sketch(block=True)
