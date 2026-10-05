# Decisiones del constructor

Registro de decisiones tomadas durante la implementación del roadmap. Cada decisión tiene un id
estable `D-NNN`, una fecha, la fase en que se tomó, su contexto, la decisión y sus consecuencias.
Las decisiones se numeran correlativamente y nunca se reutilizan.

## Decisiones iniciales (copiadas de `AGENTS.md` §16)

| Id | Decisión | Razón principal |
|---|---|---|
| D-001 | Python ≥ 3.10 con solo biblioteca estándar en runtime | Funciona en los 3 runtimes sin paso de instalación |
| D-002 | Reportes en Markdown + Mermaid; JSON y HTML derivados | Legibles por humanos y por LLMs, versionables, se ven en GitHub y VS Code |
| D-003 | JSONL para salidas grandes | Streaming, append y merge determinista |
| D-004 | Workspace `.project-review/` excluido vía `.git/info/exclude` | Junto al código, sin ensuciar el repo ni su `.gitignore` |
| D-005 | Backend de símbolos regex por defecto; tree-sitter y ctags opcionales | Cero dependencias con mejora automática si existen |
| D-006 | Gramática de citas `[@ruta:ini-fin#Símbolo]` | Parseable y verificable por linter |
| D-007 | Ground truth separado de fixtures; holdout generado tras congelar la skill | Evita sobreajuste y fuga de respuestas |
| D-008 | Documentación en español; identificadores en inglés | Preferencia del dueño + convenciones de código |
| D-009 | `SKILL.md` ≤ 5k tokens con divulgación progresiva vía `references/` | Límite práctico de Cline y costo de contexto |
| D-010 | Nombre `notemartin-project-review`, CLI `npr` | Definido por el dueño del proyecto |
| D-011 | Paquete por feature de 13 artefactos + mini-paquete por superficie | Explicación completa incluyendo todos los resultados posibles |
| D-012 | Los scripts de la skill no usan red | Confidencialidad y reproducibilidad |
| D-013 | Features con id `FEAT-NNN` (fases del roadmap usan `FNN`) | Evitar ambigüedad |
| D-014 | Umbrales canónicos en `dev/evals/thresholds.json` + Anexo C | Una sola fuente de verdad para la calidad |

## Decisiones nuevas

### D-100 — `LICENSE` MIT con copyright placeholder

- Fecha · Fase · Estado: 2026-10-05 · F00 · vigente
- Contexto: AGENTS §30 declara `metadata.license: MIT`. El roadmap no especifica el titular.
- Decisión: usar texto MIT completo con `Copyright (c) 2026 Martin` como placeholder.
- Alternativas consideradas: dejar LICENSE ausente hasta que el dueño defina el titular; usar "All rights reserved" como neutral.
- Consecuencias: el dueño puede sobre-escribir el titular sin tocar el resto. Si quiere otra licencia, F00 reabre.

### D-101 — `pyproject.toml` solo con configuración de pytest

- Fecha · Fase · Estado: 2026-10-05 · F00 · vigente
- Contexto: AGENTS §17 dice que la skill no tiene dependencias de runtime fuera de stdlib y §10 muestra `pyproject.toml` como "solo config de pytest".
- Decisión: declarar únicamente `[tool.pytest.ini_options]`, sin `name`, sin deps.
- Alternativas consideradas: declarar paquete con `name = "notemartin-project-review"` y `version`.
- Consecuencias: pytest encuentra la configuración. La skill no se confunde con un paquete pip instalable. Si en el futuro se quiere distribuir por pip, F00 reabre.

### D-102 — `dev/requirements-dev.txt` solo con `pytest`

- Fecha · Fase · Estado: 2026-10-05 · F00 · vigente
- Contexto: AGENTS §17 prohíbe deps de runtime fuera de stdlib. Las deps opcionales (PyYAML, tree-sitter, universal-cttags) se mencionan en §17 como detectables en runtime.
- Decisión: una sola línea `pytest>=8.0`.
- Alternativas consideradas: añadir `pytest-cov`, `pytest-xdist`, `ruff`, `mypy`.
- Consecuencias: CI instala lo mínimo. Cada guardián opcional se añadirá en su fase. Sin lock de versiones más allá del `>=` de pytest.

### D-103 — `dist/` con `.gitkeep` aunque esté en `.gitignore`

- Fecha · Fase · Estado: 2026-10-05 · F00 · vigente
- Contexto: el roadmap menciona `dist/` como artefactos empaquetados por F73 `package.py`. Sin `.gitkeep` el directorio no entra al repo y `find` falla al compararlo contra el árbol de §10.
- Decisión: crear `dist/.gitkeep` y añadir regla `dist/*` + `!dist/.gitkeep` en `.gitignore`.
- Alternativas consideradas: no crear `dist/` hasta F73.
- Consecuencias: el árbol coincide hoy con §10 y la primera ejecución de `package.py` tiene destino.

### D-104 — `dev/tests/test_smoke.py` con un assert trivial

- Fecha · Fase · Estado: 2026-10-05 · F00 · vigente
- Contexto: el criterio "pytest sin errores de colección (0 tests o un test trivial que pasa)" deja elección libre. Sin tests, CI no tendría evidencia de ejecución correcta.
- Decisión: `test_smoke.py` con `def test_smoke(): assert True`.
- Alternativas consideradas: dejar `dev/tests/` vacío (cumple "0 tests") y añadir el primer test en F01.
- Consecuencias: CI muestra `1 passed` desde el primer push. F01 lo reemplaza con los tests reales.

### D-105 — CI con `continue-on-error` para guardianes aún no implementados

- Fecha · Fase · Estado: 2026-10-05 · F00 · vigente
- Contexto: `overfit_guard.py` y `check_thresholds.py` se implementan en F57 y F66 respectivamente. Sin esa protección, CI falla hoy.
- Decisión: marcarlos con `continue-on-error: true` y endurecerlos en sus fases.
- Alternativas consideradas: no invocarlos hasta que existan; documentar su ausencia en el job.
- Consecuencias: CI pasa hoy sin falsear la ausencia de los guardianes; cada fase endurece su guardián.

### D-106 — Sin push en F00

- Fecha · Fase · Estado: 2026-10-05 · F00 · vigente
- Contexto: AGENTS §27 dice "nunca commitear `dist/`, workspaces `.project-review/` ni lotes de holdout antes de su generación en F82" y exige flujo por ramas. Sin remoto configurado ni autor definido, pushear es prematuro.
- Decisión: commit local `F00: estructura base` sin `git push`.
- Alternativas consideradas: configurar remoto y autor antes de pushear.
- Consecuencias: el commit queda en `main` local listo para subirse cuando el dueño lo decida.

### D-107 — Copyright `Copyright (c) 2026 Martin`

- Fecha · Fase · Estado: 2026-10-05 · F00 · vigente
- Contexto: titular del LICENSE.
- Decición: usar nombre "Martin" sin apellido.
- Alternativas consideradas: dejarlo como `TODO`; preguntar al dueño (sería Q-NNN bloqueante).
- Consecuencias: el dueño puede ajustarlo sin reabrir F00.

### D-108 — Prohibido CI en GitHub Actions (ni en ningún servicio externo)

- Fecha · Fase · Estado: 2026-10-05 · F00 (actualización) · vigente
- Contexto: el dueño del proyecto prohíbe integrar el repo con GitHub Actions o cualquier servicio externo de CI. La verificación debe ser local y registrarse como evidencia en `PROGRESS.md`. El criterio de aceptación "El workflow de CI corre (verde) en las 3 plataformas" de F00 queda obsoleto.
- Decisión:
  1. Eliminar `.github/workflows/ci.yml` del repo.
  2. Eliminar `.github/workflows/ci.yml` del árbol de §10 de `AGENTS.md` y del bloque de estructura de F00 en `ROADMAP.md`.
  3. Añadir la preferencia del dueño en `AGENTS.md` §3 ("Sin CI en GitHub Actions") y la regla dura correspondiente en §28 (regla 16).
  4. Reemplazar el bullet de "`.github/workflows/ci.yml`" en F00 por una nota que apunte a esta decisión.
  5. Marcar el criterio "El workflow de CI corre (verde) en las 3 plataformas" como **eliminado** con referencia a D-108.
  6. Ningún criterio de aceptación de ninguna fase puede requerir un job remoto para considerarse cumplido. Si una fase ya escrita lo hacía, se reabre para ajustarlo.
- Alternativas consideradas: dejar el workflow vivo pero no requerido (rechazado: el dueño prohíbe la integración en sí); usar CI en otro servicio externo (rechazado: la prohibición es contra todo servicio externo).
- Consecuencias: AGENTS y ROADMAP se alinean con la preferencia. El commit `F00: estructura base` (cb7a9ca) queda parcialmente obsoleto por la presencia del workflow eliminado; el siguiente commit documenta el cambio. F00 sigue `HECHA` con 6 de los 7 criterios cumplidos y 1 explícitamente eliminado por D-108.

## Plantilla para nuevas decisiones

```
### D-NNN — Título

- Fecha · Fase · Estado: vigente | reemplazada por D-xxx
- Contexto:
- Decisión:
- Alternativas consideradas:
- Consecuencias:
```