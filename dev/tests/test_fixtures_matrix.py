"""Tests del generador de matriz de cobertura (F06a2 T7)."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from dev.tools.fixtures_matrix import (
    _fixture_axes,
    _discover_fixtures,
    _load_target,
    _format_md,
    main,
)


# ---------------------------------------------------------------------------
# Fixtures de prueba
# ---------------------------------------------------------------------------


@pytest.fixture
def fake_repo(tmp_path: Path, monkeypatch) -> Path:
    """Construye un repo minimo con dos fixtures de prueba."""
    fx_root = tmp_path / "dev" / "fixtures"
    fx_root.mkdir(parents=True)
    target = fx_root / "target_matrix.yml"
    target.write_text(
        """\
version: 1
axes:
  languages: [python, typescript, go, rust]
  frameworks: [vscode-extension, pnpm-monorepo]
  build_systems: [pyproject, cargo]
  file_kinds: [source-text, minified-js]
  containers: [asar]
""",
        encoding="utf-8",
    )

    # Fixture Python + pyproject
    fx_py = fx_root / "fx-fake-py"
    fx_py.mkdir()
    (fx_py / "pyproject.toml").write_text("[project]\nname='x'\n")
    (fx_py / "src").mkdir()
    (fx_py / "src" / "main.py").write_text("x = 1\n")
    (fx_py / "src" / "lib.py").write_text("y = 2\n")

    # Fixture TS con package.json
    fx_ts = fx_root / "fx-fake-ts"
    fx_ts.mkdir()
    (fx_ts / "package.json").write_text(
        json.dumps({"dependencies": {"typescript": "^5.0.0"}})
    )
    (fx_ts / "src").mkdir()
    (fx_ts / "src" / "main.ts").write_text("const x = 1;\n")

    # Fixture Go
    fx_go = fx_root / "fx-fake-go"
    fx_go.mkdir()
    (fx_go / "go.mod").write_text("module example.com/x\n\ngo 1.22\n")
    (fx_go / "main.go").write_text("package main\n")

    monkeypatch.setattr("dev.tools.fixtures_matrix.FIXTURES_DIR", fx_root)
    monkeypatch.setattr("dev.tools.fixtures_matrix.TARGET_PATH", target)
    monkeypatch.setattr(
        "dev.tools.fixtures_matrix.MATRIX_OUT", fx_root / "MATRIX.md"
    )
    return tmp_path


# ---------------------------------------------------------------------------
# Descubrimiento de fixtures
# ---------------------------------------------------------------------------


class TestDiscoverFixtures:
    def test_excludes_template(self, fake_repo) -> None:
        from pathlib import Path
        # Crear carpeta con _
        (fake_repo / "dev" / "fixtures" / "_template").mkdir()
        fixtures = _discover_fixtures()
        names = [f.name for f in fixtures]
        assert "_template" not in names
        assert "fx-fake-py" in names


# ---------------------------------------------------------------------------
# Ejes cubiertos por fixture
# ---------------------------------------------------------------------------


class TestFixtureAxes:
    def test_python_and_pyproject(self, fake_repo) -> None:
        from dev.tools.fixtures_matrix import FIXTURES_DIR
        axes = _fixture_axes(FIXTURES_DIR / "fx-fake-py")
        assert "python" in axes["languages"]
        assert "pyproject" in axes["build_systems"]
        assert "shell" not in axes["languages"]
        assert "asar" not in axes["containers"]

    def test_typescript(self, fake_repo) -> None:
        from dev.tools.fixtures_matrix import FIXTURES_DIR
        axes = _fixture_axes(FIXTURES_DIR / "fx-fake-ts")
        assert "typescript" in axes["languages"]
        # npm sin pnpm-lock: pnpm no se detecta como build
        assert "pnpm" not in axes["build_systems"]

    def test_go(self, fake_repo) -> None:
        from dev.tools.fixtures_matrix import FIXTURES_DIR
        axes = _fixture_axes(FIXTURES_DIR / "fx-fake-go")
        assert "go" in axes["languages"]
        assert "go-modules" in axes["build_systems"]

    def test_asar(self, fake_repo) -> None:
        from dev.tools.fixtures_matrix import FIXTURES_DIR
        fx = FIXTURES_DIR / "fx-fake-py"
        (fx / "bundle.asar").write_bytes(b"x")
        axes = _fixture_axes(fx)
        assert "asar" in axes["containers"]


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------


class TestMain:
    def test_generates_matrix(self, fake_repo, capsys) -> None:
        rc = main([])
        assert rc == 0
        md = (fake_repo / "dev" / "fixtures" / "MATRIX.md").read_text()
        assert "Matriz de cobertura" in md
        assert "python" in md
        assert "typescript" in md
        assert "go" in md

    def test_check_passes_when_complete(self, fake_repo) -> None:
        # Renombrar target a uno mas pequeno para que pase
        target = fake_repo / "dev" / "fixtures" / "target_matrix.yml"
        target.write_text(
            """\
version: 1
axes:
  languages: [python, typescript, go]
  frameworks: []
  build_systems: [pyproject, go-modules]
  file_kinds: [source-text]
  containers: []
""",
            encoding="utf-8",
        )
        from dev.tools.fixtures_matrix import _discover_fixtures, _fixture_axes
        import sys
        # Debug: ver que se descubre
        agg = {"languages": set(), "frameworks": set(), "build_systems": set(),
               "file_kinds": set(), "containers": set()}
        for fx in _discover_fixtures():
            ax = _fixture_axes(fx)
            for k, v in ax.items():
                agg[k] |= v
        print("DISCOVERED:", agg, file=sys.stderr)
        rc = main(["--check"])
        assert rc == 0

    def test_check_fails_when_incomplete(self, fake_repo) -> None:
        target = fake_repo / "dev" / "fixtures" / "target_matrix.yml"
        target.write_text(
            """\
version: 1
axes:
  languages: [python, rust]
  frameworks: []
  build_systems: [pyproject]
  file_kinds: [source-text]
  containers: []
""",
            encoding="utf-8",
        )
        rc = main(["--check"])
        assert rc == 2

    def test_missing_target(self, tmp_path, monkeypatch) -> None:
        empty = tmp_path / "no"
        empty.mkdir()
        monkeypatch.setattr("dev.tools.fixtures_matrix.TARGET_PATH", empty / "t.yml")
        rc = main([])
        assert rc == 1
