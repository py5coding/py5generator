import py5
from py5 import Sketch


class Test(Sketch):

    def settings(self):
        self.size(500, 600)  # , py5.P2D)

    def setup(self):
        self.background(255)
        self.rect_mode(py5.CENTER)
        self.frame_rate(30)

    def draw(self):
        if self.is_key_pressed():
            if self.key == self.CODED:
                print('key code:', self.key_code)
            else:
                print('key:', self.key)
        #     print('frameRate', self.get_frame_rate())
        self.fill(self.random(255), self.random(255), self.random(255), 50.0)
        self.rect(self.mouse_x, self.mouse_y, 40, 40)

    def exiting(self):
        print('exiting the sketch')

    def key_pressed(self):
        self.save_frame('frame_####.png')

    # def mouse_entered(self):
    #     start_frame_count = self.frame_count
    #     for i in range(5000000):
    #         self.foo += i * i * 17
    #     end_frame_count = self.frame_count
    #     print('frameCount diff = ', (end_frame_count - start_frame_count))
    #     print('frameRate', self.get_frame_rate())


# py5_options = []
py5_options = ['--display=1', '--window-color=#882222', '--present']
# py5_options = ['--location=10,10', '--display=1']
test = Test()
test.run_sketch(block=False, py5_options=py5_options)
