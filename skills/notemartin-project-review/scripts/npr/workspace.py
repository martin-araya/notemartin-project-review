"""Creacion y gestion del workspace `.project-review/`."""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

from . import errors_catalog
from . import config as cfg
from .schema import validate


WORKSPACE_SUBDIRS = [
    "state", "recon", "graph", "ledger/fragments",
    "wu",
    "notes/files", "notes/modules", "notes/flows", "notes/features",
    "notes/surfaces", "notes/cross", "notes/answers",
    "openq", "verify", "reports", "logs", "dyn", "re",
]


def _git(cwd: Path, args: list[str]) -> str | None:
    """Devuelve stdout o None si git falla."""
    try:
        out = subprocess.run(
            ["git", *args], cwd=cwd, capture_output=True, text=True, check=False,
        )
        if out.returncode != 0:
            return None
        return out.stdout.strip()
    except FileNotFoundError:
        return None


def git_dir(repo: Path) -> Path | None:
    gd = repo / ".git"
    if gd.is_dir():
        return gd
    if gd.is_file():
        try:
            text = gd.read_text(encoding="utf-8")
        except OSError:
            return None
        m = re.match(r"gitdir:\s*(\S+)", text)
        if m:
            return Path(m.group(1))
    return None


def add_exclude(git_dir_path: Path, line: str) -> bool:
    """Agrega `line` a .git/info/exclude si no esta. Devuelve True si se agrego."""
    info = git_dir_path / "info"
    info.mkdir(parents=True, exist_ok=True)
    excl = info / "exclude"
    existing = ""
    if excl.is_file():
        existing = excl.read_text(encoding="utf-8")
    pattern = re.compile(rf"^\s*{re.escape(line)}\s*/?\s*$", re.MULTILINE)
    if pattern.search(existing):
        return False
    sep = "" if existing.endswith("\n") or not existing else "\n"
    with excl.open("a", encoding="utf-8") as fh:
        fh.write(f"{sep}{line}\n")
    return True


def _read_state(workspace: Path) -> dict:
    path = workspace / "state" / "state.json"
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def init(repo: Path, out: Path | None, force: bool, lang: str, skill_dir: Path) -> Path:
    """Crea el workspace. Devuelve la ruta del workspace. Lanza SystemExit en errores."""
    if not repo.is_dir():
        print(errors_catalog.format_error("NPR-E112", repo=str(repo)), file=sys.stderr)
        sys.exit(2)

    workspace = (out.resolve() if out else repo / ".project-review").resolve()
    workspace.mkdir(parents=True, exist_ok=True)
    for sub in WORKSPACE_SUBDIRS:
        (workspace / sub).mkdir(parents=True, exist_ok=True)

    state_path = workspace / "state" / "state.json"
    if state_path.is_file() and not force:
        print(errors_catalog.format_error("NPR-E105", workspace=str(workspace)), file=sys.stderr)
        sys.exit(2)

    head = _git(repo, ["rev-parse", "HEAD"])
    branch = _git(repo, ["rev-parse", "--abbrev-ref", "HEAD"]) or "unknown"
    git_warning = False
    if head is None:
        if git_dir(repo) is None:
            git_warning = True
        head = ""

    if git_warning:
        print(errors_catalog.format_error("NPR-E116", repo=str(repo)), file=sys.stderr)

    from datetime import datetime, timezone
    state = {
        "repo": str(repo.resolve()),
        "commit": head,
        "branch": branch,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "skill_version": _skill_version(skill_dir),
        "mode": "completo",
        "stage": "A",
        "config": {},
    }
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")

    gd = git_dir(repo)
    if gd is not None:
        try:
            add_exclude(gd, ".project-review/")
        except OSError as exc:
            print(errors_catalog.format_error("NPR-E111", error=str(exc)), file=sys.stderr)
            sys.exit(2)

    return workspace


def _skill_version(skill_dir: Path) -> str:
    init_py = skill_dir / "scripts" / "npr" / "__init__.py"
    if init_py.is_file():
        for line in init_py.read_text(encoding="utf-8").splitlines():
            if line.startswith("__version__"):
                _, _, _, value = line.replace("=", " ").split(" ", 3)
                return value.strip().strip('"').strip("'")
    return "0.0.0"


def load_state(workspace: Path) -> dict:
    """Lee state.json; valida contra el esquema; lanza NPR-E106 si falla."""
    state = _read_state(workspace)
    if state is None:
        print(errors_catalog.format_error("NPR-E106", workspace=str(workspace)), file=sys.stderr)
        sys.exit(2)
    schema_path = skill_dir_or_exit() / "schemas" / "state.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    errors = validate(state, schema)
    if errors:
        print(errors_catalog.format_error("NPR-E106", errors="; ".join(errors)), file=sys.stderr)
        sys.exit(2)
    return state


def _skill_dir_or_exit_path() -> Path | None:
    return Path(os.environ["NPR_HOME"]) if os.environ.get("NPR_HOME") else None


def skill_dir_or_exit() -> Path:
    sd = _skill_dir_or_exit_path()
    if sd is None:
        print(errors_catalog.format_error("NPR-E101"), file=sys.stderr)
        sys.exit(2)
    return sd