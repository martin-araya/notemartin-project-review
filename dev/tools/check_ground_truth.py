#!/usr/bin/env python3
"""Verificador del ground truth de un fixture (F06a2).

Carga ``dev/ground-truth/<fixture>/ground_truth.json`` y verifica que cada referencia
``cite`` (en cualquiera de los formatos soportados) existe en el fixture.

Formatos de referencia soportados (F06a2):

1. ``archivo:línea`` y ``archivo:inicio-fin``
2. ``archivo:línea#símbolo`` (símbolo debe aparecer en la línea/rango)
3. ``archivo:línea:columna`` (útil para bundles minificados)
4. ``contenedor!/ruta/interna:línea`` (ZIP, asar, jar, apk, vsix, whl, egg)
5. ``notebook.ipynb#celda-N:línea`` (Jupyter)
6. ``archivo#xpath`` (XML/HTML: la expresión debe encontrar al menos un nodo)
7. ``archivo#yaml-path`` (YAML/Unity/Helm; path con notación ``a.b.c[0].d``)
8. ``binario#offset`` o ``binario#símbolo`` (offset hex/decimal o símbolo ASCII)

CLI::

    python dev/tools/check_ground_truth.py <gt_dir> [--check-cc11] [--verbose]

Codigos de salida:
- 0 OK
- 1 error de uso
- 2 referencias rotas
- 3 error interno
"""
from __future__ import annotations

import argparse
import json
import re
import struct
import sys
import xml.etree.ElementTree as ET
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Parser de citas
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class CiteRef:
    """Referencia parseada, independiente del formato."""

    raw: str
    kind: str  # "text" | "container" | "notebook" | "xpath" | "yaml" | "binary"
    path: str  # ruta del archivo (o del contenedor)
    line: Optional[int] = None
    end: Optional[int] = None
    column: Optional[int] = None
    symbol: Optional[str] = None
    inner: Optional[str] = None  # ruta dentro de un contenedor
    cell: Optional[int] = None
    expr: Optional[str] = None  # xpath, yaml-path o symbol de binario
    offset: Optional[int] = None  # offset binario


_TEXT_CITE_RE = re.compile(
    r"^(?P<path>[^:\s#!]+):"
    r"(?P<line>\d+)"
    r"(?:-(?P<end>\d+))?"
    r"(?::(?P<col>\d+))?"
    r"(?:#(?P<sym>[A-Za-z_][A-Za-z0-9_.]*))?$"
)

_CONTAINER_CITE_RE = re.compile(
    r"^(?P<archive>[^!\s]+)!/(?P<inner>[^:]+):(?P<line>\d+)$"
)

_NOTEBOOK_CITE_RE = re.compile(
    r"^(?P<path>[^#]+)#celda-(?P<cell>\d+):(?P<line>\d+)$"
)

_XPATH_CITE_RE = re.compile(r"^(?P<path>[^#]+)#(?P<xpath>/.+)$")

_YAML_CITE_RE = re.compile(r"^(?P<path>[^#]+)#(?P<ypath>[^/\s#][^#]*)$")

_BINARY_OFFSET_RE = re.compile(r"^(?P<path>[^#]+)#0x(?P<off>[0-9a-fA-F]+)$")
_BINARY_DEC_RE = re.compile(r"^(?P<path>[^#]+)#(?P<off>\d+)$")
_BINARY_SYM_RE = re.compile(r"^(?P<path>[^#]+)#(?P<sym>[A-Za-z_][A-Za-z0-9_.]{2,})$")

# Extensiones que se consideran binario al desambiguar ``arch#sym``: si la extension
# esta en este set, ``arch#sym`` se trata como binario, no como YAML.
_BINARY_EXTS = frozenset({
    ".bin", ".so", ".dll", ".dylib", ".o", ".obj", ".exe", ".pyc", ".pyo",
    ".class", ".jar", ".war", ".ear", ".dex", ".wasm", ".o", ".a", ".lib",
    ".pdb", ".rel", ".sym", ".elf", ".macho", ".ko",
})


def _looks_like_binary_path(path: str) -> bool:
    lower = path.lower()
    for ext in _BINARY_EXTS:
        if lower.endswith(ext):
            return True
    return False


def parse_cite(cite: str) -> Optional[CiteRef]:
    """Clasifica y parsea una cita. Devuelve None si no matchea ningun formato.

    Orden de deteccion (importante para desambiguar):
    1. ``text`` (incluye el sufijo ``#símbolo``)
    2. ``container`` (presencia de ``!``)
    3. ``notebook`` (``#celda-``)
    4. ``xpath`` (``#/...``)
    5. ``binary`` (``#0xN``, ``#N``, ``#símbolo`` con extension binaria conocida)
    6. ``yaml`` (``#path``)
    """
    if not isinstance(cite, str) or not cite:
        return None

    # Pre-decide: si la extension es claramente binaria, priorizar binary.
    binary_path_match = re.match(r"^([^#]+)#", cite)
    looks_binary = bool(
        binary_path_match and _looks_like_binary_path(binary_path_match.group(1))
    )

    m = _TEXT_CITE_RE.match(cite)
    if m:
        return CiteRef(
            raw=cite,
            kind="text",
            path=m.group("path"),
            line=int(m.group("line")),
            end=int(m.group("end")) if m.group("end") else None,
            column=int(m.group("col")) if m.group("col") else None,
            symbol=m.group("sym"),
        )

    m = _CONTAINER_CITE_RE.match(cite)
    if m:
        return CiteRef(
            raw=cite,
            kind="container",
            path=m.group("archive"),
            line=int(m.group("line")),
            inner=m.group("inner"),
        )

    m = _NOTEBOOK_CITE_RE.match(cite)
    if m:
        return CiteRef(
            raw=cite,
            kind="notebook",
            path=m.group("path"),
            line=int(m.group("line")),
            cell=int(m.group("cell")),
        )

    m = _XPATH_CITE_RE.match(cite)
    if m:
        return CiteRef(
            raw=cite,
            kind="xpath",
            path=m.group("path"),
            expr=m.group("xpath"),
        )

    if looks_binary:
        m = _BINARY_OFFSET_RE.match(cite)
        if m:
            return CiteRef(
                raw=cite, kind="binary",
                path=m.group("path"), offset=int(m.group("off"), 16),
                expr=f"0x{m.group('off')}",
            )
        m = _BINARY_DEC_RE.match(cite)
        if m:
            return CiteRef(
                raw=cite, kind="binary",
                path=m.group("path"), offset=int(m.group("off")),
                expr=m.group("off"),
            )
        m = _BINARY_SYM_RE.match(cite)
        if m:
            return CiteRef(
                raw=cite, kind="binary",
                path=m.group("path"), symbol=m.group("sym"),
                expr=m.group("sym"),
            )

    m = _YAML_CITE_RE.match(cite)
    if m:
        return CiteRef(
            raw=cite,
            kind="yaml",
            path=m.group("path"),
            expr=m.group("ypath"),
        )

    m = _BINARY_OFFSET_RE.match(cite)
    if m:
        return CiteRef(
            raw=cite,
            kind="binary",
            path=m.group("path"),
            offset=int(m.group("off"), 16),
            expr=f"0x{m.group('off')}",
        )

    m = _BINARY_DEC_RE.match(cite)
    if m:
        return CiteRef(
            raw=cite,
            kind="binary",
            path=m.group("path"),
            offset=int(m.group("off")),
            expr=m.group("off"),
        )

    m = _BINARY_SYM_RE.match(cite)
    if m:
        return CiteRef(
            raw=cite,
            kind="binary",
            path=m.group("path"),
            symbol=m.group("sym"),
            expr=m.group("sym"),
        )

    return None


# ---------------------------------------------------------------------------
# YAML minimo (PyYAML si esta; si no, parser propio)
# ---------------------------------------------------------------------------


def _yaml_load(text: str) -> Any:
    try:
        import yaml  # type: ignore

        return yaml.safe_load(text)
    except ImportError:
        return _minimal_yaml_load(text)


def _strip_quotes(s: str) -> str:
    s = s.strip()
    if len(s) >= 2 and s[0] == s[-1] and s[0] in ('"', "'"):
        return s[1:-1]
    return s


def _coerce_scalar(s: str) -> Any:
    s = s.strip()
    if not s:
        return ""
    if s.startswith("[") and s.endswith("]"):
        return _parse_inline_list(s[1:-1])
    if s.lower() in ("true", "yes"):
        return True
    if s.lower() in ("false", "no"):
        return False
    if s.lower() in ("null", "~", ""):
        return None
    try:
        if s.startswith("0x") or s.startswith("0X"):
            return int(s, 16)
        return int(s)
    except ValueError:
        pass
    return _strip_quotes(s)


def _parse_inline_list(body: str) -> list:
    """Parsea una lista inline ``a, b, c`` ignorando comas dentro de comillas."""
    items: list = []
    current = []
    in_str: Optional[str] = None
    for ch in body:
        if in_str:
            current.append(ch)
            if ch == in_str:
                in_str = None
            continue
        if ch in ('"', "'"):
            in_str = ch
            current.append(ch)
            continue
        if ch == ",":
            items.append(_coerce_scalar("".join(current).strip()))
            current = []
            continue
        current.append(ch)
    if current:
        items.append(_coerce_scalar("".join(current).strip()))
    return items


def _parse_minimal_yaml(lines: List[str], idx: int, indent: int) -> Tuple[Any, int]:
    if idx >= len(lines):
        return None, idx
    while idx < len(lines) and not lines[idx].strip():
        idx += 1
    if idx >= len(lines):
        return None, idx
    first = lines[idx]
    first_indent = len(first) - len(first.lstrip(" "))
    if first_indent < indent:
        return None, idx
    stripped = first.lstrip(" ")
    if stripped.startswith("- "):
        return _parse_yaml_list(lines, idx, indent)
    return _parse_yaml_map(lines, idx, indent)


def _parse_yaml_map(lines: List[str], idx: int, indent: int) -> Tuple[dict, int]:
    result: dict = {}
    while idx < len(lines):
        line = lines[idx]
        if not line.strip() or line.lstrip().startswith("#"):
            idx += 1
            continue
        line_indent = len(line) - len(line.lstrip(" "))
        if line_indent < indent:
            break
        if line_indent > indent:
            idx += 1
            continue
        stripped = line.lstrip(" ")
        if stripped.startswith("- "):
            break
        if ":" not in stripped:
            idx += 1
            continue
        key, _, rest = stripped.partition(":")
        key = key.strip()
        rest = rest.strip()
        if not rest:
            child, idx = _parse_minimal_yaml(lines, idx + 1, indent + 2)
            result[key] = child
        else:
            result[key] = _coerce_scalar(rest)
            idx += 1
    return result, idx


def _parse_yaml_list(lines: List[str], idx: int, indent: int) -> Tuple[list, int]:
    result: list = []
    while idx < len(lines):
        line = lines[idx]
        if not line.strip() or line.lstrip().startswith("#"):
            idx += 1
            continue
        line_indent = len(line) - len(line.lstrip(" "))
        if line_indent < indent:
            break
        stripped = line.lstrip(" ")
        if not stripped.startswith("- "):
            break
        item_text = stripped[2:].strip()
        if not item_text:
            child, idx = _parse_minimal_yaml(lines, idx + 1, indent + 2)
            result.append(child)
            continue
        if ":" in item_text and not item_text.startswith('"'):
            k, _, v = item_text.partition(":")
            inline: dict = {k.strip(): _coerce_scalar(v.strip())}
            j = idx + 1
            while j < len(lines):
                cont = lines[j]
                if not cont.strip() or cont.lstrip().startswith("#"):
                    j += 1
                    continue
                ci = len(cont) - len(cont.lstrip(" "))
                if ci <= indent:
                    break
                cs = cont.lstrip(" ")
                if cs.startswith("- "):
                    break
                ck, _, cv = cs.partition(":")
                inline[ck.strip()] = _coerce_scalar(cv.strip())
                j += 1
            result.append(inline)
            idx = j
        else:
            result.append(_coerce_scalar(item_text))
            idx += 1
    return result, idx


def _minimal_yaml_load(text: str) -> Any:
    raw_lines = text.splitlines()
    lines: List[str] = []
    for ln in raw_lines:
        if ln.strip().startswith("#"):
            continue
        if not ln.strip():
            lines.append("")
            continue
        lines.append(ln)
    value, _ = _parse_minimal_yaml(lines, 0, 0)
    return value


# ---------------------------------------------------------------------------
# Resolucion de YAML paths
# ---------------------------------------------------------------------------


_YAML_PATH_TOKEN_RE = re.compile(r"([^.\[\]]+)|\[(\d+)\]|\[\*\]")


def _yaml_path_tokens(expr: str) -> List[Tuple[str, Optional[int], bool]]:
    """Convierte ``a.b.c[0].d[*]`` en lista de (clave, indice, wildcard)."""
    tokens: List[Tuple[str, Optional[int], bool]] = []
    pos = 0
    while pos < len(expr):
        c = expr[pos]
        if c == ".":
            pos += 1
            continue
        if c == "[":
            close = expr.find("]", pos)
            if close < 0:
                raise ValueError(f"yaml path mal formado: {expr!r}")
            inner = expr[pos + 1:close]
            if inner == "*":
                tokens.append(("", None, True))
            else:
                tokens.append(("", int(inner), False))
            pos = close + 1
        else:
            m = re.match(r"[^.\[\]]+", expr[pos:])
            if not m:
                raise ValueError(f"yaml path mal formado: {expr!r}")
            tokens.append((m.group(0), None, False))
            pos += m.end()
    return tokens


def _yaml_walk(
    node: Any,
    tokens: List[Tuple[str, Optional[int], bool]],
) -> List[Any]:
    """Devuelve la lista de nodos alcanzados (soporta wildcards en el nivel dado)."""
    results: List[Any] = [node]
    for key, idx, wildcard in tokens:
        next_results: List[Any] = []
        for cur in results:
            if isinstance(cur, dict):
                if wildcard:
                    for v in cur.values():
                        next_results.append(v)
                elif key in cur:
                    next_results.append(cur[key])
            elif isinstance(cur, list):
                if wildcard:
                    next_results.extend(cur)
                elif idx is not None and 0 <= idx < len(cur):
                    next_results.append(cur[idx])
        results = next_results
    return results


# ---------------------------------------------------------------------------
# Lectura robusta de archivos
# ---------------------------------------------------------------------------


def _read_lines_smart(path: Path) -> Tuple[List[str], str]:
    try:
        from dev.tools.encoding import read_lines  # type: ignore

        return read_lines(path)
    except Exception:
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
            return text.splitlines(), "utf-8"
        except OSError:
            return [], "utf-8"


# ---------------------------------------------------------------------------
# Validadores por formato
# ---------------------------------------------------------------------------


# Directorios de artefactos generados por build (excluidos de validacion estricta:
# se asume que el contenedor los construye). Se emite un warning, no un error.
_ARTIFACT_DIRS = ("artifacts/", "build/", "target/", "dist/")


def _is_generated(path: str) -> bool:
    return any(path.startswith(d) for d in _ARTIFACT_DIRS)


def _validate_text(fixture_root: Path, ref: CiteRef) -> List[str]:
    errs: List[str] = []
    target = fixture_root / ref.path
    if not target.is_file():
        if _is_generated(ref.path):
            return [f"WARN: artefacto no generado (esperado por build): {ref.path}"]
        return [f"archivo inexistente: {ref.path}"]

    lines, _ = _read_lines_smart(target)
    if ref.line is None or ref.line < 1 or ref.line > len(lines):
        return [f"linea {ref.line} fuera de rango en {ref.path} (1..{len(lines)})"]
    end = ref.end or ref.line
    if end > len(lines):
        return [f"linea final {end} fuera de rango en {ref.path}"]
    if ref.column is not None:
        col = ref.column
        if col < 1 or col > len(lines[ref.line - 1]) + 1:
            return [
                f"columna {col} fuera de rango en {ref.path}:{ref.line} "
                f"(1..{len(lines[ref.line - 1]) + 1})"
            ]
    if ref.symbol:
        haystack = "\n".join(lines[ref.line - 1:end])
        if ref.symbol not in haystack:
            errs.append(
                f"simbolo {ref.symbol!r} no encontrado en {ref.path}:{ref.line}-{end}"
            )
    return errs


def _open_container_member(archive: Path, inner: str) -> Optional[bytes]:
    """Lee ``inner`` desde un ZIP/jar/apk/vsix/whl/egg o un asar.

    Para asar, parseo minimo: archivo JSON con claves ``{files, header, ...}`` y
    ``files`` es un dict de ``path -> {size, offset}`` con contenido concatenado
    tras el header JSON.
    """
    suffix = archive.suffix.lower()
    is_zip = suffix in {".zip", ".jar", ".apk", ".vsix", ".whl", ".egg"}
    if is_zip or zipfile.is_zipfile(archive):
        try:
            with zipfile.ZipFile(archive) as zf:
                if inner in zf.namelist():
                    return zf.read(inner)
                for name in zf.namelist():
                    if name.endswith("/" + inner) or name == inner:
                        return zf.read(name)
        except (zipfile.BadZipFile, OSError):
            return None
        return None
    if suffix == ".asar":
        try:
            data = archive.read_bytes()
        except OSError:
            return None
        return _read_asar_member(data, inner)
    return None


def _read_asar_member(data: bytes, inner: str) -> Optional[bytes]:
    """Parser asar minimo. Formato::

        {"files": ...}<\\x00><binarios>

    El header es JSON bien formado seguido de un byte ``\\x00`` y luego los
    contenidos concatenados en el orden declarado por ``files``.
    """
    sep = data.find(b"\x00")
    if sep < 0:
        return None
    try:
        header = json.loads(data[:sep].decode("utf-8", errors="replace"))
    except json.JSONDecodeError:
        return None
    body_start = sep + 1
    files = header.get("files", {})
    if inner not in files:
        return None
    entry = files[inner]
    if "offset" in entry and "size" in entry:
        off = int(entry["offset"])
        size = int(entry["size"])
        return data[body_start + off: body_start + off + size]
    if "files" in entry and isinstance(entry["files"], dict):
        return None
    return None


def _validate_container(fixture_root: Path, ref: CiteRef) -> List[str]:
    archive = fixture_root / ref.path
    if not archive.is_file():
        if _is_generated(ref.path):
            return [f"WARN: artefacto contenedor no generado: {ref.path}"]
        return [f"contenedor inexistente: {ref.path}"]
    if ref.inner is None or ref.line is None:
        return ["contenedor: inner o line faltante"]
    member = _open_container_member(archive, ref.inner)
    if member is None:
        return [f"contenedor {ref.path}: entrada {ref.inner!r} no encontrada"]
    try:
        text = member.decode("utf-8", errors="replace")
    except Exception:
        return [f"contenedor {ref.path}: no se pudo decodificar {ref.inner}"]
    lines = text.splitlines()
    if ref.line < 1 or ref.line > len(lines):
        return [
            f"contenedor {ref.path}:{ref.inner}: linea {ref.line} fuera de rango "
            f"(1..{len(lines)})"
        ]
    return []


def _validate_notebook(fixture_root: Path, ref: CiteRef) -> List[str]:
    target = fixture_root / (ref.path or "")
    if not target.is_file():
        return [f"notebook inexistente: {ref.path}"]
    if ref.cell is None or ref.line is None:
        return ["notebook: cell o line faltante"]
    try:
        data = json.loads(target.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"notebook {ref.path} no parseable: {exc}"]
    cells = data.get("cells", [])
    if ref.cell < 0 or ref.cell >= len(cells):
        return [
            f"notebook {ref.path}: celda {ref.cell} fuera de rango (0..{len(cells) - 1})"
        ]
    src = cells[ref.cell].get("source", "")
    if isinstance(src, list):
        text = "\n".join(src)
    else:
        text = src
    lines = text.splitlines()
    if ref.line < 1 or ref.line > len(lines):
        return [
            f"notebook {ref.path} celda {ref.cell}: linea {ref.line} fuera de rango "
            f"(1..{len(lines)})"
        ]
    return []


def _xpath_walk(elem: ET.Element, expr: str) -> List[ET.Element]:
    """Resolutor minimo de XPath: soporta ``/a/b/c`` y predicados ``[@attr='v']``.

    Suficiente para los archivos XML declarativos (ADF, SOA, Android, XAML, ``.ui``,
    ``AndroidManifest.xml``). No soporta ``//`` ni ejes, solo rutas absolutas.
    """
    expr = expr.strip()
    if expr.startswith("/"):
        expr = expr[1:]
    if not expr:
        return [elem]
    steps = [s for s in expr.split("/") if s]
    # El primer step se compara contra el root actual (no contra sus hijos).
    tag, _, predicate = steps[0].partition("[")
    predicate = predicate.rstrip("]")
    if elem.tag != tag:
        return []
    if predicate and not _match_predicate(elem, predicate):
        return []
    current: List[ET.Element] = [elem]
    for step in steps[1:]:
        tag, _, predicate = step.partition("[")
        predicate = predicate.rstrip("]")
        next_elems: List[ET.Element] = []
        for c in current:
            for child in list(c):
                if child.tag == tag:
                    if predicate:
                        if _match_predicate(child, predicate):
                            next_elems.append(child)
                    else:
                        next_elems.append(child)
        current = next_elems
        if not current:
            return []
    return current


def _match_predicate(elem: ET.Element, predicate: str) -> bool:
    """Soporta ``@attr='value'`` y ``@attr=\"value\"``."""
    m = re.match(r"""@([A-Za-z_][A-Za-z0-9_.\-]*)\s*=\s*['"]([^'"]*)['"]""", predicate.strip())
    if not m:
        return False
    return elem.get(m.group(1)) == m.group(2)


def _validate_xpath(fixture_root: Path, ref: CiteRef) -> List[str]:
    target = fixture_root / (ref.path or "")
    if not target.is_file():
        return [f"xpath: archivo inexistente {ref.path}"]
    if not ref.expr:
        return ["xpath: expresion vacia"]
    try:
        tree = ET.parse(str(target))
    except ET.ParseError as exc:
        return [f"xpath {ref.path}: XML invalido: {exc}"]
    root = tree.getroot()
    matches = _xpath_walk(root, ref.expr)
    if not matches:
        return [f"xpath {ref.path}: expresion {ref.expr!r} no matchea nada"]
    return []


def _validate_yaml(fixture_root: Path, ref: CiteRef) -> List[str]:
    target = fixture_root / (ref.path or "")
    if not target.is_file():
        return [f"yaml: archivo inexistente {ref.path}"]
    if not ref.expr:
        return ["yaml: path vacio"]
    try:
        doc = _yaml_load(target.read_text(encoding="utf-8"))
    except Exception as exc:
        return [f"yaml {ref.path}: no se pudo parsear: {exc}"]
    try:
        tokens = _yaml_path_tokens(ref.expr)
    except ValueError as exc:
        return [f"yaml {ref.path}: {exc}"]
    results = _yaml_walk(doc, tokens)
    if not results:
        return [f"yaml {ref.path}: path {ref.expr!r} no encontrado"]
    return []


def _validate_binary(fixture_root: Path, ref: CiteRef) -> List[str]:
    target = fixture_root / (ref.path or "")
    if not target.is_file():
        if _is_generated(ref.path or ""):
            return [f"WARN: binario no generado: {ref.path}"]
        return [f"binario: archivo inexistente {ref.path}"]
    try:
        data = target.read_bytes()
    except OSError as exc:
        return [f"binario {ref.path}: no se pudo leer: {exc}"]
    if ref.offset is not None:
        if ref.offset < 0 or ref.offset >= len(data):
            return [
                f"binario {ref.path}: offset {ref.expr} fuera de rango (0..{len(data) - 1})"
            ]
        return []
    if ref.symbol:
        needle = ref.symbol.encode("utf-8", errors="replace")
        if len(needle) < 3:
            return [f"binario {ref.path}: simbolo {ref.symbol!r} demasiado corto (>=3)"]
        if needle not in data:
            return [f"binario {ref.path}: simbolo {ref.symbol!r} no encontrado"]
        return []
    return ["binario: ni offset ni simbolo"]


_VALIDATORS: dict[str, Callable[[Path, CiteRef], List[str]]] = {
    "text": _validate_text,
    "container": _validate_container,
    "notebook": _validate_notebook,
    "xpath": _validate_xpath,
    "yaml": _validate_yaml,
    "binary": _validate_binary,
}


def check_cite(fixture_root: Path, cite: str) -> List[str]:
    """Valida una cita en cualquiera de los formatos soportados."""
    ref = parse_cite(cite)
    if ref is None:
        return [f"cite mal formado: {cite!r}"]
    validator = _VALIDATORS.get(ref.kind)
    if validator is None:
        return [f"formato desconocido: {ref.kind}"]
    return validator(fixture_root, ref)


# ---------------------------------------------------------------------------
# Recorrido del ground truth
# ---------------------------------------------------------------------------


def _check_cite(fixture_root: Path, cite: str, where: str) -> List[str]:
    return [f"{where}: {e}" for e in check_cite(fixture_root, cite)]


def check(gt_dir: Path, fixture_root: Path, check_cc11: bool = False) -> Tuple[List[str], List[str]]:
    """Devuelve la tupla (errores, warnings) del ground truth.

    Los warnings se emiten para referencias bajo ``artifacts/``, ``build/``,
    ``target/`` o ``dist/`` que no estan generadas localmente: se asume que el
    contenedor las construye. Los callers deben tratarlos como no fatales.
    """
    errs: List[str] = []
    warns: List[str] = []
    gt_path = gt_dir / "ground_truth.json"
    if not gt_path.is_file():
        return [f"no existe {gt_path}"], []

    try:
        gt = json.loads(gt_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"{gt_path} no es JSON valido: {exc}"], []

    features = gt.get("features", [])
    if len(features) < 3:
        errs.append(f"features: solo {len(features)} (<3 minimo por paquete)")

    for fi, feature in enumerate(features):
        fid = feature.get("id", f"<feature[{fi}]>")
        for si, step in enumerate(feature.get("traces", [])):
            cite = step.get("cite", "")
            bucket = warns if _looks_like_cite_warn(cite) else errs
            for e in check_cite(fixture_root, cite):
                bucket.append(f"{fid}/trace[{si}]: {e}")
        for di, dp in enumerate(feature.get("decision_points", [])):
            f = dp.get("file") or dp.get("artifact") or ""
            ln = dp.get("line", 0)
            if not f:
                errs.append(f"{fid}/dp[{di}]: file/artifact vacio")
                continue
            target = fixture_root / f
            if not target.is_file():
                if _is_generated(f):
                    warns.append(f"{fid}/dp#{di}: artefacto no generado: {f}")
                    continue
                errs.append(f"{fid}/dp[{di}]: archivo inexistente {f}")
                continue
            lines, _ = _read_lines_smart(target)
            if ln < 1 or ln > len(lines):
                errs.append(f"{fid}/dp[{di}]: linea {ln} fuera de rango en {f}")

        for oi, outcome in enumerate(feature.get("outcomes", [])):
            if not outcome.get("user_sees"):
                errs.append(f"{fid}/outcome[{oi}]: user_sees vacio")
        if len(feature.get("outcomes", [])) < 6:
            errs.append(f"{fid}: solo {len(feature.get('outcomes', []))} outcomes (<6)")

    for ti, trap in enumerate(gt.get("traps", [])):
        if not trap.get("resolution"):
            errs.append(f"traps[{ti}]: resolution vacia")
    for ti, trap in enumerate(gt.get("package_traps", [])):
        if not trap.get("resolution"):
            errs.append(f"package_traps[{ti}]: resolution vacia")

    if len(gt.get("package_traps", [])) < 6:
        errs.append(f"package_traps: solo {len(gt.get('package_traps', []))} (<6)")

    if check_cc11:
        for e in _check_cc11(fixture_root, gt):
            errs.append(e)

    return errs, warns


def _looks_like_cite_warn(cite: str) -> bool:
    """Decide si los problemas de validacion de esta cita deben ir a warnings."""
    if not cite:
        return False
    return any(cite.startswith(d) for d in _ARTIFACT_DIRS)


# ---------------------------------------------------------------------------
# CC-11: deteccion de menciones embebidas en comentarios
# ---------------------------------------------------------------------------


def _check_cc11(fixture_root: Path, gt: dict) -> List[str]:
    """Verifica que ninguna cadena 'sensible' del ground truth este embebida en
    comentarios del codigo del fixture.

    Para F06a2, las cadenas 'sensibles' son:
    - el nombre de cada feature
    - el nombre de cada outcome
    - el nombre de cada package_trap

    Si la cadena aparece dentro de un comentario (segun la sintaxis de la extension
    del archivo), CC-11 falla: la explicacion no debe vivir en un comentario.
    """
    try:
        from dev.tools.comment_syntax import mask_comments, detect  # type: ignore
    except ImportError:
        from comment_syntax import mask_comments, detect  # type: ignore

    sensitive: List[str] = []
    for feature in gt.get("features", []):
        name = feature.get("name") or feature.get("id") or ""
        if name:
            sensitive.append(str(name))
        for outcome in feature.get("outcomes", []):
            oname = outcome.get("name") or outcome.get("id") or ""
            if oname:
                sensitive.append(str(oname))
    for trap in gt.get("package_traps", []):
        tn = trap.get("name") or trap.get("id") or ""
        if tn:
            sensitive.append(str(tn))

    errs: List[str] = []
    for path in fixture_root.rglob("*"):
        if not path.is_file():
            continue
        syntax = detect(path)
        if not syntax:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        masked = mask_comments(text, syntax)
        rel = path.relative_to(fixture_root).as_posix()
        for needle in sensitive:
            if not needle or len(needle) < 4:
                continue
            if needle in text and needle not in masked:
                errs.append(
                    f"CC-11: {rel}: {needle!r} aparece dentro de un comentario"
                )
    return errs


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Valida el ground truth de un fixture")
    parser.add_argument("gt_dir", type=Path, help="Directorio con ground_truth.json del fixture")
    parser.add_argument(
        "--check-cc11",
        action="store_true",
        help="Ademas valida CC-11 (sin menciones en comentarios).",
    )
    parser.add_argument("--verbose", action="store_true", help="Imprime resumen por formato.")
    args = parser.parse_args(argv)

    if not args.gt_dir.is_dir():
        print(f"ERROR: {args.gt_dir} no existe", file=sys.stderr)
        return 1

    fixture_name = args.gt_dir.name
    fixture_root = args.gt_dir.parent.parent / "fixtures" / fixture_name
    if not fixture_root.is_dir():
        print(f"ERROR: no se encontro el repo del fixture en {fixture_root}", file=sys.stderr)
        return 1

    errs, warns = check(args.gt_dir, fixture_root, check_cc11=args.check_cc11)
    if warns:
        print(f"WARN ({len(warns)} avisos):", file=sys.stderr)
        for w in warns:
            print(f"  {w}", file=sys.stderr)
    if errs:
        print(f"FALLO ({len(errs)} problemas):", file=sys.stderr)
        for e in errs:
            print(f"  {e}", file=sys.stderr)
        return 2

    if warns:
        print(f"OK ({args.gt_dir.name}) con {len(warns)} avisos")
    else:
        print(f"OK ({args.gt_dir.name})")
    if args.verbose:
        print("Todos los formatos validados correctamente.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
