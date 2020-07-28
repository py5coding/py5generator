import py5
from py5 import Sketch


class Test(Sketch):

    def settings(self):
        self.size(500, 600)  # , self.P2D)

    def setup(self):
        self.background(255)
        self.rect_mode(py5.CENTER)
        self.frame_rate(30)
        # TODO: why is this here and does it do anything???
        self.hint(self.ENABLE_ASYNC_SAVEFRAME)
        # self.hint(self.DISABLE_ASYNC_SAVEFRAME)

        self.pg = self.create_graphics(200, 200)  # , self.P2D)
        self.pg.begin_draw()
        self.pg.fill(self.random(255), self.random(255), self.random(255), 50.0)
        self.pg.rect(30, 40, 40, 40)
        self.pg.rect(130, 140, 40, 40)
        self.pg.end_draw()
        self.pg.load_np_pixels()
        self.pg.np_pixels[:50, :50, :2] = 255
        self.pg.update_np_pixels()

    def draw(self):
        self.image(self.pg, 200, 200)
        self.fill(self.random(255), self.random(255), self.random(255), 50.0)
        self.rect(self.mouse_x, self.mouse_y, 40, 40)

    def exiting(self):
        print('exiting the sketch')

    def key_pressed(self):
        self.save_frame('/tmp/frame_####.png', format='png')


py5_options = ['--location=400,300', '--display=1']
test = Test()
test.run_sketch(block=False, py5_options=py5_options)
