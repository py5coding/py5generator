import sys
import logging
from pathlib import Path
from collections import defaultdict
import line_profiler

from jpype import JImplements, JException, JOverride, JString, JClass

import stackprinter


_JavaNullPointerException = JClass('java.lang.NullPointerException')

logger = logging.getLogger(__name__)


# *** stacktrace configuration ***
# set stackprinter color style. Default is plaintext. Other choices are darkbg,
# darkbg2, darkbg3, lightbg, lightbg2, lightbg3.
_stackprinter_style = 'plaintext'
# prune tracebacks to only show only show stack levels in the user's py5 code.
_prune_tracebacks = True
_module_install_dir = str(Path(__file__).parent)


def handle_exception(exc_type, exc_value, exc_tb):
    # TODO: this should have its own exception handler, especially if I am going
    # to use user registered functions to respond to errors.
    py5info = []
    if _prune_tracebacks and hasattr(exc_tb, 'tb_next'):
        prev_tb = exc_tb
        trim_tb = None
        tb = exc_tb.tb_next
        while hasattr(tb, 'tb_next') and hasattr(tb, 'tb_frame'):
            f_code = tb.tb_frame.f_code
            if f_code.co_filename.startswith(_module_install_dir):
                py5info.append((f_code.co_filename[(len(_module_install_dir) + 1):], f_code.co_name))
                if trim_tb is None:
                    trim_tb = prev_tb
            prev_tb = tb
            tb = tb.tb_next
        if trim_tb:
            trim_tb.tb_next = None

    errmsg = stackprinter.format(
        thing=(exc_type, exc_value, exc_tb.tb_next),
        show_vals='line',
        style=_stackprinter_style,
        suppressed_paths=[r"lib/python.*?/site-packages/numpy/",
                          r"lib/python.*?/site-packages/py5/"])
    # TODO: trim default message and replace with something better
    # logger.critical(errmsg[:(-len(str(exc_value)))])
    logger.critical(errmsg)
    print(py5info)

    sys.last_type, sys.last_value, sys.last_traceback = exc_type, exc_value, exc_tb


def handle_exception2(exc_type, exc_value, exc_tb):
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

    errmsg = stackprinter.format(
        thing=(exc_type, exc_value, exc_tb.tb_next),
        show_vals='line',
        style=_stackprinter_style,
        suppressed_paths=[r"lib/python.*?/site-packages/numpy/",
                          r"lib/python.*?/site-packages/py5/"])
    logger.critical(errmsg)

    sys.last_type, sys.last_value, sys.last_traceback = exc_type, exc_value, exc_tb


class Py5Exception(Exception):

    def __init__(self, exception, method, args, signature_options):
        super().__init__()
        self.e = exception
        self.method = method
        self.args = args
        self.signature_options = signature_options

    def __str__(self):
        if isinstance(self.e, _JavaNullPointerException):
            return 'Java NullPointerException thrown. Is this a running sketch?'
        elif isinstance(self.e, TypeError):
            msg = "\nTypeError: The variables your code passed don't match what this method can handle."
            arg_types = ', '.join([x.__class__.__name__ for x in self.args])
            msg += f"\nThe method received these types: {arg_types}"
            msg += "\nThese are the options it can handle:"
            for sig in self.signature_options:
                msg += f"\n    {sig}" if sig else "\n    (no parameters)"
            return msg
        else:
            return self.e.__class__.__name__ + ' thrown while calling ' + self.method + ': ' + str(self.e)

    def __repr__(self):
        return str(self)


@JImplements('py5.core.Py5Methods')
class Py5Methods:

    def __init__(self, sketch):
        self._sketch = sketch
        self._functions = dict()
        self._post_hooks = defaultdict(dict)
        self._profiler = line_profiler.LineProfiler()
        self._is_terminated = False

    def set_functions(self, **kwargs):
        self._functions.update(kwargs)

    def profile_functions(self, function_names):
        for fname in function_names:
            func = self._functions[fname]
            self._profiler.add_function(func)
            self._functions[fname] = self._profiler.wrap_function(func)

    def dump_stats(self):
        self._profiler.print_stats()

    def add_post_hook(self, method_name, hook_name, hook):
        if self._is_terminated:
            hook.sketch_terminated()
        else:
            self._post_hooks[method_name][hook_name] = hook

    def add_post_hooks(self, method_hooks):
        for method_name, hook_name, hook in method_hooks:
            self.add_post_hook(method_name, hook_name, hook)

    def remove_post_hook(self, method_name, hook_name):
        if hook_name in self._post_hooks[method_name]:
            self._post_hooks[method_name].pop(hook_name)

    def terminate_hooks(self):
        for method_name, hooks in self._post_hooks.items():
            for hook_name, hook in list(hooks.items()):
                hook.sketch_terminated()
                self.remove_post_hook(method_name, hook_name)

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
        logger.info('shutdown initiated')
        try:
            self._sketch._shutdown()
            self._is_terminated = True
            self.terminate_hooks()
            logger.info('shutdown complete')
        except Exception:
            logger.exception('exception in sketch shutdown sequence')
