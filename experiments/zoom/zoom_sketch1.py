"""
sudo modprobe v4l2loopback exclusive_caps=1
v4l2-ctl --list-devices
ffmpeg -f x11grab -r 15 -s 640x480 -i :0.0+1920,25 -vcodec rawvideo -pix_fmt yuv420p -threads 0 -f v4l2 /dev/video4

https://trac.ffmpeg.org/wiki/Capture/Desktop
https://www.ffmpeg.org/ffmpeg-devices.html
"""
import time

import cv2
import numpy as np

import py5
from py5 import Sketch


alpha = 0.6


class ZoomTest(Sketch):

    def settings(self):
        # self.size(640, 480)
        self.size(700, 520)

    def setup(self):
        self.background(192)
        self.rect_mode(py5.CENTER)
        self.frame_rate(30)

        self.fill(0)
        self.text_size(20)

        self.cap = cv2.VideoCapture(0)
        self.camera_width = 640
        self.camera_height = 480
        self.pixel_count = self.width * self.height
        self.camera_pixel_count = self.camera_height * self.camera_width
        self.camera_mask = np.ones((self.camera_height, self.camera_width))
        self.sketch_mask = np.ones((self.height, self.width))

    def draw(self):
        background_color = 255 * self.norm(self.sin(self.frame_count / 100), -1, 1)
        self.background(background_color)
        self.fill(255 - background_color)
        self.text(time.strftime('%A, %B %-m %H:%M:%S %p'), self.frame_count % self.width, 50)

        ret, frame = self.cap.read()
        frame2 = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask_update = ((frame2[:, :, 0] > 50) & (frame2[:, :, 0] < 120) & (frame2[:, :, 1] > 100))
        mask_update[:, :80] = True
        mask_update[:, -80:] = True
        self.camera_mask = (1 - alpha) * self.camera_mask + alpha * mask_update
        offset = int((self.width - self.camera_width) * self.norm(self.sin(self.frame_count / 25), -1, 1))
        self.sketch_mask[:self.camera_height, offset:(offset + self.camera_width)] = self.camera_mask

        sketch_pixels = self.get_pixels()
        sketch_pixels.reshape(self.pixel_count, 4)[self.sketch_mask.flat < 0.5, 1:] = (
            frame[:, :, ::-1].reshape(self.camera_pixel_count, 3)[self.camera_mask.flat < 0.5]
        )
        self.set_pixels(sketch_pixels)

    def exit_actual(self):
        self.cap.release()


py5._prune_tracebacks = False
zoom_test = ZoomTest()
# zoom_test.profile_draw()
zoom_test.run_sketch(block=False)
