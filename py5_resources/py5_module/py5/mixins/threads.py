# *****************************************************************************
#
#   Part of the py5 library
#   Copyright (C) 2020-2023 Jim Schmitz
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
from __future__ import annotations

import sys
import threading
import time
from collections.abc import Iterable
from typing import Any, Callable, Union

from .. import bridge


class Py5Promise:
    def __init__(self):
        self._result = None
        self._is_ready = False

    @property
    def is_ready(self) -> bool:
        return self._is_ready

    @property
    def result(self) -> Any:
        return self._result

    def _set_result(self, result):
        self._result = result
        self._is_ready = True


class Py5Thread:
    def __init__(self, sketch, f, args, kwargs):
        self.sketch = sketch
        self.f = f
        self.args = args
        self.kwargs = kwargs

    def stop(self):
        pass

    def __call__(self):
        try:
            self.f(*self.args, **self.kwargs)
        except Exception:
            bridge.handle_exception(self.sketch.println, *sys.exc_info())
            self.sketch._terminate_sketch()


class Py5PromiseThread(Py5Thread):
    def __init__(self, sketch, f, promise, args, kwargs):
        super().__init__(sketch, f, args, kwargs)
        self.promise = promise

    def stop(self):
        super().stop()

    def __call__(self):
        try:
            self.promise._set_result(self.f(*self.args, **self.kwargs))
        except Exception:
            bridge.handle_exception(self.sketch.println, *sys.exc_info())
            self.sketch._terminate_sketch()


class Py5RepeatingThread(Py5Thread):
    def __init__(self, sketch, f, delay, args, kwargs):
        super().__init__(sketch, f, args, kwargs)
        self.repeat = True
        self.delay = delay
        self.e = threading.Event()

    def stop(self):
        super().stop()
        self.repeat = False
        self.e.set()

    def __call__(self):
        try:
            while self.repeat:
                start_time = time.time()
                self.f(*self.args, **self.kwargs)
                self.e.wait(max(0, start_time + self.delay - time.time()))
        except Exception:
            self.stop()
            bridge.handle_exception(self.sketch.println, *sys.exc_info())
            self.sketch._terminate_sketch()


class ThreadsMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._py5threads = {}

    def _check_param_types(self, args, kwargs):
        if not isinstance(args, Iterable) and args is not None:
            raise RuntimeError(
                "args argument must be iterable (such as a tuple or list)"
            )
        if not isinstance(kwargs, dict) and kwargs is not None:
            raise RuntimeError("kwargs argument must be a dictionary")

        kwargs = kwargs or {}
        args = args or ()

        return args, kwargs

    def _launch_py5thread(self, name, py5thread, daemon):
        if self.has_thread(name):
            self.stop_thread(name, wait=True)

        t = threading.Thread(name=name, target=py5thread, daemon=daemon)
        t.start()
        self._py5threads[t.name] = (t, py5thread)

        return t.name

    def _shutdown(self):
        self.stop_all_threads(wait=False)
        super()._shutdown()

    # *** BEGIN METHODS ***

    def launch_thread(
        self,
        f: Callable,
        name: str = None,
        *,
        daemon: bool = True,
        args: tuple = None,
        kwargs: dict = None,
    ) -> str:
        """$class_Sketch_launch_thread"""
        args, kwargs = self._check_param_types(args, kwargs)
        return self._launch_py5thread(name, Py5Thread(self, f, args, kwargs), daemon)

    def launch_promise_thread(
        self,
        f: Callable,
        name: str = None,
        *,
        daemon: bool = True,
        args: tuple = None,
        kwargs: dict = None,
    ) -> Py5Promise:
        """$class_Sketch_launch_promise_thread"""
        args, kwargs = self._check_param_types(args, kwargs)
        promise = Py5Promise()
        self._launch_py5thread(
            name, Py5PromiseThread(self, f, promise, args, kwargs), daemon
        )
        return promise

    def launch_repeating_thread(
        self,
        f: Callable,
        name: str = None,
        *,
        time_delay: float = 0,
        daemon: bool = True,
        args: tuple = None,
        kwargs: dict = None,
    ) -> str:
        """$class_Sketch_launch_repeating_thread"""
        args, kwargs = self._check_param_types(args, kwargs)
        return self._launch_py5thread(
            name, Py5RepeatingThread(self, f, time_delay, args, kwargs), daemon
        )

    def _remove_dead_threads(self):
        thread_names = list(self._py5threads.keys())
        for t_name in thread_names:
            if not self._py5threads[t_name][0].is_alive():
                del self._py5threads[t_name]

    def has_thread(self, name: str) -> None:
        """$class_Sketch_has_thread"""
        self._remove_dead_threads()
        return name in self._py5threads

    def join_thread(self, name: str, *, timeout: float = None) -> bool:
        """$class_Sketch_join_thread"""
        self._remove_dead_threads()
        if name in self._py5threads:
            self._py5threads[name][0].join(timeout)
        return not self.has_thread(name)

    def stop_thread(self, name: str, wait: bool = False) -> None:
        """$class_Sketch_stop_thread"""
        if name in self._py5threads:
            t, py5thread = self._py5threads[name]
            py5thread.stop()
            if wait:
                t.join()

    def stop_all_threads(self, wait: bool = False) -> None:
        """$class_Sketch_stop_all_threads"""
        current_thread_name = threading.current_thread().name
        for name in self.list_threads():
            if name == current_thread_name:
                # don't try to join a thread with itself
                continue
            self.stop_thread(name, wait=wait)

    def list_threads(self) -> None:
        """$class_Sketch_list_threads"""
        self._remove_dead_threads()
        return list(self._py5threads.keys())
