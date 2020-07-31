import numpy as np

from py5 import Sketch


class Test(Sketch):

    def settings(self):
        self.size(500, 500, self.P3D)

    def setup(self):
        self.rot_matrix = np.eye(4)
        self.rot_matrix[2, 3] = -433
        self.apply_rotations = True
        self.rot_x = 0
        self.rot_y = 0
        self.rot_z = 0

    def draw(self):
        self.background(128)

        reset = np.eye(4)
        reset[2, 3] = -433
        self.set_matrix(reset)

        if self.apply_rotations:
            self.rotate_x(self.rot_x)
            self.rotate_y(self.rot_y)
            self.rotate_z(self.rot_z)
        else:
            self.set_matrix(self.rot_matrix)

        self.box(100, 200, 300)

    def key_pressed(self):
        if self.key == 'x':
            self.rot_x += 0.05
        if self.key == 'y':
            self.rot_y += 0.05
        if self.key == 'z':
            self.rot_z += 0.05
        if self.key == 'X':
            self.rot_x -= 0.05
        if self.key == 'Y':
            self.rot_y -= 0.05
        if self.key == 'Z':
            self.rot_z -= 0.05
        if self.key == 'q':
            self.rot_matrix = self.get_matrix()
            # self.get_matrix(self.rot_matrix)
        if self.key == ' ':
            self.apply_rotations = not self.apply_rotations


test = Test()
test.run_sketch(block=False)
