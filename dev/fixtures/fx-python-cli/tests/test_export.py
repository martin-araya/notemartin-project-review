"""Tests for fxnotes export."""
import json
import pytest

from fxnotes import FXNotesError


def test_export_r01_json_to_file(cli_runner, tmp_path):
    cli_runner(["add", "k1", "v1"])
    out = tmp_path / "out.json"
    rc = cli_runner(["export", str(out), "--format", "json"])
    assert rc == 0
    data = json.loads(out.read_text())
    assert any(r["key"] == "k1" for r in data)


def test_export_r02_csv_to_stdout(cli_runner, capsys):
    cli_runner(["add", "k1", "v1"])
    cli_runner(["export", "-", "--format", "csv"])
    out = capsys.readouterr().out
    assert "k1" in out


def test_export_r03_json_stdout(cli_runner, capsys):
    cli_runner(["add", "k1", "v1"])
    capsys.readouterr()
    cli_runner(["export", "-"])
    out = capsys.readouterr().out
    data = json.loads(out)
    assert any(r["key"] == "k1" for r in data)


def test_export_r04_empty_export(cli_runner, tmp_path):
    out = tmp_path / "empty.json"
    rc = cli_runner(["export", str(out), "--format", "json"])
    assert rc == 0
    assert out.read_text() == "[]"


def test_export_r05_invalid_format(cli_runner):
    from fxnotes.cli import build_parser
    parser = build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(["export", "-", "--format", "xml"])


def test_export_r06_db_error_returns_one(cli_runner, monkeypatch, capsys):
    from fxnotes.db import Database
    monkeypatch.setattr(Database, "cursor",
                       lambda self: (_ for _ in ()).throw(FXNotesError("boom")))
    rc = cli_runner(["export", "-"])
    err = capsys.readouterr().err
    assert rc == 1
    assert "Export failed" in err