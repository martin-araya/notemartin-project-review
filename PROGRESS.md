# Progreso del constructor

Estado por fase de la skill `notemartin-project-review` y registro de avance.

## Tabla de fases

| Fase | Estado | Fecha | Evidencia | Notas |
|---|---|---|---|---|
| F00 | HECHA | 2026-10-05 | pytest 1 passed; validate_skill OK; árbol coincide con §10 de AGENTS; 6/7 criterios cumplidos, 1 eliminado por D-108 (CI GitHub Actions prohibido) | Commit `F00: estructura base` (cb7a9ca) + commit de actualización D-108 |
| F01 | PENDIENTE | | | |
| F02 | PENDIENTE | | | |
| F03 | PENDIENTE | | | |
| F04 | PENDIENTE | | | |
| F05 | PENDIENTE | | | |
| F06 | PENDIENTE | | | |
| F07 | PENDIENTE | | | |
| F08 | PENDIENTE | | | |
| F09 | PENDIENTE | | | |
| F10 | PENDIENTE | | | |
| F11 | PENDIENTE | | | |
| F12 | PENDIENTE | | | |
| F13 | PENDIENTE | | | |
| F14 | PENDIENTE | | | |
| F15 | PENDIENTE | | | |
| F16 | PENDIENTE | | | |
| F17 | PENDIENTE | | | |
| F18 | PENDIENTE | | | |
| F19 | PENDIENTE | | | |
| F20 | PENDIENTE | | | |
| F21 | PENDIENTE | | | |
| F22 | PENDIENTE | | | |
| F23 | PENDIENTE | | | |
| F24 | PENDIENTE | | | |
| F25 | PENDIENTE | | | |
| F26 | PENDIENTE | | | |
| F27 | PENDIENTE | | | |
| F28 | PENDIENTE | | | |
| F29 | PENDIENTE | | | |
| F30 | PENDIENTE | | | |
| F31 | PENDIENTE | | | |
| F32 | PENDIENTE | | | |
| F33 | PENDIENTE | | | |
| F34 | PENDIENTE | | | |
| F35 | PENDIENTE | | | |
| F36 | PENDIENTE | | | |
| F37 | PENDIENTE | | | |
| F38 | PENDIENTE | | | |
| F39 | PENDIENTE | | | |
| F40 | PENDIENTE | | | |
| F41 | PENDIENTE | | | |
| F42 | PENDIENTE | | | |
| F43 | PENDIENTE | | | |
| F44 | PENDIENTE | | | |
| F45 | PENDIENTE | | | |
| F46 | PENDIENTE | | | |
| F47 | PENDIENTE | | | |
| F48 | PENDIENTE | | | |
| F49 | PENDIENTE | | | |
| F50 | PENDIENTE | | | |
| F51 | PENDIENTE | | | |
| F52 | PENDIENTE | | | |
| F53 | PENDIENTE | | | |
| F54 | PENDIENTE | | | |
| F55 | PENDIENTE | | | |
| F56 | PENDIENTE | | | |
| F57 | PENDIENTE | | | |
| F58 | PENDIENTE | | | |
| F59 | PENDIENTE | | | |
| F60 | PENDIENTE | | | |
| F61 | PENDIENTE | | | |
| F62 | PENDIENTE | | | |
| F63 | PENDIENTE | | | |
| F64 | PENDIENTE | | | |
| F65 | PENDIENTE | | | |
| F66 | PENDIENTE | | | |
| F67 | PENDIENTE | | | |
| F68 | PENDIENTE | | | |
| F69 | PENDIENTE | | | |
| F70 | PENDIENTE | | | |
| F71 | PENDIENTE | | | |
| F72 | PENDIENTE | | | |
| F73 | PENDIENTE | | | |
| F74 | PENDIENTE | | | |
| F75 | PENDIENTE | | | |
| F76 | PENDIENTE | | | |
| F77 | PENDIENTE | | | |
| F78 | PENDIENTE | | | |
| F79 | PENDIENTE | | | |
| F80 | PENDIENTE | | | |
| F81 | PENDIENTE | | | |
| F82 | PENDIENTE | | | |
| F83 | PENDIENTE | | | |
| F84 | PENDIENTE | | | |
| F85 | PENDIENTE | | | |
| F86 | PENDIENTE | | | |
| F87 | PENDIENTE | | | |
| F88 | PENDIENTE | | | |

Estados válidos: `PENDIENTE`, `EN CURSO`, `HECHA`, `BLOQUEADA`, `REABIERTA`.

## Relevo

- Fecha y hora: 2026-10-05
- Agente / modelo / runtime: Kilo / MiniMax-M3 / code mode local
- Fase(s) en curso y estado: F00 HECHA; F01–F88 PENDIENTE
- Hecho en esta sesión (con commits):
  - Árbol completo de `notemartin-project-review-skill/` (raíz del repo).
  - `LICENSE` (MIT), `.gitignore`, `pyproject.toml`, `dev/requirements-dev.txt`.
  - `PROGRESS.md` con 89 filas F00..F88, secciones Relevo y Preguntas para el dueño.
  - `DECISIONS.md` con D-001..D-014 (copiadas de AGENTS §16) + D-100..D-107 nuevas.
  - Placeholders de la skill: `SKILL.md`, `README.md`, `INSTRUCCIONES.md`, `scripts/npr.py`, `scripts/.npr-marker`, `scripts/npr/__init__.py`, `scripts/npr/cli.py`.
  - `dev/tests/test_smoke.py` (1 test que pasa).
  - 7 placeholders ejecutables en `dev/tools/`.
  - `dev/holdout/SPEC.md` (placeholder).
  - ~~`.github/workflows/ci.yml`~~ (eliminado por D-108 — prohibido CI en GitHub Actions).
  - Commit `F00: estructura base` (sin push).
  - Commit de actualización por D-108: eliminar `.github/`, actualizar AGENTS §3/§10/§28 y ROADMAP F00.
- A medias (archivo → estado exacto → qué falta): nada.
- Subagentes en vuelo (id, ruta del brief, qué devolverán, dónde escribirán): ninguno.
- Comandos para verificar el estado:
  - `python -m pytest`
  - `python dev/tools/validate_skill.py skills/notemartin-project-review`
  - `find . -maxdepth 4 -type d | sort`
  - `wc -l PROGRESS.md DECISIONS.md`
- Siguiente acción exacta: F01 — Esqueleto de `SKILL.md` y validador de skill.
- Decisiones tomadas (D-NNN): D-100..D-108 (D-108 elimina el CI en GitHub Actions).
- Riesgos y bloqueos:
  - R1 — ~~El CI en GitHub Actions solo se ejecuta tras subir el repo; F00 reabre si falla al primer push.~~ Resuelto por D-108 (CI prohibido).
  - R2 — Convención de marca de fase en `ROADMAP.md` no estaba definida; se usó ✅ y se verificó visualmente.
  - R3 — `LICENSE` lleva copyright placeholder; el dueño puede ajustarlo.

## Preguntas para el dueño

- [ ] (sin preguntas)