import py5
from py5 import Sketch


class Test(Sketch):

    def settings(self):
        self.size(500, 600, self.HIDDEN)

    def setup(self):
        self.background(255)
        self.rect_mode(py5.CENTER)
        self.frame_rate(1000)

    def draw(self):
        self.fill(self.random(255), self.random(255), self.random(255), 50.0)
        self.rect(self.random(self.width), self.random(self.height), 40, 40)
        print(self.frame_count)
        self.load_np_pixels()
        if self.frame_count % 10 == 0:
            self.save_frame('/tmp/test_####.png')
        if self.frame_count == 200:
            self.exit_sketch()


test = Test()
test.run_sketch(block=False)
