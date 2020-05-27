"""
sudo modprobe v4l2loopback exclusive_caps=1
v4l2-ctl --list-devices
ffmpeg -f x11grab -r 15 -s 640x480 -i :0.0+1920,25 -vcodec rawvideo -pix_fmt yuv420p -threads 0 -f v4l2 /dev/video4

https://trac.ffmpeg.org/wiki/Capture/Desktop
https://www.ffmpeg.org/ffmpeg-devices.html
"""

import cv2
import numpy as np

import py5
from py5 import Sketch


alpha = 0.6


class ZoomTest(Sketch):

    def settings(self):
        self.size(640, 480, py5.P3D)

    def setup(self):
        self.background(192)
        self.rect_mode(py5.CENTER)
        self.frame_rate(30)

        self.cap = cv2.VideoCapture(0)
        self.mask = np.ones((self.height, self.width))
        self.rotX = 0
        self.rotY = 0
        self.rotZ = 0

    def dumb_test(self):
        out = 0
        for i in range(1000):
            out += i * i
        return out

    def draw(self):
        self.rotX += 1.5
        self.rotY += 0.8
        self.rotZ += 2.3

        self.background(192)

        self.stroke_weight(8)
        self.stroke(0)
        self.fill(255, 255, 255)
        self.translate(self.width * 0, self.height / 4, -400)
        self.rotate_x(np.radians(self.rotX))
        self.rotate_y(np.radians(self.rotY))
        self.rotate_z(np.radians(self.rotZ))
        self.box(200)

        ret, frame = self.cap.read()

        frame2 = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask_update = ((frame2[:, :, 0] > 50) & (frame2[:, :, 0] < 120) & (frame2[:, :, 1] > 100))
        mask_update[:, :50] = True
        mask_update[:, -50:] = True

        self.mask = (1 - alpha) * self.mask + alpha * mask_update

        self.load_pixels()
        sketch_pixels = self.pixels_to_numpy(self.pixels, colors='BGR').reshape(self.height, self.width, 3)
        sketch_pixels[self.mask < 0.5] = frame[self.mask < 0.5]

        self.set_new_pixels(self.numpy_to_pixels(sketch_pixels, colors='BGR'))

        # print(self.get_frame_rate())

    def exit_actual(self):
        self.cap.release()


zoom_test = ZoomTest()
zoom_test.run_sketch(block=False)
