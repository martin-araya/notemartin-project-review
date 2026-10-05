# Progreso del constructor

Estado por fase de la skill `notemartin-project-review` y registro de avance.

## Tabla de fases

| Fase | Estado | Fecha | Evidencia | Notas |
|---|---|---|---|---|
| F00 | HECHA | 2026-10-05 | pytest 1 passed; validate_skill OK; árbol coincide con §10 de AGENTS; 6/7 criterios cumplidos, 1 eliminado por D-108 (CI GitHub Actions prohibido) | Commit `F00: estructura base` (cb7a9ca) + commit de actualización D-108 |
| F01 | HECHA | 2026-10-05 | pytest 25 passed (24 nuevos + 1 smoke); validate_skill sobre skill real → OK; description 830/1024; cuerpo 142/5000 tokens; 8 disparadores ES + 6 EN | Commit `F01: SKILL.md esqueleto y validador` |
| F02 | HECHA | 2026-10-05 | pytest 25 passed; validate_skill OK; 3 borradores en dev/evals/drafts (Hermes 203 líneas, Cline 220, Kilo 227); references/22-adaptadores-runtime.md con 210 líneas, 23 fuentes citadas (URL + fecha), matriz 11×3, 4 secciones obligatorias | Commit `F02: referencia de adaptadores por runtime` |
| F03 | HECHA | 2026-10-05 | pytest 54 passed (53 nuevos + 1 smoke); validate_skill OK; scripts/npr/citations.py con 5 patrones (RANGE_SYMBOL, RANGE, LINE, GIT, DYN); references/00-principios.md con 8 leyes verificables, 14 ejemplos válidos y 11 inválidos; SHA case-insensitive normalizado a minúsculas; rechazo de paths absolutos | Commit `F03: principios y gramática de citas` |
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
- Fase(s) en curso y estado: F00 HECHA; F01 HECHA; F02 HECHA; F03 HECHA; F04–F88 PENDIENTE
- Hecho en esta sesión (con commits):
  - F00 (commit `cb7a9ca`): árbol completo de `notemartin-project-review-skill/`, LICENSE MIT, .gitignore, pyproject.toml, dev/requirements-dev.txt, PROGRESS.md (89 filas), DECISIONS.md (D-001..D-014 + D-100..D-107), 7 placeholders en dev/tools/, dev/tests/test_smoke.py, dev/holdout/SPEC.md, .github/workflows/ci.yml.
  - F00 update D-108 (commit `62bf3cc`): eliminó `.github/`, actualizó AGENTS §3/§10/§28 y ROADMAP F00; prohibió CI en GitHub Actions.
  - F01 (próximo commit): reescritura de `skills/notemartin-project-review/SKILL.md` con frontmatter literal del roadmap (description 830 chars, 8 disparadores ES + 6 EN) y 9 secciones placeholder; reescritura completa de `dev/tools/validate_skill.py` (≈ 320 líneas) con las 7 reglas; creación de `dev/tests/test_validate_skill.py` con 24 tests que cubren todos los criterios del roadmap.
  - F02 (próximo commit): lanzamiento de 3 subagentes investigadores en paralelo (Hermes 203 líneas, Cline 220 líneas, Kilo 227 líneas) en `dev/evals/drafts/`. Fusión en `references/22-adaptadores-runtime.md` (210 líneas, 23 fuentes con URL + fecha 2026-10-05).
  - F03 (próximo commit): `scripts/npr/citations.py` con 5 patrones ordenados por especificidad (RANGE_SYMBOL primero), dataclass `Citation` inmutable, normalización (path sin `./`, SHA en minúsculas) y rechazo de paths absolutos y rangos invertidos. `references/00-principios.md` con 8 leyes (cada una con bloque "Cumplida por:" que nombra un gate o linter), 14 ejemplos válidos y 11 inválidos. `dev/tests/test_citations.py` con 29 tests que cubren cada patrón, normalización, orden, casos adyacentes y un test que lee el propio `.md` y verifica que el parser coincide exactamente con la lista declarada.
- A medias (archivo → estado exacto → qué falta): nada.
- Subagentes en vuelo (id, ruta del brief, qué devolverán, dónde escribirán): ninguno.
- Comandos para verificar el estado:
  - `python -m pytest` → 25 passed (24 nuevos + 1 smoke)
  - `python dev/tools/validate_skill.py skills/notemartin-project-review` → OK (código 0)
  - `python dev/tools/validate_skill.py skills/notemartin-project-review --json` → `{"ok": true, ...}`
  - `wc -l skills/notemartin-project-review/references/22-adaptadores-runtime.md` → 210
- Siguiente acción exacta: F04 — Esquemas de datos del workspace.
- Decisiones tomadas (D-NNN): D-100..D-136 (D-108 CI prohibido; D-109..D-114 validador; D-115..D-121 investigación F02; D-122..D-129 contradicciones; D-130..D-136 gramática de citas).
- Riesgos y bloqueos:
  - R1 — Resuelto por D-108.
  - R2 — Resuelto (✅ visible en ROADMAP).
  - R3 — `LICENSE` lleva copyright placeholder; el dueño puede ajustarlo.
  - R4 — El parser YAML propio es robusto para el subset usado (mapas 2 niveles, listas inline, folded block `>-`); si en el futuro se añaden anchors/tags, D-109 obliga a instalar PyYAML.

## Preguntas para el dueño

- [ ] (sin preguntas)