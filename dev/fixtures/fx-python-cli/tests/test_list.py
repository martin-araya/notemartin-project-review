"""Tests for fxnotes list."""
import pytest

from fxnotes import FXNotesError


def test_list_r01_empty(cli_runner, capsys):
    cli_runner(["list"])
    out = capsys.readouterr().out
    assert "0 entries" in out


def test_list_r02_with_entries(cli_runner, capsys):
    cli_runner(["add", "k1", "v1"])
    capsys.readouterr()  # discard
    cli_runner(["add", "k2", "v2"])
    capsys.readouterr()
    cli_runner(["list"])
    out = capsys.readouterr().out
    assert "k1\t" in out
    assert "k2\t" in out


def test_list_r03_filter_by_tag(cli_runner, capsys):
    cli_runner(["add", "k1", "v1", "--tag", "alpha"])
    capsys.readouterr()
    cli_runner(["add", "k2", "v2", "--tag", "beta"])
    capsys.readouterr()
    cli_runner(["list", "--tag", "alpha"])
    out = capsys.readouterr().out
    lines = [l for l in out.splitlines() if l.startswith("k")]
    assert any(l.startswith("k1") for l in lines)
    assert not any(l.startswith("k2") for l in lines)


def test_list_r04_sort_by_key(cli_runner, capsys):
    cli_runner(["add", "b", "v"])
    capsys.readouterr()
    cli_runner(["add", "a", "v"])
    capsys.readouterr()
    cli_runner(["list", "--sort-by", "key"])
    out = capsys.readouterr().out
    lines = [l for l in out.splitlines() if l.startswith(("a", "b"))]
    assert lines == sorted(lines)


def test_list_r05_invalid_sort_key(cli_runner):
    from fxnotes.cli import build_parser
    parser = build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(["list", "--sort-by", "evil"])


def test_list_r06_empty_swallow_db_error(cli_runner, capsys, monkeypatch):
    from fxnotes.db import Database
    monkeypatch.setattr(Database, "cursor",
                       lambda self: (_ for _ in ()).throw(FXNotesError("boom")))
    cli_runner(["list"])
    out = capsys.readouterr().out
    assert "0 entries" in out