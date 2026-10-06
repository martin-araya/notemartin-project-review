"""Tests for fxnotes delete."""
import io
import pytest

from fxnotes import NotFoundError, CancelledError, ValidationError


def test_delete_r01_success_soft(cli_runner, monkeypatch):
    monkeypatch.setenv("FXNOTES_CONFIRM", "false")
    cli_runner(["add", "k1", "v"])
    rc = cli_runner(["delete", "k1"])
    assert rc == 0


def test_delete_r02_not_found(cli_runner):
    with pytest.raises(NotFoundError, match="key not found"):
        cli_runner(["delete", "missing"])


def test_delete_r03_validation_empty_key(cli_runner):
    with pytest.raises(ValidationError, match="key cannot be empty"):
        cli_runner(["delete", ""])


def test_delete_r04_archived_is_dead_branch(cli_runner, capsys):
    cli_runner(["add", "k1", "v"])
    rc = cli_runner(["delete", "k1", "--archived"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "deprecated" in out.lower()


def test_delete_r05_no_undo_plus_confirm_false_is_permanent(cli_runner, monkeypatch, capsys):
    monkeypatch.setenv("FXNOTES_CONFIRM", "false")
    cli_runner(["add", "k1", "v"])
    rc = cli_runner(["delete", "k1", "--no-undo"])
    out = capsys.readouterr().out
    assert "permanently" in out.lower()


def test_delete_r06_user_rejects_ask(cli_runner, monkeypatch):
    monkeypatch.setenv("FXNOTES_CONFIRM", "ask")
    cli_runner(["add", "k1", "v"])
    monkeypatch.setattr("sys.stdin", io.StringIO("n\n"))
    with pytest.raises(CancelledError, match="cancelled"):
        cli_runner(["delete", "k1"])