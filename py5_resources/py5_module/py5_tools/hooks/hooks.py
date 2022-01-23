# *****************************************************************************
#
#   Part of the py5 library
#   Copyright (C) 2020-2022 Jim Schmitz
#
#   This library is free software: you can redistribute it and/or modify it
#   under the terms of the GNU Lesser General Public License as published by
#   the Free Software Foundation, either version 2.1 of the License, or (at
#   your option) any later version.
#
#   This library is distributed in the hope that it will be useful, but
#   WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser
#   General Public License for more details.
#
#   You should have received a copy of the GNU Lesser General Public License
#   along with this library. If not, see <https://www.gnu.org/licenses/>.
#
# *****************************************************************************
import time
from collections import deque
from threading import Thread

import numpy as np


class BaseHook:

    def __init__(self, hook_name):
        self.hook_name = hook_name
        self.is_ready = False
        self.exception = None
        self.is_terminated = False

    def hook_finished(self, sketch):
        sketch._remove_post_hook('draw', self.hook_name)
        self.is_ready = True

    def hook_error(self, sketch, e):
        self.exception = e
        sketch._remove_post_hook('draw', self.hook_name)
        self.is_terminated = True

    def sketch_terminated(self):
        self.is_terminated = True


class ScreenshotHook(BaseHook):

    def __init__(self, filename):
        super().__init__('py5screenshot_hook')
        self.filename = filename

    def __call__(self, sketch):
        try:
            sketch.save_frame(self.filename, use_thread=False)
            self.hook_finished(sketch)
        except Exception as e:
            self.hook_error(sketch, e)


class SaveFramesHook(BaseHook):

    def __init__(self, dirname, filename, period, start, limit):
        super().__init__('py5save_frames_hook')
        self.dirname = dirname
        self.filename = filename
        self.period = period
        self.start = start
        self.limit = limit
        self.num_offset = None
        self.filenames = []
        self.last_frame_time = 0

    def __call__(self, sketch):
        try:
            if time.time() - self.last_frame_time < self.period:
                return
            if self.num_offset is None:
                self.num_offset = 0 if self.start is None else sketch.frame_count - self.start
            num = sketch.frame_count - self.num_offset
            frame_filename = sketch._insert_frame(
                str(self.dirname / self.filename), num=num)
            sketch.save_frame(frame_filename, use_thread=True)
            self.filenames.append(frame_filename)
            self.last_frame_time = time.time()
            if len(self.filenames) == self.limit:
                self.hook_finished(sketch)
        except Exception as e:
            self.hook_error(sketch, e)


class GrabFramesHook(BaseHook):

    def __init__(self, period, count):
        super().__init__('py5grab_frames_hook')
        self.period = period
        self.count = count
        self.frames = []
        self.last_frame_time = 0

    def __call__(self, sketch):
        try:
            if time.time() - self.last_frame_time < self.period:
                return
            sketch.load_np_pixels()
            self.frames.append(sketch.np_pixels[:, :, 1:].copy())
            self.last_frame_time = time.time()
            if len(self.frames) == self.count:
                self.hook_finished(sketch)
        except Exception as e:
            self.hook_error(sketch, e)


class Processor(Thread):

    def __init__(self, f, input_queue, processed_queue=None):
        super().__init__()
        self.f = f
        self.input_queue = input_queue
        self.processed_queue = processed_queue

        self.stop_processing = False

    def run(self):
        while not self.stop_processing:
            if self.input_queue:
                self.f(data := self.input_queue.pop())
                if self.processed_queue is not None:
                    self.processed_queue.appendleft(data)


class ProcessFramesHook(BaseHook):

    def __init__(self, period, count, f):
        super().__init__('py5process_frames_hook')
        self.period = period
        self.count = count

        self.frames = deque()
        self.grabbed_frames_count = 0
        self.last_frame_time = 0

        self.processor = Processor(f, self.frames)
        self.processor.start()

    def __call__(self, sketch):
        try:
            if time.time() - self.last_frame_time < self.period:
                return
            if self.grabbed_frames_count < self.count:
                sketch.load_np_pixels()
                self.frames.appendleft(sketch.np_pixels[:, :, 1:].copy())
                self.grabbed_frames_count += 1
                self.last_frame_time = time.time()
            if self.grabbed_frames_count == self.count and len(self.frames) == 0:
                self.processor.stop_processing = True
                self.hook_finished(sketch)
        except Exception as e:
            self.hook_error(sketch, e)


class ProcessBlocksHook(BaseHook):

    def __init__(self, period, count, block_size, f):
        super().__init__('py5block_process_blocks_hook')
        self.period = period
        self.count = count
        self.block_size = block_size

        self.blocks = deque()
        self.used_blocks = deque()
        self.block = None
        self.block_shape = None
        self.block_index = 0
        self.grabbed_frames_count = 0
        self.last_frame_time = 0

        self.processor = Processor(f, self.blocks, self.used_blocks)
        self.processor.start()

    def __call__(self, sketch):
        try:
            if time.time() - self.last_frame_time < self.period:
                return
            if self.grabbed_frames_count < self.count:
                if self.block is None:
                    if self.block_shape is None:
                        self.block_shape = self.block_size, *sketch.np_pixels.shape[1:3], 3
                    if self.used_blocks:
                        self.block = self.used_blocks.pop()
                    else:
                        self.block = np.empty(self.block_shape, np.uint8)

                sketch.load_np_pixels()
                self.block[self.block_index] = sketch.np_pixels[:, :, 1:]
                self.block_index += 1
                self.grabbed_frames_count += 1
                self.last_frame_time = time.time()

                if self.block_index == self.block_size or self.grabbed_frames_count == self.count:
                    self.blocks.appendleft(self.block[:self.block_index])
                    self.block = None

            if self.grabbed_frames_count == self.count and len(self.blocks) == 0:
                self.processor.stop_processing = True
                self.hook_finished(sketch)
        except Exception as e:
            self.hook_error(sketch, e)


class SketchPortalHook(BaseHook):
    def __init__(self, displayer, throttle_frame_rate, time_limit):
        super().__init__('py5sketch_portal_hook')
        self.displayer = displayer
        self.period = 1 / throttle_frame_rate if throttle_frame_rate else 0
        self.time_limit = time_limit
        self.last_frame_time = 0
        self.start_time = time.time()

    def __call__(self, sketch):
        try:
            if self.time_limit and time.time() > self.start_time + self.time_limit:
                self.hook_finished(sketch)
            if time.time() < self.last_frame_time + self.period:
                return
            sketch.load_np_pixels()
            self.displayer(sketch.np_pixels[:, :, 1:])
            self.last_frame_time = time.time()
        except Exception as e:
            self.hook_error(sketch, e)
