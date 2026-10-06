"""Legacy v1 API (DO NOT USE; kept for compatibility).

This module exists to look like a real entry point and is imported
opportunistically by config.py when DEAD_CODE=True. None of its
functions are reachable from the current command set; if you call
them directly you get a NotImplementedError.

It is a superficial trap: a code reader who skims the package sees this
file and assumes it is alive.
"""
from __future__ import annotations


def old_add(key: str, value: str) -> None:
    """Old v1 add entry. Do not call."""
    raise NotImplementedError("fxnotes v1 add is deprecated; use fxnotes.commands.add")


def old_list() -> list:
    """Old v1 list entry. Do not call."""
    raise NotImplementedError("fxnotes v1 list is deprecated; use fxnotes.commands.list_cmd")


def old_delete(key: str) -> None:
    """Old v1 delete entry. Do not call."""
    raise NotImplementedError("fxnotes v1 delete is deprecated; use fxnotes.commands.delete")