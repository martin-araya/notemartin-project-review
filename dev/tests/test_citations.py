"""Tests para `scripts/npr/citations.py` (F03)."""
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent.parent
SKILL = ROOT / "skills" / "notemartin-project-review"
sys.path.insert(0, str(SKILL / "scripts"))

from npr.citations import parse_citations, PATTERNS, Citation, CITATION_KIND  # noqa: E402


# ---- 01..05: patron LINE -----------------------------------------------
def test_01_line_single_digit():
    [c] = parse_citations("[@src/cli.py:1]")
    assert c.kind == "LINE"
    assert c.path == "src/cli.py"
    assert c.start == 1 and c.end == 1


def test_line_multi_digit():
    [c] = parse_citations("[@src/cli.py:12345]")
    assert c.kind == "LINE"
    assert c.start == 12345


def test_line_normalizes_leading_dot_slash():
    [c] = parse_citations("[@./src/cli.py:1]")
    assert c.path == "src/cli.py"


# ---- 06..10: patron RANGE ----------------------------------------------
def test_06_range_basic():
    [c] = parse_citations("[@src/cli.py:10-25]")
    assert c.kind == "RANGE"
    assert c.path == "src/cli.py"
    assert c.start == 10 and c.end == 25


def test_range_single_line_same_ini_fin():
    [c] = parse_citations("[@a/b/c/d.py:1-1]")
    assert c.kind == "RANGE"
    assert c.start == 1 and c.end == 1


def test_range_md_file():
    [c] = parse_citations("[@docs/guide.md:1-100]")
    assert c.kind == "RANGE"
    assert c.path == "docs/guide.md"


def test_range_inverted_rejected():
    assert parse_citations("[@src/cli.py:25-10]") == []


# ---- 11..15: patron RANGE_SYMBOL ---------------------------------------
def test_11_range_symbol_basic():
    [c] = parse_citations("[@src/cli.py:10-25#main]")
    assert c.kind == "RANGE_SYMBOL"
    assert c.path == "src/cli.py"
    assert c.start == 10 and c.end == 25
    assert c.symbol == "main"


def test_range_symbol_dotted():
    [c] = parse_citations("[@src/foo.py:10-25#Foo.bar]")
    assert c.symbol == "Foo.bar"


def test_range_symbol_underscore_start():
    [c] = parse_citations("[@src/foo.py:10-25#_priv]")
    assert c.symbol == "_priv"


def test_range_symbol_empty_rejected():
    assert parse_citations("[@src/cli.py:1-2#]") == []


def test_range_symbol_digit_start_rejected():
    assert parse_citations("[@src/cli.py:1-2#1foo]") == []


def test_range_symbol_with_space_rejected():
    assert parse_citations("[@src/cli.py:1-2#sym bólico]") == []


# ---- 16..18: patron GIT ------------------------------------------------
def test_16_git_short_sha():
    [c] = parse_citations("[@git:abc1234]")
    assert c.kind == "GIT"
    assert c.sha == "abc1234"


def test_git_full_sha():
    sha = "0123456789abcdef0123456789abcdef01234567"
    [c] = parse_citations(f"[@git:{sha}]")
    assert c.kind == "GIT"
    assert c.sha == sha


def test_git_normalizes_uppercase():
    [c] = parse_citations("[@git:ABC1234DEF]")
    assert c.sha == "abc1234def"


def test_git_non_hex_rejected():
    assert parse_citations("[@git:XYZ1234]") == []


# ---- 19..20: patron DYN ------------------------------------------------
def test_19_dyn_with_dash():
    [c] = parse_citations("[@dyn:trace-001]")
    assert c.kind == "DYN"
    assert c.dyn_id == "trace-001"


def test_dyn_empty_rejected():
    assert parse_citations("[@dyn:]") == []


# ---- 21..24: invalidos adicionales -------------------------------------
def test_21_missing_at_sign():
    assert parse_citations("[src/cli.py:10]") == []


def test_range_incomplete_rejected():
    assert parse_citations("[@src/cli.py:10-]") == []


def test_range_no_dash_rejected():
    assert parse_citations("[@src/cli.py:10 25]") == []


def test_line_non_numeric_rejected():
    assert parse_citations("[@src/cli.py:abc]") == []


# ---- 25..26: combinacion y orden ---------------------------------------
def test_25_adjacent_citations_in_order():
    out = parse_citations("[@a:1-5][@b:2-3]")
    assert len(out) == 2
    assert out[0].path == "a"
    assert out[1].path == "b"


def test_multiple_citations_with_surrounding_text():
    text = "ver [@src/foo.ts:10] y luego [@src/bar.ts:20-30#X] y por último [@git:abc1234]"
    out = parse_citations(text)
    assert len(out) == 3
    assert [c.kind for c in out] == ["LINE", "RANGE_SYMBOL", "GIT"]


# ---- 27: estructura del módulo -----------------------------------------
def test_27_has_5_patterns():
    assert set(PATTERNS.keys()) == set(CITATION_KIND)
    assert len(PATTERNS) == 5


# ---- 28: normalización ------------------------------------------------
def test_28_path_without_leading_dot_slash():
    [c] = parse_citations("[@./src/cli.py:1]")
    assert c.path == "src/cli.py"


# ---- 29..30: prueba del propio .md (criterio de aceptación 1) ----------
PRINCIPIOS = SKILL / "references" / "00-principios.md"


def _extract_fenced(text: str, info_string: str) -> list:
    """Extrae lineas de un fence cuyo info-string sea exactamente `info_string`."""
    lines = text.splitlines()
    out, inside, current = [], False, []
    target = info_string.lower()
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```"):
            if inside:
                out.extend(current)
                inside, current = False, []
                continue
            info = stripped.strip("`").strip().lower()
            if info == target:
                inside, current = True, []
            continue
        if inside:
            current.append(line)
    return [l for l in out if l.strip()]


def test_29_doc_valid_examples_all_parse():
    assert PRINCIPIOS.is_file(), f"no existe {PRINCIPIOS}"
    text = PRINCIPIOS.read_text(encoding="utf-8")
    valid = _extract_fenced(text, "valido")
    invalids = _extract_fenced(text, "invalido")
    assert len(valid) >= 10, f"solo {len(valid)} ejemplos validos en el doc"
    assert len(invalids) >= 10, f"solo {len(invalids)} ejemplos invalidos en el doc"

    valid_clean = [l.split("//", 1)[0].strip() for l in valid]
    invalids_clean = [l.split("//", 1)[0].strip() for l in invalids]

    parsed_valid = [c for line in valid_clean for c in parse_citations(line)]
    assert len(parsed_valid) == len(valid_clean), (
        f"ejemplos validos que no parsean: "
        f"{[l for l in valid_clean if not parse_citations(l)]}"
    )

    for line in invalids_clean:
        assert parse_citations(line) == [], f"invalido aceptado: {line!r}"


def test_30_doc_contains_eight_laws_with_cumplida_por():
    text = PRINCIPIOS.read_text(encoding="utf-8")
    for i in range(1, 9):
        assert f"Ley {i}" in text, f"falta Ley {i}"
        assert "Cumplida por" in text, "falta el bloque 'Cumplida por:' en alguna ley"