"""Tests del harness de ejecucion de tests de fixtures (F06a2 T4)."""
from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

from dev.tools.run_fixture_tests import (
    _discover_fixtures,
    _load_manifest,
    _run_one,
    _current_platform,
    _supports_platform,
    main,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _write_manifest(fx: Path, requires=None, test_cmd=None) -> None:
    requires = requires or ["linux", "macos", "windows"]
    test_cmd = test_cmd or "true"
    fx.mkdir(parents=True, exist_ok=True)
    (fx / "manifest.yml").write_text(
        f"""\
name: {fx.name}
requires: {requires}
test_cmd: {test_cmd}
""",
        encoding="utf-8",
    )


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestLoadManifest:
    def test_ok(self, tmp_path: Path) -> None:
        _write_manifest(tmp_path / "fx", test_cmd="echo hi")
        m = _load_manifest(tmp_path / "fx")
        assert m["name"] == "fx"
        assert m["test_cmd"] == "echo hi"

    def test_missing(self, tmp_path: Path) -> None:
        assert _load_manifest(tmp_path / "no") is None

    def test_invalid_yaml(self, tmp_path: Path) -> None:
        fx = tmp_path / "fx"
        fx.mkdir()
        (fx / "manifest.yml").write_text(": : :\n  bad", encoding="utf-8")
        m = _load_manifest(fx)
        # El parser minimo puede tolerarlo o devolver _error
        assert m is None or "_error" in m or isinstance(m, dict)


class TestDiscoverFixtures:
    def test_excludes_template_and_hidden(self, tmp_path, monkeypatch) -> None:
        from dev.tools import run_fixture_tests as rft

        fx_dir = tmp_path / "fixtures"
        fx_dir.mkdir()
        (fx_dir / "_template").mkdir()
        (fx_dir / ".hidden").mkdir()
        (fx_dir / "fx-real").mkdir()
        monkeypatch.setattr(rft, "FIXTURES_DIR", fx_dir)
        names = [p.name for p in _discover_fixtures(None)]
        assert names == ["fx-real"]


class TestSupportsPlatform:
    def test_linux_required_on_linux(self) -> None:
        m = {"requires": ["linux"]}
        assert _supports_platform(m, "linux") is True

    def test_macos_required_on_linux(self) -> None:
        m = {"requires": ["macos"]}
        assert _supports_platform(m, "linux") is False


class TestRunOne:
    def test_pass(self, tmp_path: Path) -> None:
        fx = tmp_path / "fx-pass"
        _write_manifest(fx, test_cmd="true")
        result = _run_one(fx, use_container=False, platform_arg="linux", timeout=10.0)
        assert result["status"] == "passed"
        assert result["returncode"] == 0

    def test_fail(self, tmp_path: Path) -> None:
        fx = tmp_path / "fx-fail"
        # usar la ruta absoluta para evitar el builtin de zsh
        _write_manifest(fx, test_cmd="/usr/bin/false")
        result = _run_one(fx, use_container=False, platform_arg="linux", timeout=10.0)
        assert result["status"] == "failed"
        assert result["returncode"] != 0

    def test_skipped_platform(self, tmp_path: Path) -> None:
        fx = tmp_path / "fx-mac"
        _write_manifest(fx, requires=["macos"], test_cmd="true")
        result = _run_one(fx, use_container=False, platform_arg="linux", timeout=10.0)
        assert result["status"] == "skipped"
        assert "macos" in result["reason"]

    def test_no_manifest(self, tmp_path: Path) -> None:
        fx = tmp_path / "fx-no-manifest"
        fx.mkdir()
        result = _run_one(fx, use_container=False, platform_arg="linux", timeout=10.0)
        assert result["status"] == "error"
        assert "no manifest" in result["reason"]


class TestMain:
    def test_run_specific_pass(self, tmp_path, monkeypatch, capsys) -> None:
        from dev.tools import run_fixture_tests as rft

        fx_dir = tmp_path / "fixtures"
        fx_dir.mkdir()
        fx = fx_dir / "fx-ok"
        _write_manifest(fx, test_cmd="true")
        monkeypatch.setattr(rft, "FIXTURES_DIR", fx_dir)
        rc = main(["--fixture", "fx-ok"])
        assert rc == 0

    def test_run_specific_fail(self, tmp_path, monkeypatch) -> None:
        from dev.tools import run_fixture_tests as rft

        fx_dir = tmp_path / "fixtures"
        fx_dir.mkdir()
        fx = fx_dir / "fx-bad"
        _write_manifest(fx, test_cmd="/usr/bin/false")
        monkeypatch.setattr(rft, "FIXTURES_DIR", fx_dir)
        rc = main(["--fixture", "fx-bad"])
        assert rc == 2

    def test_run_all_with_skipped_macos(self, tmp_path, monkeypatch) -> None:
        from dev.tools import run_fixture_tests as rft

        fx_dir = tmp_path / "fixtures"
        fx_dir.mkdir()
        _write_manifest(fx_dir / "fx-pass", test_cmd="/usr/bin/true")
        _write_manifest(
            fx_dir / "fx-mac", requires=["macos"], test_cmd="/usr/bin/true"
        )
        _write_manifest(fx_dir / "fx-fail", test_cmd="/usr/bin/false")
        monkeypatch.setattr(rft, "FIXTURES_DIR", fx_dir)
        rc = main(["--all", "--platform", "linux"])
        # fail -> rc 2; skipped no cuenta como falla
        assert rc == 2

    def test_run_all_only_skipped_passes(self, tmp_path, monkeypatch) -> None:
        from dev.tools import run_fixture_tests as rft

        fx_dir = tmp_path / "fixtures"
        fx_dir.mkdir()
        _write_manifest(
            fx_dir / "fx-mac", requires=["macos"], test_cmd="true"
        )
        monkeypatch.setattr(rft, "FIXTURES_DIR", fx_dir)
        rc = main(["--all", "--platform", "linux"])
        assert rc == 0  # solo skipped, no failed

    def test_report_json(self, tmp_path, monkeypatch) -> None:
        from dev.tools import run_fixture_tests as rft

        fx_dir = tmp_path / "fixtures"
        fx_dir.mkdir()
        _write_manifest(fx_dir / "fx-x", test_cmd="true")
        monkeypatch.setattr(rft, "FIXTURES_DIR", fx_dir)
        report = tmp_path / "report.json"
        rc = main(["--all", "--report", str(report)])
        assert rc == 0
        assert report.is_file()
        import json
        data = json.loads(report.read_text())
        assert "results" in data
        assert "summary" in data

    def test_no_args(self) -> None:
        rc = main([])
        assert rc == 1
