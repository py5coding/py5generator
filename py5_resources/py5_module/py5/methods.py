import sys
from pathlib import Path
from collections import defaultdict
import line_profiler

import stackprinter

from jpype import JImplements, JException, JOverride, JString


# *** stacktrace configuration ***
# set stackprinter color style. Default is plaintext. Other choices are darkbg,
# darkbg2, darkbg3, lightbg, lightbg2, lightbg3.
_stackprinter_style = 'plaintext'
# prune tracebacks to only show only show stack levels in the user's py5 code.
_prune_tracebacks = True
_module_install_dir = str(Path(__file__).parent)


def handle_exception(exc_type, exc_value, exc_tb):
    if _prune_tracebacks:
        def _prune_traceback(exc_tb):
            # remove py5 traceback frames at the top and bottom of the stack
            prev_tb = exc_tb
            start_tb = exc_tb.tb_next
            tb = start_tb
            while hasattr(tb, 'tb_next') and hasattr(tb, 'tb_frame') and not tb.tb_frame.f_code.co_filename.startswith(_module_install_dir):
                prev_tb = tb
                tb = tb.tb_next
            prev_tb.tb_next = None
            return exc_tb

        exc_tb = _prune_traceback(exc_tb)
        prev_exc = exc_value
        next_exc = exc_value.__context__
        while next_exc:
            while isinstance(prev_exc, Py5Exception) and isinstance(next_exc, (TypeError, JException)):
                prev_exc.__context__ = next_exc.__context__
                next_exc = next_exc.__context__
            if not next_exc:
                break
            next_exc.__traceback__ = _prune_traceback(next_exc.__traceback__)
            prev_exc = next_exc
            next_exc = next_exc.__context__

    # TODO: can I have this go to a logger instead? Need errors to be visible
    # when this is run from a Jupyter notebook
    stackprinter.show(thing=(exc_type, exc_value, exc_tb.tb_next),
                      show_vals='line',
                      style=_stackprinter_style,
                      suppressed_paths=[r"lib/python.*?/site-packages/numpy/",
                                        r"lib/python.*?/site-packages/py5/",
                                        r"lib/python.*?/site-packages/jnius/"])

    sys.last_type, sys.last_value, sys.last_traceback = exc_type, exc_value, exc_tb


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


@JImplements('py5.core.Py5Methods')
class Py5Methods:

    def __init__(self, sketch):
        self._sketch = sketch
        self._functions = dict()
        self._post_hooks = defaultdict(dict)
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

    def add_post_hook(self, method_name, hook_name, function):
        self._post_hooks[method_name][hook_name] = function

    def add_post_hooks(self, method_hooks):
        for method_name, hook_name, function in method_hooks:
            self.add_post_hook(method_name, hook_name, function)

    def remove_post_hook(self, method_name, hook_name):
        if hook_name in self._post_hooks[method_name]:
            self._post_hooks[method_name].pop(hook_name)

    @JOverride
    def get_function_list(self):
        return [JString(s) for s in self._functions.keys()]

    @JOverride
    def run_method(self, method_name, params):
        try:
            if method_name in self._functions:
                self._functions[method_name](*params)
                if method_name in self._post_hooks:
                    for hook in list(self._post_hooks[method_name].values()):
                        hook(self._sketch)
                return True
        except Exception:
            handle_exception(*sys.exc_info())
            self._sketch._terminate_sketch()
            return False

    @JOverride
    def shutdown(self):
        print('shutdown called')
        self._sketch._shutdown()
