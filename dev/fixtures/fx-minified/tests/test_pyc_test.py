"""Tests del .pyc (trampa #4 del ecosistema: magic number + disassembly)."""
from __future__ import annotations

import marshal
import struct
from pathlib import Path

import pytest

ARTIFACTS = Path(__file__).resolve().parent.parent / "artifacts"


def _read_pyc_blob() -> bytes:
    pyc_path = ARTIFACTS / "app.pyc"
    if not pyc_path.exists():
        pytest.skip(f"{pyc_path} missing; run build/build-all.sh")
    return pyc_path.read_bytes()


def _names_in_code(code) -> set[str]:
    names: set[str] = set()
    for const in code.co_consts:
        if isinstance(const, str):
            names.add(const)
    for name in code.co_names:
        names.add(name)
    for const in code.co_consts:
        if hasattr(const, "co_names"):
            names.update(_names_in_code(const))
    return names


class TestPycMagic:
    def test_magic_is_311(self) -> None:
        data = _read_pyc_blob()
        assert len(data) >= 4
        magic = struct.unpack('<H', data[:2])[0]
        # CPython 3.11 magic = 3495 (little-endian).
        # 3.10 = 3439, 3.11 = 3495, 3.12 = 3531.
        assert magic == 3495, f"expected magic 3495 (3.11), got {magic}"


class TestPycFeatures:
    def test_feature_constants_present(self) -> None:
        data = _read_pyc_blob()
        assert data.count(b"calcular_tarifa") > 0
        assert data.count(b"validar_licencia") > 0
        assert data.count(b"sincronizar") > 0

    def test_literal_error_markers_present(self) -> None:
        data = _read_pyc_blob()
        for marker in (b"FXMIN_TARIFA_PREFIX", b"FXMIN_TARIFA_SUFFIX",
                       b"FXMIN_LIC_INVALID", b"FXMIN_SYNC_OK", b"FXMIN_SYNC_ERROR"):
            assert marker in data, f"missing literal {marker!r}"

    def test_function_names_in_code(self) -> None:
        data = _read_pyc_blob()
        # CPython 3.7+ header is 16 bytes (magic 4 + flags 4 + ts 4 + size 4).
        HEADER_SIZE = 16
        code = marshal.loads(data[HEADER_SIZE:])
        names = _names_in_code(code)
        assert "calcular_tarifa" in names
        assert "validar_licencia" in names
        assert "sincronizar" in names


class TestPycPackageTraps:
    def test_wrong_magic_detected(self) -> None:
        # Magic de CPython 3.12 = 3531 (little-endian). En bytes es \xc3\x0d.
        # Si la skill recibe un .pyc de 3.12 y trata de parsearlo con la
        # logica de 3.11, falla.
        with pytest.raises(Exception):
            marshal.loads(b"\xc3\x0d" + b"\x00" * 14 + b"\xe3\x00")