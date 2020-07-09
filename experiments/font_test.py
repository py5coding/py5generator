import py5
from py5 import Sketch


class Test(Sketch):

    # def __init__(self):
    #     super().__init__()

    def settings(self):
        self.size(600, 500, py5.P2D)

    def setup(self):
        # self.font = self.create_font("Ubuntu", 32)
        self.font = self.load_font("Ubuntu-32.vlw")
        self.text_align(py5.CENTER, py5.CENTER)
        self.fill(255)

    def draw(self):
        self.background(0)
        self.text_font(self.font)
        letters = 'test message'
        self.text(letters, self.width / 2, self.height / 2)
        self.no_loop()


test = Test()
test.run_sketch(block=True)
