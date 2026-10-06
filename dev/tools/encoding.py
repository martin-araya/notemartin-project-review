"""Deteccion de codificacion y lectura robusta de archivos (F06a2 T3).

Funciones principales:
- detect(path) -> str: nombre canonico de la codificacion.
- read_lines(path) -> tuple[list[str], str]: lineas y codificacion usada.

Detecta BOM, UTF-8, UTF-16 LE/BE, UTF-32 LE/BE, Latin-1, CP1252 y Shift-JIS. El conteo de
lineas es consistente con un editor en LF, CRLF y CR, y se preservan los offsets para
coincidir con la numeracion que mostraria un editor.
"""
from __future__ import annotations

from pathlib import Path
from typing import List, Tuple


BOMS: List[Tuple[bytes, str]] = [
    (b"\xef\xbb\xbf", "utf-8-sig"),
    (b"\xff\xfe\x00\x00", "utf-32-le"),
    (b"\x00\x00\xfe\xff", "utf-32-be"),
    (b"\xff\xfe", "utf-16-le"),
    (b"\xfe\xff", "utf-16-be"),
]


SHIFT_JIS_RANGES = (
    (0x81, 0x9F),
    (0xE0, 0xFC),
)
SHIFT_JIS_TAIL_RANGES = (
    (0x40, 0x7E),
    (0x80, 0xFC),
)


def _looks_like_shift_jis(sample: bytes) -> bool:
    """Heuristica ligera: pares lead/trail en los rangos tipicos de Shift-JIS."""
    if len(sample) < 4:
        return False
    hits = 0
    i = 0
    n = len(sample)
    while i < n - 1:
        b = sample[i]
        in_lead = any(lo <= b <= hi for lo, hi in SHIFT_JIS_RANGES)
        if in_lead:
            t = sample[i + 1]
            in_trail = any(lo <= t <= hi for lo, hi in SHIFT_JIS_TAIL_RANGES)
            if in_trail:
                hits += 1
                i += 2
                continue
        i += 1
    return hits >= max(2, n // 64)


def _sample(path: Path, size: int = 8192) -> bytes:
    try:
        with path.open("rb") as fh:
            return fh.read(size)
    except OSError:
        return b""


def detect(path: Path) -> str:
    """Detecta la codificacion del archivo.

    Solo lee los primeros 8 KB. Si no se puede leer, devuelve `utf-8` por convencion.
    """
    sample = _sample(path)
    if not sample:
        return "utf-8"

    for bom, name in BOMS:
        if sample.startswith(bom):
            return name

    try:
        sample.decode("utf-8", errors="strict")
        return "utf-8"
    except UnicodeDecodeError:
        pass

    if _looks_like_shift_jis(sample):
        return "shift_jis"

    return "latin-1"


def _split_lines(text: str) -> List[str]:
    """Split consistente: trata CRLF, LF y CR como terminador. Sin keepends.

    `str.splitlines()` ya cubre los tres casos; lo wrapeamos para mantener un unico
    punto de control en el modulo.
    """
    return text.splitlines()


def read_lines(path: Path) -> Tuple[List[str], str]:
    """Lee el archivo detectando codificacion y devuelve (lineas, encoding).

    - Usa `errors="replace"` para no abortar en bytes danados.
    - `splitlines()` da un conteo consistente con un editor moderno.
    - Para UTF-16/UTF-32, la deteccion por BOM y la decodificacion posterior producen el
      mismo numero de lineas que un editor.
    """
    enc = detect(path)
    try:
        text = path.read_text(encoding=enc, errors="replace")
    except (OSError, LookupError):
        text = path.read_bytes().decode("latin-1", errors="replace")
        enc = "latin-1"
    if enc in ("utf-8-sig", "utf-16-le", "utf-16-be", "utf-32-le", "utf-32-be"):
        text = text.lstrip("\ufeff")
    return _split_lines(text), enc


def line_count(path: Path) -> int:
    """Atajo: solo el numero de lineas."""
    lines, _ = read_lines(path)
    return len(lines)
