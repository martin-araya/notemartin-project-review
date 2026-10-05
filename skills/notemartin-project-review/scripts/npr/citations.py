"""Gramática de citas de la skill `notemartin-project-review`.

Soporta 5 patrones:
- LINE         : [@<path>:<linea>]
- RANGE        : [@<path>:<ini>-<fin>]
- RANGE_SYMBOL : [@<path>:<ini>-<fin>#<simbolo>]
- GIT          : [@git:<sha>]
- DYN          : [@dyn:<id>]

Las rutas son relativas a la raíz del repo, sin `./` inicial, con `/` como
separador. Los SHA se normalizan a minúsculas. Un rango con fin < ini se
considera inválido.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional

PATH_RE = r"[A-Za-z0-9_./-]+"
LINE_RE = r"\d+"
RANGE_RE = rf"{LINE_RE}-{LINE_RE}"
SYMBOL_RE = r"[A-Za-z_][A-Za-z0-9_.]*"
SHA_RE = r"[0-9a-fA-F]{7,40}"
DYN_ID_RE = r"[A-Za-z0-9_-]+"

CITATION_KIND = ("RANGE_SYMBOL", "RANGE", "LINE", "GIT", "DYN")

PATTERNS = {
    "RANGE_SYMBOL": re.compile(rf"\[@({PATH_RE}):({RANGE_RE})#({SYMBOL_RE})\]"),
    "RANGE": re.compile(rf"\[@({PATH_RE}):({RANGE_RE})\]"),
    "LINE": re.compile(rf"\[@({PATH_RE}):({LINE_RE})\]"),
    "GIT": re.compile(rf"\[@git:({SHA_RE})\]"),
    "DYN": re.compile(rf"\[@dyn:({DYN_ID_RE})\]"),
}


@dataclass(frozen=True)
class Citation:
    kind: str
    raw: str
    path: Optional[str] = None
    start: Optional[int] = None
    end: Optional[int] = None
    symbol: Optional[str] = None
    sha: Optional[str] = None
    dyn_id: Optional[str] = None

    def __post_init__(self):
        if self.kind not in CITATION_KIND:
            raise ValueError(f"kind invalido: {self.kind!r}")
        if self.path is not None:
            normalized = self.path
            while normalized.startswith("./"):
                normalized = normalized[2:]
            if normalized != self.path:
                object.__setattr__(self, "path", normalized)
            if normalized.startswith("/"):
                raise ValueError(f"path absoluto no permitido: {self.path!r}")
        if self.sha is not None:
            lower = self.sha.lower()
            if lower != self.sha:
                object.__setattr__(self, "sha", lower)
        if self.start is not None and self.end is not None:
            if self.end < self.start:
                raise ValueError(f"rango invalido {self.start}-{self.end}")


def _build_citation(kind: str, match: re.Match, raw: str) -> Citation:
    groups = match.groups()
    if kind == "RANGE_SYMBOL":
        path, rng, symbol = groups
        ini, fin = rng.split("-", 1)
        return Citation(
            kind=kind, raw=raw,
            path=path, start=int(ini), end=int(fin), symbol=symbol,
        )
    if kind == "RANGE":
        path, rng = groups
        ini, fin = rng.split("-", 1)
        return Citation(
            kind=kind, raw=raw,
            path=path, start=int(ini), end=int(fin),
        )
    if kind == "LINE":
        path, line = groups
        return Citation(
            kind=kind, raw=raw,
            path=path, start=int(line), end=int(line),
        )
    if kind == "GIT":
        (sha,) = groups
        return Citation(kind=kind, raw=raw, sha=sha)
    if kind == "DYN":
        (dyn_id,) = groups
        return Citation(kind=kind, raw=raw, dyn_id=dyn_id)
    raise ValueError(f"patron sin constructor: {kind}")


def parse_citations(text: str) -> list:
    """Devuelve todas las citas válidas en orden de aparición."""
    citations = []
    for m in re.finditer(r"\[@[^\]\n]*\]", text):
        candidate = m.group(0)
        for kind, pat in PATTERNS.items():
            sub = pat.fullmatch(candidate)
            if sub is None:
                continue
            try:
                citations.append(_build_citation(kind, sub, candidate))
            except ValueError:
                pass
            break
    return citations