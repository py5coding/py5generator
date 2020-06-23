import sys
import line_profiler

import stackprinter

from jnius import PythonJavaClass, java_method, JavaException


# *** stacktrace configuration ***
# set stackprinter color style. Default is plaintext. Other choices are darkbg,
# darkbg2, darkbg3, lightbg, lightbg2, lightbg3.
_stackprinter_style = 'plaintext'
# prune tracebacks to only show only show stack levels in the user's py5 code.
_prune_tracebacks = True


class Py5Exception(Exception):

    def __init__(self, exception_classname, msg, method, args):
        super().__init__()
        self.exception_classname = exception_classname
        self.msg = msg
        self.method = method
        self.args = args

    def __str__(self):
        return self.exception_classname + ' thrown while calling ' + self.method + ': ' + self.msg

    def __repr__(self):
        return str(self)


class Py5Methods(PythonJavaClass):
    __javainterfaces__ = ['py5/core/Py5Methods']

    def __init__(self, sketch):
        self._sketch = sketch
        self._functions = dict()
        self._profiler = line_profiler.LineProfiler()

    def set_functions(self, **kwargs):
        self._functions.update(kwargs)

    def profile_functions(self, function_names):
        for fname in function_names:
            func = self._functions[fname]
            self._profiler.add_function(func)
            self._functions[fname] = self._profiler.wrap_function(func)

    def dump_stats(self):
        self._profiler.print_stats()

    @java_method('()[Ljava/lang/Object;')
    def get_function_list(self):
        return self._functions.keys()

    @java_method('(Ljava/lang/String;[Ljava/lang/Object;)V')
    def run_method(self, method_name, params):
        try:
            if method_name in self._functions:
                self._functions[method_name](*params)
        except Exception:
            exc_type, exc_value, exc_tb = sys.exc_info()

            if _prune_tracebacks:
                def _prune_traceback(exc_tb):
                    # remove py5 traceback frames at the top and bottom of the stack
                    prev_tb = exc_tb
                    start_tb = exc_tb.tb_next
                    tb = start_tb
                    while hasattr(tb, 'tb_next') and hasattr(tb, 'tb_frame') and tb.tb_frame.f_code.co_filename != __file__:
                        prev_tb = tb
                        tb = tb.tb_next
                    prev_tb.tb_next = None
                    return exc_tb

                exc_tb = _prune_traceback(exc_tb)
                prev_exc = exc_value
                next_exc = exc_value.__context__
                while next_exc:
                    while isinstance(prev_exc, Py5Exception) and isinstance(next_exc, JavaException):
                        prev_exc.__context__ = next_exc.__context__
                        next_exc = next_exc.__context__
                    if not next_exc:
                        break
                    next_exc.__traceback__ = _prune_traceback(next_exc.__traceback__)
                    prev_exc = next_exc
                    next_exc = next_exc.__context__

            stackprinter.show(thing=(exc_type, exc_value, exc_tb.tb_next),
                              show_vals='line',
                              style=_stackprinter_style,
                              suppressed_paths=[r"lib/python.*?/site-packages/numpy/",
                                                r"lib/python.*?/site-packages/py5/",
                                                r"lib/python.*?/site-packages/jnius/"])

            sys.last_type, sys.last_value, sys.last_traceback = exc_type, exc_value, exc_tb
            self._sketch.get_surface().stopThread()
