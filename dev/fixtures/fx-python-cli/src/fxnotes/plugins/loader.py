"""Dynamic plugin loader for fxnotes commands.

Third-party commands register themselves under the
`fxnotes.commands` entry-point group. At runtime we import each module
on demand with importlib.import_module. The dynamic import is the
superficial trap: a static import scanner cannot resolve what plugin
modules are available without iterating the entry points.
"""
from __future__ import annotations

import importlib
from importlib import metadata as ipmd
from typing import Callable


PLUGIN_GROUP = "fxnotes.commands"


def discover() -> list:
    """Returns [(name, callable), ...] for every registered plugin."""
    out = []
    for ep in ipmd.entry_points(group=PLUGIN_GROUP):
        try:
            module = importlib.import_module(ep.module)
            obj = getattr(module, ep.attr, None)
            if obj is None:
                continue
            out.append((ep.name, obj))
        except Exception:
            continue
    return out


def load(name: str) -> Callable | None:
    """Dynamically import the plugin command with the given name."""
    for ep in ipmd.entry_points(group=PLUGIN_GROUP):
        if ep.name == name:
            try:
                module = importlib.import_module(ep.module)
                return getattr(module, ep.attr, None)
            except Exception:
                return None
    return None