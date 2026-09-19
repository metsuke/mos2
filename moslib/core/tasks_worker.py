"""Worker daemon de tareas automáticas."""

from __future__ import annotations

import threading

_worker_thread: threading.Thread | None = None
_stop = threading.Event()
_interval = 30.0


def worker_running() -> bool:
    return _worker_thread is not None and _worker_thread.is_alive()


def _loop() -> None:
    from moslib.core.tasks import tick

    while not _stop.is_set():
        try:
            tick()
        except Exception:
            pass
        _stop.wait(_interval)


def start_worker(interval: float = 30.0) -> bool:
    global _worker_thread, _interval
    _interval = max(5.0, float(interval))
    if worker_running():
        return False
    _stop.clear()
    _worker_thread = threading.Thread(target=_loop, name="mos-tareas", daemon=True)
    _worker_thread.start()
    return True


def stop_worker() -> None:
    _stop.set()
    t = _worker_thread
    if t is not None:
        t.join(timeout=2.0)
