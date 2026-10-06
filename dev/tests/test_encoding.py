"""Tests de deteccion de codificacion y lectura robusta (F06a2 T3)."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from dev.tools.encoding import detect, read_lines, line_count


def _write_bytes(tmp_path: Path, name: str, data: bytes) -> Path:
    p = tmp_path / name
    p.write_bytes(data)
    return p


class TestDetectBOM:
    def test_utf8_sig(self, tmp_path: Path) -> None:
        p = _write_bytes(tmp_path, "u.txt", b"\xef\xbb\xbfhello\nworld\n")
        assert detect(p) == "utf-8-sig"

    def test_utf16_le(self, tmp_path: Path) -> None:
        p = _write_bytes(tmp_path, "u.txt", b"\xff\xfeh\x00i\x00\n\x00")
        assert detect(p) == "utf-16-le"

    def test_utf16_be(self, tmp_path: Path) -> None:
        p = _write_bytes(tmp_path, "u.txt", b"\xfe\xff\x00h\x00i\x00\n")
        assert detect(p) == "utf-16-be"

    def test_utf32_le(self, tmp_path: Path) -> None:
        p = _write_bytes(tmp_path, "u.txt", b"\xff\xfe\x00\x00h\x00\x00\x00")
        assert detect(p) == "utf-32-le"

    def test_utf32_be(self, tmp_path: Path) -> None:
        p = _write_bytes(tmp_path, "u.txt", b"\x00\x00\xfe\xff\x00\x00\x00h")
        assert detect(p) == "utf-32-be"


class TestDetectFallback:
    def test_pure_utf8(self, tmp_path: Path) -> None:
        p = _write_bytes(tmp_path, "u.txt", "cafe \u00e1\n".encode("utf-8"))
        assert detect(p) == "utf-8"

    def test_latin1(self, tmp_path: Path) -> None:
        p = _write_bytes(tmp_path, "u.txt", b"cafe \xe1\n")
        assert detect(p) == "latin-1"

    def test_cp1252(self, tmp_path: Path) -> None:
        p = _write_bytes(tmp_path, "u.txt", b"smart \x93quotes\x94\n")
        assert detect(p) == "latin-1"

    def test_shift_jis(self, tmp_path: Path) -> None:
        text = "\u3053\u3093\u306b\u3061\u306f\n\u4e16\u754c\n"
        p = _write_bytes(tmp_path, "u.txt", text.encode("shift_jis"))
        assert detect(p) == "shift_jis"

    def test_empty_file(self, tmp_path: Path) -> None:
        p = _write_bytes(tmp_path, "u.txt", b"")
        assert detect(p) == "utf-8"


class TestReadLines:
    def test_utf8_simple(self, tmp_path: Path) -> None:
        p = tmp_path / "f.txt"
        p.write_text("a\nb\nc\n", encoding="utf-8")
        lines, enc = read_lines(p)
        assert enc == "utf-8"
        assert lines == ["a", "b", "c"]

    def test_utf8_no_trailing_newline(self, tmp_path: Path) -> None:
        p = tmp_path / "f.txt"
        p.write_text("a\nb\nc", encoding="utf-8")
        lines, _ = read_lines(p)
        assert lines == ["a", "b", "c"]

    def test_crlf(self, tmp_path: Path) -> None:
        p = tmp_path / "f.txt"
        p.write_bytes(b"a\r\nb\r\nc\r\n")
        lines, _ = read_lines(p)
        assert lines == ["a", "b", "c"]

    def test_cr_only(self, tmp_path: Path) -> None:
        p = tmp_path / "f.txt"
        p.write_bytes(b"a\rb\rc\r")
        lines, _ = read_lines(p)
        assert lines == ["a", "b", "c"]

    def test_utf16_line_count_matches_editor(self, tmp_path: Path) -> None:
        p = tmp_path / "f.txt"
        p.write_bytes("\u00e1\n\u00e9\n\u00ed\n".encode("utf-16"))
        lines, _ = read_lines(p)
        assert lines == ["\u00e1", "\u00e9", "\u00ed"]
        assert line_count(p) == 3

    def test_latin1_lines(self, tmp_path: Path) -> None:
        p = tmp_path / "f.txt"
        p.write_bytes(b"cafe \xe1\notro\n")
        lines, enc = read_lines(p)
        assert enc == "latin-1"
        assert lines[0] == "cafe \xe1"
        assert lines[1] == "otro"

    def test_bom_utf8_stripped(self, tmp_path: Path) -> None:
        p = tmp_path / "f.txt"
        p.write_bytes(b"\xef\xbb\xbfhola\nmundo\n")
        lines, enc = read_lines(p)
        assert enc == "utf-8-sig"
        assert lines == ["hola", "mundo"]


class TestLineNumbers:
    """Los numeros de linea tienen que coincidir con lo que muestra un editor (1-based)."""

    def test_first_line_is_one(self, tmp_path: Path) -> None:
        p = tmp_path / "f.txt"
        p.write_text("uno\ndos\ntres\n", encoding="utf-8")
        lines, _ = read_lines(p)
        assert lines[0] == "uno"
        assert lines[1] == "dos"
        assert lines[2] == "tres"

    def test_long_lines_preserve_offsets(self, tmp_path: Path) -> None:
        p = tmp_path / "f.txt"
        line = "x" * 5000
        p.write_text(line + "\nsegunda\n", encoding="utf-8")
        lines, _ = read_lines(p)
        assert len(lines[0]) == 5000
        assert lines[1] == "segunda"
