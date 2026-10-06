"""Command registry: dispatch by string from a dict.

This file exposes COMMANDS, a dict mapping command name -> module. The
superficial trap is the dispatch table itself: a reader who looks at
add.py or delete.py in isolation cannot tell which commands exist.
"""
from . import add as add_mod
from . import delete as delete_mod
from . import export as export_mod
from . import list_cmd as list_mod


COMMANDS = {
    "add": add_mod,
    "list": list_mod,
    "delete": delete_mod,
    "export": export_mod,
}