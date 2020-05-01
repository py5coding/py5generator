import py5
from py5 import Py5Applet


class Test(Py5Applet):

    def settings(self):
        self.size(500, 600, py5.P2D)

    def setup(self):
        self.background(255)
        self.rect_mode(py5.CENTER)
        self.frame_rate(30)
        self.foo = 0

    def draw(self):
        if self.is_key_pressed():
            if self.key == self.CODED:
                print('key code:', self.key_code)
            else:
                print('key:', self.key)
        #     print('frameRate', self.get_frame_rate())
        self.fill(self.random(255), self.random(255), self.random(255), 50.0)
        self.rect(self.mouse_x, self.mouse_y, 40, 40)

    # def mouse_moved(self):
    #     # for i in range(100000):
    #     #     self.foo += i * i * 17
    #     self.foo = self.random(1)
    #     print('frameRate', self.get_frame_rate())


test = Test()
test.run_sketch(block=False)
