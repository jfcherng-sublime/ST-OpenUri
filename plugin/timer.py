import threading
from typing import Callable, Optional


class RepeatingTimer:
    def __init__(self, interval_ms: int, func: Callable, *args, **kwargs) -> None:
        self.interval_s = interval_ms / 1000
        self.timer: Optional[threading.Timer] = None
        self.is_running = False
        self.set_func(func, *args, **kwargs)

    def set_func(self, func: Callable, *args, **kwargs) -> None:
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def set_interval(self, interval_ms: int) -> None:
        self.interval_s = interval_ms / 1000

    def start(self) -> None:
        self.timer = threading.Timer(self.interval_s, self._callback)
        self.timer.start()
        self.is_running = True

    def cancel(self) -> None:
        if self.timer:
            self.timer.cancel()
        self.is_running = False

    def _callback(self) -> None:
        self.func(*self.args, **self.kwargs)
        self.start()
