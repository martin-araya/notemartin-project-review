"""Tiny event bus used by the CLI to broadcast lifecycle events.

Other modules can register listeners via `on(event, fn)` and emit with
`emit(event, **payload)`. Failures inside a listener are swallowed so
the main flow is not interrupted by telemetry bugs.
"""
from __future__ import annotations

from collections import defaultdict
from typing import Callable


_listeners: dict = defaultdict(list)


def on(event: str, fn: Callable) -> None:
    _listeners[event].append(fn)


def emit(event: str, **payload) -> None:
    for fn in list(_listeners.get(event, [])):
        try:
            fn(**payload)
        except Exception:
            pass


def reset() -> None:
    _listeners.clear()