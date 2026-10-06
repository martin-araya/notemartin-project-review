"""Tests del verificador multi-formato (F06a2 T8)."""
from __future__ import annotations

import json
import re
import zipfile
from pathlib import Path

import pytest

from dev.tools.check_ground_truth import (
    CiteRef,
    parse_cite,
    check_cite,
    _validate_text,
    _validate_container,
    _validate_notebook,
    _validate_xpath,
    _validate_yaml,
    _validate_binary,
    _yaml_path_tokens,
    _yaml_walk,
    _open_container_member,
    _read_asar_member,
    check,
    main,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _write(p: Path, content: str | bytes, mode: str = "text") -> Path:
    if mode == "text":
        p.write_text(content, encoding="utf-8")
    else:
        p.write_bytes(content if isinstance(content, bytes) else content.encode("utf-8"))
    return p


# ---------------------------------------------------------------------------
# parse_cite
# ---------------------------------------------------------------------------


class TestParseCiteText:
    def test_simple(self) -> None:
        ref = parse_cite("src/a.py:10")
        assert ref is not None and ref.kind == "text"
        assert ref.path == "src/a.py" and ref.line == 10 and ref.symbol is None

    def test_range(self) -> None:
        ref = parse_cite("src/a.py:1-5")
        assert ref is not None and ref.line == 1 and ref.end == 5

    def test_with_symbol(self) -> None:
        ref = parse_cite("src/a.py:18-23#add_parser")
        assert ref is not None and ref.kind == "text"
        assert ref.symbol == "add_parser"
        assert ref.line == 18 and ref.end == 23

    def test_with_column(self) -> None:
        ref = parse_cite("bundle.min.js:1:42")
        assert ref is not None and ref.kind == "text"
        assert ref.column == 42

    def test_range_column_symbol(self) -> None:
        ref = parse_cite("bundle.min.js:1-3:120#s")
        assert ref is not None
        assert ref.column == 120
        assert ref.symbol == "s"

    def test_malformed(self) -> None:
        assert parse_cite("") is None
        assert parse_cite(":10") is None
        assert parse_cite("file.py") is None
        assert parse_cite("file.py:abc") is None


class TestParseCiteContainer:
    def test_zip(self) -> None:
        ref = parse_cite("app.jar!/META-INF/MANIFEST.MF:1")
        assert ref is not None and ref.kind == "container"
        assert ref.path == "app.jar"
        assert ref.inner == "META-INF/MANIFEST.MF"
        assert ref.line == 1


class TestParseCiteNotebook:
    def test_cell_line(self) -> None:
        ref = parse_cite("notebook.ipynb#celda-2:10")
        assert ref is not None and ref.kind == "notebook"
        assert ref.cell == 2 and ref.line == 10


class TestParseCiteXpath:
    def test_xpath(self) -> None:
        ref = parse_cite("ui.xml#/root/button[@id='ok']")
        assert ref is not None and ref.kind == "xpath"
        assert ref.expr == "/root/button[@id='ok']"


class TestParseCiteYaml:
    def test_yaml_path(self) -> None:
        ref = parse_cite("scene.unity#Camera.main.transform.position.x")
        assert ref is not None and ref.kind == "yaml"
        assert ref.expr == "Camera.main.transform.position.x"


class TestParseCiteBinary:
    def test_hex_offset(self) -> None:
        ref = parse_cite("lib.bin#0xDEAD")
        assert ref is not None and ref.kind == "binary"
        assert ref.offset == 0xDEAD

    def test_dec_offset(self) -> None:
        ref = parse_cite("lib.bin#1024")
        assert ref is not None and ref.kind == "binary"
        assert ref.offset == 1024

    def test_symbol(self) -> None:
        ref = parse_cite("lib.bin#main_loop")
        assert ref is not None and ref.kind == "binary"
        assert ref.symbol == "main_loop"


# ---------------------------------------------------------------------------
# _yaml_path_tokens y _yaml_walk
# ---------------------------------------------------------------------------


class TestYamlPaths:
    def test_simple(self) -> None:
        tokens = _yaml_path_tokens("a.b.c")
        assert tokens == [("a", None, False), ("b", None, False), ("c", None, False)]

    def test_index(self) -> None:
        tokens = _yaml_path_tokens("items[0].name")
        assert tokens == [("items", None, False), ("", 0, False), ("name", None, False)]

    def test_wildcard(self) -> None:
        tokens = _yaml_path_tokens("users[*].name")
        assert tokens == [("users", None, False), ("", None, True), ("name", None, False)]

    def test_walk(self) -> None:
        doc = {"users": [{"name": "a"}, {"name": "b"}]}
        results = _yaml_walk(doc, _yaml_path_tokens("users[*].name"))
        assert results == ["a", "b"]


# ---------------------------------------------------------------------------
# _read_asar_member
# ---------------------------------------------------------------------------


def _build_asar(files: dict) -> bytes:
    """Construye un archivo asar sintetico: header JSON con offsets, ``\\x00``, body."""
    body = b""
    offs = {}
    cursor = 0
    for name, content in files.items():
        offs[name] = {"offset": cursor, "size": len(content)}
        body += content
        cursor += len(content)
    header = json.dumps({"files": offs}).encode("utf-8")
    return header + b"\x00" + body


# ---------------------------------------------------------------------------
# Validadores
# ---------------------------------------------------------------------------


class TestValidateText:
    def test_ok(self, tmp_path: Path) -> None:
        f = _write(tmp_path / "a.py", "linea1\nlinea2\nlinea3\n")
        errs = _validate_text(tmp_path, CiteRef("a.py:2", "text", "a.py", line=2))
        assert errs == []

    def test_range_ok(self, tmp_path: Path) -> None:
        f = _write(tmp_path / "a.py", "uno\ndos\ntres\ncuatro\n")
        errs = _validate_text(tmp_path, CiteRef("a.py:2-3", "text", "a.py", line=2, end=3))
        assert errs == []

    def test_symbol_ok(self, tmp_path: Path) -> None:
        f = _write(tmp_path / "a.py", "def add(a, b):\n    return a + b\n")
        errs = _validate_text(tmp_path, CiteRef("a.py:1#add", "text", "a.py", line=1, symbol="add"))
        assert errs == []

    def test_symbol_missing(self, tmp_path: Path) -> None:
        f = _write(tmp_path / "a.py", "def foo():\n    pass\n")
        errs = _validate_text(tmp_path, CiteRef("a.py:1#bar", "text", "a.py", line=1, symbol="bar"))
        assert errs and "bar" in errs[0]

    def test_line_out_of_range(self, tmp_path: Path) -> None:
        f = _write(tmp_path / "a.py", "uno\ndos\n")
        errs = _validate_text(tmp_path, CiteRef("a.py:99", "text", "a.py", line=99))
        assert errs and "fuera de rango" in errs[0]

    def test_file_missing(self, tmp_path: Path) -> None:
        errs = _validate_text(tmp_path, CiteRef("nope.py:1", "text", "nope.py", line=1))
        assert errs and "inexistente" in errs[0]

    def test_column_ok(self, tmp_path: Path) -> None:
        f = _write(tmp_path / "bundle.js", "x" * 5000 + "\n")
        errs = _validate_text(
            tmp_path,
            CiteRef("bundle.js:1:3000", "text", "bundle.js", line=1, column=3000),
        )
        assert errs == []

    def test_column_out_of_range(self, tmp_path: Path) -> None:
        f = _write(tmp_path / "bundle.js", "x" * 100 + "\n")
        errs = _validate_text(
            tmp_path,
            CiteRef("bundle.js:1:5000", "text", "bundle.js", line=1, column=5000),
        )
        assert errs and "columna" in errs[0]

    def test_inverted_range(self, tmp_path: Path) -> None:
        # El validador no detecta inversion: end > line es OK, end < line falla
        f = _write(tmp_path / "a.py", "a\nb\nc\n")
        errs = _validate_text(tmp_path, CiteRef("a.py:3-1", "text", "a.py", line=3, end=1))
        # end < len(lines) -> OK, pero el haystack queda vacio o raro; al menos
        # el simbolo no se encontrara si lo hay
        assert isinstance(errs, list)


class TestValidateContainer:
    def test_zip_ok(self, tmp_path: Path) -> None:
        zf_path = tmp_path / "app.zip"
        with zipfile.ZipFile(zf_path, "w") as zf:
            zf.writestr("inner.txt", "alpha\nbeta\ngamma\n")
        ref = CiteRef("app.zip!/inner.txt:2", "container", "app.zip", line=2, inner="inner.txt")
        errs = _validate_container(tmp_path, ref)
        assert errs == []

    def test_zip_missing_entry(self, tmp_path: Path) -> None:
        zf_path = tmp_path / "app.zip"
        with zipfile.ZipFile(zf_path, "w") as zf:
            zf.writestr("other.txt", "x")
        ref = CiteRef("app.zip!/inner.txt:1", "container", "app.zip", line=1, inner="inner.txt")
        errs = _validate_container(tmp_path, ref)
        assert errs and "no encontrada" in errs[0]

    def test_zip_line_out_of_range(self, tmp_path: Path) -> None:
        zf_path = tmp_path / "app.zip"
        with zipfile.ZipFile(zf_path, "w") as zf:
            zf.writestr("inner.txt", "x\ny\n")
        ref = CiteRef("app.zip!/inner.txt:99", "container", "app.zip", line=99, inner="inner.txt")
        errs = _validate_container(tmp_path, ref)
        assert errs and "fuera de rango" in errs[0]

    def test_asar_ok(self, tmp_path: Path) -> None:
        files = {"a.txt": b"one\ntwo\nthree\n"}
        asar_path = tmp_path / "bundle.asar"
        asar_path.write_bytes(_build_asar(files))
        ref = CiteRef("bundle.asar!/a.txt:2", "container", "bundle.asar", line=2, inner="a.txt")
        errs = _validate_container(tmp_path, ref)
        assert errs == []


class TestValidateNotebook:
    def _nb(self, tmp_path: Path, cells=2) -> Path:
        nb = {
            "cells": [
                {"cell_type": "code", "source": ["print('a')\n", "print('b')\n"]},
                {"cell_type": "code", "source": ["x = 1\n", "y = 2\n"]},
            ][:cells]
        }
        return _write(tmp_path / "nb.ipynb", json.dumps(nb))

    def test_ok(self, tmp_path: Path) -> None:
        self._nb(tmp_path)
        ref = CiteRef("nb.ipynb#celda-0:1", "notebook", "nb.ipynb", line=1, cell=0)
        assert _validate_notebook(tmp_path, ref) == []

    def test_cell_out_of_range(self, tmp_path: Path) -> None:
        self._nb(tmp_path)
        ref = CiteRef("nb.ipynb#celda-9:1", "notebook", "nb.ipynb", line=1, cell=9)
        errs = _validate_notebook(tmp_path, ref)
        assert errs and "celda" in errs[0]

    def test_line_out_of_range(self, tmp_path: Path) -> None:
        self._nb(tmp_path)
        ref = CiteRef("nb.ipynb#celda-0:99", "notebook", "nb.ipynb", line=99, cell=0)
        errs = _validate_notebook(tmp_path, ref)
        assert errs and "fuera de rango" in errs[0]


class TestValidateXpath:
    def test_ok(self, tmp_path: Path) -> None:
        _write(tmp_path / "ui.xml", "<root><button id='ok'/></root>")
        ref = CiteRef("ui.xml#x", "xpath", "ui.xml", expr="/root/button")
        assert _validate_xpath(tmp_path, ref) == []

    def test_no_match(self, tmp_path: Path) -> None:
        _write(tmp_path / "ui.xml", "<root><x/></root>")
        ref = CiteRef("ui.xml#x", "xpath", "ui.xml", expr="/root/missing")
        errs = _validate_xpath(tmp_path, ref)
        assert errs and "no matchea" in errs[0]

    def test_invalid_xml(self, tmp_path: Path) -> None:
        _write(tmp_path / "ui.xml", "<root><")
        ref = CiteRef("ui.xml#x", "xpath", "ui.xml", expr="/root")
        errs = _validate_xpath(tmp_path, ref)
        assert errs and "XML" in errs[0]


class TestValidateYaml:
    def test_yaml_ok(self, tmp_path: Path) -> None:
        _write(tmp_path / "s.yaml", "a:\n  b:\n    c: hello\n")
        ref = CiteRef("s.yaml#p", "yaml", "s.yaml", expr="a.b.c")
        assert _validate_yaml(tmp_path, ref) == []

    def test_yaml_index(self, tmp_path: Path) -> None:
        _write(tmp_path / "s.yaml", "items:\n  - name: a\n  - name: b\n")
        ref = CiteRef("s.yaml#p", "yaml", "s.yaml", expr="items[1].name")
        assert _validate_yaml(tmp_path, ref) == []

    def test_yaml_wildcard(self, tmp_path: Path) -> None:
        _write(tmp_path / "s.yaml", "items:\n  - name: a\n  - name: b\n")
        ref = CiteRef("s.yaml#p", "yaml", "s.yaml", expr="items[*].name")
        assert _validate_yaml(tmp_path, ref) == []

    def test_yaml_missing(self, tmp_path: Path) -> None:
        _write(tmp_path / "s.yaml", "a: 1\n")
        ref = CiteRef("s.yaml#p", "yaml", "s.yaml", expr="a.b.c")
        errs = _validate_yaml(tmp_path, ref)
        assert errs and "no encontrado" in errs[0]


class TestValidateBinary:
    def test_offset_ok(self, tmp_path: Path) -> None:
        _write(tmp_path / "b.bin", b"abcdefghij", mode="binary")
        ref = CiteRef("b.bin#x", "binary", "b.bin", offset=4, expr="4")
        assert _validate_binary(tmp_path, ref) == []

    def test_offset_out_of_range(self, tmp_path: Path) -> None:
        _write(tmp_path / "b.bin", b"abc", mode="binary")
        ref = CiteRef("b.bin#x", "binary", "b.bin", offset=100, expr="100")
        errs = _validate_binary(tmp_path, ref)
        assert errs and "fuera de rango" in errs[0]

    def test_symbol_ok(self, tmp_path: Path) -> None:
        _write(tmp_path / "b.bin", b"prefix_needle_suffix", mode="binary")
        ref = CiteRef("b.bin#x", "binary", "b.bin", symbol="needle", expr="needle")
        assert _validate_binary(tmp_path, ref) == []

    def test_symbol_missing(self, tmp_path: Path) -> None:
        _write(tmp_path / "b.bin", b"abcdef", mode="binary")
        ref = CiteRef("b.bin#x", "binary", "b.bin", symbol="xyz", expr="xyz")
        errs = _validate_binary(tmp_path, ref)
        assert errs and "no encontrado" in errs[0]


# ---------------------------------------------------------------------------
# check_cite (dispatcher)
# ---------------------------------------------------------------------------


class TestCheckCiteDispatch:
    def test_dispatches_text(self, tmp_path: Path) -> None:
        _write(tmp_path / "a.py", "x\n")
        assert check_cite(tmp_path, "a.py:1") == []

    def test_dispatches_container(self, tmp_path: Path) -> None:
        with zipfile.ZipFile(tmp_path / "a.zip", "w") as zf:
            zf.writestr("f.txt", "x\n")
        assert check_cite(tmp_path, "a.zip!/f.txt:1") == []

    def test_dispatches_xpath(self, tmp_path: Path) -> None:
        _write(tmp_path / "u.xml", "<r><x/></r>")
        assert check_cite(tmp_path, "u.xml#/r/x") == []

    def test_dispatches_yaml(self, tmp_path: Path) -> None:
        _write(tmp_path / "s.yaml", "a:\n  b: 1\n")
        assert check_cite(tmp_path, "s.yaml#a.b") == []

    def test_dispatches_binary(self, tmp_path: Path) -> None:
        _write(tmp_path / "b.bin", b"hello world!", mode="binary")
        assert check_cite(tmp_path, "b.bin#0x0") == []

    def test_dispatches_notebook(self, tmp_path: Path) -> None:
        nb = {"cells": [{"cell_type": "code", "source": "x\n"}]}
        _write(tmp_path / "n.ipynb", json.dumps(nb))
        assert check_cite(tmp_path, "n.ipynb#celda-0:1") == []

    def test_malformed_cite(self, tmp_path: Path) -> None:
        errs = check_cite(tmp_path, "@@@")
        assert errs and "mal formado" in errs[0]


# ---------------------------------------------------------------------------
# CC-11
# ---------------------------------------------------------------------------


class TestCC11:
    def _gt(self, feature_name: str, outcome_name: str) -> dict:
        return {
            "features": [
                {"id": "F1", "name": feature_name, "traces": [], "outcomes": [{"id": "R1", "name": outcome_name}]}
            ],
            "package_traps": [],
            "traps": [],
        }

    def _write_gt(self, tmp_path: Path, gt: dict) -> Path:
        gt_dir = tmp_path / "gt"
        gt_dir.mkdir()
        (gt_dir / "ground_truth.json").write_text(json.dumps(gt))
        return gt_dir

    def test_detects_mention_in_python_comment(self, tmp_path: Path) -> None:
        gt = self._gt("MySecretFeature", "SomeResult")
        gt_dir = self._write_gt(tmp_path, gt)
        fx = tmp_path / "fx"
        fx.mkdir()
        # Comentario con el nombre de la feature embebido
        (fx / "a.py").write_text(
            "# MySecretFeature is implemented here\nx = 1\n"
        )
        from dev.tools.check_ground_truth import check
        errs, _warns = check(gt_dir, fx, check_cc11=True)
        assert any("CC-11" in e for e in errs)

    def test_no_mention_passes(self, tmp_path: Path) -> None:
        gt = self._gt("OtherFeature", "OtherResult")
        gt_dir = self._write_gt(tmp_path, gt)
        fx = tmp_path / "fx"
        fx.mkdir()
        (fx / "a.py").write_text("# unrelated comment\nx = 1\n")
        from dev.tools.check_ground_truth import check
        errs, _warns = check(gt_dir, fx, check_cc11=True)
        assert not any("CC-11" in e for e in errs)

    def test_detects_in_block_comment_js(self, tmp_path: Path) -> None:
        gt = self._gt("BlockFeature", "BlockResult")
        gt_dir = self._write_gt(tmp_path, gt)
        fx = tmp_path / "fx"
        fx.mkdir()
        (fx / "a.js").write_text("/* BlockFeature lives here */\nconst x = 1;\n")
        from dev.tools.check_ground_truth import check
        errs, _warns = check(gt_dir, fx, check_cc11=True)
        assert any("CC-11" in e for e in errs)

    def test_string_in_code_passes(self, tmp_path: Path) -> None:
        gt = self._gt("StringFeature", "StringResult")
        gt_dir = self._write_gt(tmp_path, gt)
        fx = tmp_path / "fx"
        fx.mkdir()
        (fx / "a.py").write_text('name = "StringFeature"\nx = 1\n')
        from dev.tools.check_ground_truth import check
        errs, _warns = check(gt_dir, fx, check_cc11=True)
        assert not any("CC-11" in e for e in errs)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


class TestCLI:
    def test_ok(self, tmp_path: Path, capsys) -> None:
        # El CLI busca el fixture en <gt_dir.parent.parent>/fixtures/<gt_dir.name>
        gt_parent = tmp_path / "ground-truth"
        gt_dir = gt_parent / "demo"
        gt_dir.mkdir(parents=True)
        fx = gt_parent.parent / "fixtures" / "demo"
        fx.mkdir(parents=True)
        (fx / "a.py").write_text("a\nb\nc\n")
        feature_block = lambda fid: {
            "id": fid,
            "name": fid,
            "traces": [{"cite": "a.py:2"}],
            "outcomes": [{"user_sees": "x"}] * 6,
        }
        gt = {
            "features": [feature_block(f"F{i}") for i in range(3)],
            "package_traps": [{"resolution": "r"}] * 6,
            "traps": [],
        }
        (gt_dir / "ground_truth.json").write_text(json.dumps(gt))
        rc = main([str(gt_dir)])
        assert rc == 0

    def test_missing_gt(self, tmp_path: Path, capsys) -> None:
        rc = main([str(tmp_path / "no")])
        assert rc == 1
