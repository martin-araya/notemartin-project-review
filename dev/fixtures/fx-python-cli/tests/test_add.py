"""Tests for fxnotes add."""
import pytest

from fxnotes import ValidationError, DatabaseError


def test_add_r01_success(cli_runner):
    rc = cli_runner(["add", "k1", "value one"])
    assert rc == 0


def test_add_r02_validation_empty_key(cli_runner):
    with pytest.raises(ValidationError, match="key cannot be empty"):
        cli_runner(["add", "", "value"])


def test_add_r03_validation_too_long_key(cli_runner, monkeypatch):
    from fxnotes.config import load_config
    monkeypatch.setattr("fxnotes.config.load_config",
                      lambda p=None: {**({"db_path": ":memory:", "max_key_len": 5, "max_value_len": 4096})})
    with pytest.raises(ValidationError, match="key exceeds"):
        cli_runner(["add", "x" * 10, "v"])


def test_add_r04_duplicate(cli_runner):
    cli_runner(["add", "k1", "v1"])
    with pytest.raises(DatabaseError, match="duplicate"):
        cli_runner(["add", "k1", "v2"])


def test_add_r05_value_too_long(cli_runner, monkeypatch):
    monkeypatch.setenv("FXNOTES_MAX_VALUE_LEN", "5")
    with pytest.raises(ValidationError, match="value exceeds"):
        cli_runner(["add", "k1", "x" * 100])


def test_add_r06_race_lost(cli_runner):
    """Trap exists in code: add() does SELECT-then-INSERT, allowing race."""
    import inspect
    from fxnotes.commands import add as add_mod
    src = inspect.getsource(add_mod.run)
    assert "SELECT 1 FROM notes WHERE key = ?" in src, "add must check existence before INSERT"
    assert "lost race" in src, "add must map IntegrityError to DatabaseError(lost race)"