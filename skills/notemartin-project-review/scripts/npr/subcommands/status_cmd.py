"""Subcomando `npr status`."""
from __future__ import annotations

import json
import sys
from pathlib import Path

from .. import errors_catalog, workspace as ws_mod
from ..schema import load_schema, validate as validate_instance


COMMAND = "status"


def add_parser(sub):
    p = sub.add_parser(COMMAND, help="Muestra el estado actual del workspace")
    p.add_argument("--json", dest="as_json", action="store_true", help="Salida en JSON")
    return p


def handle(args, ctx) -> int:
    skill_dir, workspace_dir, effective, origin, logger = ctx
    if workspace_dir is None:
        print(errors_catalog.format_error("NPR-E104"), file=sys.stderr)
        return 1
    state = ws_mod.load_state(workspace_dir)
    payload = _gather(workspace_dir, payload_extra={"stage": state["stage"]})

    if getattr(args, "as_json", False):
        # validar contra el esquema state (relajado: campos extra permitidos)
        schema = load_schema("state")
        errors = validate_instance(payload, schema)
        if errors:
            print("FALLO", file=sys.stderr)
            for e in errors:
                print(f"  {e}", file=sys.stderr)
            return 2
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
        return 0

    print(f"workspace: {workspace_dir}")
    print(f"etapa:     {payload['stage']}")
    print(f"commit:    {payload['commit'] or '(no-git)'}")
    print(f"cobertura: {payload['coverage_pct']:.1f}%")
    print(f"WUs pendientes: {payload['wus_pending']}")
    print(f"preguntas abiertas: {payload['open_questions']}")
    print(f"siguiente accion: {payload['next_action']}")
    return 0


def _gather(workspace: Path, payload_extra: dict | None = None) -> dict:
    state = ws_mod.load_state(workspace)
    coverage_pct = _coverage_pct(workspace)
    wus_pending = _wus_pending(workspace)
    open_q = _open_questions(workspace)
    next_action = _next_action(state.get("stage"))
    payload = {
        "repo": state["repo"],
        "commit": state["commit"],
        "branch": state["branch"],
        "created_at": state["created_at"],
        "skill_version": state["skill_version"],
        "mode": state["mode"],
        "stage": state["stage"],
        "config": state.get("config", {}),
        "coverage_pct": coverage_pct,
        "wus_pending": wus_pending,
        "open_questions": open_q,
        "next_action": next_action,
    }
    if payload_extra:
        payload.update(payload_extra)
    return payload


def _coverage_pct(workspace: Path) -> float:
    ledger = workspace / "ledger" / "ledger.jsonl"
    if not ledger.is_file():
        return 0.0
    total, done = 0, 0
    with ledger.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            total += 1
            if rec.get("state") == "done":
                done += 1
    return (done / total * 100.0) if total else 0.0


def _wus_pending(workspace: Path) -> int:
    plan = workspace / "wu" / "plan.md"
    if not plan.is_file():
        return 0
    text = plan.read_text(encoding="utf-8")
    return text.count("- [ ]")


def _open_questions(workspace: Path) -> int:
    oq = workspace / "openq" / "openq.jsonl"
    if not oq.is_file():
        return 0
    n = 0
    with oq.open(encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                n += 1
    return n


def _next_action(stage: str) -> str:
    if stage == "A":
        return "ejecutar `npr recon` (F25)"
    return "ver PROGRESS.md"