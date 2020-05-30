import os
from pathlib import Path
import threading
import time

import numpy as np


DATA = np.random.randint(256, size=(1000, 1000), dtype=np.int32)


def regular_file():

    data = DATA.flatten().tobytes()

    def write_file():
        with open('/tmp/test_regular_file', 'wb') as f:
            f.write(data)

    def read_file():
        with open('/tmp/test_regular_file', 'rb') as f:
            data = f.read()
        return len(data)

    t1 = threading.Thread(target=write_file)
    t2 = threading.Thread(target=read_file)

    t1.start()
    t1.join()
    t2.start()
    t2.join()


NAMED_PIPE = Path('/tmp/named_pipe_perf_test')
if not NAMED_PIPE.exists():
    os.mkfifo(NAMED_PIPE)


def named_pipe():

    data = DATA.flatten().tobytes()

    def write_pipe():
        pipe_w = os.open(NAMED_PIPE, os.O_WRONLY)
        os.write(pipe_w, data)
        os.close(pipe_w)

    def read_pipe():
        pipe_r = os.open(NAMED_PIPE, os.O_RDONLY)
        out = os.read(pipe_r, len(data))
        os.close(pipe_r)

        return len(out)

    t1 = threading.Thread(target=write_pipe)
    t2 = threading.Thread(target=read_pipe)

    t1.start()
    t2.start()
    t1.join()
    t2.join()


def test(f, n=1000):
    start_time = time.time()

    for i in range(n):
        f()

    end_time = time.time()

    return 1000 * (end_time - start_time) / n
