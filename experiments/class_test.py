import py5
from py5 import Sketch


class Test(Sketch):

    def settings(self):
        self.size(500, 600, py5.P2D)

    def setup(self):
        self.background(255)
        self.rect_mode(py5.CENTER)
        self.frame_rate(30)
        self.hint(self.ENABLE_ASYNC_SAVEFRAME)
        # self.hint(self.DISABLE_ASYNC_SAVEFRAME)

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
        self.save_frame('/tmp/frame_####.png', format='png')
        self.load_np_pixels()
        self.np_pixels[:20, :, :2] = 255
        self.np_pixels[:20, :, 2:] = 0
        self.update_np_pixels()
        # self.get_py5applet().mySaveFrame('frame_####.jpeg')

    # def mouse_entered(self):
    #     start_frame_count = self.frame_count
    #     for i in range(5000000):
    #         self.foo += i * i * 17
    #     end_frame_count = self.frame_count
    #     print('frameCount diff = ', (end_frame_count - start_frame_count))
    #     print('frameRate', self.get_frame_rate())


def _save_frame(sketch):
    if sketch.frame_count % 100 == 0:
        sketch.save_frame('/tmp/frame_####.png')


# py5_options = []
# py5_options = ['--display=1', '--window-color=#882222', '--present']
py5_options = ['--location=400,300', '--display=1']
test = Test()

# test._add_post_hook('draw', _save_frame)
# test._remove_post_hook('draw')
test.run_sketch(py5_options=py5_options)
