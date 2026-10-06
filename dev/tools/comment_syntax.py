"""Sintaxis de comentarios por extension y nombre de archivo (F06a2 T2).

Carga ``dev/tools/comment_syntax.json`` y expone:

- ``detect(path) -> list[tuple[str, str]]``: pares (apertura, cierre) que delimitan
  comentarios en el archivo. ``[]`` si no se reconoce la extension.
- ``mask_comments(text, syntax) -> str``: devuelve el texto con los comentarios
  reemplazados por espacios, conservando offsets, longitud de lineas y numero de
  saltos de linea (util para CC-11).
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import List, Tuple

Comment = Tuple[str, str]
WARNED_EXTENSIONS: set = set()

_DATA_PATH = Path(__file__).resolve().parent / "comment_syntax.json"
_CACHE: dict | None = None


def _load() -> dict:
    global _CACHE
    if _CACHE is None:
        with _DATA_PATH.open("r", encoding="utf-8") as fh:
            _CACHE = json.load(fh)
    return _CACHE


def detect(path: Path) -> List[Comment]:
    """Devuelve la lista de delimitadores de comentario para el archivo."""
    data = _load()
    name = path.name
    if name in data.get("by_filename", {}):
        return [tuple(c) for c in data["by_filename"][name]]
    ext = path.suffix.lower()
    syntax = data.get("by_extension", {}).get(ext)
    if syntax is None:
        if ext and ext not in WARNED_EXTENSIONS:
            WARNED_EXTENSIONS.add(ext)
        return []
    return [tuple(c) for c in syntax]


def _mask_block(text: str, start: int, end_open: str, end_close: str) -> str:
    """Enmascara con espacios un comentario de bloque que empieza en ``start``
    con el delimitador ``end_open`` y termina con ``end_close``.

    Preserva los saltos de linea internos para no alterar el conteo.
    """
    close = text.find(end_close, start + len(end_open))
    if close < 0:
        end_idx = len(text)
    else:
        end_idx = close + len(end_close)
    span = text[start:end_idx]
    masked_span = "".join("\n" if c == "\n" else " " for c in span)
    return text[:start] + masked_span + text[end_idx:]


def _mask_line(text: str, start: int, end_open: str) -> str:
    """Enmascara con espacios un comentario de linea que empieza en ``start``.

    El delimitador de cierre es un salto de linea, asi que se preserva el ``\\n``
    (necesario para que el conteo de lineas no cambie).
    """
    nl = text.find("\n", start)
    if nl < 0:
        end_idx = len(text)
    else:
        end_idx = nl
    return text[:start] + " " * (end_idx - start) + text[end_idx:]


def mask_comments(text: str, syntax: List[Comment]) -> str:
    """Devuelve ``text`` con todos los comentarios reemplazados por espacios.

    Preserva longitud, posiciones y numero de lineas para que la numeracion
    de los editores no cambie.
    """
    if not syntax:
        return text
    result = text
    changed = True
    iterations = 0
    while changed and iterations < 200:
        changed = False
        iterations += 1
        earliest: Tuple[int, Comment] | None = None
        for end_open, end_close in syntax:
            idx = result.find(end_open)
            if idx < 0:
                continue
            if earliest is None or idx < earliest[0]:
                earliest = (idx, (end_open, end_close))
        if earliest is None:
            break
        start, (open_delim, close_delim) = earliest
        if close_delim == "\n":
            result = _mask_line(result, start, open_delim)
        else:
            result = _mask_block(result, start, open_delim, close_delim)
        changed = True
    return result


def has_comment_syntax(path: Path) -> bool:
    """Atajo: True si la extension del archivo tiene alguna sintaxis de comentario."""
    return bool(detect(path))


# Sintaxis minima cuando la extension no esta en la tabla. Solo cubre el caso
# comun de "linea con #" y devuelve lista vacia si nada matchea.
FALLBACK_LINE_COMMENT = "#"
