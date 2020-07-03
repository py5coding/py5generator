import threading
from collections.abc import Iterable
from typing import Callable, Dict, Tuple


class Repeater:

    def __init__(self, f, args, kwargs):
        self.f = f
        self.args = args
        self.kwargs = kwargs
        self.repeat = True

    def __call__(self):
        while self.repeat:
            self.f(*self.args, **self.kwargs)


class ThreadsMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._repeating_threads = {}

    # TODO: need to check for errors and stop

    # *** BEGIN METHODS ***

    def _check_param_types(self, args, kwargs):
        if not isinstance(args, Iterable) and args is not None:
            raise RuntimeError('args argument must be iterable (such as a tuple or list)')
        if not isinstance(kwargs, dict) and kwargs is not None:
            raise RuntimeError('kwargs argument must be a dictionary')

        kwargs = kwargs or {}
        args = args or ()

        return args, kwargs

    def launch_thread(self, f: Callable, args: Tuple = None, kwargs: Dict = None, name: str = None) -> None:
        """$class_launch_thread"""
        args, kwargs = self._check_param_types(args, kwargs)
        t = threading.Thread(target=f, args=args, kwargs=kwargs, name=name)
        t.start()

    def launch_repeating_thread(self, f: Callable, args: Tuple = None, kwargs: Dict = None, name: str = None) -> None:
        """$class_launch_repeating_thread"""
        args, kwargs = self._check_param_types(args, kwargs)

        repeater = Repeater(f, args, kwargs)

        t = threading.Thread(target=repeater, name=name)
        t.start()

        if name:
            self._repeating_threads[name] = (t, repeater)

    def has_repeating_thread(self, name: str) -> None:
        """$class_has_repeating_thread"""
        return name in self._repeating_threads

    def stop_repeating_thread(self, name: str, wait: bool = False) -> None:
        """$class_stop_repeating_thread"""
        if name in self._repeating_threads:
            t, repeater = self._repeating_threads[name]
            repeater.repeat = False
            if wait:
                t.join()
            del self._repeating_threads[name]
