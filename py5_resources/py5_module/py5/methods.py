import sys
import logging
from pathlib import Path
from collections import defaultdict
from typing import Union
import line_profiler

from jpype import JImplements, JOverride, JString, JClass
# TODO: what was this?
# from numpy.lib.arraysetops import isin

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


_EXCEPTION_MSGS = {

}


def _exception_msg(exc_type_name, exc_msg, py5info):
    msg = _EXCEPTION_MSGS.get(exc_type_name, exc_msg)
    try:
        if isinstance(msg, str):
            return msg
        elif isinstance(msg, callable):
            return msg(exc_type_name, exc_msg, py5info)
        else:
            logger.error(f'unknown exception msg type for {exc_type_name}')
            return exc_msg
    except Exception as e:
        # TODO: properly say something about what went wrong
        logger.error('error', e.with_traceback())
        return exc_msg


def register_exception_msg(exc_type_name: str, msg: Union[str, callable]):
    _EXCEPTION_MSGS[exc_type_name] = msg


def handle_exception(exc_type, exc_value, exc_tb):
    py5info = []
    try:
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
    except Exception as e:
        logger.critical(f'Exception thrown while examining error traceback: {str(e)}')

    errmsg = stackprinter.format(
        thing=(exc_type, exc_value, exc_tb.tb_next),
        show_vals='line',
        style=_stackprinter_style,
        suppressed_paths=[r"lib/python.*?/site-packages/numpy/",
                          r"lib/python.*?/site-packages/py5/"])

    if _prune_tracebacks:
        errmsg = errmsg.replace(str(exc_value),
                                _exception_msg(exc_type.__name__, str(exc_value), py5info))

    logger.critical(errmsg)

    sys.last_type, sys.last_value, sys.last_traceback = exc_type, exc_value, exc_tb


# TODO: can't I get rid of this now???
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
