# flake8: noqa
"""
This code demos py5 class mode. This is useful for users who want to use a class
or want to have several sketches running at the same time.

It can be run from the command line, like so:

$ python test_class_mode.py
"""

from py5 import Sketch


class Test(Sketch):

    def settings(self):
        self.size(500, 500, self.P2D)


    def setup(self):
        self.background(255)
        self.rect_mode(self.CENTER)


    def draw(self):
        if self.is_key_pressed():
            print('frameRate', self.get_frame_rate())

        self.fill(self.random(255), self.random(255), self.random(255), 50.0)
        self.rect(self.mouse_x, self.mouse_y, 40, 40)

        if self.frame_count == 300:
            self.save_frame('/tmp/frame_###.png')


    def mouse_entered(self):
        print('mouse entered')


    def mouse_exited(self):
        print('mouse exited')

test = Test()
test.run_sketch()
