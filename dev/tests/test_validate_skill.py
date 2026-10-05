"""Tests para `dev/tools/validate_skill.py` (F01).

Casos (hex) y origen:
- 01-valid  : el caso feliz pasa todas las reglas.
- 02-name-uppercase : name con mayusculas falla.
- 03-name-too-long  : name de 65 chars falla por longitud.
- 04-name-mismatch  : name != nombre de carpeta falla.
- 05-desc-too-long  : description > 1024 chars falla.
- 06-desc-empty     : description vacia falla.
- 07-body-overflow  : cuerpo > 5000 tokens falla.
- 08-link-broken-skill   : enlace roto en SKILL.md.
- 09-link-broken-references : enlace roto en references/.
- 10-abs-users    : ruta /Users/ detectada.
- 11-abs-home     : ruta /home/ detectada.
- 12-abs-windows  : ruta C:\\Users\\ detectada.
- 13-secret-aws   : AKIA... detectada.
- 14-secret-ghp   : ghp_... detectada.
- 15-secret-glpat : glpat-... detectada.
- 16-secret-openai: sk-... detectada.
- 17-secret-ant   : sk-ant-... detectada.
- 18-url-link-ignored   : http(s):// no se valida como archivo.
- 19-anchor-link-ignored: #ancla no se valida.
- 20-main-code-2-on-failure.
- 21-main-code-0-on-success.
- 22-json-output-shape.
- 23-real-description-triggers : la SKILL.md real tiene >= 6 disparadores ES y >= 4 EN.
- 24-real-description-length    : la description real <= 1024 chars.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent.parent
VALIDATOR = ROOT / "dev" / "tools" / "validate_skill.py"
REAL_SKILL = ROOT / "skills" / "notemartin-project-review"


def _make_skill(tmp_path, *, name="my-skill", dir_name=None, body="# hola\n\ntexto.",
                fm_extras="", extra_files=None, fm_description=None):
    """Crea una carpeta de skill sintetica con SKILL.md y devuelve su Path."""
    folder = tmp_path / (dir_name or name)
    folder.mkdir()
    desc = fm_description or "Skill de prueba para tests de validacion."
    fm = f"""---
name: {name}
description: >-
  {desc}
version: 0.1.0
license: MIT
metadata:
  hermes:
    tags: [test]
{fm_extras}---
"""
    (folder / "SKILL.md").write_text(fm + body, encoding="utf-8")
    (folder / "scripts").mkdir()
    (folder / "scripts" / "npr.py").write_text("#!/usr/bin/env python3\n", encoding="utf-8")
    if extra_files:
        for relpath, content in extra_files.items():
            target = folder / relpath
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
    return folder


def _run(skill_dir, *args):
    """Ejecuta el validador como subproceso y devuelve (returncode, stdout, stderr)."""
    proc = subprocess.run(
        [sys.executable, str(VALIDATOR), str(skill_dir), *args],
        capture_output=True, text=True,
    )
    return proc.returncode, proc.stdout, proc.stderr


def _run_inproc(skill_dir, *args):
    """Ejecuta el validador en proceso y devuelve (returncode, stdout, stderr)."""
    import io
    from contextlib import redirect_stdout, redirect_stderr

    sys.path.insert(0, str(VALIDATOR.parent))
    import validate_skill

    saved_argv = sys.argv
    sys.argv = [str(VALIDATOR), str(skill_dir), *args]
    buf_out, buf_err = io.StringIO(), io.StringIO()
    rc = 1
    try:
        with redirect_stdout(buf_out), redirect_stderr(buf_err):
            try:
                rc = validate_skill.main()
            except SystemExit as e:
                rc = e.code if isinstance(e.code, int) else 1
    finally:
        sys.argv = saved_argv
        if str(VALIDATOR.parent) in sys.path:
            sys.path.remove(str(VALIDATOR.parent))
    return rc, buf_out.getvalue(), buf_err.getvalue()


# ---- 01 -----------------------------------------------------------------
def test_01_valid_skill_passes(tmp_path):
    skill = _make_skill(tmp_path)
    rc, out, err = _run(skill)
    assert rc == 0, f"rc={rc} out={out!r} err={err!r}"
    assert "OK" in out


# ---- 02 -----------------------------------------------------------------
def test_02_name_with_uppercase_fails(tmp_path):
    skill = _make_skill(tmp_path, name="My-Skill", dir_name="My-Skill")
    rc, out, err = _run(skill)
    assert rc == 2
    assert "name" in err.lower()
    assert "no cumple" in err.lower()


# ---- 03 -----------------------------------------------------------------
def test_03_name_too_long_fails(tmp_path):
    long_name = "a" + "b" * 64
    skill = _make_skill(tmp_path, name=long_name, dir_name=long_name)
    rc, out, err = _run(skill)
    assert rc == 2
    assert "excede 64" in err


# ---- 04 -----------------------------------------------------------------
def test_04_name_must_match_directory(tmp_path):
    skill = _make_skill(tmp_path, name="correct-name", dir_name="other-name")
    rc, out, err = _run(skill)
    assert rc == 2
    assert "no coincide con la carpeta" in err


# ---- 05 -----------------------------------------------------------------
def test_05_description_too_long_fails(tmp_path):
    long_desc = "x" * 1025
    skill = _make_skill(tmp_path, fm_description=long_desc)
    rc, out, err = _run(skill)
    assert rc == 2
    assert "description" in err.lower()
    assert "1024" in err


# ---- 06 -----------------------------------------------------------------
def test_06_description_empty_fails(tmp_path):
    skill_text = """---
name: test-skill
description:
version: 0.1.0
license: MIT
---
# hola
"""
    folder = tmp_path / "test-skill"
    folder.mkdir()
    (folder / "SKILL.md").write_text(skill_text, encoding="utf-8")
    rc, out, err = _run(folder)
    assert rc == 2
    assert "description" in err.lower()


# ---- 07 -----------------------------------------------------------------
def test_07_body_over_5000_tokens_fails(tmp_path):
    big_body = "x" * 20005
    skill = _make_skill(tmp_path, body=big_body)
    rc, out, err = _run(skill)
    assert rc == 2
    assert "tokens" in err.lower()


# ---- 08 -----------------------------------------------------------------
def test_08_broken_relative_link_in_skill_md(tmp_path):
    skill = _make_skill(tmp_path, body="Ver [doc](references/missing.md) por favor.")
    rc, out, err = _run(skill)
    assert rc == 2
    assert "enlace roto" in err
    assert "missing.md" in err


# ---- 09 -----------------------------------------------------------------
def test_09_broken_relative_link_in_references(tmp_path):
    skill = _make_skill(
        tmp_path,
        extra_files={"references/00.md": "ver [otro](references/01.md)\n"},
    )
    rc, out, err = _run(skill)
    assert rc == 2
    assert "enlace roto" in err


# ---- 10 -----------------------------------------------------------------
def test_10_absolute_user_path_detected(tmp_path):
    skill = _make_skill(tmp_path, body="Mira /Users/jane/foo por favor.")
    rc, out, err = _run(skill)
    assert rc == 2
    assert "ruta absoluta" in err
    assert "/Users/" in err


# ---- 11 -----------------------------------------------------------------
def test_11_absolute_home_path_detected(tmp_path):
    skill = _make_skill(tmp_path, body="ver /home/martin/x")
    rc, out, err = _run(skill)
    assert rc == 2
    assert "ruta absoluta" in err


# ---- 12 -----------------------------------------------------------------
def test_12_absolute_windows_path_detected(tmp_path):
    skill = _make_skill(tmp_path, body="ver C:\\Users\\jane\\foo")
    rc, out, err = _run(skill)
    assert rc == 2
    assert "ruta absoluta" in err


# ---- 13 -----------------------------------------------------------------
def test_13_aws_secret_detected(tmp_path):
    skill = _make_skill(tmp_path, body="key: AKIAIOSFODNN7EXAMPLE")
    rc, out, err = _run(skill)
    assert rc == 2
    assert "secreto" in err.lower()
    assert "aws_access_key" in err


# ---- 14 -----------------------------------------------------------------
def test_14_github_pat_detected(tmp_path):
    token = "ghp_" + "a" * 36
    skill = _make_skill(tmp_path, body=f"token: {token}")
    rc, out, err = _run(skill)
    assert rc == 2
    assert "github_pat" in err


# ---- 15 -----------------------------------------------------------------
def test_15_gitlab_token_detected(tmp_path):
    token = "glpat-" + "a" * 20
    skill = _make_skill(tmp_path, body=f"token: {token}")
    rc, out, err = _run(skill)
    assert rc == 2
    assert "gitlab_pat" in err


# ---- 16 -----------------------------------------------------------------
def test_16_openai_key_detected(tmp_path):
    token = "sk-" + "a" * 20
    skill = _make_skill(tmp_path, body=f"token: {token}")
    rc, out, err = _run(skill)
    assert rc == 2
    assert "openai_key" in err


# ---- 17 -----------------------------------------------------------------
def test_17_anthropic_key_detected(tmp_path):
    token = "sk-ant-" + "a" * 20
    skill = _make_skill(tmp_path, body=f"token: {token}")
    rc, out, err = _run(skill)
    assert rc == 2
    assert "anthropic_key" in err


# ---- 18 -----------------------------------------------------------------
def test_18_external_url_link_ignored(tmp_path):
    skill = _make_skill(tmp_path, body="Ver [docs](https://example.com).")
    rc, out, err = _run(skill)
    assert rc == 0, f"rc={rc} err={err!r}"


# ---- 19 -----------------------------------------------------------------
def test_19_anchor_link_ignored(tmp_path):
    skill = _make_skill(tmp_path, body="Ver [seccion](#arriba).")
    rc, out, err = _run(skill)
    assert rc == 0, f"rc={rc} err={err!r}"


# ---- 20 -----------------------------------------------------------------
def test_20_main_returns_2_on_failure(tmp_path):
    skill = _make_skill(tmp_path, name="My-Skill")
    rc, out, err = _run_inproc(skill)
    assert rc == 2


# ---- 21 -----------------------------------------------------------------
def test_21_main_returns_0_on_success(tmp_path):
    skill = _make_skill(tmp_path)
    rc, out, err = _run_inproc(skill)
    assert rc == 0


# ---- 22 -----------------------------------------------------------------
def test_22_json_output_shape(tmp_path):
    skill = _make_skill(tmp_path)
    rc, out, err = _run(skill, "--json")
    assert rc == 0
    data = json.loads(out)
    assert "ok" in data and data["ok"] is True
    assert "results" in data and isinstance(data["results"], list)
    rules = {r["rule"] for r in data["results"]}
    assert {"name", "description", "body_tokens", "links", "absolute_paths", "secrets"} <= rules


# ---- 23 -----------------------------------------------------------------
def test_23_real_description_has_enough_triggers():
    text = (REAL_SKILL / "SKILL.md").read_text(encoding="utf-8")
    fm = text.split("---", 2)[1]
    desc_match = re.search(r"description:\s*>-\s*\n((?:  .*\n)+)", fm)
    assert desc_match is not None, "frontmatter.description no encontrado"
    desc = desc_match.group(1).strip().replace("\n  ", " ")

    es_triggers = [
        "analiza este repositorio",
        "cómo funciona esta app",
        "explícame el flujo",
        "qué pasa en cada caso",
        "ingeniería inversa",
        "documenta este repo",
    ]
    en_triggers = [
        "how does this codebase work",
        "reverse engineer",
        "trace this feature",
        "explain this repo",
    ]
    es_hits = sum(1 for t in es_triggers if t.lower() in desc.lower())
    en_hits = sum(1 for t in en_triggers if t.lower() in desc.lower())
    assert es_hits >= 6, f"solo {es_hits}/6 disparadores ES en la description"
    assert en_hits >= 4, f"solo {en_hits}/4 disparadores EN en la description"


# ---- 24 -----------------------------------------------------------------
def test_24_real_description_length_under_1024():
    text = (REAL_SKILL / "SKILL.md").read_text(encoding="utf-8")
    fm = text.split("---", 2)[1]
    desc_match = re.search(r"description:\s*>-\s*\n((?:  .*\n)+)", fm)
    desc = desc_match.group(1).strip().replace("\n  ", " ")
    assert len(desc) <= 1024, f"description tiene {len(desc)} chars (>1024)"