import time
import threading
from collections.abc import Iterable
from typing import Callable, Dict, Tuple


class Repeater:

    def __init__(self, f, args, kwargs):
        self.f = f
        self.args = args
        self.kwargs = kwargs
        self.repeat = True

    def stop(self):
        self.repeat = False

    def __call__(self):
        while self.repeat:
            self.f(*self.args, **self.kwargs)


class TimeDelayRepeater(Repeater):

    def __init__(self, f, delay, args, kwargs):
        super().__init__(f, args, kwargs)
        self.delay = delay
        self.e = threading.Event()

    def stop(self):
        super().stop()
        self.e.set()

    def __call__(self):
        while self.repeat:
            start_time = time.time()
            self.f(*self.args, **self.kwargs)
            self.e.wait(max(0, start_time + self.delay - time.time()))


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

    def launch_thread(self, f: Callable, name: str, args: Tuple = None, kwargs: Dict = None) -> None:
        """$class_launch_thread"""
        args, kwargs = self._check_param_types(args, kwargs)
        t = threading.Thread(target=f, args=args, kwargs=kwargs, name=name)
        t.start()

    def _launch_repeater(self, name, repeater):
        if self.has_repeating_thread(name):
            self.stop_repeating_thread(name, wait=True)

        t = threading.Thread(target=repeater, name=name)
        t.start()
        self._repeating_threads[name] = (t, repeater)

    def launch_repeating_thread(self, f: Callable, name: str,
                                args: Tuple = None, kwargs: Dict = None) -> None:
        """$class_launch_repeating_thread"""
        args, kwargs = self._check_param_types(args, kwargs)
        self._launch_repeater(name, Repeater(f, args, kwargs))

    def launch_repeating_time_thread(self, f: Callable, name: str, time_delay: float,
                                     args: Tuple = None, kwargs: Dict = None) -> None:
        """$class_launch_repeating_time_thread"""
        args, kwargs = self._check_param_types(args, kwargs)
        self._launch_repeater(name, TimeDelayRepeater(f, time_delay, args, kwargs))

    def has_repeating_thread(self, name: str) -> None:
        """$class_has_repeating_thread"""
        return name in self._repeating_threads

    def stop_repeating_thread(self, name: str, wait: bool = False) -> None:
        """$class_stop_repeating_thread"""
        if name in self._repeating_threads:
            t, repeater = self._repeating_threads[name]
            repeater.stop()
            if wait:
                t.join()
            del self._repeating_threads[name]

    def stop_all_repeating_threads(self, wait: bool = False) -> None:
        """$class_stop_all_repeating_threads"""
        for name in self.list_repeating_threads():
            self.stop_repeating_thread(name, wait=wait)

    def list_repeating_threads(self) -> None:
        """$class_list_repeating_threads"""
        return list(self._repeating_threads.keys())

    def _shutdown(self):
        self.stop_all_repeating_threads(wait=True)
        super()._shutdown()
