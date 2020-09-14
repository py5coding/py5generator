# import re
# import inspect

import py5


class SettingsCallInterceptor:

    # need all of the renderer constants
    P3D = py5.P3D
    P2D = py5.P2D
    JAVA2D = py5.JAVA2D

    def __init__(self):
        self._calls = []

    def size(self, *args):
        self._calls.append(('size', args))

    def fullscreen(self, *args):
        self._calls.append(('fullscreen', args))

    def smooth(self, *args):
        self._calls.append(('smooth', args))

    def no_smooth(self, *args):
        self._calls.append(('no_smooth', args))

    def pixel_density(self, *args):
        self._calls.append(('pixel_density', args))


# class SizeArgs(Exception):

#     def __init__(self, args):
#         super().__init__()
#         self.args = args


# def size(*args):
#     raise SizeArgs(args)


def setup():
    print('running setup')
    py5.size(500, 500, py5.P2D)
    print('after size')
    py5.background(255)
    py5.rect_mode(py5.CENTER)


def draw():
    py5.fill(py5.random(255), py5.random(255), py5.random(255), 50.0)
    py5.rect(py5.mouse_x, py5.mouse_y, 40, 40)


# try:
#     setup()
# except SizeArgs as e:
#     args = e.args
# except Exception:
#     args = None

# SIZE_PARAMS_REGEX = re.compile(r'size\(([^\)]*)\)')
# FULLSCREEN_PARAMS_REGEX = re.compile(r'fullscreen\(([^\)]*)\)')
# SMOOTH_PARAMS_REGEX = re.compile(r'smooth\(([^\)]*)\)')
# NO_SMOOTH_PARAMS_REGEX = re.compile(r'no_smooth\(([^\)]*)\)')
# PIXEL_DENSITY_PARAMS_REGEX = re.compile(r'pixel_density\(([^\)]*)\)')

# setup_code = inspect.getsource(setup).split('\n')

# size_params = SIZE_PARAMS_REGEX.findall(setup_code[1])
# fullscreen_params = FULLSCREEN_PARAMS_REGEX.findall(setup_code[1])
# smooth_params = SMOOTH_PARAMS_REGEX.findall(setup_code[2])
# no_smooth_params = NO_SMOOTH_PARAMS_REGEX.findall(setup_code[2])

def settings():
    print('in my settings')
    interceptor = SettingsCallInterceptor()
    try:
        exec(setup.__code__, dict(py5=interceptor, this=interceptor))
    except Exception:
        pass

    for fname, args in interceptor._calls:
        print(f'making call to {fname}')
        getattr(py5, fname)(*args)
        py5.get_current_sketch()._neutralize_method(fname)


"""
# add these to Sketch:

    def _dummy_method(self, *args, **kwargs):
        # do nothing method
        pass

    def _neutralize_method(self, method_name):
        # replace method implementation with method that does nothing
        setattr(self, method_name, self._dummy_method)
"""

py5.run_sketch()
