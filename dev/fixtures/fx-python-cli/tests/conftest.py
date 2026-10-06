"""Conftest for fxnotes tests."""
import os
import sys
import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def tmp_db(monkeypatch, tmp_path):
    db_path = tmp_path / "notes.db"
    monkeypatch.setenv("FXNOTES_DB_PATH", str(db_path))
    monkeypatch.setenv("FXNOTES_CONFIRM", "ask")
    monkeypatch.setenv("FXNOTES_DEAD_CODE", "false")
    return db_path


@pytest.fixture
def cli_runner(monkeypatch, tmp_db):
    """Returns a function that runs fxnotes and returns (rc, stdout, stderr)."""
    from fxnotes import cli

    def _run(args, stdin=None):
        from fxnotes.config import load_config
        from fxnotes.db import Database

        ctx = {"config": load_config(None), "db": Database(str(tmp_db))}
        ctx["db"].connect()
        try:
            from fxnotes.cli import build_parser
            parser = build_parser()
            parsed = parser.parse_args(args)
            from fxnotes.commands import COMMANDS
            return COMMANDS[parsed.command].run(parsed, ctx)
        finally:
            ctx["db"].close()

    return _run