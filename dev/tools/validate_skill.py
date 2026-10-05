#!/usr/bin/env python3
"""Validador de la skill `notemartin-project-review` (F01).

Verifica:
- name cumple ^[a-z0-9]+(-[a-z0-9]+)*$, <= 64 chars y == nombre de carpeta.
- description: presente y <= 1024 chars.
- frontmatter es YAML valido (PyYAML si esta; parser propio si no).
- cuerpo: estimacion de tokens (chars // 4) <= 5000.
- enlaces relativos en SKILL.md y references/**/*.md apuntan a archivos existentes.
- no hay rutas absolutas del desarrollador (/Users/, C:\\Users\\, /home/).
- no hay secretos (regex de claves API comunes).

Codigos de salida: 0 ok, 2 validacion fallida, 1 error de uso.
"""
import argparse
import json
import re
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Optional


NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MAX_NAME_LEN = 64
MAX_DESCRIPTION_LEN = 1024
MAX_BODY_TOKENS = 5000
TOKEN_DIVISOR = 4

LINK_RE = re.compile(r"\[(?P<text>[^\]]*)\]\((?P<target>[^)\s]+)(?:\s+\"[^\"]*\")?\)")

ABS_PATH_PATTERNS = [
    re.compile(r"(?<![A-Za-z]):?/(?:Users|home)/[^\s)]+"),
    re.compile(r"C:\\Users\\[^\s)]+"),
]

SECRET_PATTERNS = [
    ("aws_access_key", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("github_pat", re.compile(r"gh[pousr]_[A-Za-z0-9]{36,}")),
    ("gitlab_pat", re.compile(r"glpat-[A-Za-z0-9_-]{20,}")),
    ("slack_token", re.compile(r"xox[abprs]-[A-Za-z0-9-]{10,}")),
    ("openai_key", re.compile(r"sk-[A-Za-z0-9]{20,}")),
    ("anthropic_key", re.compile(r"sk-ant-[A-Za-z0-9-]{20,}")),
]


@dataclass
class Result:
    rule: str
    ok: bool
    msg: str = ""
    file: Optional[str] = None
    line: Optional[int] = None


@dataclass
class Report:
    ok: bool
    results: list = field(default_factory=list)

    def add(self, result: Result) -> None:
        self.results.append(result)
        if not result.ok:
            self.ok = False


def _yaml_load(text: str) -> Any:
    """Devuelve un mapa del frontmatter. Usa PyYAML si esta; si no, parser propio."""
    try:
        import yaml  # type: ignore

        return yaml.safe_load(text)
    except ImportError:
        result, _ = _minimal_yaml_load(text)
        return result


def _minimal_yaml_load(text: str) -> Any:
    """Parser YAML minimo para el subset usado en SKILL.md.

    Soporta: mapas anidados (indentacion 2 espacios), escalares string,
    listas con '- ', block scalars '>'-folded. No soporta anchors, tags,
    comillas con escape ni multilinea con '|'.
    """
    lines = [l.rstrip() for l in text.splitlines() if l.strip() and not l.strip().startswith("#")]
    return _parse_block(lines, 0, 0)


def _parse_block(lines: list, start: int, indent: int) -> tuple:
    """Devuelve (value, next_index). value es dict o list segun el primer token."""
    if start >= len(lines):
        return None, start
    first = lines[start]
    first_indent = len(first) - len(first.lstrip())
    if first_indent < indent:
        return None, start
    stripped = first.lstrip()
    if stripped.startswith("- "):
        return _parse_list(lines, start, indent)
    return _parse_map(lines, start, indent)


def _parse_map(lines: list, start: int, indent: int) -> tuple:
    result: dict = {}
    i = start
    while i < len(lines):
        line = lines[i]
        line_indent = len(line) - len(line.lstrip())
        if line_indent < indent:
            break
        if line_indent > indent:
            i += 1
            continue
        stripped = line.lstrip()
        if stripped.startswith("- "):
            break
        if ":" not in stripped:
            i += 1
            continue
        key, _, rest = stripped.partition(":")
        key = key.strip()
        rest = rest.strip()
        if not rest:
            child, i = _parse_block(lines, i + 1, indent + 2)
            result[key] = child
        elif rest in (">-", ">", "|-", "|"):
            child, i = _parse_block_scalar(lines, i + 1, indent + 2)
            result[key] = child
        else:
            result[key] = _strip_quotes(rest)
            i += 1
    return result, i


def _parse_list(lines: list, start: int, indent: int) -> tuple:
    result: list = []
    i = start
    while i < len(lines):
        line = lines[i]
        line_indent = len(line) - len(line.lstrip())
        if line_indent < indent:
            break
        stripped = line.lstrip()
        if not stripped.startswith("- "):
            break
        item = stripped[2:].strip()
        if not item:
            i += 1
            continue
        if ":" in item and not item.startswith('"'):
            inline_map: dict = {}
            k, _, v = item.partition(":")
            inline_map[k.strip()] = _strip_quotes(v.strip())
            i += 1
            while i < len(lines):
                cont = lines[i]
                cont_indent = len(cont) - len(cont.lstrip())
                if cont_indent <= indent:
                    break
                cont_stripped = cont.lstrip()
                if cont_stripped.startswith("- "):
                    break
                ck, _, cv = cont_stripped.partition(":")
                inline_map[ck.strip()] = _strip_quotes(cv.strip())
                i += 1
            result.append(inline_map)
        else:
            result.append(_strip_quotes(item))
            i += 1
    return result, i


def _parse_block_scalar(lines: list, start: int, indent: int) -> tuple:
    chunks: list = []
    i = start
    while i < len(lines):
        line = lines[i]
        line_indent = len(line) - len(line.lstrip())
        if line_indent < indent:
            break
        chunks.append(line.lstrip())
        i += 1
    text = " ".join(chunks)
    return text, i


def _strip_quotes(s: str) -> str:
    if len(s) >= 2 and s[0] == s[-1] and s[0] in ('"', "'"):
        return s[1:-1]
    return s


def load_skill_md(skill_dir: Path) -> tuple:
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        return None, None, "SKILL.md no existe"
    text = skill_md.read_text(encoding="utf-8")
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None, text, "frontmatter no delimitado por '---'"
    fm_text = parts[1].lstrip("\n")
    body = parts[2]
    try:
        fm = _yaml_load(fm_text)
    except Exception as exc:
        return None, body, f"frontmatter no es YAML valido: {exc}"
    if not isinstance(fm, dict):
        return None, body, "frontmatter no es un mapa"
    return fm, body, ""


def check_name(fm: dict, dir_name: str) -> Result:
    name = fm.get("name")
    if not isinstance(name, str) or not name:
        return Result("name", False, 'falta el campo "name"')
    if len(name) > MAX_NAME_LEN:
        return Result("name", False, f'name "{name}" excede {MAX_NAME_LEN} chars')
    if not NAME_RE.match(name):
        return Result("name", False, f'name "{name}" no cumple {NAME_RE.pattern}')
    if name != dir_name:
        return Result("name", False, f'name "{name}" no coincide con la carpeta "{dir_name}"')
    return Result("name", True, f'name="{name}"')


def check_description(fm: dict) -> Result:
    desc = fm.get("description")
    if not isinstance(desc, str) or not desc:
        return Result("description", False, 'falta el campo "description" o esta vacio')
    if len(desc) > MAX_DESCRIPTION_LEN:
        return Result("description", False, f'description {len(desc)} chars excede {MAX_DESCRIPTION_LEN}')
    return Result("description", True, f"description {len(desc)}/{MAX_DESCRIPTION_LEN}")


def check_body_tokens(body: str) -> Result:
    tokens = len(body) // TOKEN_DIVISOR
    if tokens > MAX_BODY_TOKENS:
        return Result("body_tokens", False, f"cuerpo de {tokens} tokens (limite {MAX_BODY_TOKENS})")
    return Result("body_tokens", True, f"cuerpo {tokens}/{MAX_BODY_TOKENS} tokens")


def _md_files(skill_dir: Path) -> list:
    out = []
    skill_md = skill_dir / "SKILL.md"
    if skill_md.is_file():
        out.append(skill_md)
    refs = skill_dir / "references"
    if refs.is_dir():
        out.extend(sorted(refs.rglob("*.md")))
    tmpl = skill_dir / "templates"
    if tmpl.is_dir():
        out.extend(sorted(tmpl.rglob("*.md")))
    return out


def check_relative_links(skill_dir: Path) -> list:
    results = []
    for md in _md_files(skill_dir):
        text = md.read_text(encoding="utf-8")
        for lineno, line in enumerate(text.splitlines(), start=1):
            for m in LINK_RE.finditer(line):
                target = m.group("target")
                if target.startswith(("http://", "https://", "mailto:")):
                    continue
                if target.startswith("#"):
                    continue
                resolved = (md.parent / target).resolve()
                if not resolved.exists():
                    rel = md.relative_to(skill_dir.parent) if skill_dir.parent in md.parents else md
                    results.append(Result(
                        "links", False,
                        f'enlace roto en {rel}:{lineno}: "{target}"',
                        file=str(rel), line=lineno,
                    ))
    if not results:
        results.append(Result("links", True, "0 enlaces revisados"))
    return results


def check_no_absolute_paths(skill_dir: Path) -> list:
    results = []
    for md in _md_files(skill_dir):
        text = md.read_text(encoding="utf-8")
        for lineno, line in enumerate(text.splitlines(), start=1):
            for pat in ABS_PATH_PATTERNS:
                m = pat.search(line)
                if m:
                    rel = md.relative_to(skill_dir.parent) if skill_dir.parent in md.parents else md
                    results.append(Result(
                        "absolute_paths", False,
                        f'ruta absoluta del desarrollador en {rel}:{lineno}: "{m.group(0)}"',
                        file=str(rel), line=lineno,
                    ))
    if not results:
        results.append(Result("absolute_paths", True, "0 ocurrencias"))
    return results


def check_no_secrets(skill_dir: Path) -> list:
    results = []
    for md in _md_files(skill_dir):
        text = md.read_text(encoding="utf-8")
        for lineno, line in enumerate(text.splitlines(), start=1):
            for kind, pat in SECRET_PATTERNS:
                if pat.search(line):
                    rel = md.relative_to(skill_dir.parent) if skill_dir.parent in md.parents else md
                    results.append(Result(
                        "secrets", False,
                        f"posible secreto en {rel}:{lineno}: {kind}",
                        file=str(rel), line=lineno,
                    ))
    if not results:
        results.append(Result("secrets", True, "0 ocurrencias"))
    return results


def run_all(skill_dir: Path) -> Report:
    report = Report(ok=True)
    skill_dir = skill_dir.resolve()
    if not skill_dir.is_dir():
        report.add(Result("path", False, f"{skill_dir} no es una carpeta"))
        return report

    fm, body, err = load_skill_md(skill_dir)
    if err or fm is None:
        report.add(Result("frontmatter", False, err or "frontmatter ausente"))
        return report
    report.add(Result("frontmatter", True, "frontmatter OK"))

    dir_name = skill_dir.name
    report.add(check_name(fm, dir_name))
    report.add(check_description(fm))
    report.add(check_body_tokens(body))

    for r in check_relative_links(skill_dir):
        report.add(r)
    for r in check_no_absolute_paths(skill_dir):
        report.add(r)
    for r in check_no_secrets(skill_dir):
        report.add(r)

    return report


def render_human(report: Report) -> str:
    lines = []
    for r in report.results:
        prefix = "OK" if r.ok else "ERROR"
        where = ""
        if r.file:
            where = f" [{r.file}:{r.line}]" if r.line else f" [{r.file}]"
        lines.append(f"{r.rule}: {prefix}{where} - {r.msg}")
    lines.append("OK" if report.ok else "FALLO")
    return "\n".join(lines)


def render_json(report: Report) -> str:
    return json.dumps({"ok": report.ok, "results": [asdict(r) for r in report.results]}, ensure_ascii=False, indent=2)


def main() -> int:
    parser = argparse.ArgumentParser(description="Valida una instalacion de la skill")
    parser.add_argument("skill_dir", type=Path, help="Carpeta de la skill")
    parser.add_argument("--json", dest="as_json", action="store_true", help="Salida en JSON")
    args = parser.parse_args()

    report = run_all(args.skill_dir)
    out = render_json(report) if args.as_json else render_human(report)
    if report.ok:
        print(out)
        return 0
    print(out, file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())