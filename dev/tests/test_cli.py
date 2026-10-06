"""Tests para la CLI `npr` (F05).

Cubre los 7 criterios de aceptacion de F05:
- init idempotente
- init en dir sin git
- git status limpio tras init
- status --json valida contra state
- --help lista subcomandos
- config show con precedencia 4 niveles
- catalogo de errores NPR-Exxx completo
"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent.parent
SKILL = ROOT / "skills" / "notemartin-project-review"
NPR = SKILL / "scripts" / "npr.py"
SKILL_DIR = str(SKILL)

sys.path.insert(0, str(SKILL / "scripts"))


def _run(args: list[str], cwd: Path | None = None, env: dict | None = None) -> subprocess.CompletedProcess:
    cmd = [sys.executable, str(NPR), "--skill-dir", SKILL_DIR, *args]
    full_env = os.environ.copy()
    if env:
        full_env.update(env)
    return subprocess.run(cmd, cwd=cwd or Path.cwd(), capture_output=True, text=True, env=full_env)


@pytest.fixture
def tmp_repo(tmp_path: Path):
    """Crea un repo git temporal con un commit limpio (sin untracked)."""
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.email", "test@test"], cwd=repo, check=False)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=repo, check=False)
    (repo / "tracked.txt").write_text("tracked\n")
    subprocess.run(["git", "add", "tracked.txt"], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "init"], cwd=repo, check=True)
    return repo


@pytest.fixture
def tmp_dir_no_git(tmp_path: Path):
    d = tmp_path / "no-git"
    d.mkdir()
    (d / "file.txt").write_text("hi\n")
    return d


# ---- 01: --help muestra todos los subcomandos ---------------------------
def test_01_help_lists_all_subcommands():
    proc = _run(["--help"])
    assert proc.returncode == 0
    expected = [
        "init", "config", "status", "resume", "recon", "inventory", "classify",
        "stack", "deps", "lockfiles", "workspaces", "imports", "symbols",
        "entrypoints", "surfaces", "env", "llm", "git", "graph", "partition",
        "ledger", "brief", "feature", "surface", "branches", "errors",
        "callgraph", "impact", "question", "claims", "verify", "lint", "gate",
        "openq", "report", "diff", "compare", "dyn", "re",
    ]
    for cmd in expected:
        assert cmd in proc.stdout, f"falta subcomando '{cmd}' en --help"


# ---- 02: init crea el arbol completo ------------------------------------
def test_02_init_creates_workspace_tree(tmp_repo):
    proc = _run(["init", str(tmp_repo)], cwd=tmp_repo)
    assert proc.returncode == 0
    ws = tmp_repo / ".project-review"
    expected_dirs = [
        "state", "recon", "graph", "ledger", "ledger/fragments", "wu",
        "notes", "notes/files", "notes/modules", "notes/flows",
        "notes/features", "notes/surfaces", "notes/cross", "notes/answers",
        "openq", "verify", "reports", "logs", "dyn", "re",
    ]
    for d in expected_dirs:
        assert (ws / d).is_dir(), f"falta subdirectorio {d}"


# ---- 03: init idempotente sin --force -----------------------------------
def test_03_init_is_idempotent_without_force(tmp_repo):
    p1 = _run(["init", str(tmp_repo)], cwd=tmp_repo)
    assert p1.returncode == 0
    p2 = _run(["init", str(tmp_repo)], cwd=tmp_repo)
    assert p2.returncode != 0
    assert "NPR-E105" in p2.stderr


# ---- 04: init con --force sobrescribe ------------------------------------
def test_04_init_with_force_overwrites(tmp_repo):
    p1 = _run(["init", str(tmp_repo)], cwd=tmp_repo)
    assert p1.returncode == 0
    first_sha = (tmp_repo / ".project-review" / "state" / "state.json").read_text()
    p2 = _run(["init", str(tmp_repo), "--force"], cwd=tmp_repo)
    assert p2.returncode == 0
    second_sha = (tmp_repo / ".project-review" / "state" / "state.json").read_text()
    assert first_sha != second_sha or "NPR-E105" not in p2.stderr


# ---- 05: init en directorio sin git --------------------------------------
def test_05_init_in_non_git_repo_warns_and_proceeds(tmp_dir_no_git):
    proc = _run(["init", str(tmp_dir_no_git)], cwd=tmp_dir_no_git)
    assert proc.returncode == 0
    state = json.loads((tmp_dir_no_git / ".project-review" / "state" / "state.json").read_text())
    assert state["commit"] == ""
    assert state["branch"] == "unknown"
    assert "NPR-E116" in proc.stderr


# ---- 06: git status limpio tras init -------------------------------------
def test_06_init_does_not_dirty_repo_git_status(tmp_repo):
    proc = _run(["init", str(tmp_repo)], cwd=tmp_repo)
    assert proc.returncode == 0
    status = subprocess.run(
        ["git", "status", "--porcelain"], cwd=tmp_repo, capture_output=True, text=True, check=True,
    )
    assert status.stdout.strip() == "", f"git status no quedo limpio: {status.stdout!r}"


# ---- 07: exclude sin duplicar la linea -----------------------------------
def test_07_init_does_not_duplicate_exclude_line(tmp_repo):
    _run(["init", str(tmp_repo), "--force"], cwd=tmp_repo)
    _run(["init", str(tmp_repo), "--force"], cwd=tmp_repo)
    excl = (tmp_repo / ".git" / "info" / "exclude").read_text()
    matches = re.findall(r"^\s*\.project-review/?\s*$", excl, re.MULTILINE)
    assert len(matches) == 1, f"exclude duplicado: {excl!r}"


# ---- 08: status --json valida contra state -------------------------------
def test_08_status_json_validates_against_state_schema(tmp_repo):
    _run(["init", str(tmp_repo)], cwd=tmp_repo)
    proc = _run(["status", "--json"], cwd=tmp_repo)
    assert proc.returncode == 0, f"status fallo: {proc.stderr}"
    payload = json.loads(proc.stdout)

    from npr.schema import load_schema, validate
    schema = load_schema("state")
    errors = validate(payload, schema)
    assert errors == [], f"status --json no valida: {errors}"


# ---- 09: status humano devuelve 0 ----------------------------------------
def test_09_status_human_returns_zero(tmp_repo):
    _run(["init", str(tmp_repo)], cwd=tmp_repo)
    proc = _run(["status"], cwd=tmp_repo)
    assert proc.returncode == 0
    assert "etapa" in proc.stdout
    assert "cobertura" in proc.stdout


# ---- 10: config show lista effective con origen -------------------------
def test_10_config_show_lists_effective_with_origin(tmp_repo):
    _run(["init", str(tmp_repo)], cwd=tmp_repo)
    proc = _run(["config", "show"], cwd=tmp_repo)
    assert proc.returncode == 0
    assert "lang" in proc.stdout
    assert "default" in proc.stdout or "workspace" in proc.stdout or "cli_set" in proc.stdout


# ---- 11: config show refleja precedencia 4 niveles ----------------------
def test_11_config_show_precedence_4_levels(tmp_repo, tmp_path):
    _run(["init", str(tmp_repo)], cwd=tmp_repo)

    # nivel 3: archivo --config
    cli_cfg = tmp_path / "cli.json"
    cli_cfg.write_text(json.dumps({"lang": "en", "workspace.dir": "custom-ws"}))

    # nivel 4: --set (maxima prioridad)
    proc = _run(
        ["--config", str(cli_cfg), "--set", "lang=fr", "config", "show", "--json"],
        cwd=tmp_repo,
    )
    assert proc.returncode == 0
    payload = json.loads(proc.stdout)
    assert payload["config"]["lang"] == "fr", f"--set no gano: {payload['config']['lang']}"
    assert payload["origin"]["lang"] == "cli_set"
    assert payload["config"]["workspace.dir"] == "custom-ws"
    assert payload["origin"]["workspace.dir"] == "cli_file"


# ---- 12: catalogo de errores es caminable --------------------------------
def test_12_errors_catalog_is_walkable():
    from npr.errors_catalog import ERRORS, format_error
    assert len(ERRORS) >= 10
    for code, info in ERRORS.items():
        assert code.startswith("NPR-E")
        assert "msg" in info and info["msg"]
        assert "causa" in info and info["causa"]
        assert "accion" in info and info["accion"]
        rendered = format_error(code)
        assert code in rendered
        assert info["msg"] in rendered


# ---- 13: subcomando stub devuelve NPR-E113 -------------------------------
def test_13_subcommand_stub_returns_npr_e113(tmp_repo):
    _run(["init", str(tmp_repo)], cwd=tmp_repo)
    proc = _run(["inventory"], cwd=tmp_repo)
    assert proc.returncode == 0
    assert "NPR-E113" in proc.stderr


# ---- 14: subcomando desconocido devuelve error ---------------------------
def test_14_unknown_subcommand_returns_error(tmp_repo):
    proc = _run(["no-existe"], cwd=tmp_repo)
    assert proc.returncode != 0
    assert "invalid choice" in proc.stderr or "NPR-E102" in proc.stderr


# ---- 15: log file creado tras init + status ------------------------------
def test_15_log_file_created(tmp_repo):
    _run(["init", str(tmp_repo)], cwd=tmp_repo)
    _run(["status"], cwd=tmp_repo)
    log_path = tmp_repo / ".project-review" / "logs" / "npr.log"
    assert log_path.is_file()
    assert log_path.stat().st_size > 0


# ---- 16: exit codes documentados (0 ok, 1 uso, 2 gate, 3 interno) --------
def test_16_exit_code_zero_on_init(tmp_repo):
    proc = _run(["init", str(tmp_repo)], cwd=tmp_repo)
    assert proc.returncode == 0


# ---- 17: SKILL_DIR no resuelto devuelve NPR-E101 -----------------------
def test_17_no_skill_dir_raises_npr_e101(tmp_path, tmp_repo):
    proc = subprocess.run(
        [sys.executable, str(NPR), "init", str(tmp_repo)],
        cwd=tmp_repo,
        capture_output=True, text=True,
        env={
            "PATH": os.environ.get("PATH", ""),
            "NPR_HOME": str(tmp_path / "nope"),
            "HERMES_HOME": str(tmp_path / "nope2"),
            "HOME": str(tmp_path / "nope3"),
        },
    )
    assert "NPR-E101" in proc.stderr


# ---- 18: --set mal formado devuelve NPR-E110 ----------------------------
def test_18_set_with_malformed_syntax_returns_npr_e110(tmp_repo):
    _run(["init", str(tmp_repo)], cwd=tmp_repo)
    proc = _run(["--set", "sin-igual", "config", "show"], cwd=tmp_repo)
    assert "NPR-E110" in proc.stderr
    assert proc.returncode == 2


# ---- 19: init no toca .gitignore del repo --------------------------------
def test_19_init_does_not_touch_repo_gitignore(tmp_repo):
    gi = tmp_repo / ".gitignore"
    gi.write_text("node_modules/\n")
    _run(["init", str(tmp_repo)], cwd=tmp_repo)
    assert gi.read_text() == "node_modules/\n"


# ---- 20: resume es stub -------------------------------------------------
def test_20_resume_stub_returns_npr_e113(tmp_repo):
    _run(["init", str(tmp_repo)], cwd=tmp_repo)
    proc = _run(["resume"], cwd=tmp_repo)
    assert proc.returncode == 0
    assert "NPR-E113" in proc.stderr