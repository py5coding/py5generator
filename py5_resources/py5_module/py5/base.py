import functools


def _py5base_param(argnum):
    def decorator(f):
        @functools.wraps(f)
        def decorated(self_, *args):
            if isinstance(args[argnum], Py5Base):
                args = (*args[:argnum],
                        args[argnum]._instance,
                        *args[(argnum + 1):])
            return f(self_, *args)
        return decorated
    return decorator


class Py5Base:

    def __init__(self, instance):
        self._instance = instance

    def _shutdown(self):
        self._shutdown_complete = True

    def _replace_instance(self, new_instance):
        self._instance = new_instance
