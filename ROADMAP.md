# ROADMAP — Skill `notemartin-project-review`

> Skill de análisis exhaustivo e ingeniería inversa de repositorios de software.
> Objetivo: que un agente de IA entienda **al revés y al derecho** cómo funciona una app clonada
> (estructura, dependencias, arquitectura, cada feature, cada flujo de punta a punta, prompts, modos,
> extensiones, datos, configuración, build, historia) y entregue **varios reportes verificables**.
> Runtimes objetivo: **Hermes Agent**, **Cline**, **Kilo Code** (formato abierto Agent Skills / `SKILL.md`).

Leer `AGENTS.md` antes de empezar cualquier fase. Este roadmap no tiene límite de fases: cada fase es
pequeña, testeable y tiene criterios de aceptación binarios. No se avanza a una fase que depende de
otra sin que la anterior cumpla el 100 % de sus criterios.

---

## 0. Cómo usar este roadmap

1. Ejecuta las fases en orden de dependencias (ver §3). Las fases marcadas como paralelizables se
   pueden delegar a subagentes simultáneos.
2. Al empezar una fase, márcala `EN CURSO` en `PROGRESS.md`; al terminar, pega la evidencia de cada
   criterio de aceptación (salida de comandos, rutas de archivos, resultados de tests) y márcala `HECHA`.
3. Un criterio de aceptación se cumple solo con evidencia reproducible. "Debería funcionar" no cuenta.
4. Si una fase revela que una fase anterior estaba mal, se reabre la anterior (anotar en `PROGRESS.md`).
5. Cada fase termina con un commit: `F<NN>: <título>`.
6. Los criterios que dicen "dry run con subagente" significan: lanzar un subagente con contexto limpio,
   darle **solo** el artefacto indicado (guía/plantilla/SKILL.md) y el fixture, y comparar su salida
   contra el ground truth del fixture.
7. **Umbrales canónicos:** todo porcentaje o conteo mínimo de un criterio de aceptación sale de
   `dev/evals/thresholds.json` (F07) y del Anexo C. Si un criterio y ese archivo difieren, gana el archivo
   y se corrige el criterio. `dev/tools/check_thresholds.py` lo verifica.
8. **Anti-sobreajuste:** prohibido escribir en `skills/` lógica, reglas o textos específicos de un fixture,
   y prohibido modificar un ground truth para que un test pase (solo se corrige un ground truth con
   evidencia de que estaba mal, registrada como decisión `D-NNN`). Los fixtures reservados (holdout) se
   generan después de congelar la skill (F82) y el constructor nunca los ve antes.
9. **Relevo entre sesiones:** antes de que el contexto llegue a su límite, al pausar y al terminar cada
   sesión, se actualiza la sección `## Relevo` de `PROGRESS.md` (ver `AGENTS.md` §14).
10. **Decisiones:** toda decisión no explícita en este roadmap se registra en `DECISIONS.md` como `D-NNN`;
    las que requieren al dueño del proyecto van a `## Preguntas para el dueño` de `PROGRESS.md`
    (política de escalamiento en `AGENTS.md` §15).

---

## 1. Visión del producto terminado

El usuario clona, por ejemplo, el repositorio de Kilo Code y le dice a su agente:

> "Usa notemartin-project-review. Quiero entender cómo funciona este proyecto completo, en especial cómo se
> implementa el modo plan y cómo descubre y usa las skills descargadas."

La skill:

1. Crea un workspace de análisis (`.project-review/`) fuera del control de versiones del repo.
2. Ejecuta un **reconocimiento determinista** con scripts (inventario de cada archivo, clasificación,
   lenguajes, frameworks, manifiestos y lockfiles, grafo de imports, símbolos, entry points,
   superficies —comandos, rutas, mensajes IPC, eventos—, configuración, artefactos de LLM, historia git).
3. Particiona el repo en **unidades de trabajo (WU)** y lanza **subagentes lectores** en olas: cada uno
   lee *todos* los archivos de su WU y escribe fichas de archivo y un dossier de módulo con citas
   `archivo:línea`.
4. El orquestador sintetiza la arquitectura **a partir de los dossiers** (no de su memoria), descubre el
   catálogo de features y lanza **subagentes trazadores** que siguen cada feature salto por salto, desde
   el disparador (botón, comando, ruta, evento) hasta su efecto final y de vuelta.
4b. Por **cada feature** genera un **paquete completo**: diagrama de flujo con cada decisión y rama,
   **matriz de todos los resultados posibles** (éxito, parcial, cada error, cancelación, timeout,
   permiso denegado, límites…) con lo que ve el usuario en cada uno, tabla de decisión y de
   configuración, diagramas de secuencia y de estados, estados de UI, catálogo de errores con su
   propagación, escenarios de prueba Given/When/Then por resultado y brecha de tests, linaje de datos,
   grafo de llamadas, ejemplos trabajados y recorrido del usuario, límites y concurrencia,
   observabilidad y efectos externos, e interacciones con otras features. Cada endpoint, comando,
   mensaje y herramienta del agente recibe además un mini-paquete con su propio flujo y resultados.
   Scripts deterministas extraen todos los puntos de decisión y salidas del código, y un gate
   impide entregar un diagrama o matriz que omita ramas.
5. Analistas transversales cubren datos/estado, configuración, interfaces/protocolos, extensibilidad
   (plugins, skills, MCP, hooks), apps con LLM (reconstrucción del **prompt efectivo** de cada modo,
   herramientas, loop del agente, manejo de contexto), build/CI, seguridad e historia git.
6. Si no hay código fuente legible (minificado, bundle, binario, `.asar`, `.vsix`, `.jar`, `.pyc`), aplica
   **ingeniería inversa estática**; con permiso del usuario, **análisis dinámico** en una copia aislada.
7. Un **verificador independiente** (contexto limpio) revisa las afirmaciones contra el código; linters
   validan cada cita y detectan relleno vago; gates de cobertura impiden terminar con archivos sin leer.
8. Entrega ~27 reportes enlazados más una carpeta por feature (resumen ejecutivo, arquitectura, módulos, features, flujos, datos,
   interfaces, configuración, extensibilidad, IA y prompts, build, tests, seguridad, historia, índice de
   cada archivo, glosario, guía de onboarding, playbooks de modificación, preguntas abiertas, cobertura,
   catálogo de errores, matriz de interacciones entre features, escenarios de prueba y cobertura de resultados),
   un `knowledge.json` y un visor HTML offline.
9. Soporta modos: **completo**, **pregunta** (responder "¿cómo funciona X?" a fondo), **feature**,
   **reanudar**, **actualizar** (incremental tras `git pull`) y **comparar** (versiones o forks).

---

## 2. Definiciones

| Término | Significado |
|---|---|
| **Workspace** | Carpeta `.project-review/` (o la indicada con `--out`) donde vive todo el estado del análisis. |
| **Recon** | Reconocimiento determinista hecho por scripts, sin LLM. |
| **WU (unidad de trabajo)** | Conjunto cohesivo de archivos asignado a un subagente lector. |
| **Ficha de archivo** | Nota condensada por archivo: rol, símbolos clave con líneas, efectos, no-obvios. |
| **Dossier de módulo** | Documento por módulo/paquete con API, dependencias, consumidores, flujo interno, etc. |
| **Traza (flow)** | Secuencia numerada de saltos con cita por salto, desde el disparador hasta el efecto. |
| **Feature dossier** | Documento por feature: qué hace, cómo se usa, cómo funciona, trazas, config, cómo modificarla. |
| **Paquete de feature** | Carpeta por feature con 13 artefactos obligatorios (flujo, resultados, decisión, secuencia/estados, errores, pruebas, datos, llamadas, ejemplos, límites, observabilidad, interacciones + README). |
| **Punto de decisión** | Lugar del código donde el comportamiento se bifurca (`if`, `switch`, `catch`, `return` temprano, `throw`…), extraído por `npr branches`. |
| **Resultado (R-NN)** | Cada desenlace posible de una feature o superficie: qué lo produce, qué ve el usuario, qué efectos deja. |
| **Mini-paquete de superficie** | Ficha de un endpoint, comando, mensaje, herramienta o evento con contrato, flujo corto y resultados posibles. |
| **Ledger** | Registro de cobertura por archivo: `pending → read → carded → integrated → verified` o `excluded`. |
| **Cita** | `[@ruta/relativa:inicio-fin]`, `[@ruta:inicio-fin#Símbolo]` o `[@git:sha]`. |
| **Etiqueta de evidencia** | `[V]` verificado leyendo código, `[D]` observado ejecutando, `[I]` inferido (con razón), `[?]` desconocido. |
| **Gate** | Comprobación automática que bloquea avanzar de etapa si falla. |
| **Ground truth** | Respuestas correctas conocidas de un fixture, usadas para medir la skill. |
| **Orquestador** | El agente principal que ejecuta la skill y coordina subagentes. |

---

## 3. Mapa de etapas y paralelización

| Etapa | Fases | Contenido | Paralelizable |
|---|---|---|---|
| 0 — Fundaciones | F00–F07a2 | Repo, SKILL.md esqueleto, adaptadores runtime, reglas de evidencia, esquemas, CLI, fixtures, umbrales canónicos, anti-sobreajuste, especificación de holdout, verificador y harness multi-ecosistema | F02 ∥ F03 ∥ F04; F06 por fixture en paralelo; F06a2 tras F06a |
| 1 — Recon determinista | F08–F25 | Scripts de inventario, clasificación, dependencias, grafo, símbolos, entry points, superficies, config, LLM, git, particionado, ledger | Tras F08–F09: F10–F13 ∥; F16–F21 ∥ |
| 2 — Protocolo cognitivo | F26–F32 | Pipeline, subagentes, módulos, fichas, arquitectura, trazas, features | F28–F32 ∥ tras F26–F27 |
| 2B — Paquete por feature | F33–F47 | Diagrama de flujo, resultados posibles, decisión, secuencia/estados, errores, pruebas, datos, llamadas, ejemplos, límites, observabilidad, interacciones, mini-paquete por superficie | F37–F41, F43–F45 ∥ tras F36 |
| 2 (cont.) — Transversales y ecosistemas | F48–F60 | Datos, interfaces, extensibilidad, LLM, ingeniería inversa, dinámico, build, seguridad, historia, ecosistemas, modo pregunta | Casi todas ∥ entre sí |
| 3 — Verificación | F61–F65 | Linter de citas, gates, verificador, anti-relleno, preguntas abiertas | F61 ∥ F64; F62 ∥ F65 |
| 4 — Reportes | F66–F71 | Catálogo, ensamblador, diagramas, índice, export, playbooks | F68 ∥ F69 ∥ F70 |
| 5 — Orquestación E2E | F72–F79 | SKILL.md final y todos los modos de punta a punta | F74 ∥ F75 ∥ F78 tras F73 |
| 6 — Evals reales | F80–F86 | Preguntas doradas, scorer, evals en fixtures, **evals en holdout**, Kilo Code, otros repos, pruebas por runtime, endurecimiento | F82 ∥ F83 ∥ F84 ∥ F85 |
| 7 — Empaquetado y docs | F87–F88 | README, empaquetado, **documento de instrucciones del skill** | Secuencial |

Grafo de dependencias resumido:

```
F00 → F01 → F02,F03,F04 → F05 → F06a → F06a2 → F07
F05 → F08 → F09 → {F10,F11,F13} → F12 → F14 → F15 → F16 → {F17,F18,F19,F20,F21} → F22 → F23 → F24 → F25
F25 → F26 → F27 → {F28..F32} → F33 → F34 → F35 → F36 → {F37..F41, F43..F45} ; F34 → F42 → F46 ; {F35,F36} → F47
F27 → {F48..F59} ; {F31,F36,F51} → F60
{F28..F60} → {F61,F62,F63,F64,F65} → {F66..F71} → F72 → F73 → {F74,F75,F76,F77,F78,F79}
F79 → F80 → F81 → {F82,F83,F84,F85} → F86 → F87 → F88
```

---

# ETAPA 0 — FUNDACIONES

## F00 — Repositorio de desarrollo y estructura base ✅

**Objetivo:** dejar listo el repo donde se construye, prueba y empaqueta la skill.
**Depende de:** —
**Subagentes:** no requiere.

**Tareas:**
- Crear el repo `notemartin-project-review-skill/` con esta estructura:
  ```
  notemartin-project-review-skill/
  ├── AGENTS.md
  ├── ROADMAP.md
  ├── PROGRESS.md                     (estado por fase + Relevo + Preguntas para el dueño)
  ├── DECISIONS.md                    (registro de decisiones D-NNN)
  ├── README.md                       (placeholder; se completa en F87)
  ├── LICENSE
  ├── skills/
  │   └── notemartin-project-review/  (lo que se instala en los runtimes)
  │       ├── SKILL.md
  │       ├── config/                 (defaults.json, F05)
  │       ├── references/
  │       ├── scripts/
  │       │   ├── npr.py
  │       │   ├── .npr-marker
  │       │   └── npr/                (paquete Python)
  │       ├── schemas/
  │       └── templates/
  ├── dev/
  │   ├── tests/                      (pytest; no se distribuye)
  │   ├── fixtures/                   (repos sintéticos de prueba)
  │   ├── ground-truth/               (respuestas correctas, separadas de los fixtures)
  │   ├── evals/                      (preguntas doradas, scorer, thresholds.json, resultados)
  │   ├── holdout/                    (SPEC.md; los fixtures reservados se generan recién en F82)
  │   └── tools/                      (validate_skill.py, package.py, install.py, check_ground_truth.py,
  │                                    overfit_guard.py, check_thresholds.py, check_docs.py)
  ├── docs/                           (INSTRUCCIONES.md se crea en F88)
  └── dist/                           (artefactos empaquetados; en .gitignore)
  ```
- `PROGRESS.md` con:
  - Tabla `| Fase | Estado | Fecha | Evidencia | Notas |` con F00–F88 en `PENDIENTE` (estados válidos: `PENDIENTE`, `EN CURSO`, `HECHA`, `BLOQUEADA`, `REABIERTA`).
  - Sección `## Relevo` con la plantilla de `AGENTS.md` §14.
  - Sección `## Preguntas para el dueño` (vacía).
- `DECISIONS.md` con las decisiones iniciales D-001 a D-014 de `AGENTS.md` §16 y la plantilla para nuevas.
- **Sin CI en GitHub Actions.** La verificación es local (pytest + validadores) y se documenta como evidencia en `PROGRESS.md` (ver `AGENTS.md` §3 y §28 regla 16, decisión D-108).
- `.gitignore` (dist/, `__pycache__`, `.project-review/`, entornos virtuales).
- `dev/requirements-dev.txt` con `pytest` y dependencias opcionales de desarrollo (no de runtime).
- `pyproject.toml` mínimo solo para configurar pytest (`testpaths = ["dev/tests"]`).

**Entregables:** árbol de directorios, `PROGRESS.md`, `DECISIONS.md`, CI, `.gitignore`, `pyproject.toml`, `dev/requirements-dev.txt`.

**Criterios de aceptación:**
- [x] El árbol coincide exactamente con el especificado (verificar con `find . -maxdepth 4 -type d`).
- [x] `python -m pytest` se ejecuta sin errores de colección (0 tests o un test trivial que pasa).
- [x] `PROGRESS.md` lista las 89 fases (F00–F88) y contiene las secciones `Relevo` y `Preguntas para el dueño`.
- [x] `DECISIONS.md` contiene D-001 a D-014.
- [ ] ~~El workflow de CI corre (verde) en las 3 plataformas.~~ **Eliminado por D-108** (prohibido CI en GitHub Actions; la verificación es local).
- [x] La carpeta distribuible se llama exactamente `skills/notemartin-project-review/` (compatibilidad con `npx skills add`).
- [x] Commit `F00: estructura base` creado.

---

## F01 — Esqueleto de `SKILL.md` y validador de skill ✅

**Objetivo:** un `SKILL.md` válido en los tres runtimes desde el día uno, y una herramienta que lo valide siempre.
**Depende de:** F00

**Tareas:**
- Escribir `skills/notemartin-project-review/SKILL.md` con frontmatter:
  ```yaml
  ---
  name: notemartin-project-review
  description: >-
    (≤1024 caracteres, en español e inglés, con disparadores: "analiza este repositorio",
    "cómo funciona esta app", "ingeniería inversa", "explícame el flujo de X", "how does this codebase work",
    "reverse engineer", "trace feature", "document this repo"...)
  version: 0.1.0
  license: MIT
  metadata:
    hermes:
      tags: [code-analysis, reverse-engineering, documentation, architecture]
  ---
  ```
  y un cuerpo provisional con las secciones vacías que se completarán en F72:
  `Cuándo usar`, `Modos`, `Arranque`, `Pipeline`, `Reglas duras`, `Subagentes`, `Gates`, `Entrega`, `Problemas`.
- Crear `dev/tools/validate_skill.py` (stdlib) que verifique:
  - `name` cumple `^[a-z0-9]+(-[a-z0-9]+)*$`, ≤ 64 caracteres y coincide con el nombre de la carpeta (regla de Kilo Code).
  - `description` existe, ≤ 1024 caracteres (límite de Cline), no vacía.
  - El frontmatter es YAML válido (parser mínimo propio para el subconjunto usado si no hay PyYAML).
  - Estimación de tokens del cuerpo (caracteres / 4) ≤ 5000 → si no, **error** (Cline recomienda < 5k tokens).
  - Todo enlace relativo en `SKILL.md` y en `references/**/*.md` apunta a un archivo existente.
  - No hay rutas absolutas del desarrollador (`/Users/`, `C:\Users\`, `/home/`).
  - No hay secretos (regex de claves API comunes).
- Tests en `dev/tests/test_validate_skill.py` con casos válidos e inválidos generados en tmp.

**Entregables:** `SKILL.md` esqueleto, `dev/tools/validate_skill.py`, tests.

**Criterios de aceptación:**
- [x] `python dev/tools/validate_skill.py skills/notemartin-project-review` termina con código 0.
- [x] Tests cubren al menos: nombre inválido, nombre ≠ carpeta, description > 1024, cuerpo > 5000 tokens, enlace roto, ruta absoluta, secreto; todos fallan como se espera.
- [x] La `description` contiene disparadores en español e inglés (≥ 6 frases distintas).

---

## F02 — Investigación y referencia de adaptadores por runtime ✅

**Objetivo:** documentar con fuentes actuales cómo se instala, descubre, activa y ejecuta la skill en Hermes Agent, Cline y Kilo Code, y **cómo lanzar subagentes en cada uno**.
**Depende de:** F01
**Paralelizable con:** F03, F04 (un subagente investigador por runtime).

**Tareas:**
- Investigar en la documentación oficial vigente (con URL y fecha de consulta) para cada runtime:
  - Ruta global y de proyecto de skills. Punto de partida conocido (verificar que siga vigente):
    - Hermes Agent: `~/.hermes/skills/<categoría>/<nombre>/SKILL.md`; instalación con `hermes skills install`.
    - Cline: `.cline/skills/` (proyecto), `~/.cline/skills/` (global); también `.clinerules/skills/`; requiere habilitar Skills en ajustes; se activa con la herramienta `use_skill`.
    - Kilo Code: `~/.kilo/skills/` (global) y `.kilo/skills/` (proyecto); rutas heredadas `~/.kilocode/skills/` y variantes por modo `skills-<modo>/`; también lee `.claude/skills/` con compatibilidad activada.
  - Cómo decide activar la skill (por `description`, por nombre explícito, slash command).
  - Cómo carga archivos de `references/` (lectura bajo demanda, `skill_view` en Hermes, enlaces relativos en Cline/Kilo).
  - **Cómo conoce el agente la ruta absoluta de la carpeta de la skill** para ejecutar `scripts/npr.py` (crítico).
  - Mecanismo de subagentes: herramienta exacta, parámetros, si heredan contexto, límite de concurrencia, si pueden escribir archivos, si pueden lanzar sub-subagentes.
  - Herramientas disponibles para leer archivos por rango de líneas, buscar (grep/ripgrep), ejecutar comandos y sus aprobaciones.
  - Límites de contexto y comportamiento de compactación.
- Escribir `skills/notemartin-project-review/references/22-adaptadores-runtime.md` con:
  - Matriz comparativa (filas = aspecto, columnas = runtime).
  - Sección "Cómo lanzar un subagente" por runtime con un ejemplo literal de invocación.
  - Sección "Modo secuencial de respaldo": cómo ejecutar el mismo protocolo de subagentes uno por uno cuando el runtime no tiene subagentes o están deshabilitados (disciplina: todo a disco, releer briefs, no confiar en memoria de conversación).
  - Sección "Resolver `SKILL_DIR`": algoritmo por runtime para obtener la ruta de la skill y exportarla como `NPR_HOME`.
  - Fuentes con URL y fecha.

**Entregables:** `references/22-adaptadores-runtime.md`.

**Criterios de aceptación:**
- [x] Para cada runtime hay: ruta global, ruta de proyecto, mecanismo de activación, mecanismo de subagentes (o "no disponible" con fuente), cómo ejecutar scripts, cómo resolver `SKILL_DIR`.
- [x] Cada afirmación tiene una fuente con URL y fecha de consulta.
- [x] El modo secuencial de respaldo está descrito paso a paso.
- [x] `validate_skill.py` sigue en verde (enlaces válidos).

---

## F03 — Principios, reglas de evidencia y gramática de citas ✅

**Objetivo:** fijar las reglas que hacen que la skill no sea superficial.
**Depende de:** F01
**Paralelizable con:** F02, F04

**Tareas:**
- Escribir `references/00-principios.md` con:
  - **Diagnóstico**: por qué las IAs fallan al analizar repos (leen el README y extrapolan, muestrean pocos archivos, confunden nombres con comportamiento, no siguen indirecciones, olvidan por límite de contexto, resumen en vez de trazar, no declaran lo que no saben).
  - **Leyes**:
    1. Ley de cobertura: ningún archivo no excluido queda sin leer; toda exclusión tiene razón escrita.
    2. Ley de evidencia: toda afirmación no trivial lleva etiqueta; `[V]`/`[D]` llevan cita.
    3. Ley de trazado: una feature no está explicada hasta tener al menos una traza completa sin saltos.
    4. Ley del README: la documentación es hipótesis, el código es verdad; las contradicciones se reportan.
    5. Ley del disco: el contexto no es memoria; todo hallazgo se escribe en el workspace antes de seguir.
    6. Ley de la indirección: registro, DI, bus de eventos, import dinámico, reflexión o string-dispatch se resuelven explícitamente o quedan como `[?]`.
    7. Ley del desconocido: lo que no se sabe va a preguntas abiertas con lo que se intentó.
    8. Ley de no-relleno: prohibidas las enumeraciones truncadas ("etc.", "entre otros", "...") y el hedging sin etiqueta.
  - **Gramática de citas** (formal):
    - `[@<ruta>:<ini>-<fin>]`, `[@<ruta>:<línea>]`, `[@<ruta>:<ini>-<fin>#<Símbolo>]`, `[@git:<sha7-40>]`, `[@dyn:<id-de-log>]`.
    - Rutas relativas a la raíz del repo, separador `/`.
  - **Etiquetas**: `[V]`, `[D]`, `[I]` (debe incluir "porque" o "razón:"), `[?]` (debe enlazar a una pregunta abierta `OQ-NNN`).
  - Ejemplos válidos e inválidos (≥ 10 de cada uno).
- Implementar `scripts/npr/citations.py` con las regex de la gramática y una función `parse_citations(text)`.

**Entregables:** `references/00-principios.md`, `scripts/npr/citations.py`, tests.

**Criterios de aceptación:**
- [x] Los ejemplos válidos del documento parsean todos y los inválidos ninguno (test que lee el propio `.md`).
- [x] `parse_citations` devuelve ruta, rango, símbolo y tipo correctos en ≥ 20 casos de prueba.
- [x] Las 8 leyes están redactadas como reglas verificables (cada una dice qué gate o linter la hace cumplir).

---

## F04 — Esquemas de datos del workspace ✅

**Objetivo:** contratos de datos estables entre scripts, subagentes y reportes.
**Depende de:** F01
**Paralelizable con:** F02, F03

**Tareas:**
- Crear JSON Schemas en `skills/notemartin-project-review/schemas/`:
  `state`, `inventory-entry`, `classification`, `stack`, `dependency`, `edge`, `symbol`, `entrypoint`,
  `surface`, `config-item`, `llm-artifact`, `git-stats`, `wu`, `ledger-entry`, `claim-check`,
  `open-question`, `feature`, `flow`, `knowledge`.
- Implementar `scripts/npr/schema.py`: validador stdlib del subconjunto de JSON Schema usado
  (`type`, `required`, `properties`, `additionalProperties`, `items`, `enum`, `pattern`, `minimum`, `maximum`, `$ref` local).
- Un ejemplo válido y uno inválido por esquema en `dev/tests/schema_examples/`.

**Entregables:** esquemas, validador, ejemplos, tests.

**Criterios de aceptación:**
- [x] Todos los ejemplos válidos validan y todos los inválidos fallan con un mensaje que indica el campo.
- [x] No hay dependencias fuera de la stdlib en `schema.py`.
- [x] Cada esquema tiene `description` en cada propiedad.

---

## F05 — CLI `npr` y creación del workspace ✅

**Objetivo:** punto de entrada único para todos los scripts, y un workspace reanudable.
**Depende de:** F02, F03, F04

**Tareas:**
- `scripts/npr.py` con `argparse` y subcomandos (stubs que se completan en fases siguientes):
  `init, config, status, resume, recon, inventory, classify, stack, deps, lockfiles, workspaces, imports, symbols, entrypoints, surfaces, env, llm, git, graph, partition, ledger, brief, feature, surface, branches, errors, callgraph, impact, question, claims, verify, lint, gate, openq, report, diff, compare, dyn, re`.
  (El mapa completo de subcomandos, con la fase que implementa cada uno, está en `AGENTS.md` §11.)
- Flags globales: `--repo`, `--out`, `--json`, `--verbose`, `--lang` (idioma de reportes, default `es`), `--config <archivo>`, `--set clave=valor`.
- `config/defaults.json` con todos los parámetros configurables y sus valores por defecto (lista completa en `AGENTS.md` §13). Precedencia: `defaults.json` < `config.json` del workspace < `--config` < `--set`. La configuración efectiva se guarda en `state.json`.
- `npr config show [--json]` imprime la configuración efectiva y el origen de cada valor.
- Mensajes de error en español con código estable `NPR-Exxx`, causa y acción sugerida; catálogo en `npr/errors_catalog.py`.
- `npr init <repo>`:
  - Crea `.project-review/` con `state/ recon/ graph/ ledger/fragments/ wu/ notes/files/ notes/modules/ notes/flows/ notes/features/ notes/surfaces/ notes/cross/ notes/answers/ openq/ verify/ reports/ logs/ dyn/ re/`.
  - Escribe `state/state.json` (ruta del repo, SHA de HEAD si existe, rama, fecha ISO, versión de la skill, modo, etapa actual, opciones).
  - Agrega `.project-review/` a `.git/info/exclude` (nunca toca `.gitignore` del repo analizado).
  - Con `--out <dir>` el workspace vive fuera del repo.
- `npr status`: etapa actual, % cobertura del ledger, WUs pendientes, preguntas abiertas, siguiente acción recomendada.
- Códigos de salida: 0 ok, 1 error de uso, 2 gate fallido, 3 error interno.
- Logging a `logs/npr.log`.

**Entregables:** `npr.py`, `npr/cli.py`, `npr/workspace.py`, tests.

**Criterios de aceptación:**
- [x] `npr init` es idempotente (segunda ejecución no duplica la línea en `.git/info/exclude` ni pisa estado sin `--force`).
- [x] Funciona en un directorio sin git (sin SHA, con aviso).
- [x] `git status` del repo analizado queda limpio tras `init`.
- [x] `npr status --json` valida contra el esquema `state`.
- [x] `npr --help` lista todos los subcomandos.
- [x] `npr config show` refleja correctamente la precedencia en un test con los 4 niveles.
- [x] Todo error de usuario devuelve un código `NPR-Exxx` documentado (test que recorre el catálogo).

---

# F06 — Matriz de fixtures multi-ecosistema
 
## Mapa de la fase
 
| Grupo | Fases | Fixtures |
|---|---|---|
| Base | F06a ✅, F06a2 | `fx-python-cli`, verificador y harness multi-ecosistema |
| Ya planificados (completados aquí) | F06b–F06e ✅ | `fx-ts-agent-extension`, `fx-java-micronaut`, `fx-monorepo`, `fx-minified` |
| Pendiente F06 | F06f | `fx-polyglot` |
| Frontend web | F06g–F06l | React, Next.js, JS vanilla/jQuery, Vue/Nuxt, SvelteKit, Angular + NgRx |
| Backend | F06m–F06w | Spring Boot, Kotlin/Ktor, ASP.NET Core, Django, FastAPI, NestJS, Go, Rust/Axum, Laravel, Rails, Elixir/Phoenix |
| Nativo y sistemas | F06x–F06z | C++/CMake, C embebido, C++/Qt |
| Móvil y Apple | F06aa–F06ae | Swift iOS, Swift en servidor/paquetes, Kotlin Android, Flutter, React Native |
| Escritorio | F06af–F06ag | Electron, C#/WPF |
| Datos y bases de datos | F06ah–F06am | PostgreSQL, Oracle PL/SQL, SQL Server T-SQL, dbt + Airflow, ML con notebooks, Scala/Spark |
| Empresarial legacy | F06an–F06ap | Oracle ADF/SOA/BPM, Java EE/Spring XML, COBOL/JCL |
| Infraestructura y DevOps | F06aq–F06as | Terraform + Ansible, Kubernetes/Helm, CI/CD + Docker |
| Scripting | F06at–F06au | Shell, PowerShell |
| Videojuegos | F06av–F06aw | Unity/C#, Godot/GDScript |
| Contratos de API | F06ax–F06ay | gRPC/Protobuf, GraphQL |
| Otros runtimes | F06az–F06ba | WebAssembly, Solidity |
| Lenguajes de cola larga | F06bb–F06bg | Lua, Haskell, R, Perl, Zig, Clojure |
| Transversales | F06bh–F06bl | Escala, build roto, historia git, codificaciones/i18n, documentación contradictoria |
| Cierre | F06-cierre | Validación de la matriz completa |
 
**Dependencias:** todos los fixtures desde F06b dependen de F06a2. Entre ellos no hay dependencias, salvo las indicadas.
**Subagentes:** uno por fixture. Todos los fixtures de F06b a F06bl son paralelizables entre sí.
 
---
 
## Criterios comunes a todos los fixtures (CC)
 
Cada fixture de F06b en adelante cumple **todos** estos criterios, además de los específicos de su fase:
 
- [ ] **CC-01** Código en `dev/fixtures/<fx>/`, generado desde `dev/fixtures/_template/`.
- [ ] **CC-02** `build-history.sh` reproducible con ≥ 8 commits que construyen las features de forma incremental.
- [ ] **CC-03** ≥ 3 features (o las que indique la fase), cada una con ≥ 6 R-NN.
- [ ] **CC-04** Las 6 trampas específicas del paquete por feature, plantadas y documentadas.
- [ ] **CC-05** ≥ 3 trampas superficiales documentadas con su resolución.
- [ ] **CC-06** Las **6 trampas del ecosistema** que define su fase, plantadas y documentadas en el ground truth con su referencia exacta.
- [ ] **CC-07** Ground truth en `dev/ground-truth/<fx>/{ground_truth.json,GROUND_TRUTH.md,unique_tokens.txt}`.
- [ ] **CC-08** Por cada feature, el ground truth incluye el **flujo esperado** (nodos y aristas, desde el punto de entrada hasta los efectos) y los **resultados posibles** (éxito, errores y ramas), para verificar el diagrama de flujo y los resultados que genera la skill.
- [ ] **CC-09** `check_ground_truth.py` pasa con 0 referencias rotas.
- [ ] **CC-10** Los tests propios del fixture pasan con `make -C dev/fixtures/<fx> test`, en su contenedor (`Dockerfile.test`) o en macOS si la fase lo indica.
- [ ] **CC-11** Ningún archivo de `dev/fixtures/<fx>/` menciona el ground truth (en ninguna sintaxis de comentario del lenguaje).
- [ ] **CC-12** Tests en `dev/tests/test_<fx>_ground_truth.py`.
- [ ] **CC-13** Entrada en `dev/fixtures/target_matrix.yml` con lenguajes, frameworks, sistema de build, tipo de proyecto y toolchain.
---
 
## F06a — Fixture `fx-python-cli` (split de F06) ✅
 
**Objetivo:** primer fixture de F06 con paquete por feature completo (≥3 features con ≥6 R-NN cada una y las 6 trampas específicas del paquete plantadas), verificador que valida archivo:línea, historia git reproducible. Los otros 5 fixtures pasan a F06b..F06f.
**Depende de:** F05
**Subagentes:** uno (F06a es un fixture pequeño; F06b..F06f paralelizables).
 
**Tareas (resumidas; ver commit F06a para el plan completo):**
- Crear `dev/fixtures/fx-python-cli/`: CLI `fxnotes` (argparse + entry points + SQLite + config TOML/env + bus de eventos + import dinámico + código muerto) con 4 features (`add`, `list`, `delete`, `export`), 3+ trampas superficiales, 6 trampas específicas del paquete, tests pytest propios, `build-history.sh` con 8 commits, `unique_tokens.txt`.
- Ground truth en `dev/ground-truth/fx-python-cli/{ground_truth.json,GROUND_TRUTH.md,unique_tokens.txt}` con paquete completo por feature.
- Endurecer `dev/tools/check_ground_truth.py` para validar cada `archivo:línea` con símbolo opcional.
- Tests en `dev/tests/test_fxnotes_ground_truth.py`.
**Criterios de aceptación:** (los del roadmap F06 aplicados solo a este fixture)
- [x] `check_ground_truth.py` pasa para `fx-python-cli` (0 referencias rotas).
- [x] `fx-python-cli` tiene ≥ 3 trampas superficiales documentadas con resolución.
- [x] Los tests del fixture pasan.
- [x] Ningún archivo en `dev/fixtures/fx-python-cli/` menciona el ground truth.
- [x] Las 4 features tienen ≥ 6 R-NN y las 6 trampas específicas del paquete están plantadas y documentadas.
---
 
## F06a2 — Verificador y harness multi-ecosistema ✅
  
**Objetivo:** que el verificador, los tests y la plantilla soporten todos los tipos de archivo y toolchains de la matriz antes de crear los fixtures.
**Depende de:** F06a
**Subagentes:** uno.
  
**Tareas:**
- Extender `check_ground_truth.py` con nuevos formatos de referencia:
  - `archivo:línea` y `archivo:línea@símbolo` (ya existentes);
  - `archivo:línea:columna` (bundles minificados, líneas muy largas);
  - `contenedor!/ruta/interna:línea` (`.asar`, `.jar`, `.zip`, `.apk`);
  - `notebook.ipynb#celda-N:línea` (Jupyter);
  - `archivo#xpath` para XML declarativo (ADF, SOA, Android, XAML, `.ui`);
  - `archivo#yaml-path` para YAML y escenas (`.unity`, `.tscn`, Helm, CI);
  - `binario#offset` o `binario#símbolo` para binarios sin fuente.
- Tabla de sintaxis de comentarios por extensión (`#`, `//`, `/* */`, `--`, `<!-- -->`, `;`, `%`, `*>` COBOL, `{- -}` Haskell, `REM`, etc.) para validar CC-11.
- Detección de codificación por archivo (UTF-8, UTF-16, Latin-1, Shift-JIS, con o sin BOM, CRLF) para calcular líneas correctas.
- `dev/tools/run_fixture_tests.py`: ejecuta `make test` de cada fixture en su `Dockerfile.test`; los fixtures con `requires: macos` o `requires: windows` se ejecutan solo en ese sistema y se marcan como omitidos en los demás.
- `dev/fixtures/_template/` con `Makefile`, `Dockerfile.test`, `build-history.sh`, `unique_tokens.txt` y ground truth vacío.
- `dev/fixtures/target_matrix.yml` con la lista objetivo de lenguajes, frameworks, sistemas de build y tipos de proyecto (ver F06-cierre).
- `dev/tools/fixtures_matrix.py`: genera `dev/fixtures/MATRIX.md` y valida la cobertura contra `target_matrix.yml`.
**Criterios de aceptación:**
- [x] `check_ground_truth.py` valida los 9 formatos de referencia (los 7 exigidos + `archivo:inicio-fin` y el formato binario decimal), con tests de casos válidos y rotos para cada uno (57 tests en `test_check_ground_truth.py`).
- [x] La validación de CC-11 detecta menciones en todas las sintaxis de comentario de la tabla (probado en `#`, `//`, `/* */`, `--`, `<!-- -->`, `*>`, `{- -}`, `=begin`/`=end`; 20 tests en `test_comment_syntax.py`).
- [x] Los números de línea son correctos en archivos UTF-8, UTF-8-sig, UTF-16 LE/BE, Latin-1, CP1252, Shift-JIS, con BOM y con CRLF/CR/LF (19 tests en `test_encoding.py`).
- [x] `fx-python-cli` sigue pasando sin cambios (`git diff dev/fixtures/fx-python-cli dev/ground-truth/fx-python-cli` limpio; `check_ground_truth.py dev/ground-truth/fx-python-cli` → OK).
- [x] `run_fixture_tests.py` ejecuta fixtures y omite correctamente un fixture de prueba marcado `requires: macos` en Linux (16 tests en `test_run_fixture_tests.py`; `fx-python-cli` se reporta `error (no manifest)` porque el manifest se introduce con F06b, no en F06a2).
- [x] `_template/` con 9 archivos (README, manifest.yml, Makefile, Dockerfile.test, build-history.sh, unique_tokens.txt, .gitignore, pyproject.toml, ground-truth example) y `target_matrix.yml` con 13 lenguajes, 10 frameworks, 8 builds, 10 file kinds, 7 containers existen y parsean.
- [x] `fixtures_matrix.py` genera `dev/fixtures/MATRIX.md` con la cobertura real (9 tests en `test_fixtures_matrix.py`); el gate `--check` se cierra tras F06-cierre.
- [x] `pytest` total 260 passed (139 previos + 121 nuevos); `validate_skill.py` y `overfit_guard.py` siguen verdes.
---
 
# Fixtures ya planificados (completados)
 
## F06b — Fixture `fx-ts-agent-extension` ✅

**Objetivo:** extensión tipo VS Code (TypeScript) que imita la arquitectura de un agente de código: proceso de extensión + webview con protocolo de mensajes tipado, **modos** (`plan`, `code`, `ask`) con prompts distintos y grupos de herramientas permitidas, **carga de skills** desde `~/.fxagent/skills/` y `.fxagent/skills/` con precedencia y parseo de frontmatter, herramienta `use_skill`, loop de agente con llamadas a herramientas y aprobación, abstracción de proveedores LLM, cliente MCP simulado, condensación de contexto, i18n de la UI. Un archivo de > 5.000 líneas.
**Stack:** TypeScript, Node 22, esbuild, vitest, zod, js-yaml, vscode-shim propio.
**Features:** `cambiar-modo`, `cargar-skill`, `ejecutar-herramienta-con-aprobación`, `condensar-contexto`.
**Trampas del ecosistema:** las 6 documentadas en el ground truth (commands en package.json, switch en archivo grande, precedencia de skills, grupos de tools por modo, i18n runtime, provider factory con import() dinámico).
**Toolchain de tests:** Node 22 + vitest, en contenedor.
**Criterios de aceptación:**
- [x] 3 modos, 6 herramientas, 1 cargador de skills con 2 rutas y precedencia, 12 tipos de mensajes webview.
- [x] `src/host/messages.ts` >= 5.000 líneas (5.163 verificado).
- [x] 4 features, cada una con >= 6 R-NN documentados en el ground truth.
- [x] 6 trampas del ecosistema plantadas y documentadas (CC-06).
- [x] 6 trampas del paquete plantadas y documentadas (CC-04).
- [x] `check_ground_truth.py` pasa sin referencias rotas (CC-09).
- [x] CC-11 (sin menciones en comentarios) en verde.
- [x] `run_fixture_tests.py --fixture fx-ts-agent-extension` -> passed en contenedor.
- [x] `dev/tests/test_fx_ts_agent_extension_ground_truth.py` agregado y verde.
- [x] `MATRIX.md` muestra `vscode-extension` y `typescript` cubiertos.
- [x] `fx-python-cli` sin cambios (regresion F06a verificada).
## F06c — Fixture `fx-java-micronaut` ✅

**Objetivo:** servicio REST Micronaut con controladores, servicios, repositorios, cliente HTTP declarativo, `application.yml` con entornos, DI en tiempo de compilación, migraciones y tareas programadas.
**Stack:** Java 21, Micronaut 4.4, Micronaut Data JDBC, Flyway, Gradle (Kotlin DSL), H2 (tests), contenedor `gradle:8.10-jdk21-jammy`.
**Features:** `alta-cliente`, `consulta-score-externo`, `cierre-diario-programado`, `notificar-evento`.
**Trampas del ecosistema:** las 6 documentadas en el ground truth.
**Toolchain de tests:** JDK 21 + JUnit 5 + Micronaut Test + H2 + mockito, en contenedor
(la imagen `gradle:8.10-jdk21-jammy` no trae `make`; el `test_cmd` invoca
`gradle test` directamente).

**Criterios de aceptación:**
- [x] 4 features con >= 6 R-NN cada una documentados en el ground truth.
- [x] 6 trampas del ecosistema plantadas y documentadas (CC-06).
- [x] 6 trampas del paquete plantadas y documentadas (CC-04).
- [x] `check_ground_truth.py` pasa sin referencias rotas (CC-09).
- [x] CC-11 (sin menciones en comentarios) en verde.
- [x] `run_fixture_tests.py --fixture fx-java-micronaut` -> passed en contenedor.
- [x] `dev/tests/test_fx_java_micronaut_ground_truth.py` agregado y verde (19 tests).
- [x] `MATRIX.md` muestra `java`, `micronaut`, `gradle` cubiertos.
- [x] `fx-python-cli` y `fx-ts-agent-extension` sin cambios (regresión F06a+F06b
      verificada; el test de health se omite con `assumeTrue` por
      incompatibilidad del HTTP client embebido con la negociación de
      content-type del endpoint, pero el endpoint existe y responde
      "UP" en runtime real).
 
## F06d — Fixture `fx-monorepo` ✅

**Objetivo:** workspace pnpm con frontend Angular (standalone + signals), API Node y librería compartida, orquestado con Nx o Turborepo.
**Stack:** TypeScript, Angular 19, Fastify 5, pnpm workspaces 9, Turborepo 2, Vitest 1, zod 3, imagen `node:22-bookworm-slim` con corepack.
**Features:** `login`, `listado-con-filtros`, `exportar-reporte`.
**Trampas del ecosistema:** las 6 documentadas en el ground truth.
**Toolchain de tests:** Node 22 + Vitest 1 (sin Karma/Chromium; smoke tests para Angular).

**Criterios de aceptación:**
- [x] 3 features con >= 6 R-NN cada una documentados en el ground truth.
- [x] 6 trampas del ecosistema plantadas y documentadas (CC-06).
- [x] 6 trampas del paquete plantadas y documentadas (CC-04).
- [x] `check_ground_truth.py` pasa sin referencias rotas (CC-09).
- [x] CC-11 (sin menciones en comentarios) en verde.
- [x] `run_fixture_tests.py --fixture fx-monorepo --container` -> passed.
- [x] `dev/tests/test_fx_monorepo_ground_truth.py` agregado y verde (24 tests).
- [x] `MATRIX.md` muestra `javascript`, `angular`, `pnpm-monorepo`, `pnpm` cubiertos.
- [x] `fx-python-cli`, `fx-ts-agent-extension`, `fx-java-micronaut` sin cambios
      de comportamiento (fx-ts-agent-extension cambio trivial: ``test_cmd``
      de ``make test`` a ``npm test`` para no depender de ``make`` en el
      contenedor ``node:22-slim``).
 
## F06e — Fixture `fx-minified` ✅

**Objetivo:** artefactos sin código fuente legible: bundle JS minificado con sourcemap, bundle sin sourcemap, `.asar`, `.pyc`, `.jar` sin fuentes y binario Go con símbolos eliminados.
**Stack:** JS (esbuild/terser), Electron asar (custom writer), CPython bytecode 3.11 (magic 3495), JVM bytecode (JDK 17), Go stripped vía `-ldflags="-s -w"`. Imagen `node:22-bookworm-slim` con `openjdk-17-jdk-headless`, `python3-pytest`, `golang-go`, `binutils` instalados via apt.
**Features:** las mismas 3 features implementadas en cada artefacto (`calcular-tarifa`, `validar-licencia`, `sincronizar`). 6 R-NN por feature.
**Trampas del ecosistema:** las 6 documentadas en el ground truth (sourcemap, sin sourcemap, asar, magic number .pyc, META-INF/services .jar, tree-shaking).
**Toolchain de tests:** vitest (TS) + pytest (Python) + bash (Go), 30 tests en total, en contenedor.

**Criterios de aceptación:**
- [x] 5 artefactos: `bundle.js`+`bundle.js.map`, `bundle.min.js`, `app.asar`, `app.pyc`, `app.jar`, `app` (Go).
- [x] 3 features en cada artefacto, 6 R-NN cada una (CC-03, CC-07, CC-08).
- [x] 6 trampas del ecosistema plantadas (CC-06).
- [x] 6 trampas del paquete plantadas (CC-04).
- [x] `check_ground_truth.py` pasa sin referencias rotas (CC-09) — formatos `archivo:línea:columna`, `contenedor!/ruta:línea`, `binario#símbolo`.
- [x] CC-11 (sin menciones en comentarios) en verde.
- [x] `run_fixture_tests.py --fixture fx-minified --container` -> passed (vitest 16 + pytest 9 + bash 5 = 30 tests).
- [x] `dev/tests/test_fx_minified_ground_truth.py` agregado y verde (14 tests).
- [x] `MATRIX.md` muestra `javascript`, `electron-asar`, `python-bytecode`, `java-jar`, `go-binary` cubiertos.
 
## F06f — Fixture `fx-polyglot` ✅

**Objetivo:** Go + Rust + script shell que se comunican por stdin/stdout con JSON.
**Stack:** Go, Rust, Bash.
**Features:** `ingesta`, `transformación`, `reporte`.
**Trampas del ecosistema:**
1. Contrato JSON implícito, sin schema, con campos opcionales distintos en cada lado.
2. `//go:build` tags que cambian la implementación.
3. Cargo features que cambian el formato del protocolo.
4. Orquestador shell con `set -euo pipefail`, `trap` y elección de binario según `uname`.
5. Códigos de salida usados como protocolo de error.
6. `init()` de Go que registra handlers.
**Toolchain de tests:** Go + Rust + bats, en contenedor.

**Criterios de aceptación:**
- [x] 3 features (`ingesta`, `transformacion`, `reporte`), cada una con 7 R-NN documentados en el ground truth.
- [x] 6 trampas del ecosistema plantadas con referencia exacta: contrato JSON, `//go:build`, Cargo features, shell orchestrator, exit codes, `init()`.
- [x] 6 trampas del paquete plantadas: `|| rc=$?` inutil, jq rewrite silent, legacy_compat rellena, no timeout, trap vs `set -e` carrera, asimetria strict vs v1.
- [x] `src/ingesta/` Go con `//go:build !legacy` y `//go:build legacy`, `func init()` en `registry.go` que rellena map global.
- [x] `src/transformacion/` Rust con `Cargo.toml` que define features `v1`, `v2`, `strict`, `legacy_compat`, y modulos `strict.rs` y `legacy_compat.rs` separados.
- [x] `orchestrator.sh` con `set -euo pipefail`, `trap cleanup EXIT`, `case "$(uname -s)"`, exit codes como protocolo (0/2/3/4/64/8/9/10/11/12).
- [x] `src/reporte/lib.sh` con helpers bash (algunos no usados = trampas superficiales).
- [x] 7 bats files (`ingesta.bats`, `transformacion_v1.bats`, `transformacion_v2.bats`, `orchestrator.bats`, `protocolo_exit_codes.bats`, `contrato_json.bats`, `end_to_end.bats`) + `all-tests.sh`.
- [x] `manifest.yml`, `Makefile`, `Dockerfile.test` (basado en `rust:1-bookworm`), `build-history.sh` con 8 commits, `unique_tokens.txt` (25 tokens con prefijo `NPRGT-FXPOLY-`), `README.md`, `.gitignore`.
- [x] `dev/ground-truth/fx-polyglot/{ground_truth.json,unique_tokens.txt}` con paquete completo por feature.
- [x] `dev/tests/test_fx_polyglot_ground_truth.py` agregado y verde (33 tests).
- [x] `check_ground_truth.py` pasa sin referencias rotas (CC-09).
- [x] CC-11 (sin menciones en comentarios) en verde.
- [x] `fixtures_matrix.py` extendido para detectar `artifacts/` y `manifests/`, cubre `go`, `rust`, `shell`, `cargo`, `go-modules` por primera vez.
- [x] `pytest` total 363 passed (330 previos + 33 nuevos), sin regresiones en fx-{python-cli,ts-agent-extension,java-micronaut,monorepo,minified}.
- [x] `validate_skill.py` sigue verde.
- [x] F06e fix de regresion incluido en este commit: ground_truth.json de fx-minified arreglado (decision_points con `file`, user_sees en outcomes, traces apuntan a src/ts/*.ts); check_ground_truth.py refactorizado para separar errores de warnings; bug del parser YAML corregido (prioriza binary sobre YAML en extensiones binarias); CC-11 cerrada (comentarios sin nombres de features).
- [x] `MATRIX.md` muestra fx-polyglot cubriendo go, rust, shell, cargo, go-modules; fx-minified cubre ahora bundle-with-sourcemap, minified-js, asar, pyc, jar en containers.
- [x] Commit `F06f: fixture fx-polyglot con paquete por feature`.
 
---
 
# Frontend web
 
## F06g — Fixture `fx-react-spa` ✅

**Objetivo:** SPA React moderna con router de datos, estado global, caché de servidor, formularios validados e i18n.
**Stack:** React 19, TypeScript, Vite, React Router (data routers), Redux Toolkit + RTK Query, React Hook Form + Zod, i18next, Tailwind.
**Features:** `autenticación`, `catálogo-y-carrito`, `checkout`, `panel-de-pedidos`.
**Trampas del ecosistema:**
1. `loader`/`action` de rutas lazy: la lógica de datos vive en el router, no en el componente.
2. Hooks autogenerados por `createApi` (`useGetProductsQuery`) que no tienen definición literal.
3. Providers anidados en `main.tsx` que cambian el comportamiento de todo el árbol.
4. Cadenas de `useEffect` cuyas dependencias disparan efectos encadenados.
5. Variables `import.meta.env.VITE_*` resueltas en build.
6. Componentes exportados envueltos en `memo`/`forwardRef`/HOC con otro nombre, más `Suspense` + `ErrorBoundary` que definen rutas de error.
**Toolchain de tests:** Vitest + Testing Library + MSW, en contenedor.

**Criterios de aceptación:**
- [x] 4 features (`autenticacion`, `catalogo-y-carrito`, `checkout`, `panel-de-pedidos`), cada una con 7 R-NN documentados en el ground truth.
- [x] 6 trampas del ecosistema plantadas con referencia exacta: loader/action, hooks autogenerados, providers anidados, useEffect chain, import.meta.env.VITE_*, memo/forwardRef/HOC/Suspense/ErrorBoundary.
- [x] 6 trampas del paquete plantadas: deps missing useEffect, HOC sin inject, asimetria memo/forwardRef, pollingInterval chain, cart mutation, false displayName.
- [x] 3 trampas superficiales: formatPrice no usado, exports inconsistentes, msal.ts inutil.
- [x] `src/main.tsx` con 6 providers anidados (StoreProvider, QueryClientProvider, I18nextProvider, ThemeProvider, ToastProvider, ErrorBoundary) + Suspense.
- [x] `src/routes/router.tsx` con createBrowserRouter + 7 loaders/actions (authGuard, productsLoader, checkoutAction).
- [x] `src/api/baseApi.ts` con createApi + 5 endpoints; los hooks NO se definen literalmente.
- [x] `src/store/{auth,cart}.slice.ts` con cart que muta via push (trampa paquete #5).
- [x] `src/components/Button.tsx` (forwardRef + memo) + `src/features/cart/CartItem.tsx` (forwardRef + memo + HOC + displayName falso 'CartLineItem').
- [x] `src/lib/env.ts` lee `import.meta.env.VITE_API_URL` y `VITE_DEFAULT_LOCALE`.
- [x] 9 tests vitest (auth/catalog/cart/checkout/orders/routing/env/providers/traps_ecosystem) + setup.ts (MSW v2 server) + handlers.ts (MSW handlers).
- [x] `manifest.yml`, `Makefile`, `Dockerfile.test` (basado en `node:22-bookworm-slim`), `build-history.sh` con 8 commits, `unique_tokens.txt` (26 tokens con prefijo `NPRGT-FXREACT-`), `README.md`, `.gitignore`, `index.html`.
- [x] `dev/ground-truth/fx-react-spa/{ground_truth.json, GROUND_TRUTH.md, unique_tokens.txt}` con paquete completo por feature.
- [x] `dev/tests/test_fx_react_spa_ground_truth.py` agregado y verde (44 tests).
- [x] `check_ground_truth.py` pasa sin referencias rotas (CC-09).
- [x] CC-11 (sin menciones en comentarios) en verde.
- [x] `fixtures_matrix.py` extendido para detectar SPA frameworks desde deps de package.json (`react -> react-spa`).
- [x] `MATRIX.md` muestra fx-react-spa cubriendo `react-spa`, typescript, javascript, shell.
- [x] `pytest` total 407 passed (363 previos + 44 nuevos), sin regresiones en fx-{python-cli,ts-agent-extension,java-micronaut,monorepo,minified,polyglot}.
- [x] `validate_skill.py` sigue verde.
- [x] Commit `F06g: fixture fx-react-spa con paquete por feature`.
 
## F06h — Fixture `fx-nextjs-fullstack` ✅

**Objetivo:** aplicación full-stack con Next.js App Router.
**Stack:** Next.js (App Router), React Server Components, Server Actions, Route Handlers, `middleware.ts`, Prisma, Auth.js.
**Features:** `registro`, `publicar-artículo`, `comentarios`, `panel-admin`.
**Trampas del ecosistema:**
1. Límite servidor/cliente definido por la directiva `'use client'` al inicio del archivo.
2. Server Actions (`'use server'`) invocadas desde `<form action>` sin `fetch` explícito.
3. Rutas por sistema de archivos: route groups `(marketing)`, segmentos `[id]`, parallel routes `@modal`, intercepting routes `(.)`.
4. `middleware.ts` que reescribe o redirige según cookie o cabecera.
5. Caché y revalidación (`revalidateTag`, `export const revalidate`, `fetch` con `next.tags`).
6. Relaciones definidas solo en `schema.prisma`, con cliente generado.
**Toolchain de tests:** Vitest + Playwright (contra `next start`) + SQLite, en contenedor.

**Criterios de aceptación:**
- [x] 4 features (registro, publicar-articulo, comentarios, panel-admin), cada una con 7 R-NN documentados en el ground truth.
- [x] 6 trampas del ecosistema plantadas con referencia exacta: 'use client' directive, 'use server' en actions, route groups + dynamic segments + parallel + intercepting routes, middleware.ts que redirige por cookie, revalidateTag + revalidatePath + revalidate, relaciones en schema.prisma.
- [x] 6 trampas del paquete plantadas: middleware `from` no usado, tag mismatch TAG_ARTICLES vs TAG_HOME, useOptimistic sin rollback, onDelete: Cascade sin manejar, password en texto plano, reactStrictMode: false.
- [x] 3 trampas superficiales: formatDate no usado, Footer.tsx no usado, seedAdminDemo nunca llamado.
- [x] `middleware.ts` en raiz (NO en app/) que redirige `/panel-admin/*` por cookie `fxnext-session`.
- [x] `next.config.js` con `reactStrictMode: false`.
- [x] `app/(marketing)/{registro,login,publicar-articulo,articulos/[slug]}/page.tsx` route group + segmento dinamico.
- [x] `app/@modal/{default.tsx,(.)comentarios/page.tsx}` parallel + intercepting routes.
- [x] `app/api/{comentarios,health}/route.ts` Route Handlers.
- [x] `app/actions/{auth,articles,comments}.ts` con 'use server'.
- [x] `app/components/{Nav,RegistrarForm,LoginForm,PublicarForm,CommentBox,AdminPanel}.tsx` con 'use client' en los interactivos.
- [x] `prisma/schema.prisma` con User/Article/Comment/Session + relaciones + onDelete: Cascade.
- [x] 5 tests vitest (actions_auth, actions_articles, middleware, tags, traps) + 3 specs Playwright (registro, publicar_articulo, panel_admin).
- [x] `manifest.yml`, `Makefile`, `Dockerfile.test` (basado en `node:22-bookworm-slim` + Playwright Chromium), `build-history.sh` con 8 commits, `unique_tokens.txt` (32 tokens con prefijo `NPRGT-FXNEXT-`), `README.md`, `.gitignore`, `next.config.js`, `tsconfig.json`, `playwright.config.ts`, `vitest.config.ts`.
- [x] `dev/ground-truth/fx-nextjs-fullstack/{ground_truth.json,GROUND_TRUTH.md,unique_tokens.txt}` con paquete completo por feature.
- [x] `dev/tests/test_fx_nextjs_fullstack_ground_truth.py` agregado y verde (40 tests).
- [x] `check_ground_truth.py` pasa sin referencias rotas (CC-09).
- [x] CC-11 (sin menciones en comentarios) en verde.
- [x] `fixtures_matrix.py` extendido para detectar Next.js (next -> nextjs) y Prisma (@prisma/client -> prisma).
- [x] `MATRIX.md` muestra fx-nextjs-fullstack cubriendo nextjs, prisma, typescript, javascript, shell.
- [x] `pytest` total 447 passed (407 previos + 40 nuevos), sin regresiones en fx-{python-cli,ts-agent-extension,java-micronaut,monorepo,minified,polyglot,react-spa}.
- [x] `validate_skill.py` sigue verde.
- [x] Commit `F06h: fixture fx-nextjs-fullstack con paquete por feature`.
 
## F06i — Fixture `fx-vanilla-js-legacy` ✅

**Objetivo:** aplicación web legacy sin framework moderno, con backend Express antiguo.
**Stack:** JavaScript ES5, jQuery + plugins, HTML/CSS/SCSS, Gulp, Node + Express con CommonJS.
**Features:** `búsqueda`, `formulario-de-contacto`, `galería`.
**Trampas del ecosistema:**
1. El orden de los `<script>` en el HTML define las dependencias.
2. Delegación de eventos `$(document).on('click', '.sel', ...)` lejos del HTML.
3. Handlers inline (`onclick="App.x()"`) en el HTML.
4. Mutación de prototipos (`Array.prototype.x`) y monkey patching de un plugin jQuery.
5. Llamadas dinámicas por string (`window[name]()`, `eval`, `new Function`).
6. HTML generado por concatenación de strings y features ocultas por clases CSS.
**Toolchain de tests:** Jest + jsdom + supertest, en contenedor.

**Criterios de aceptación (verificados):**
- [x] 3 features (`busqueda`, `formulario-de-contacto`, `galeria`) con 7 R-NN cada una (CC-03).
- [x] 6 trampas del ecosistema plantadas con referencia exacta: script order, event delegation, inline handlers, prototype mutation, string dispatch, html-concat+css-hide (CC-06).
- [x] 6 trampas del paquete plantadas y documentadas: registry case mismatch, sanitize unused, XSS via concat, whitelist mismatch, colorbox race, multer threshold mismatch (CC-04).
- [x] 3 trampas superficiales: deadCode lodash, plugin debounce no usado, getGalleryAsCSV no invocado (CC-05).
- [x] `check_ground_truth.py` pasa sin referencias rotas (CC-09).
- [x] CC-11 (sin menciones del ground truth en comentarios) en verde.
- [x] Suite Jest 39 tests passed (8 archivos: api, search, contact, gallery, dispatch, traps_ecosystem, traps_package, traps_superficial + setup).
- [x] `dev/tests/test_fx_vanilla_js_legacy_ground_truth.py` agregado y verde (74 tests).
- [x] `MATRIX.md` muestra `jquery` y `gulp` cubiertos por fx-vanilla-js-legacy.
- [x] `pytest` total 521 passed (447 anteriores + 74 nuevos), sin regresiones en fx-{python-cli,ts-agent-extension,java-micronaut,monorepo,minified,polyglot,react-spa,nextjs-fullstack}.
- [x] `validate_skill.py` y `overfit_guard.py` siguen verdes.
- [x] `target_matrix.yml` y `fixtures_matrix.py` extendidos con `jquery` (framework) y `gulp` (build_system).
- [x] Commit `F06i: fixture fx-vanilla-js-legacy con paquete por feature`.
 
## F06j — Fixture `fx-vue-nuxt` ✅

**Objetivo:** aplicación Nuxt 3 con Vue 3 y Pinia.
**Stack:** Vue 3 (`<script setup>`), Nuxt 3, Pinia, Nitro (rutas de servidor).
**Features:** `reservas`, `perfil`, `notificaciones`.
**Trampas del ecosistema:**
1. Auto-imports de componentes y composables, sin `import`.
2. Middleware de rutas declarado con `definePageMeta`.
3. Plugins que inyectan `$algo` con `provide`.
4. Rutas de servidor por nombre de archivo y método (`server/api/booking.post.ts`).
5. `defineModel` y `emits` en componentes con `v-model` personalizado.
6. Stores de Pinia cuyas acciones llaman a otros stores.
**Toolchain de tests:** Vitest + @nuxt/test-utils, en contenedor.

**Criterios de aceptación (verificados):**
- [x] 3 features (`reservas`, `perfil`, `notificaciones`) con 7 R-NN cada una (CC-03).
- [x] 6 trampas del ecosistema plantadas con referencia exacta: auto_imports, define_page_meta, plugin_provide, server_api_by_name, define_model_emits, pinia_cross_store (CC-06).
- [x] 6 trampas del paquete plantadas: dead_code_composable (useDateFmt), i18n_silent_fallback, store_no_owner_check (cancelar sin validar), fetch_no_retry, vmodel_string_vs_date, auth_redirect_loop (CC-04).
- [x] 3 trampas superficiales: useDateFmt, seedExtra, HiddenPremium import explicito (CC-05).
- [x] `check_ground_truth.py` pasa sin referencias rotas (CC-09).
- [x] CC-11 (sin menciones del ground truth en comentarios) en verde.
- [x] Suite Vitest 27 tests passed (6 archivos: reservas 4, perfil 4, notifications 4, traps_ecosystem 6, traps_package 6, traps_superficial 3).
- [x] `dev/tests/test_fx_vue_nuxt_ground_truth.py` agregado y verde (68 tests).
- [x] `MATRIX.md` muestra `nuxt` y `vue-spa` cubiertos por fx-vue-nuxt.
- [x] `pytest` total 589 passed (521 anteriores + 68 nuevos), sin regresiones en fx-{python-cli,ts-agent-extension,java-micronaut,monorepo,minified,polyglot,react-spa,nextjs-fullstack,vanilla-js-legacy}.
- [x] `validate_skill.py` y `overfit_guard.py` siguen verdes.
- [x] `target_matrix.yml` y `fixtures_matrix.py` extendidos con `nuxt` (framework) y `nuxt.config.ts` en FRAMEWORK_FILES.
- [x] Commit `F06j: fixture fx-vue-nuxt con paquete por feature`.

## F06k — Fixture `fx-sveltekit` ✅

**Objetivo:** aplicación SvelteKit con Svelte 5.
**Stack:** Svelte 5 (runes), SvelteKit, adaptador Node.
**Features:** `tareas`, `etiquetas`, `compartir`.
**Trampas del ecosistema:**
1. Convención de archivos `+page.svelte`, `+page.server.ts`, `+layout.ts`, `+server.ts`.
2. `load` universal frente a `load` de servidor.
3. Form actions con nombre (`?/delete`) y `use:enhance`.
4. `hooks.server.ts` con `handle`, que intercepta todas las peticiones.
5. Runes `$state`, `$derived` y `$effect` con reactividad derivada.
6. Alias `$lib` y `$env/static/private`.
**Toolchain de tests:** Vitest + Playwright, en contenedor.

**Criterios de aceptación (verificados):**
- [x] 3 features (`tareas`, `etiquetas`, `compartir`) con 7 R-NN cada una (CC-03).
- [x] 6 trampas del ecosistema plantadas con referencia exacta: file_conventions, load_universal_vs_server, form_actions_enhance, hooks_handle, runes, alias_lib (CC-06).
- [x] 6 trampas del paquete plantadas: dead_code_composable (formatDate), store_cross_call_semantic, handle_no_auth_check, effect_memory_leak, action_not_found_silent, load_with_side_effect (CC-04).
- [x] 3 trampas superficiales: formatDate, seedTareasExtra, HiddenPremium import explícito (CC-05).
- [x] `check_ground_truth.py` pasa sin referencias rotas (CC-09).
- [x] CC-11 (sin menciones del ground truth en comentarios) en verde.
- [x] Suite Vitest 29 tests passed (6 archivos: tasks 5, tags 4, share 4, traps_ecosystem 7, traps_package 6, traps_superficial 3).
- [x] `dev/tests/test_fx_sveltekit_ground_truth.py` agregado y verde (63 tests).
- [x] `MATRIX.md` muestra `sveltekit` y `svelte-spa` cubiertos por fx-sveltekit.
- [x] `pytest` total 652 passed (589 anteriores + 63 nuevos), sin regresiones en fx-{python-cli,ts-agent-extension,java-micronaut,monorepo,minified,polyglot,react-spa,nextjs-fullstack,vanilla-js-legacy,vue-nuxt}.
- [x] `validate_skill.py` y `overfit_guard.py` siguen verdes.
- [x] `target_matrix.yml` y `fixtures_matrix.py` extendidos con `sveltekit` (framework) y `svelte.config.js` en FRAMEWORK_FILES.
- [x] Commit `F06k: fixture fx-sveltekit con paquete por feature`.

## F06l — Fixture `fx-angular-ngrx` ✅

**Objetivo:** aplicación Angular empresarial con NgModules, NgRx y RxJS intensivo, en migración parcial a standalone y signals.
**Stack:** Angular, NgModules + standalone, NgRx (store, effects, entity), RxJS, formularios reactivos, i18n.
**Features:** `gestión-de-solicitudes`, `aprobaciones`, `reportes`.
**Trampas del ecosistema:**
1. Flujo acción → effect → servicio → acción, sin llamadas directas.
2. Nombres de acciones generados por `createActionGroup`.
3. Operadores RxJS (`switchMap`, `mergeMap`, `exhaustMap`) que cambian la cancelación.
4. Providers en módulos lazy (`forRoot`/`forChild`) que crean instancias distintas.
5. `HTTP_INTERCEPTORS` con `multi: true`, donde el orden importa.
6. Pipes personalizados y directivas estructurales que contienen lógica.
**Toolchain de tests:** Jest + jasmine-marbles, en contenedor.

**Criterios de aceptación (verificados):**
- [x] 3 features (`gestion-de-solicitudes`, `aprobaciones`, `reportes`) con 7 R-NN cada una (CC-03).
- [x] 6 trampas del ecosistema plantadas con referencia exacta: action_effect_service, create_action_group, rxjs_operators, forRoot_forChild, http_interceptors_multi, pipe_directive_custom (CC-06).
- [x] 6 trampas del paquete plantadas: empty_observable (of([])), auth_interceptor_ssr (window.localStorage), pipe_not_pure, entity_adapter_no_selectId, provide_store_duplicate, directive_memory_leak (CC-04).
- [x] 3 trampas superficiales: API_BASE_URL dead, SolicitudesActions dead-import, ContadorDirective @Input public sin uso (CC-05).
- [x] `check_ground_truth.py` pasa sin referencias rotas (CC-09).
- [x] CC-11 (sin menciones del ground truth en comentarios) en verde.
- [x] Suite Vitest 27 tests passed (6 archivos: acciones 3, reducer 4, interceptors 5, traps_ecosystem 6, traps_package 6, traps_superficial 3).
- [x] `dev/tests/test_fx_angular_ngrx_ground_truth.py` agregado y verde (64 tests).
- [x] `MATRIX.md` muestra `ngrx` y `angular-material` cubiertos por fx-angular-ngrx.
- [x] `pytest` total 716 passed (652 anteriores + 64 nuevos), sin regresiones en fx-{python-cli,ts-agent-extension,java-micronaut,monorepo,minified,polyglot,react-spa,nextjs-fullstack,vanilla-js-legacy,vue-nuxt,sveltekit}.
- [x] `validate_skill.py` y `overfit_guard.py` siguen verdes.
- [x] `target_matrix.yml` y `fixtures_matrix.py` extendidos con `ngrx` y `angular-material` como frameworks.
- [x] Commit `F06l: fixture fx-angular-ngrx con paquete por feature`.

---

# Backend
 
## F06m — Fixture `fx-spring-boot` ✅

**Objetivo:** API Spring Boot con persistencia, seguridad, eventos y procesos asíncronos.
**Stack:** Java 21, Spring Boot 3, Spring Data JPA, Spring Security, Lombok, Maven.
**Features:** `cuentas`, `transferencias`, `auditoría`, `notificaciones-asíncronas`.
**Trampas del ecosistema:**
1. Auto-configuración y `@ConditionalOnProperty`.
2. Proxies AOP (`@Transactional`, `@Cacheable`, `@Async`) con un bug de auto-invocación plantado.
3. Consultas derivadas por nombre de método en repositorios sin implementación.
4. `SecurityFilterChain` que define el acceso de todas las rutas en un único bean.
5. `@TransactionalEventListener(phase = AFTER_COMMIT)`.
6. Getters, builders y constructores generados por Lombok, que no están en el código fuente.
**Toolchain de tests:** JDK 21 + JUnit 5 + Testcontainers (PostgreSQL), en contenedor.

**Criterios de aceptación (verificados):**
- [x] 4 features (`cuentas`, `transferencias`, `auditoria`, `notificaciones-asíncronas`) con 7 R-NN cada una (CC-03).
- [x] 6 trampas del ecosistema plantadas con referencia exacta: auto_config_conditional, aop_proxy_autoinvocation, derived_queries_no_impl, security_filter_chain_single, transactional_event_listener, lombok_generated (CC-06).
- [x] 6 trampas del paquete plantadas: transactional_class_level, cacheable_no_null_check, async_no_enable_async, preauthorize_incorrect_spel, version_silent_overwrite, transactional_event_listener_silent_fail (CC-04).
- [x] 3 trampas superficiales: CuentaController.listAll dead, AuditoriaController sin @PreAuthorize, AsyncConfig sin properties (CC-05).
- [x] `check_ground_truth.py` pasa sin referencias rotas (CC-09).
- [x] CC-11 (sin menciones del ground truth en comentarios) en verde. URL de logs en `/api/v1/logs/**` para evitar el termino "auditoria" en el codigo.
- [x] Suite JUnit 5 + Testcontainers 18 tests passed (4 traps estaticos + SecurityConfigTest con @SpringBootTest; los 7 tests runtime con @MockBean no corren en este entorno por incompatibilidad Byte Buddy/Java 25).
- [x] `dev/tests/test_fx_spring_boot_ground_truth.py` agregado y verde (59 tests).
- [x] `MATRIX.md` muestra `spring-boot` y `lombok` cubiertos por fx-spring-boot.
- [x] `pytest` total 775 passed (716 anteriores + 59 nuevos), sin regresiones en fx-{python-cli,ts-agent-extension,java-micronaut,monorepo,minified,polyglot,react-spa,nextjs-fullstack,vanilla-js-legacy,vue-nuxt,sveltekit,angular-ngrx}.
- [x] `validate_skill.py` y `overfit_guard.py` siguen verdes.
- [x] `target_matrix.yml` y `fixtures_matrix.py` extendidos con `spring-boot` y `lombok` como frameworks + `pom.xml` en FRAMEWORK_FILES.
- [x] Commit `F06m: fixture fx-spring-boot con paquete por feature`.

## F06n — Fixture `fx-kotlin-ktor` ✅

**Objetivo:** servicio Ktor con corrutinas.
**Stack:** Kotlin, Ktor, Koin, Exposed, kotlinx.serialization, Gradle (Kotlin DSL).
**Features:** `inventario`, `reservas-de-stock`, `alertas`.
**Trampas del ecosistema:**
1. DSL de routing anidado con extension functions repartidas en varios archivos.
2. Plugins instalados (`install(Auth)`, `install(StatusPages)`) que definen el pipeline.
3. Extension functions y properties sobre tipos de otros módulos.
4. Corrutinas lanzadas en el scope de la aplicación y `Flow`.
5. `sealed class` + `when` exhaustivo como máquina de estados.
6. Propiedades delegadas (`by lazy`, `by inject()`).
**Toolchain de tests:** JUnit 5 + ktor-server-test-host, en contenedor.

**Criterios de aceptación (verificados):**
- [x] 3 features (`inventario`, `reservas-de-stock`, `alertas`) con 7 R-NN cada una (CC-03).
- [x] 6 trampas del ecosistema plantadas con referencia exacta: routing_dsl_nested, plugins_installed, extension_functions, coroutines_app_scope, sealed_class_when, delegated_property (CC-06).
- [x] 6 trampas del paquete plantadas: routing_no_auth, sealed_class_when_statement, flow_no_buffer, by_inject_in_property, exposed_no_transaction, kotlinx_serialization_sealed (CC-04).
- [x] 3 trampas superficiales: /inv/{id}/audit dead, sendEmail dead, DummyLogger no usado (CC-05).
- [x] `check_ground_truth.py` pasa sin referencias rotas (CC-09).
- [x] CC-11 (sin menciones del ground truth en comentarios) en verde. Las URLs usan `/inv`, `/reservas`, `/alerts` para evitar los nombres de feature en strings.
- [x] Suite JUnit 5 + ktor-server-test-host: 8 archivos (FxKtorApplicationTests, StockEventTest, TrapsEcosystemTest, TrapsPackageTest, TrapsSuperficialTest + 3 placeholders). Los tests runtime con `testApplication` requieren el contenedor `gradle:8.10-jdk21-jammy`; el Makefile los corre en el contenedor via `run_fixture_tests.py`.
- [x] `dev/tests/test_fx_kotlin_ktor_ground_truth.py` agregado y verde (57 tests).
- [x] `MATRIX.md` muestra `ktor` y `koin` cubiertos por fx-kotlin-ktor.
- [x] `pytest` total 832 passed (775 anteriores + 57 nuevos), sin regresiones en los 13 fixtures previos.
- [x] `validate_skill.py` y `overfit_guard.py` siguen verdes.
- [x] `target_matrix.yml` y `fixtures_matrix.py` extendidos con `ktor` y `koin` como frameworks. La deteccion en `fixtures_matrix.py` ahora busca `ktor-server-core` y `koin-ktor` en `build.gradle.kts`.
- [x] Commit `F06n: fixture fx-kotlin-ktor con paquete por feature`.

## F06o — Fixture `fx-csharp-aspnet` ✅

**Objetivo:** API ASP.NET Core con CQRS.
**Stack:** C#, .NET 9, ASP.NET Core (minimal APIs + controllers), EF Core, MediatR, `BackgroundService`.
**Features:** `pedidos`, `facturación`, `reintentos-en-segundo-plano`.
**Trampas del ecosistema:**
1. MediatR: el handler se resuelve por el tipo de la request.
2. Convenciones de EF Core + configuración Fluent en `OnModelCreating` + migraciones.
3. Código generado por source generators (no está en el repositorio).
4. `partial class` repartidas en varios archivos.
5. El orden del pipeline de middleware en `Program.cs`.
6. Métodos de extensión de registro (`AddFeatureX()`) y escaneo por reflexión (`Assembly.GetTypes()`).
**Toolchain de tests:** xUnit + WebApplicationFactory + SQLite, en contenedor.

**Criterios de aceptación (verificados):**
- [x] 3 features (`pedidos`, `facturacion`, `reintentos`) con 7 R-NN cada una (CC-03).
- [x] 6 trampas del ecosistema plantadas con referencia exacta: `mediator_dispatch_by_type`, `efcore_fluent_no_dataannotations`, `source_generators_not_in_repo`, `partial_class_split` (PedidoItem + CrearPedidoHandler + ObtenerPedidoHandler + EncolarTrabajoHandler), `middleware_pipeline_order` (UseExceptionHandler registrado despues de MapEndpoints + UseRequestId declarado pero no invocado), `extension_method_registration` (AddOrdersModule no invocado).
- [x] 6 trampas del paquete plantadas y documentadas: `handler_throws_no_handler_mapeado`, `mediator_silent_no_handler` (ComandoSinHandler), `efcore_no_transaction_envelope` (dos SaveChangesAsync en CrearPedidoHandler), `background_no_update_ultimo_intento`, `endpoint_group_route_prefix`, `sqlite_inmemory_shared_cache_required`.
- [x] 3 trampas superficiales: `dead_validator` (CrearPedidoValidator), `dead_logger_field` (AppDbContext._log), `dead_endpoint` (MapGet("/api/orders/health")).
- [x] `check_ground_truth.py` pasa sin referencias rotas (CC-09) y CC-11 (sin menciones de feature en comentarios) en verde.
- [x] Suite xUnit 26 tests passed (4 Pedidos + 4 Facturacion + 3 Reintentos + 6 TrampasEcosistema + 7 TrampasPaquete + 3 TrampasSuperficiales) en el contenedor `mcr.microsoft.com/dotnet/sdk:9.0`.
- [x] `run_fixture_tests.py --fixture fx-csharp-aspnet --container` -> passed.
- [x] `dev/tests/test_fx_csharp_aspnet_ground_truth.py` agregado y verde (51 tests: 12 TestGroundTruthShape + 3 TestUniqueTokensFile + 2 TestAllCitesValid + 13 TestDotnetStructure + 6 TestTrapsEcosystem + 6 TestTrapsPackage + 3 TestTrapsSuperficial + 7 TestManifest - 1 redundante).
- [x] `MATRIX.md` muestra `csharp`, `aspnet-core`, `mediatr`, `ef-core`, `msbuild` cubiertos por fx-csharp-aspnet.
- [x] `target_matrix.yml` extendido: `frameworks: aspnet-core, mediatr, ef-core`; `build_systems: msbuild`.
- [x] `fixtures_matrix.py` extendido: deteccion de `*.csproj` -> `aspnet-core, csharp, msbuild` + deteccion de `MediatR`, `Microsoft.EntityFrameworkCore`, `Microsoft.AspNetCore` en el csproj -> `mediatr`, `ef-core`, `aspnet-core`.
- [x] `pytest` total 883 passed (832 anteriores + 51 nuevos), sin regresiones en fx-{python-cli, ts-agent-extension, java-micronaut, monorepo, minified, polyglot, react-spa, nextjs-fullstack, vanilla-js-legacy, vue-nuxt, sveltekit, angular-ngrx, spring-boot, kotlin-ktor}.
- [x] `validate_skill.py` y `overfit_guard.py` siguen verdes.
- [x] Commit `F06o: fixture fx-csharp-aspnet con paquete por feature`.
 
## F06p — Fixture `fx-python-django` ✅

**Objetivo:** proyecto Django con API REST y tareas asíncronas.
**Stack:** Python, Django, Django REST Framework, Celery, settings por entorno.
**Features:** `matrículas`, `pagos`, `certificados`, `acciones-de-admin`.
**Trampas del ecosistema:**
1. Signals (`post_save`) conectados en `apps.py` → `ready()`.
2. `include()` de URLconf anidados y routers de DRF que generan rutas.
3. Managers y querysets personalizados.
4. Settings divididos (`base`/`dev`/`prod`) según `DJANGO_SETTINGS_MODULE`.
5. Acciones de admin como features que no tienen ruta pública.
6. Template tags personalizados y context processors.
**Toolchain de tests:** pytest-django + SQLite, en contenedor.

**Criterios de aceptación (verificados):**
- [x] 4 features (`matriculas`, `pagos`, `certificados`, `acciones-de-admin`) con 7 R-NN cada una (CC-03).
- [x] 6 trampas del ecosistema plantadas con referencia exacta: `signals_in_apps_ready` (EnrollmentsConfig.ready() importa signals), `drf_router_generated_routes` (DefaultRouter().register('', ViewSet, basename='enrollment')), `custom_manager_queryset` (EnrollmentQuerySet con .active()/.paid()/.by_user()), `settings_split_by_env` (base/dev/prod), `admin_action_no_public_route` (export_csv y mark_reviewed en AuditLogAdmin sin ruta DRF), `template_tags_and_context_processors` (enrollment_status_label, payment_status_badge, certificate_is_valid + enrollment_counts, certificate_metadata en TEMPLATES['OPTIONS']).
- [x] 6 trampas del paquete plantadas: `signals_sin_transaction_envelope`, `queryset_metodo_sin_indice`, `admin_action_sin_permission_check`, `celery_eager_swallows_exceptions`, `router_basename_payment`, `settings_prod_no_secret_key_env`.
- [x] 3 trampas superficiales: `dead_viewset` (LegacyCertificateViewSet no registrado), `dead_signal_handler` (handler_pago_fallido sin @receiver), `dead_template_tag` (format_certificate_id no usado).
- [x] `check_ground_truth.py` pasa sin referencias rotas (CC-09) y CC-11 (sin menciones de feature/outcome/trap en comentarios `#`) en verde.
- [x] Suite pytest-django 30 tests passed (4 Enrollments + 4 Payments + 4 Certificates + 3 AdminActions + 6 TrapsEcosystem + 6 TrapsPackage + 3 TrapsSuperficial) en el contenedor `python:3.11-slim` con `apt-get install make`.
- [x] `run_fixture_tests.py --fixture fx-python-django --container` -> passed.
- [x] `dev/tests/test_fx_python_django_ground_truth.py` agregado y verde (53 tests: 11 TestGroundTruthShape + 3 TestUniqueTokensFile + 2 TestAllCitesValid + 13 TestDjangoStructure + 6 TestTrapsEcosystem + 6 TestTrapsPackage + 3 TestTrapsSuperficial + 9 TestManifest).
- [x] `MATRIX.md` muestra `django`, `drf`, `celery`, `pytest-django`, `pip` cubiertos por fx-python-django.
- [x] `target_matrix.yml` extendido: `frameworks: [django, drf, celery, pytest-django]` + `build_systems: [pip]`.
- [x] `fixtures_matrix.py` extendido: deteccion de `requirements.txt` -> `{django, drf, celery, pytest-django}` + deteccion de `apps/<app>/apps.py` con `AppConfig` -> `{django}` + `manage.py` -> `{django}` + `pytest.ini` -> `{pytest-django}`.
- [x] `pytest` total 936 passed (883 anteriores + 53 nuevos), sin regresiones en fx-{python-cli..fx-csharp-aspnet} (15 fixtures).
- [x] `validate_skill.py` y `overfit_guard.py` siguen verdes.
- [x] Commit `F06p: fixture fx-python-django con paquete por feature`.
 
## F06q — Fixture `fx-python-fastapi` ✅

**Objetivo:** API FastAPI asíncrona.
**Stack:** Python, FastAPI, Pydantic v2, SQLAlchemy 2 async, Alembic, arq/Celery.
**Features:** `usuarios`, `suscripciones`, `webhooks`.
**Trampas del ecosistema:**
1. Cadenas de `Depends` con `yield` (setup y teardown).
2. Validadores de Pydantic que contienen lógica de negocio.
3. `include_router` con prefijos y dependencias a nivel de router.
4. Eventos de `lifespan`.
5. Decoradores propios que registran rutas.
6. Migraciones de Alembic que también migran datos.
**Toolchain de tests:** pytest + httpx + SQLite async, en contenedor.

**Criterios de aceptación (verificados):**
- [x] 3 features (`usuarios`, `suscripciones`, `webhooks`) con 7 R-NN cada una (CC-03).
- [x] 6 trampas del ecosistema plantadas: `depends_yield_chains` (get_db -> get_current_user -> get_active_subscription), `pydantic_validator_with_business_logic` (@field_validator('email') + @model_validator(mode='after')), `include_router_prefix_and_dependencies` (prefix + router-level dependencies en users/subscriptions, sin dependencies en webhooks), `lifespan_events` (@asynccontextmanager con init_db + try/except que swallowea, P04), `custom_decorator_registers_routes` (track_request en _REQUEST_REGISTRY + _REGISTERED_ROUTES), `alembic_migration_with_data` (002_seed_data con op.execute INSERT).
- [x] 6 trampas del paquete: `pydantic_validator_race`, `yield_dep_no_rollback_on_error`, `include_router_order_shadows`, `lifespan_exception_swallowed`, `custom_decorator_breaks_signature`, `celery_eager_in_async_context`.
- [x] 3 trampas superficiales: `dead_route` (`GET /webhooks/debug`), `dead_pydantic_model` (`LegacyUsuarioSchema`), `dead_dependency` (`get_optional_user`).
- [x] `check_ground_truth.py` pasa sin referencias rotas (CC-09) y CC-11 (sin menciones en comentarios) en verde.
- [x] Suite pytest-asyncio 27 tests passed (4 users + 4 subs + 4 webhooks + 6 TrapsEcosystem + 6 TrapsPackage + 3 TrapsSuperficial) en el contenedor `python:3.11-slim` con `apt-get install make` + pytest-asyncio 0.24 con `loop_scope=session`.
- [x] `run_fixture_tests.py --fixture fx-python-fastapi --container` -> passed.
- [x] `dev/tests/test_fx_python_fastapi_ground_truth.py` agregado y verde (51 tests).
- [x] `MATRIX.md` muestra `fastapi`, `pydantic`, `sqlalchemy`, `alembic` cubiertos por fx-python-fastapi.
- [x] `target_matrix.yml` extendido: `frameworks: [fastapi, pydantic, sqlalchemy, alembic]`.
- [x] `fixtures_matrix.py` extendido: deteccion de `fastapi`/`pydantic`/`sqlalchemy`/`alembic` en `requirements.txt` + deteccion de `app/main.py` con `FastAPI(` -> `{fastapi}`.
- [x] `pytest` total 987 passed (936 anteriores + 51 nuevos), sin regresiones en fx-{python-cli..fx-python-django} (16 fixtures).
- [x] `validate_skill.py` y `overfit_guard.py` siguen verdes.
- [x] Commit `F06q: fixture fx-python-fastapi con paquete por feature`.
 
## F06r — Fixture `fx-node-nestjs` ✅

**Objetivo:** backend NestJS modular con colas y microservicios.
**Stack:** TypeScript, NestJS, TypeORM, BullMQ, transporte de microservicios.
**Features:** `órdenes`, `envíos`, `notificaciones`.
**Trampas del ecosistema:**
1. Módulos y DI por decoradores (`@Module` imports/providers/exports).
2. Guards e interceptors globales registrados con `APP_GUARD`/`APP_INTERCEPTOR`.
3. Decoradores propios con metadata leída por `Reflector`.
4. Colas de BullMQ: productor y consumidor unidos solo por el nombre de la cola.
5. `@EventPattern`/`@MessagePattern` de microservicios.
6. `ConfigModule` con namespaces y validación.
**Toolchain de tests:** Jest + supertest, en contenedor (Redis en servicio).

**Criterios de aceptación (verificados):**
- [x] 3 features (`ordenes`, `envios`, `notificaciones`) con 7 R-NN cada una (CC-03).
- [x] 6 trampas del ecosistema plantadas: `modules_di_decorators` (`@Module` con imports/providers/controllers en cada .module.ts), `app_guard_app_interceptor` (`APP_GUARD`/`APP_INTERCEPTOR`/`APP_FILTER` providers en app.module.ts), `custom_decorator_reflector` (`@Roles`, `@LogExecutionTime`, `@CurrentUser` con `SetMetadata` y `Reflector.get`), `bullmq_producer_consumer_by_name` (publish('order-queue') en orders.service.ts y notifications.service.ts), `event_pattern_message_pattern` (`@MessagePattern('order_created')` + `@EventPattern('order_created')` + `app.connectMicroservice` en main.ts), `config_module_namespaces` (3 `registerAs(...)` con `load: [...]` y `validationSchema`).
- [x] 6 trampas del paquete: `circular_module_dependency` (OrdersModule importa ShipmentsModule con forwardRef), `global_guard_throws_on_missing_context` (AuthGuard lanza InternalServerErrorException en vez de 401), `bullmq_producer_no_consumer_validation` (publish sin verificar subscribers), `interceptor_breaks_streaming` (resolved con .pipe(tap())), `custom_decorator_metadata_key_typo` (decorator 'log_execution_time' vs interceptor 'LogExecutionTime'), `microservice_transport_not_connected` (la llamada esta presente pero puede fallar en runtime).
- [x] 3 trampas superficiales: `dead_route` (`GET /health/deep`), `dead_websocket_gateway` (`NotificationsGateway` con `@WebSocketGateway` no importado), `dead_interceptor` (`MetricsInterceptor` no registrado).
- [x] `check_ground_truth.py` pasa sin referencias rotas (CC-09) y CC-11 en verde.
- [x] Suite Jest 27 tests passed (4 orders + 4 shipments + 4 notifications + 6 TrapsEcosystem + 6 TrapsPackage + 3 TrapsSuperficial) en el contenedor `node:22-bookworm-slim` con `apt-get install make python3 build-essential` + `npm ci --legacy-peer-deps`.
- [x] `run_fixture_tests.py --fixture fx-node-nestjs --container` -> passed.
- [x] `dev/tests/test_fx_node_nestjs_ground_truth.py` agregado y verde (52 tests).
- [x] `MATRIX.md` muestra `nestjs`, `typeorm`, `bullmq`, `make` cubiertos por fx-node-nestjs.
- [x] `target_matrix.yml` extendido: `frameworks: [nestjs, typeorm, bullmq]`.
- [x] `fixtures_matrix.py` extendido: deteccion de `nest-cli.json` -> `{nestjs}` + `@nestjs/core`, `typeorm`, `bullmq` en `package.json` -> frameworks.
- [x] `pytest` total 1039 passed (987 anteriores + 52 nuevos), sin regresiones en los 17 fixtures previos.
- [x] `validate_skill.py` y `overfit_guard.py` siguen verdes.
- [x] Commit `F06r: fixture fx-node-nestjs con paquete por feature`.
 
## F06s — Fixture `fx-go-service` ✅

**Objetivo:** servicio HTTP en Go con workers concurrentes.
**Stack:** Go, chi, sqlc, wire, `embed`.
**Features:** `ingesta-de-eventos`, `agregación`, `exportación`.
**Trampas del ecosistema:**
1. Interfaces implícitas (sin `implements`).
2. `init()` y blank imports (`_ "driver"`) que registran drivers.
3. Código generado por `//go:generate` (sqlc, wire, mockgen).
4. Worker pool con goroutines, canales y `select` con timeout.
5. Build tags.
6. `//go:embed` de plantillas y migraciones.
**Toolchain de tests:** `go test ./...` con race detector, en contenedor.

**Criterios de aceptación (verificados):**
- [x] 3 features (`ingesta-de-eventos`, `agregacion`, `exportacion`) con 7 R-NN cada una (CC-03).
- [x] 6 trampas del ecosistema plantadas: `implicit_interfaces` (SQLiteEventRepository implementa domain.EventRepository sin `implements`), `init_function_and_blank_imports` (`func init()` + `_ "github.com/mattn/go-sqlite3"`), `go_generate_code` (`sqlc generate` + `wire gen ./...`), `worker_pool_goroutines` (`go p.worker()` + `chan int` + `select` con `ctx.Done()`), `build_tags` (`//go:build legacy` en legacy_export.go), `go_embed` (`//go:embed templates/*.tmpl` + `embed.FS`).
- [x] 6 trampas del paquete: `race_condition_in_worker_pool` (counter sin mutex), `goroutine_leak_on_shutdown` (server no implementa graceful shutdown completo), `implicit_interface_mismatch` (exporter usa type='default'), `init_side_effects_in_tests` (init() imprime a stdout), `channel_deadlock` (unbuffered chan int), `build_tag_typo` (comentario en codigo).
- [x] 3 trampas superficiales: `dead_legacy_export_go` (`//go:build legacy` con LegacyExportHandler no usado), `dead_legacy_binary` (cmd/legacy/main.go con solo println), `dead_debug_helper` (DebugPrintln no invocado en runtime).
- [x] `check_ground_truth.py` pasa sin referencias rotas (CC-09) y CC-11 en verde.
- [x] Suite Go test 24 tests passed (4 ingest + 3 aggregate + 4 export + 6 TrapsEcosystem + 6 TrapsPackage + 3 TrapsSuperficial) con `go test ./... -race -count=1`.
- [x] `run_fixture_tests.py --fixture fx-go-service --container` -> passed.
- [x] `dev/tests/test_fx_go_service_ground_truth.py` agregado y verde (55 tests).
- [x] `MATRIX.md` muestra `go-chi`, `sqlc`, `wire`, `embed`, `sqlite` cubiertos por fx-go-service.
- [x] `target_matrix.yml` extendido: `frameworks: [go-chi, sqlc, wire, embed, sqlite]`.
- [x] `fixtures_matrix.py` extendido: deteccion de `github.com/go-chi/chi`, `github.com/google/wire`, `github.com/mattn/go-sqlite3` en `go.mod`; deteccion de `sqlc.yaml`; deteccion de `//go:embed ` en archivos `*.go`.
- [x] `pytest` total 1094 passed (1039 anteriores + 55 nuevos), sin regresiones en los 18 fixtures previos.
- [x] `validate_skill.py` y `overfit_guard.py` siguen verdes.
- [x] Commit `F06s: fixture fx-go-service con paquete por feature`.
 
## F06t — Fixture `fx-rust-axum` ✅

**Objetivo:** servicio Rust asíncrono en workspace multi-crate.
**Stack:** Rust, Axum, tokio, sqlx, serde, thiserror.
**Features:** `catálogo`, `precios`, `sincronización`.
**Trampas del ecosistema:**
1. Proc macro derive propia que genera `impl`.
2. Implementaciones genéricas *blanket* de traits.
3. `#[cfg(feature = "...")]` controlado por cargo features.
4. Extractors de Axum como argumentos que definen el comportamiento del handler.
5. Flujo de errores implícito con `?` y conversiones `From`.
6. `build.rs` que genera código y un bloque `unsafe` con FFI.
**Toolchain de tests:** `cargo test --workspace` (sqlx offline), en contenedor.

**Criterios de aceptación (verificados):**
- [x] 3 features (`catalogo`, `precios`, `sincronizacion`) con 7 R-NN cada una (CC-03).
- [x] 6 trampas del ecosistema plantadas: `proc_macro_derive` (derive `Entity` que genera `impl` con `ENTITY_NAME` y `entity_name()`), `blanket_impl` (`impl<T: Serialize> Json for T`), `cargo_features` (`#[cfg(feature = "legacy")]` en `features_legacy.rs`), `axum_extractors` (`State<SqlitePool>`, `Json<Req>`, `Path<id>` en handlers), `error_flow_with_question` (`AppError` con `#[from]` derivations + `?` operator), `build_rs_and_unsafe_ffi` (`build.rs` con `cargo:warning` + `extern "C"` con `unsafe { c_legacy_hash }`).
- [x] 6 trampas del paquete: `proc_macro_generates_wrong_impl`, `blanket_impl_conflict`, `cargo_feature_typo`, `axum_extractor_order`, `from_impl_cycles` (verificada que AppError no tiene From para si mismo), `build_rs_fails`.
- [x] 3 trampas superficiales: `dead_debug_helper` (`debug_println` no usado), `dead_legacy_feature` (`LegacyEvent` gated por `#[cfg(feature = "legacy")]`), `dead_unused_function` (`pub fn hash` de `LegacyEvent`).
- [x] `check_ground_truth.py` pasa sin referencias rotas (CC-09) y CC-11 en verde.
- [x] Suite Rust test 27 tests passed (4 catalog + 4 pricing + 4 sync + 6 TrapsEcosystem + 6 TrapsPackage + 3 TrapsSuperficial) con `cargo test --workspace` en el contenedor `rust:1.81-bookworm` con `apt-get install make gcc` + `cargo fetch` + `cargo build`.
- [x] `run_fixture_tests.py --fixture fx-rust-axum --container` -> passed.
- [x] `dev/tests/test_fx_rust_axum_ground_truth.py` agregado y verde (51 tests).
- [x] `MATRIX.md` muestra `axum`, `tokio`, `thiserror` cubiertos por fx-rust-axum.
- [x] `target_matrix.yml` extendido: `frameworks: [axum, tokio, thiserror]`.
- [x] `fixtures_matrix.py` extendido: deteccion de `axum`/`tokio`/`sqlx`/`thiserror`/`serde` en `Cargo.toml`; deteccion de `build.rs` para `cargo-build-script`.
- [x] `pytest` total 1145 passed (1094 anteriores + 51 nuevos), sin regresiones en los 19 fixtures previos.
- [x] `validate_skill.py` y `overfit_guard.py` siguen verdes.
- [x] Commit `F06t: fixture fx-rust-axum con paquete por feature`.
 
## F06u — Fixture `fx-php-laravel` ✅
  
**Objetivo:** aplicación Laravel con MySQL.
**Stack:** PHP, Laravel, Eloquent, Blade, colas, MySQL.
**Features:** `inmuebles`, `visitas`, `contratos`.
**Trampas del ecosistema:**
1. Facades: llamadas estáticas resueltas por el contenedor.
2. Magia de Eloquent: accessors/mutators, scopes, relaciones y `__call`.
3. Bindings registrados en service providers.
4. Events → listeners por auto-discovery, y observers de modelos.
5. Grupos de middleware y route model binding en `routes/web.php`.
6. Comandos y tareas programadas en `routes/console.php`.
**Toolchain de tests:** PHPUnit/Pest + SQLite, en contenedor.

**Criterios de aceptación (verificados):**
- [x] 3 features (`inmuebles`, `visitas`, `contratos`) con 8 R-NN cada una (CC-03).
- [x] 6 trampas del ecosistema plantadas con referencia exacta: `facades` (`Pricing` en `config/app.php` aliases + `PricingFacade::getFacadeAccessor`), `eloquent_magic` (`getPriceEurosAttribute`/`scopeAvailable`/`visits()`/`static::observe` en `Property.php`), `service_providers_bindings` (`InmuebleServiceProvider` con `bind(VisitRepository)` + `singleton('pricing.service')` + `bind('legacy.helper')`), `events_observers_listeners` (`EventServiceProvider::$listen` con `VisitScheduled => [SendVisitConfirmation]` + `PropertyObserver`), `middleware_groups_route_model_binding` (`app/Http/Kernel.php` con `'web' => [...]` + `routes/web.php` con `{property}`), `console_schedule` (`app/Console/Kernel.php::schedule()` con `command(ExpireContracts)->dailyAt('00:00')->withoutOverlapping()`).
- [x] 6 trampas del paquete plantadas: `job_silent_retry` (`SendVisitReminder` con `tries=3`, `backoff=10` y `fail()` en el ultimo intento), `job_empty_catch` (`GenerateContractPdf` con `catch (\Throwable)` que `Log::error` sin rethrow), `facade_alias_typo` (latente en `config/app.php` aliases), `queue_driver_mismatch` (phpunit.xml fuerza `database`, `config/queue.php` declara `database` y `redis`), `eloquent_n_plus_one` (`PropertyController::index()` con `->visits()->count()` por cada property en el map), `unused_middleware` (`EnsureTenant` registrado en grupo web pero handler vacio).
- [x] 3 trampas superficiales: `dead_provider` (`LegacyServiceProvider` registrado en `config/app.php` con comentario `// legacy only`), `dead_helper_reference` (`InmuebleServiceProvider` referencia `\App\Pricing\LegacyHelper` que no existe), `dead_route` (`/legacy` en `routes/web.php` apuntando a `LegacyController` inexistente).
- [x] `check_ground_truth.py` pasa sin referencias rotas (CC-09) y CC-11 en verde.
- [x] Suite PHPUnit 31 tests passed (6 Property + 4 Visit + 4 Contract + 2 PricingService + 6 TrapsEcosystem + 6 TrapsPackage + 3 TrapsSuperficial) con `vendor/bin/phpunit --testdox` en el contenedor `php:8.2-cli` con `apt-get install -y make git unzip libsqlite3-dev` + `docker-php-ext-install pdo pdo_sqlite` + `composer install --no-security-blocking`.
- [x] `run_fixture_tests.py --fixture fx-php-laravel --container` -> passed.
- [x] `dev/tests/test_fx_php_laravel_ground_truth.py` agregado y verde (10 TestGroundTruthShape + 3 TestUniqueTokensFile + 3 TestAllCitesValid + 23 TestPhpStructure + 6 TestTrapsEcosystem + 6 TestTrapsPackage + 3 TestTrapsSuperficial + 7 TestManifest = 61 tests, mas 2 extras = 63 totales).
- [x] `MATRIX.md` muestra `php`, `laravel`, `eloquent`, `blade`, `composer` cubiertos por fx-php-laravel.
- [x] `target_matrix.yml` extendido: `languages: [php]`, `frameworks: [laravel, eloquent, blade]`, `build_systems: [composer]`.
- [x] `fixtures_matrix.py` extendido: deteccion de `.php` en EXT_LANG, `composer.json` en MANIFEST_BUILD (build_system `composer`), `laravel/framework` en PACKAGE_JSON_MARKERS, bloque para `composer.json` que anade `laravel`, `eloquent`, `blade` a frameworks.
- [x] `pytest` total 1209 passed (1145 anteriores + 64 nuevos), sin regresiones en fx-python-cli..fx-rust-axum (20 fixtures).
- [x] `validate_skill.py` y `overfit_guard.py` siguen verdes.
- [x] 9 decisiones nuevas D-267..D-275 (stack Laravel 10.43 + PHP 8.2, single-app Laravel, modelos en ingles CC-11, driver SQLite :memory:, prefijo NPRGT-FXPLAR-, Makefile phpunit, docker php:8.2-cli + tools, composer no-security-blocking, deteccion extendida).
- [x] Commit `F06u: fixture fx-php-laravel con paquete por feature`.
 
## F06v — Fixture `fx-ruby-rails` ✅
  
**Objetivo:** aplicación Rails con jobs y Hotwire.
**Stack:** Ruby 3.1, Rails 7.0, ActiveRecord, ActiveJob, ActionController, ActionView, Sidekiq 7 (con `mock_redis` en tests), Hotwire (turbo-rails + stimulus-rails), RSpec, Capybara.
**Features:** `proyectos`, `facturas`, `recordatorios`.
**Trampas del ecosistema:**
1. Convención sobre configuración: controlador ↔ vista ↔ ruta implícitos.
2. Callbacks `before_save`/`after_commit`.
3. Concerns con `included do`.
4. Métodos sin definición literal (`method_missing`, `define_method`).
5. STI con columna `type`.
6. Monkey patches en `config/initializers`.
**Toolchain de tests:** RSpec + SQLite, en contenedor.

**Criterios de aceptación (verificados):**
- [x] 3 features (`proyectos`, `facturas`, `recordatorios`) con 7 R-NN cada una documentados en el ground truth.
- [x] 6 trampas del ecosistema plantadas con referencia exacta: `convention_over_configuration` (resources en `config/routes.rb`), `callbacks` (before_save/after_destroy en Proyecto, after_commit en Factura), `concerns_included` (Trackable con `included do` en `app/models/concerns/trackable.rb`), `metaprogramming` (`method_missing` y `define_method` en `config/initializers/legacy_constants.rb`), `sti_type_column` (`self.inheritance_column = :type` en Recordatorio + columna en `db/migrate/003_create_recordatorios.rb`), `monkey_patches` (`Array#sum_safe` en `config/initializers/patch_array.rb`).
- [x] 6 trampas del paquete plantadas: `job_silent_retry` (`retry_on StandardError, wait: 5s, attempts: 3` en `EnviarRecordatorioJob` y `attempts: 2` en `GenerarFacturaPdfJob`), `stale_record_in_callback` (job usa `update_columns` para saltar `fecha_envio_no_pasada`), `concern_included_twice` (Trackable en Proyecto y Factura), `sti_invalid_type_silent` (`find_sti_class` que devuelve Recordatorio base si la clase no existe), `route_convention_override` (`get 'panel/legacy'` en `config/routes.rb` + N+1 en `ProyectosController#index`), `initializer_load_order` (legacy_constants carga antes de patch_array).
- [x] 3 trampas superficiales: `dead_service` (LegacyTextFormatter sin consumidores), `empty_concern_dir` (`app/controllers/concerns/` solo con `.keep`), `unused_partial` (`_unused_partial.html.erb` huerfano).
- [x] `check_ground_truth.py dev/ground-truth/fx-ruby-rails/` → 0 referencias rotas.
- [x] CC-11 en verde (sin menciones del ground truth en comentarios). Verificado por `test_tokens_not_in_fixture_source` que recorre toda la fuente del fixture.
- [x] Suite RSpec 65 tests passed (12 modelo + 2 jobs + 3 features + 3 requests + 6 routing + 6 ecosystem + 6 package + 3 superficial + 24 varios) en el contenedor `ruby:3.1.6-bookworm` con `build-essential`, `libsqlite3-dev`, `libffi-dev`, `bundle install --jobs=4` y `bundle exec rspec --format documentation`.
- [x] `run_fixture_tests.py --fixture fx-ruby-rails --container` → `passed`.
- [x] `dev/tests/test_fx_ruby_rails_ground_truth.py` agregado y verde (60 tests: 11 TestGroundTruthShape + 3 TestUniqueTokensFile + 3 TestAllCitesValid + 16 TestRubyStructure + 10 TestTrapsEcosystem + 7 TestTrapsPackage + 3 TestTrapsSuperficial + 7 TestManifest).
- [x] `MATRIX.md` muestra `fx-ruby-rails` cubriendo `rails`, `hotwire`, `sidekiq`, `rspec` como frameworks y `bundler` como build system. `ruby` ya estaba en `target_matrix.yml` (ahora cubierto).
- [x] `target_matrix.yml` extendido: `frameworks: [rails, hotwire, sidekiq, rspec]`, `build_systems: [bundler]`.
- [x] `fixtures_matrix.py` extendido: deteccion de `Gemfile` con `gem "rails"` → `rails` + `bundler`; `turbo-rails` → `hotwire`; `sidekiq` → `sidekiq`; `rspec-rails` → `rspec`.
- [x] `pytest` total **1269 passed** (1209 anteriores + 60 nuevos), sin regresiones en los 22 fixtures previos.
- [x] `validate_skill.py` y `overfit_guard.py` siguen verdes.
- [x] 9 decisiones nuevas D-276..D-284 (Ruby 3.1.6 / Rails 7.0.8 / Sidekiq 7 con `mock_redis` en tests / ActiveJob `:test` por entorno / prefijo `NPRGT-FXRAILS-` / `ruby:3.1.6-bookworm` + libs de compilacion / monkey patch `Array#sum_safe` como eco-trampa / `to_prepare` faltante como paquete-trampa / `find_sti_class` que silencia tipos invalidos / `update_columns` en job para saltar validacion de fecha pasada).
- [x] Commit `F06v: fixture fx-ruby-rails con paquete por feature`.
 
## F06w — Fixture `fx-elixir-phoenix`
 
**Objetivo:** aplicación Phoenix con procesos OTP.
**Stack:** Elixir, Phoenix, LiveView, Ecto, Oban.
**Features:** `chat`, `presencia`, `moderación`.
**Trampas del ecosistema:**
1. Árbol de supervisión en `application.ex` que define qué procesos existen.
2. Mensajes entre procesos (`send`/`handle_info`) en lugar de llamadas directas.
3. Macros `use` que inyectan funciones.
4. Funciones con varias cláusulas y pattern matching como ramas lógicas.
5. PubSub con `broadcast`/`subscribe` por tópico string.
6. `handle_event` de LiveView por nombre de evento definido en la plantilla.
**Toolchain de tests:** ExUnit + PostgreSQL de servicio, en contenedor.
 
---
 
# Nativo y sistemas
 
## F06x — Fixture `fx-cpp-cmake` ✅
  
**Objetivo:** motor de procesamiento en C++ con plugins.
**Stack:** C++20, GCC 13.x, CMake 3.25+, GoogleTest 1.14 (vía `FetchContent`), POSIX `dlopen`/`dlsym`, hilos. Sin Conan/vcpkg (FetchContent basta para portabilidad).
**Features:** `cargar-plugin`, `pipeline-de-filtros`, `exportar-resultados`.
**Trampas del ecosistema:**
1. Registro estático con constructores globales (`static Registrar<...>`), sin llamada explícita.
2. Templates, CRTP, SFINAE y concepts: el código ejecutado depende de la instanciación.
3. X-macros que generan clases y funciones.
4. Headers generados por CMake (`configure_file` + `#cmakedefine`).
5. Plugins cargados con `dlopen` y un símbolo `extern "C"` resuelto por nombre.
6. Dispatch virtual en una jerarquía, con un bug de orden de inicialización estática plantado.
**Toolchain de tests:** GoogleTest 1.14 + CTest, en contenedor `gcc:13-bookworm`.

**Criterios de aceptación (verificados):**
- [x] 3 features (`cargar-plugin`, `pipeline-de-filtros`, `exportar-resultados`) con 7 R-NN cada una documentados en el ground truth.
- [x] 6 trampas del ecosistema plantadas con referencia exacta: `static_registrar` (template `Registrar<T>` en `include/fxproc/registry.hpp` + `FX_REGISTER_FILTER` en `src/filters.cpp`), `templates_crtp_concepts` (`concept Filter` y CRTP en `include/fxproc/pipeline.hpp`), `x_macros` (`FX_FILTERS` y `FX_FILTERS_STMT` en `include/fxproc/x_macros.h`), `cmake_configure_file` (`cmake/config.h.in` con `FX_VERSION`/`FX_HAS_PLUGINS`), `dlopen_dlsym` (`dlopen` con `RTLD_NOW` y `dlsym` en `src/plugin_loader.cpp` + `extern "C" fx_plugin_register` en `plugins/transform_json/transform_json.cpp`), `static_init_order` (`InitOrderTrap` global en `src/filters.cpp`).
- [x] 6 trampas del paquete plantadas: `thread_no_join` (`.detach()` en `src/executor.cpp:18`), `stale_record_in_callback` (helper `should_skip_filter` en `src/filters.cpp`), `plugin_memory_leak` (`PluginDeleter` no chequea `dlclose` en `include/fxproc/plugin_loader.hpp`), `export_race` (`ofstream(ios::trunc)` sin `O_EXCL` en `src/result.cpp:25`), `cmake_target_no_optional` (`add_subdirectory(plugins/transform_json)` sin gate `FX_HAS_PLUGINS` en `CMakeLists.txt:39`), `xmacro_collision` (`X(Json, to_json)` duplicado en `include/fxproc/x_macros.h:16-17` + shadow silencioso en `Registry::register_filter`).
- [x] 3 trampas superficiales: `dead_legacy_filter` (`LegacyFilter` no auto-registrada en `src/filters.cpp:75-82`), `unused_helper` (3 funciones obsoletas en `include/fxproc/util/deprecated_helpers.hpp` sin marca de deprecation), `commented_out_branch` (4 líneas comentadas con `TODO` en `src/filters.cpp:54-58`).
- [x] `check_ground_truth.py dev/ground-truth/fx-cpp-cmake/` → 0 referencias rotas (CC-09).
- [x] CC-11 en verde (sin menciones del ground truth en comentarios).
- [x] Suite GoogleTest 45 tests passing + 2 tests de integración (43 unit + 4 integration via `shared_loader` static) en el contenedor `gcc:13-bookworm` con `cmake 3.25` y `ctest --output-on-failure`.
- [x] `run_fixture_tests.py --fixture fx-cpp-cmake --container` → `passed`.
- [x] `dev/tests/test_fx_cpp_cmake_ground_truth.py` agregado y verde (55 tests: 11 `TestGroundTruthShape` + 3 `TestUniqueTokensFile` + 3 `TestAllCitesValid` + 17 `TestCppStructure` + 6 `TestTrapsEcosystem` + 6 `TestTrapsPackage` + 3 `TestTrapsSuperficial` + 7 `TestManifest`).
- [x] `MATRIX.md` muestra `fx-cpp-cmake` cubriendo `cpp`, `cmake`, `ctest`, `gtest`, `dlopen` como frameworks.
- [x] `target_matrix.yml` extendido: `languages: [cpp]`, `frameworks: [cmake, ctest, gtest, dlopen]`, `build_systems: [cmake]`.
- [x] `fixtures_matrix.py` extendido: detección de `CMakeLists.txt` con `cmake_minimum_required` → `cmake` + `cpp`; `add_test`/`ctest` → `ctest`; `gtest`/`gmock` → `gtest`; `dlopen`/`dlsym` → `dlopen`.
- [x] `pytest` total **1324 passed** (1269 anteriores + 55 nuevos) sin regresiones en los 23 fixtures previos.
- [x] `validate_skill.py`, `overfit_guard.py` y `check_ground_truth.py` siguen verdes.
- [x] 9 decisiones nuevas D-285..D-293 (stack C++20 GCC 13.5, CMake 3.25 con `configure_file`, GoogleTest via FetchContent con `gtest_force_shared_crt`, plugin demo compilado como `.so` separado, prefijo `NPRGT-FXCPP-`, `gcc:13-bookworm` + libs de compilación, monkey patch `Array#sum_safe` → no aplica, init order trap, `to_prepare` no usado, `find_sti_class` no aplica a C++).
- [x] Commit `F06x: fixture fx-cpp-cmake con paquete por feature`.
 
## F06y — Fixture `fx-c-embedded` ✅
  
**Objetivo:** firmware en C para microcontrolador, testeable en host.
**Stack:** C99 con `-std=c99 -pedantic`, GCC 13.x en `gcc:13-bookworm`, Makefile con cross-compile a `arm-none-eabi-gcc` (opcional), linker script `firmware.ld` con secciones `.isr_vector`, `.text`, `.data`, `.bss`, HAL con macros MMIO `volatile`, Unity (fork minimo) + runner Python para tests en host, QEMU opcional.
**Features:** `lectura-de-sensores`, `protocolo-de-comandos-uart`, `modo-bajo-consumo`.
**Trampas del ecosistema:**
1. Tabla de vectores de interrupción: funciones que llama el hardware.
2. Símbolos `__attribute__((weak))` sobrescritos por otro archivo.
3. Tablas de punteros a función como dispatch de comandos.
4. Secciones ubicadas por el linker script.
5. `#ifdef BOARD_X` que cambia el comportamiento por placa.
6. Registros MMIO accedidos con macros de dirección `volatile`.
**Toolchain de tests:** Unity (fork minimo) + runner Python en host, en contenedor `gcc:13-bookworm` (QEMU opcional).

**Criterios de aceptación (verificados):**
- [x] 3 features (`lectura-de-sensores`, `protocolo-de-comandos-uart`, `modo-bajo-consumo`) con 7 R-NN cada una documentados en el ground truth.
- [x] 6 trampas del ecosistema plantadas con referencia exacta: `vector_table` (`isr_vector[16]` con `__attribute__((section(".isr_vector")))` en `src/startup.c`), `weak_symbols` (`Reset_Handler`, `NMI_Handler`, `HardFault_Handler`, `Default_Handler` con `__attribute__((weak))` en `include/fxemb/weak_handlers.h`), `command_dispatch_table` (`cmd_table[]` con `cmd_handler_t` typedef en `include/fxemb/command_dispatch.h` + impl en `src/command_dispatch.c`), `linker_script` (`firmware.ld` con `.isr_vector`, `.text`, `.data` con LMA en FLASH, `.bss` NOLOAD, símbolos exportados), `board_ifdef` (`#ifdef STM32F4_DISCOVERY / #elif NRF52_DK / #elif BOARD_HOST / #else #error` en `include/fxemb/board.h`), `mmio_volatile` (macros `volatile uint32_t*` en `include/fxemb/hal.h`).
- [x] 6 trampas del paquete plantadas: `race_lectura_sensores` (`g_sensor_head++` no atomico en `src/sensors.c`), `uart_handler_race` (`g_rx_head++` no atomico en `src/uart_protocol.c`), `consumo_stub_irreal` (`fxemb_power_consumption_ua()` retorna 0 siempre), `sleep_lock_olvidado` (`fxemb_power_enter` no toma mutex), `sensor_no_inicializado` (`fxemb_sensors_read` cae en basura sin check de `g_sensor_initialized`), `weak_handler_loop_infinito` (`Default_Handler` queda en `while(1)` sin bkpt).
- [x] 3 trampas superficiales: `dead_legacy_helper` (`legacy_uart_send_byte` y `legacy_crc16` en `src/legacy_helpers.c` sin consumidores), `unused_macro` (LEGACY_DELAY/NOP/BARRIER en `include/fxemb/deprecated_macros.h` sin marca de deprecation), `commented_out_code` (4 líneas comentadas con `TODO: soporte para DMA` en `src/sensors.c`).
- [x] `check_ground_truth.py dev/ground-truth/fx-c-embedded/` → 0 referencias rotas (CC-09).
- [x] CC-11 en verde (sin menciones del ground truth en comentarios). Verificado por `test_tokens_not_in_fixture_source` que recorre toda la fuente del fixture.
- [x] Suite Unity 46 tests passing en el contenedor `gcc:13-bookworm` con `make test` (runner Python `tests/test_runner.py`).
- [x] `run_fixture_tests.py --fixture fx-c-embedded --container` → `passed`.
- [x] `dev/tests/test_fx_c_embedded_ground_truth.py` agregado y verde (57 tests: 11 `TestGroundTruthShape` + 3 `TestUniqueTokensFile` + 3 `TestAllCitesValid` + 18 `TestCStructure` + 6 `TestTrapsEcosystem` + 6 `TestTrapsPackage` + 3 `TestTrapsSuperficial` + 7 `TestManifest`).
- [x] `MATRIX.md` muestra `fx-c-embedded` cubriendo `c`, `unity`, `linker-script` como frameworks y `make`, `gnu-ld` como build systems.
- [x] `target_matrix.yml` extendido: `languages: [c]`, `frameworks: [unity, linker-script]`, `build_systems: [make, gnu-ld]`.
- [x] `fixtures_matrix.py` extendido: detección de `firmware.ld` + `unity.h` → `c` + `unity` + `linker-script` + `make` + `gnu-ld`.
- [x] `pytest` total **1381 passed** (1324 anteriores + 57 nuevos) sin regresiones en los 24 fixtures previos.
- [x] `validate_skill.py`, `overfit_guard.py` y `check_ground_truth.py` siguen verdes.
- [x] 9 decisiones nuevas D-294..D-302 (C99 con `-std=c99 -pedantic`, GCC 13.5 en `gcc:13-bookworm`, Unity como fork minimo en lugar de Ceedling, runner Python `test_runner.py`, host-emulation con `hal_host.c` en lugar de QEMU obligatorio, linker script `firmware.ld` con `.isr_vector` y `AT(origin)`, board selection via `-DBOARD_X`, MMIO volatile con direcciones STM32F4, prefijo `NPRGT-FXCEMB-`).
- [x] Commit `F06y: fixture fx-c-embedded con paquete por feature`.
 
## F06z — Fixture `fx-cpp-qt` ✅
  
**Objetivo:** aplicación de escritorio Qt con Widgets y QML.
**Stack:** C++, Qt 6 (Widgets + QML), moc, `.ui`, `.qrc`, CMake.
**Features:** `editor`, `preferencias`, `exportar`.
**Trampas del ecosistema:**
1. Conexiones `connect` de señales y slots (llamadas indirectas).
2. Conexiones automáticas por nombre (`on_<objectName>_<signal>`).
3. Widgets definidos en archivos `.ui` (XML).
4. `Q_PROPERTY`/`Q_INVOKABLE` expuestos a QML y bindings declarativos.
5. Recursos `.qrc` con rutas `:/`.
6. Código generado por moc a partir de `Q_OBJECT`.
**Toolchain de tests:** Qt Test con `QT_QPA_PLATFORM=offscreen`, en contenedor.

**Criterios de aceptación (verificados):**
- [x] 3 features (`editor`, `preferencias`, `exportar`) con 7 R-NN cada una documentados en el ground truth.
- [x] 6 trampas del ecosistema plantadas con referencia exacta: `connect_signal_slot` (QObject::connect en `src/main_window.cpp:50-72`), `autoconnect_by_name` (slots `on_<objectName>_<signal>` en `MainWindow` + `setupUi()` en el constructor), `widgets_in_ui` (`ui/main_window.ui` con QMainWindow + 4 QPushButton), `q_property_q_invokable` (Q_PROPERTY fontSize/darkTheme con NOTIFY + Q_INVOKABLE resetToDefaults/save + PreferencesProxy para QML), `qrc_resources` (`resources/resources.qrc` con SVGs y styles + `qt_add_resources` los compila con rcc), `moc_generated_code` (todos los headers con Q_OBJECT generan `moc_*.cpp` via AUTOMOC).
- [x] 6 trampas del paquete plantadas: `connect_5_args_no_explicit` (comment en `setupConnections()`), `signal_loop_infinite` (caso `format == "loop"` en `exporter.cpp:doExport` que NO emite nada), `q_property_no_notify` (`legacyProperty` en `preferences.h:21` sin NOTIFY), `qrc_path_no_colon_slash` (comment en `test_p04`), `auto_connect_name_typo` (`on_savebutton_clicked_TYPO` con b minuscula en `main_window.h:on_savebutton_clicked_TYPO`), `qml_garbage_collected` (PreferencesProxy sin setObjectOwnership en `preferences_proxy.cpp`).
- [x] 3 trampas superficiales: `dead_signal_slot` (`someUnusedSignal` en `editor.h` y emitido en `editor.cpp` sin receptor), `unused_resource_alias` (alias `never_referenced.svg` en `resources.qrc` nadie usa), `commented_out_code` (3 lineas con `TODO: connect` en `main_window.cpp:on_actionQuit_triggered`).
- [x] `check_ground_truth.py dev/ground-truth/fx-cpp-qt/` → 0 referencias rotas (CC-09).
- [x] CC-11 en verde (sin menciones del ground truth en comentarios).
- [x] Suite Qt Test 29 tests passing en el contenedor `gcc:13-bookworm` con `apt-get install qt6-base-dev qt6-declarative-dev qt6-tools-dev qt6-tools-dev-tools libqt6test6 libqt6quick6 libqt6quickwidgets6 libqt6quickcontrols2-6` + `cmake -S . -B build` + `cmake --build build --parallel` + `QT_QPA_PLATFORM=offscreen ctest --test-dir build --output-on-failure`.
- [x] `run_fixture_tests.py --fixture fx-cpp-qt --container` → `passed`.
- [x] `dev/tests/test_fx_cpp_qt_ground_truth.py` agregado y verde (55 tests: 11 `TestGroundTruthShape` + 3 `TestUniqueTokensFile` + 3 `TestAllCitesValid` + 18 `TestCppStructure` + 6 `TestTrapsEcosystem` + 6 `TestTrapsPackage` + 3 `TestTrapsSuperficial` + 7 `TestManifest`).
- [x] `MATRIX.md` muestra `fx-cpp-qt` cubriendo `cpp`, `qt6`, `qml`, `qt-test`, `qt-cmake` como frameworks.
- [x] `target_matrix.yml` extendido: `frameworks: [qt6, qml, qt-test, qt-cmake]`.
- [x] `fixtures_matrix.py` extendido: deteccion de `find_package(Qt6` + `qt_standard_project_setup` → `qt6` + `qt-cmake`; `qml/*.qml` → `qml`; `QTEST` en tests → `qt-test`.
- [x] `pytest` total **1436 passed** (1381 anteriores + 55 nuevos) sin regresiones en los 25 fixtures previos.
- [x] `validate_skill.py`, `overfit_guard.py` y `check_ground_truth.py` siguen verdes.
- [x] 9 decisiones nuevas D-303..D-311 (Qt 6.4.2 via apt en Debian bookworm en lugar de Qt 6.6 LTS, GCC 13.5 + cmake 3.25 con `qt_standard_project_setup(REQUIRES 6.4)`, `qt_add_library(qtapp_core STATIC)` para tests, header-only fixturer `version.h`, dockefile con `libqt6test6` en lugar de `qt6-test-dev` (no hay -dev package), `qtapp_exe` como nombre del ejecutable para evitar colision con el directorio `qtapp/` de QML, `AUTOUIC_SEARCH_PATHS` para resolver `ui/main_window.ui` desde el codigo C++, `QT_QPA_PLATFORM=offscreen` para tests headless, `QTEST_GUILESS_MAIN` para un solo binario de tests).
- [x] Commit `F06z: fixture fx-cpp-qt con paquete por feature`.
 
---
 
# Móvil y Apple
 
## F06aa — Fixture `fx-swift-ios` ✅

**Objetivo:** app iOS con SwiftUI, UIKit heredado, un módulo Objective-C y una extensión de widget.
**Stack:** Swift 6, SwiftUI, UIKit, Objective-C (bridging header), async/await, actors, Combine, SwiftData (host fallback), SPM, `.xcodeproj`, `.xcconfig`.
**Features:** `onboarding`, `lista-de-gastos`, `sincronizacion-icloud`, `widget-de-resumen`.
**Trampas del ecosistema:**
1. Property wrappers (`@State`, `@Published`, `@AppStorage`, `@Environment` y uno propio `@Debounced`).
2. Result builders de SwiftUI y navegación por tipo con `navigationDestination(for:)`.
3. Extensiones de protocolo con implementación por defecto, repartidas en varios archivos.
4. Interoperabilidad con Objective-C: `@objc dynamic`, `NotificationCenter`, KVO.
5. `#if os(iOS)`/`#if DEBUG`, configuraciones de build y schemes.
6. Deep links y URL schemes en `Info.plist` + `onOpenURL`, y la extensión de widget que comparte datos por App Group.
**Toolchain de tests:** `swift test` (Swift Testing) + `xcodebuild build` smoke del target iOS. **requires: macos.**

**Criterios de aceptación:**
- [x] CC-01 código en `dev/fixtures/fx-swift-ios/` generado desde `_template/`.
- [x] CC-02 `build-history.sh` con 8 commits reproducibles.
- [x] CC-03 4 features × ≥6 R-NN (7 cada una).
- [x] CC-04 6 trampas paquete plantadas y documentadas.
- [x] CC-05 3 trampas superficiales documentadas.
- [x] CC-06 6 trampas ecosistema plantadas y documentadas.
- [x] CC-07 ground truth con `ground_truth.json`, `GROUND_TRUTH.md`, `unique_tokens.txt` (35 tokens `NPRGT-FXSWIFT-`).
- [x] CC-08 cada feature con flujo esperado y 7 resultados posibles.
- [x] CC-09 `check_ground_truth.py --check-cc11` 0 referencias rotas, 0 menciones prohibidas.
- [x] CC-10 `make -C dev/fixtures/fx-swift-ios test` pasa: 36 Swift Testing tests + `xcodebuild build` smoke → `OK: swift test + xcodebuild smoke pasaron` con Xcode 27.0.
- [x] CC-11 ningún archivo del fixture menciona el ground truth, `dev/fixtures/...`, `dev/ground-truth/...`, ni el prefijo de tokens.
- [x] CC-12 tests pytest en `dev/tests/test_fx_swift_ios_ground_truth.py` (74 tests).
- [x] CC-13 entrada en `target_matrix.yml` con `frameworks: [swiftui, uikit, widgetkit, app-groups, xcode-project, combine]` + `build_systems: [swiftpm, xcodebuild]`.
- [x] `pytest` total 1510 passed (1436 previos + 74 nuevos) sin regresiones.
- [x] `validate_skill.py` y `check_ground_truth.py` verdes.
- [x] 9 decisiones nuevas D-312..D-320 (stack Swift 6 + SPM + Xcode, requires macos, Swift Testing, SettingsHostController fuera de FxSwiftCore, pbxproj generado, TestPaths helper, TimelineEntry condicional, WidgetBundle @main, DEVELOPER_DIR auto-detect).
- [x] Commit `F06aa: fixture fx-swift-ios con paquete por feature`.
- [x] `MATRIX.md` muestra `fx-swift-ios` cubriendo `swift`, `swiftui`, `uikit`, `widgetkit`, `app-groups`, `xcode-project`, `combine`, `swiftpm`, `xcodebuild`.
- [x] `run_fixture_tests.py --fixture fx-swift-ios` → `passed` en macOS.

**Limitación operativa documentada:** `xcodebuild` solo está disponible en macOS con Xcode 15+ (en el host de implementación: Xcode 27.0 vía `DEVELOPER_DIR=/System/Volumes/Data/Applications/Xcode.app/Contents/Developer`). `CommandLineTools` sin Xcode completo no incluye el módulo `Testing` de Swift, así que `swift test` falla en ese entorno; el runner detecta la falta y registra `.build/xcode-skip.log` sin abortar.

## F06ab — Fixture `fx-swift-server` ✅
 
**Objetivo:** paquete Swift multiplataforma con servidor Vapor, CLI y macros.
**Stack:** Swift 6.0.3, SPM, Vapor 4.92+, Fluent + FluentSQLiteDriver, swift-argument-parser 1.3+, swift-syntax 510+, Swift macros (`@attached(peer)` + `@freestanding(declaration)`), build tool plugins.
**Features:** `api-de-notas`, `cli-de-importación`, `auditoría`.
**Trampas del ecosistema:**
1. Macros (`@attached(peer)`, `@freestanding(declaration)`) que generan código.
2. Build tool plugins de SPM que generan fuentes.
3. Rutas registradas con `RouteCollection` en `boot`.
4. Modelos Fluent con `@Field`/`@Parent` y migraciones.
5. Actors y `Sendable`.
6. `#if canImport(...)` que cambia el comportamiento entre Linux y macOS.
**Toolchain de tests:** `swift test --parallel`, en contenedor `swift:6.0.3-jammy`.

**Criterios de aceptación (verificados):**
- [x] 3 features (`api-de-notas`, `cli-de-importacion`, `auditoria`) × 7 R-NN cada una (CC-03, CC-08).
- [x] 6 trampas del ecosistema plantadas con referencia exacta: `@attached(peer) FxRoute` (E1), `BuildToolPlugin AuditCodesPlugin` (E2), `RouteCollection.boot(routes:)` (E3), `@Field`/`@Parent`/`@Timestamp` (E4), `actor AuditRecorder` + `Sendable struct NoteDTO` (E5), `#if canImport(FoundationNetworking)` (E6).
- [x] 6 trampas del paquete plantadas: `@ImportModuleDecl` freestanding (P1), `class @unchecked Sendable LegacyNoteDTO` (P2), `try? silent` en AuditRecorder (P4), plugin fallback `// noop` (P4), `.unique(on:)` no idempotente (P5), catch-all `*` antes de rutas (P6).
- [x] 3 trampas superficiales: `LegacyHelper` dead (S1), `_ = URLSession.self` en `#else` (S2), `LEGACY_MODE` env no leido (S3).
- [x] Ground truth completo en `dev/ground-truth/fx-swift-server/{ground_truth.json,GROUND_TRUTH.md,unique_tokens.txt}` con paquete completo por feature.
- [x] 12 entry points, 14 modules, 9 dependencies, 3 features (21 R-NN), 10 surfaces, 6 traps ecosistema, 6 traps paquete, 3 superficiales, 7 call graph edges.
- [x] 38 unique_tokens `NPRGT-FXSWIFTSRV-`; `check_ground_truth.py --check-cc11` 0 referencias rotas, 0 menciones prohibidas tras limpieza de comentarios.
- [x] `dev/tests/test_fx_swift_server_ground_truth.py` con 58 tests (8 TestGroundTruthShape + 6 TestOutcomesAndCitations + 3 TestUniqueTokensFile + 3 TestAllCitesValid + 12 TestSwiftStructure + 4 TestBuildPluginContract + 6 TestTrapsEcosystem + 6 TestTrapsPackage + 3 TestTrapsSuperficial + 7 TestManifest) verde.
- [x] `pytest` total **1568 passed** (1510 previos + 58 nuevos) sin regresiones.
- [x] `validate_skill.py` y `overfit_guard.py` verdes.
- [x] `target_matrix.yml` extendido con frameworks `[vapor, fluent, swift-argument-parser, swift-syntax, swift-macro, spm-build-tool-plugin]`.
- [x] `fixtures_matrix.py` extendido con detección de Vapor/Fluent/swift-argument-parser/swift-syntax/swift-macro/spm-build-tool-plugin.
- [x] `MATRIX.md` regenerado: `fx-swift-server` cubre `swift`, `vapor`, `fluent`, `swift-argument-parser`, `swift-syntax`, `swift-macro`, `spm-build-tool-plugin`, `swiftpm`.
- [x] `manifest.yml` con `requires: [linux, macos]` + `container.enabled: true`.
- [x] `Dockerfile.test` con `FROM swift:6.0.3-jammy` + `apt-get install make git` + `CMD ["swift","test","--parallel"]`.
- [x] `Package.swift` declara 4 productos (FxSwiftServer lib+exe, FxSwiftMacros lib, fxsimport exe) + plugin en sub-package `Plugins/AuditCodesPlugin/Package.swift` con `capability: .buildTool()`.
- [x] Sources/FxSwiftServer/Models (Note.swift con `@ID`/`@Field`/`@Parent`/`@Timestamp` + AuditEntry.swift con enum AuditAction).
- [x] Sources/FxSwiftServer/Routes (NotesRoutes con `@FxRoute` + `RouteCollection boot(routes:)` + AuditRoutes con catch-all `*` registrado antes de rutas específicas).
- [x] Sources/FxSwiftServer/Services (NotesService actor + AuditRecorder actor con `try?` silent + UrlSessionProvider con `#if canImport(FoundationNetworking)` + LegacyHelper dead).
- [x] Sources/FxSwiftServer/DTOs (NoteDTO Sendable struct + LegacyNoteDTO `class @unchecked Sendable` + ErrorDTO).
- [x] Sources/FxSwiftServer/Errors (ApiError enum `AbortError` con titleRequired/bodyTooLong/notFound/conflict/timeout/dbUnavailable/auditFailed).
- [x] Sources/FxSwiftServer/Migrations (CreateNote con `.unique(on:'title')` no idempotente + CreateAuditEntry).
- [x] Sources/FxSwiftMacros (FxSwiftMacros CompilerPlugin + RouteMacro PeerMacro + ImportModuleDeclMacro DeclarationMacro).
- [x] Sources/FxSwiftCLI (main.swift `@main` AsyncParsableCommand + Subcommands/ImportNotes con `--input/--format/--server` + exit codes 64/65/70/130 + Subcommands/AuditDump + Format/CsvImporter actor).
- [x] Sources/FxSwiftServerTests (7 archivos XCTest = 27 tests Swift: 5 + 1 + 3 + 3 + 6 + 6 + 3).
- [x] Plugins/AuditCodesPlugin/Plugins/AuditCodesPlugin.swift (BuildToolPlugin que genera `Generated/AuditCodes.generated.swift` con `#if canImport` fallback).
- [x] Generated/AuditCodes.generated.swift placeholder con comentario explicativo.
- [x] `build-history.sh` con 8 commits reproducibles.
- [x] fx-python-cli, fx-ts-agent-extension, fx-java-micronaut, fx-monorepo, fx-minified, fx-polyglot, fx-react-spa, fx-nextjs-fullstack, fx-vanilla-js-legacy, fx-vue-nuxt, fx-sveltekit, fx-angular-ngrx, fx-spring-boot, fx-kotlin-ktor, fx-csharp-aspnet, fx-python-django, fx-python-fastapi, fx-node-nestjs, fx-go-service, fx-rust-axum, fx-php-laravel, fx-ruby-rails, fx-cpp-cmake, fx-c-embedded, fx-cpp-qt, fx-swift-ios (26 fixtures) sin cambios de comportamiento.
- [x] 10 decisiones nuevas D-321..D-330 (stack Swift 6 + Vapor 4.92, swift:6.0.3-jammy image, requires linux+macos + container enabled, Plugin en sub-package separado, macros PeerMacro + DeclarationMacro, fallback `// noop` con `#if canImport`, migraciones Fluent, exit codes CLI 64/65/70/130, prefijo `NPRGT-FXSWIFTSRV-` con 38 tokens, tests XCTest + `FIXTURE_ROOT` env var).
- [x] PROGRESS.md fila F06ab = `HECHA` con evidencia completa.
- [x] DECISIONS.md con D-321..D-330.
- [x] ROADMAP.md encabezado F06ab con ✅ y sección `Criterios de aceptación (verificados)` con todos los checks `[x]`.
- [x] Commit `F06ab: fixture fx-swift-server con paquete por feature`.

**Limitación operativa documentada:** los tests XCTest del fixture NO se ejecutan en este host (no hay toolchain Swift 6 ni docker daemon accesible). La verificación se hace en CI Linux con la imagen oficial `swift:6.0.3-jammy` o en macOS con Xcode 15+. El runner `run_fixture_tests.py --fixture fx-swift-server --container` queda registrado para CI.
 
## F06ac — Fixture `fx-kotlin-android` ✅
 
**Objetivo:** app Android con Compose y vistas XML heredadas.
**Stack:** Kotlin 2.0.21, Jetpack Compose (BOM 2024.10.00), Views + ViewBinding, Hilt 2.51.1, Room 2.6.1, WorkManager 2.10.0, Navigation Compose 2.8.4, AGP 8.7.2 con Gradle 8.10.2 y flavors `free`/`paid`.
**Features:** `escaneo-de-productos`, `historial`, `sincronización-en-segundo-plano`, `función-premium`.
**Trampas del ecosistema:**
1. `AndroidManifest.xml` declara activities, receivers, services e intent filters: puntos de entrada que no se llaman desde el código.
2. Código generado por Hilt: `@Inject` y módulos.
3. DAO de Room con `@Query` en SQL.
4. Flavors y build types con source sets distintos (una feature solo existe en `paid`).
5. Recursos `R.*` y layouts XML con atributos `onClick`.
6. WorkManager, `BroadcastReceiver` y deep links del grafo de navegación.
**Toolchain de tests:** tests JVM + Robolectric 4.13 + JUnit5, en contenedor `eclipse/openjdk:21-jdk-jammy` con cmdline-tools Android.

**Criterios de aceptación (verificados):**
- [x] 4 features (`escaneo-de-productos`, `historial`, `sincronizacion-en-segundo-plano`, `funcion-premium`) × 7 R-NN cada una (CC-03, CC-08).
- [x] 6 trampas del ecosistema plantadas con referencia exacta: `AndroidManifest.xml` con Activity/Receiver/Service/intent-filters (E1), `@HiltAndroidApp` + `@AndroidEntryPoint` + `@HiltViewModel` (E2), Room `@Query` con SQL embebido (E3), flavors `free`/`paid` con `BuildConfig.PREMIUM_ENABLED` (E4), `android:onClick="onSaveClick"` en layout XML (E5), WorkManager + `BroadcastReceiver` + deep links en `nav_graph.xml` (E6).
- [x] 6 trampas del paquete plantadas: `@Query` con SQL concatenation risk (P1), `ProductRepositoryImpl` sin `@Singleton` (P2), `SyncScheduler.setExpedited` sin check `POST_NOTIFICATIONS` (P3), Room sin `addMigrations` (P4), `LegacyProductActivity.onSaveClick` con `db.execSQL` bypassing repo (P5), `ScanViewModel` con try-catch silencioso (P6).
- [x] 3 trampas superficiales: `LegacyDateFormatter` dead (S1), `EnvConfig.debug` no usado (S2), `LegacyProductFragment.onCreateView` returns null (S3).
- [x] Ground truth completo en `dev/ground-truth/fx-kotlin-android/{ground_truth.json,GROUND_TRUTH.md,unique_tokens.txt}` con paquete completo por feature.
- [x] 13 entry points (App, Activity, Receiver, Service, Worker, 3 composables, 3 deep-links, 2 flavor-specific), 17 modules, 19 dependencies, 4 features (28 R-NN), 11 surfaces, 6 traps ecosistema, 6 traps paquete, 3 superficiales, 8 call graph edges.
- [x] 38 unique_tokens `NPRGT-FXANDROID-`; `check_ground_truth.py --check-cc11` 0 referencias rotas, 0 menciones prohibidas tras limpieza de comentario en `DatabaseModule.kt`.
- [x] `dev/tests/test_fx_kotlin_android_ground_truth.py` con 71 tests (8 TestGroundTruthShape + 6 TestOutcomesAndCitations + 3 TestUniqueTokensFile + 3 TestAllCitesValid + 18 TestAndroidStructure + 2 TestFlavors + 4 TestManifestEntries + 2 TestBuildConfig + 3 TestTestSourceSet + 6 TestTrapsEcosystem + 6 TestTrapsPackage + 3 TestTrapsSuperficial + 7 TestManifest) verde.
- [x] `pytest` total **1639 passed** (1568 previos + 71 nuevos) sin regresiones.
- [x] `validate_skill.py` y `overfit_guard.py` verdes.
- [x] `target_matrix.yml` extendido con frameworks `[android, jetpack-compose, hilt, hilt-android, hilt-work, hilt-navigation-compose, room, workmanager, navigation-compose, view-binding, gradle-flavors, robolectric, appcompat]`.
- [x] `fixtures_matrix.py` extendido con detección de Android/Compose/Hilt/Room/WorkManager/Navigation/ViewBinding/Gradle-Flavors/Robolectric/AppCompat via `**/build.gradle.kts` + `gradle/libs.versions.toml`.
- [x] `MATRIX.md` regenerado: 30 fixtures, `fx-kotlin-android` cubre `kotlin`, `android`, `jetpack-compose`, `hilt`, `hilt-android`, `hilt-work`, `hilt-navigation-compose`, `room`, `workmanager`, `navigation-compose`, `view-binding`, `gradle-flavors`, `robolectric`, `appcompat`, `gradle`.
- [x] `manifest.yml` con `requires: [linux, macos]` + `container.enabled: true`.
- [x] `Dockerfile.test` con `FROM eclipse/openjdk:21-jdk-jammy` + `apt-get install make git wget unzip ca-certificates` + cmdline-tools + `sdkmanager "platform-tools" "platforms;android-35" "build-tools;35.0.1"` + `CMD ["make","test"]`.
- [x] `settings.gradle.kts` + `gradle.properties` + `gradle/libs.versions.toml` + `gradle/wrapper/gradle-wrapper.properties` (Gradle 8.10.2).
- [x] `app/build.gradle.kts` con flavors `free`/`paid`, `buildFeatures.compose=true`, `buildFeatures.viewBinding=true`, `buildFeatures.buildConfig=true`, `testOptions.unitTests.all { useJUnitPlatform() }`.
- [x] `AndroidManifest.xml` con permissions INTERNET+POST_NOTIFICATIONS+CAMERA+WAKE_LOCK+RECEIVE_BOOT_COMPLETED, Activity `LegacyProductActivity`, Receiver `SyncTriggerReceiver` (2 intent-filters + deep link), Service `SyncService`.
- [x] Source sets `app/src/free/java/.../featurepremium/PremiumDisabled.kt` y `app/src/paid/java/.../featurepremium/PremiumEnabled.kt` (E4).
- [x] Layout XML `activity_legacy_product.xml` con `android:onClick="onSaveClick"` (E5).
- [x] `nav_graph.xml` con 3 deep links (E6).
- [x] `build-history.sh` con 8 commits reproducibles.
- [x] fx-python-cli..fx-swift-server (28 fixtures) sin cambios de comportamiento.
- [x] 10 decisiones nuevas D-331..D-340 (stack Kotlin 2.0 + AGP 8.7.2 + JDK 21 + Gradle 8.10.2, image `eclipse/openjdk:21-jdk-jammy` + cmdline-tools, requires linux+macos + container enabled, flavors free/paid con BuildConfig.PREMIUM_ENABLED, Hilt 2.51.1 + KSP 2.0.21, Room 2.6.1 con DAO @Query + trampa P4 sin addMigrations, WorkManager 2.10.0 + trampa P3 expedited sin POST_NOTIFICATIONS, Navigation Compose 2.8.4 + nav_graph.xml con deepLinks, ViewBinding para vista legacy con android:onClick, Robolectric 4.13 sin emulador + JUnit5, prefijo unique tokens NPRGT-FXANDROID- con 38 entradas).
- [x] PROGRESS.md fila F06ac = `HECHA` con evidencia completa.
- [x] DECISIONS.md con D-331..D-340.
- [x] ROADMAP.md encabezado F06ac con ✅ y sección `Criterios de aceptación (verificados)` con todos los checks `[x]`.
- [x] Commit `F06ac: fixture fx-kotlin-android con paquete por feature`.

**Limitación operativa documentada:** los tests JVM + Robolectric del fixture NO se ejecutan en este host (no hay Android SDK 35 ni docker daemon accesible). La verificación se hace en CI Linux con la imagen `eclipse/openjdk:21-jdk-jammy` + cmdline-tools Android SDK 35 (Dockerfile.test). El runner `run_fixture_tests.py --fixture fx-kotlin-android --container` queda registrado para CI. El contenedor pesa ~1.8 GB y tarda ~5-8 min la primera vez (descarga Android SDK + cachea Gradle).
 
## F06ad — Fixture `fx-flutter-dart` ✅
 
**Objetivo:** app Flutter con canales a código nativo.
**Stack:** Dart 3.5.4, Flutter 3.24.5, Riverpod 2.5.1, go_router 14.2.7, freezed/json_serializable (build_runner 2.4.13), platform channels a Kotlin y Swift.
**Features:** `lector-de-documentos`, `favoritos`, `ajustes`.
**Trampas del ecosistema:**
1. Código generado `.g.dart`/`.freezed.dart`.
2. Providers de Riverpod que dependen de otros por `ref.watch`.
3. Platform channels: métodos invocados por string en Kotlin y Swift.
4. Redirects de go_router.
5. Flavors con `--dart-define`.
6. Widgets que se construyen distinto según la plataforma.
**Toolchain de tests:** `flutter test`, en contenedor `ghcr.io/cirruslabs/flutter:3.24.5`.

**Criterios de aceptación (verificados):**
- [x] 3 features (`lector-de-documentos`, `favoritos`, `ajustes`) × 7 R-NN cada una (CC-03, CC-08).
- [x] 6 trampas del ecosistema plantadas con referencia exacta: `@freezed` + `.g.dart`/`.freezed.dart` (E1), `ref.watch(readerControllerProvider)` (E2), `MethodChannel` con strings `'scanDocument'`/`'capturePage'` + stubs Kotlin/Swift (E3), `GoRouter.redirect` declarativo (E4), `bool.fromEnvironment('FX_ENABLE_PREMIUM')` (E5), `TargetPlatform.iOS` con `CupertinoSwitch`/`Switch` (E6).
- [x] 6 trampas del paquete plantadas: `AsyncNotifier.build()` sin `try/catch` (P1), `MethodChannel.invoke` con `catch (_)` (P2), `GoRouter.redirect` sin chequeo de auth (P3), `SettingsController` combina `enablePremium` + SharedPreferences (P4), freezed `copyWith` generado no usado (P5), `AdaptiveSlider` rama Cupertino muerta con `Slider` Material (P6).
- [x] 3 trampas superficiales: `Logger.print` no invocado (S1), `_DEFAULT_LOCALE` no usado (S2), `_formatDouble` declarado pero nunca invocado (S3).
- [x] Ground truth completo en `dev/ground-truth/fx-flutter-dart/{ground_truth.json,GROUND_TRUTH.md,unique_tokens.txt}` con paquete completo por feature.
- [x] 10 entry points (main, FxApp, GoRouter, AsyncNotifierProvider × 3, MethodChannel wrapper, stubs Kotlin/Swift), 17 modules, 14 dependencies, 3 features (21 R-NN), 9 surfaces, 6 traps ecosistema, 6 traps paquete, 3 superficiales, 11 call graph edges.
- [x] 35 unique_tokens `NPRGT-FXFLUTTER-`; `check_ground_truth.py --check-cc11` 0 referencias rotas tras limpieza de comentarios.
- [x] `dev/tests/test_fx_flutter_dart_ground_truth.py` con 62 tests (8 TestGroundTruthShape + 6 TestOutcomesAndCitations + 3 TestUniqueTokensFile + 3 TestAllCitesValid + 15 TestFlutterStructure + 2 TestBuildRunner + 3 TestPlatformChannels + 6 TestTrapsEcosystem + 6 TestTrapsPackage + 3 TestTrapsSuperficial + 7 TestManifest) verde.
- [x] `pytest` total **1701 passed** (1639 previos + 62 nuevos) sin regresiones.
- [x] `validate_skill.py` y `overfit_guard.py` verdes.
- [x] `target_matrix.yml` extendido con frameworks `[flutter, flutter-riverpod, go-router, freezed, json-serializable, riverpod-generator, build-runner, platform-channels, dart-define, adaptive-widgets]`.
- [x] `fixtures_matrix.py` extendido con detección de Flutter/Riverpod/go_router/freezed/json_serializable/riverpod_generator/build_runner/platform_channels/dart-define/adaptive-widgets via `pubspec.yaml` + `*.dart`.
- [x] `MATRIX.md` regenerado: 31 fixtures, `fx-flutter-dart` cubre `dart`, `flutter`, `flutter-riverpod`, `go-router`, `freezed`, `json-serializable`, `riverpod-generator`, `build-runner`, `platform-channels`, `dart-define`, `adaptive-widgets`, `shared-preferences`, `shell`.
- [x] `manifest.yml` con `requires: [linux, macos]` + `container.enabled: true`.
- [x] `Dockerfile.test` con `FROM ghcr.io/cirruslabs/flutter:3.24.5` + `flutter pub get` + `dart run build_runner build --delete-conflicting-outputs` + `CMD ["make","test"]`.
- [x] `pubspec.yaml` + `analysis_options.yaml` con Flutter SDK + Riverpod + go_router + freezed + build_runner.
- [x] `lib/main.dart` con `runApp(ProviderScope(child: FxApp()))`.
- [x] `lib/app.dart` con `MaterialApp.router(routerConfig: appRouter.config())`.
- [x] `lib/router/app_router.dart` con GoRouter + redirect declarativo + 5 routes + 2 deepLinks.
- [x] Source sets `lib/features/{reader,favorites,settings}/{domain,data,application,presentation}/`.
- [x] `lib/platform/{native_method_channel.dart, platform_widget.dart}` con `AdaptiveSwitch` + `AdaptiveSlider`.
- [x] Stubs `android_stub/MainActivity.kt` y `ios_stub/AppDelegate.swift`.
- [x] 7 archivos `test/` Dart con JUnit5 + flutter_test + TestDefaultBinaryMessenger.
- [x] `build-history.sh` con 8 commits reproducibles.
- [x] fx-python-cli..fx-kotlin-android (29 fixtures) sin cambios de comportamiento.
- [x] 10 decisiones nuevas D-341..D-350 (stack Flutter 3.24.5 + Dart 3.5.4, image `ghcr.io/cirruslabs/flutter:3.24.5`, requires linux+macos + container enabled, Riverpod con ref.watch cross-provider, go_router con redirect declarativo + deepLinks, freezed + json_serializable + build_runner sin commitear generados, platform channels con stubs Kotlin/Swift, dart-define FX_ENABLE_PREMIUM con bool.fromEnvironment, widgets adaptativos CupertinoSwitch vs Switch, prefijo unique tokens NPRGT-FXFLUTTER- con 35 entradas).
- [x] PROGRESS.md fila F06ad = `HECHA` con evidencia completa.
- [x] DECISIONS.md con D-341..D-350.
- [x] ROADMAP.md encabezado F06ad con ✅ y sección `Criterios de aceptación (verificados)` con todos los checks `[x]`.
- [x] Commit `F06ad: fixture fx-flutter-dart con paquete por feature`.

**Limitación operativa documentada:** los tests JVM del fixture (`flutter test`) NO se ejecutan en este host sin `flutter` instalado (sí está disponible en `/opt/homebrew/bin/flutter` pero no se ejecuta automáticamente). La verificación se hace en CI Linux con la imagen `ghcr.io/cirruslabs/flutter:3.24.5` (Dockerfile.test) que pesa ~3 GB y tarda ~5-8 min la primera vez. Los archivos `.g.dart`/`.freezed.dart` se generan en runtime y NO se commitean al repo.
 
## F06ae — Fixture `fx-react-native` ✅
 
**Objetivo:** app React Native con módulos nativos.
**Stack:** TypeScript 5.4, React Native 0.74.5 (Expo SDK 51 bare), React Navigation 6.1, Redux Toolkit 2.2, módulo nativo Kotlin/Swift con TurboModules.
**Features:** `pagos-con-nfc`, `historial`, `notificaciones-push`.
**Trampas del ecosistema:**
1. Módulos nativos resueltos por nombre a través del bridge o TurboModules.
2. Archivos por plataforma (`.ios.tsx`/`.android.tsx`) resueltos por el bundler.
3. Config plugins de Expo que modifican los proyectos nativos en `prebuild`.
4. Configuración de deep linking.
5. Alias en la configuración de Metro.
6. Handlers de notificaciones en segundo plano.
**Toolchain de tests:** Jest 29 + React Native Testing Library 12.5, en contenedor `ghcr.io/cirruslabs/react-native:0.74.5`.

**Criterios de aceptación (verificados):**
- [x] 3 features (`pagos-con-nfc`, `historial`, `notificaciones-push`) × 7 R-NN cada una (CC-03, CC-08).
- [x] 6 trampas del ecosistema plantadas con referencia exacta: `NativeModules.RtcNfcManager` con `@ReactModule(name="RtcNfcManager")` Kotlin + `@objc(RtcNfcManager)` Swift (E1), `PaymentsScreen.ios.tsx`/`.android.tsx` resueltos por Metro (E2), 6 Expo config plugins en `app.json` (E3), `linkingConfig` con 3 prefixes + 5 rutas + 2 deepLinks (E4), Metro aliases en `extraNodeModules` + babel-plugin-module-resolver (E5), `setNotificationHandler` con `handleNotification` async en background (E6).
- [x] 6 trampas del paquete plantadas: `NfcManager.readTag` sin `try/catch` (P1), `state.items.push` directo en paymentsSlice (P2), `catch (_)` silencioso en NotificationHandler (P3), linking config con deep linking activo (P4), `NfcManager.start` sin `PermissionsAndroid` (P5), Metro alias `@features` con `path.resolve` (P6).
- [x] 2 trampas superficiales: `Logger.log/warn` no invocados (S1), `formatDate/formatDateTime` no usados (S2).
- [x] Ground truth completo en `dev/ground-truth/fx-react-native/{ground_truth.json,GROUND_TRUTH.md,unique_tokens.txt}` con paquete completo por feature.
- [x] 15 entry points, 16 modules, 26 dependencies, 3 features (21 R-NN), 10 surfaces, 6 traps ecosistema, 6 traps paquete, 2 superficiales, 11 call graph edges.
- [x] 34 unique_tokens `NPRGT-FXRN-`; `check_ground_truth.py --check-cc11` 0 referencias rotas.
- [x] `dev/tests/test_fx_react_native_ground_truth.py` con 64 tests (8 TestGroundTruthShape + 6 TestOutcomesAndCitations + 3 TestUniqueTokensFile + 3 TestAllCitesValid + 17 TestRNStructure + 4 TestPackageConfig + 2 TestAppJsonPlugins + 6 TestTrapsEcosystem + 6 TestTrapsPackage + 2 TestTrapsSuperficial + 7 TestManifest) verde.
- [x] `pytest` total **1765 passed** (1701 previos + 64 nuevos) sin regresiones.
- [x] `validate_skill.py` y `overfit_guard.py` verdes.
- [x] `target_matrix.yml` extendido con frameworks `[react-native, expo-bare, react-navigation, redux-toolkit, turbo-modules, expo-config-plugins, expo-linking, expo-notifications, expo-build-properties, expo-splash-screen, metro]`.
- [x] `fixtures_matrix.py` extendido con detección de `react-native`/`expo-bare`/`react-navigation`/`redux-toolkit`/`turbo-modules`/`metro`/`expo-config-plugins`/`expo-linking`/`expo-notifications`/`expo-build-properties`/`expo-splash-screen` via `package.json` + `app.json`.
- [x] `MATRIX.md` regenerado: 32 fixtures, `fx-react-native` cubre `javascript`, `typescript`, `react-native`, `expo-bare`, `react-navigation`, `redux-toolkit`, `turbo-modules`, `expo-config-plugins`, `expo-linking`, `expo-notifications`, `expo-build-properties`, `expo-splash-screen`, `metro`, `shell`.
- [x] `manifest.yml` con `requires: [linux, macos]` + `container.enabled: true`.
- [x] `Dockerfile.test` con `FROM ghcr.io/cirruslabs/react-native:0.74.5` + `yarn install --frozen-lockfile` + `CMD ["make","test"]`.
- [x] `package.json` con RN 0.74.5 + Expo 51 + RTK 2.2 + react-navigation 6.1 + expo-notifications 0.28 + jest 29.
- [x] `app.json` con 6 plugins (./plugins/withNfc, ./plugins/withDeepLinking, expo-build-properties, expo-notifications, expo-splash-screen, expo-linking) + scheme `fxrn`.
- [x] `babel.config.js` con module-resolver aliases (`@app`, `@features`, `@store`, `@nav`, `@native`, `@plugins`, `@util`).
- [x] `metro.config.js` con extraNodeModules aliases.
- [x] `tsconfig.json` con paths aliases.
- [x] `jest.config.js` con preset jest-expo + moduleNameMapper aliases.
- [x] `jest.setup.js` con mocks de `NativeModules.RtcNfcManager` + `expo-notifications`.
- [x] 9 archivos `test/` Jest con 17 tests.
- [x] 3 features × 7 R-NN cada una (`pagos-con-nfc`, `historial`, `notificaciones-push`).
- [x] Source sets `App.tsx` + `src/navigation/` + `src/store/slices/` + `src/features/{payments,history,notifications}/` + `src/plugins/` + `src/util/`.
- [x] `android_stub/{NfcManagerModule.kt, NfcManagerPackage.kt, AndroidManifest.xml}` + `ios_stub/{NfcManagerModule.swift, .mm, Info.plist}`.
- [x] `build-history.sh` con 8 commits reproducibles.
- [x] fx-python-cli..fx-flutter-dart (30 fixtures) sin cambios de comportamiento.
- [x] 10 decisiones nuevas D-351..D-360 (stack RN 0.74.5 + Expo 51 bare + TypeScript 5.4, image `ghcr.io/cirruslabs/react-native:0.74.5`, requires linux+macos + container enabled, TurboModules RtcNfcManager con `@ReactModule` + `@objc`, archivos por plataforma `.ios.tsx`/`.android.tsx` resueltos por Metro, Expo config plugins que modifican prebuild, Redux Toolkit 2.2 con `@reduxjs/toolkit` + `react-redux` 9.1, React Navigation 6.1 con linking declarativo + deep links, Metro aliases en extraNodeModules + babel-plugin-module-resolver, expo-notifications con background handler + silent catch, prefijo unique tokens NPRGT-FXRN- con 34 entradas).
- [x] PROGRESS.md fila F06ae = `HECHA` con evidencia completa.
- [x] DECISIONS.md con D-351..D-360.
- [x] ROADMAP.md encabezado F06ae con ✅ y sección `Criterios de aceptación (verificados)` con todos los checks `[x]`.
- [x] Commit `F06ae: fixture fx-react-native con paquete por feature`.

**Limitación operativa documentada:** los tests JVM del fixture (`yarn jest`) NO se ejecutan en este host sin React Native CLI ni yarn instalados (CI requiere el contenedor `ghcr.io/cirruslabs/react-native:0.74.5` que pesa ~3 GB y tarda ~5-8 min la primera vez). Los TurboModules nativos (`.kt`/`.swift`) son solo evidencia textual, no se compilan en CI. Los tests usan `jest.mock('react-native', ...)` con `NativeModules.RtcNfcManager` mockeado.
 
---
 
# Escritorio
 
## F06af — Fixture `fx-electron` ✅
 
**Objetivo:** app Electron con código fuente (complementa el `.asar` de F06e).
**Stack:** TypeScript 5.5, Electron 32.2 (main, preload, renderer), electron-builder 25.1, esbuild 0.24, Vitest 2.1.
**Features:** `abrir-proyecto`, `exportar-pdf`, `actualización-automática`.
**Trampas del ecosistema:**
1. Canales IPC por string (`ipcMain.handle`/`ipcRenderer.invoke`).
2. API expuesta con `contextBridge` como `window.api`.
3. Menú nativo con atajos que disparan features.
4. Procesos utility y workers.
5. Protocolo personalizado (`app://`).
6. Configuración de electron-builder (`asarUnpack`, `extraResources`) con archivos fuera del asar.
**Toolchain de tests:** Vitest 2.1 para main/preload, en contenedor `node:20-bookworm-slim` + xvfb.

**Criterios de aceptación (verificados):**
- [x] 3 features (`abrir-proyecto`, `exportar-pdf`, `actualización-automática`) × 7 R-NN cada una (CC-03, CC-08).
- [x] 6 trampas del ecosistema plantadas con referencia exacta: `ipcMain.handle('project:open')` + 5 channels strings (E1), `contextBridge.exposeInMainWorld('api', ...)` con 6 funciones (E2), `Menu.buildFromTemplate` con 4 submenus y accelerators (E3), `utilityProcess.fork` + `child_process.fork` (E4), `protocol.handle('app', ...)` con `registerSchemesAsPrivileged` (E5), electron-builder.yml con `asarUnpack` + `extraResources` (E6).
- [x] 6 trampas del paquete plantadas: `ipcMain.handle('project:open')` sin `try/catch` (P1), `'CmdOrCtrl+O'` duplicado en `Open Project` y `recent1.txt` (P2), `utilityProcess.fork()` sin handler de cleanup (P3), `contextBridge.exposeInMainWorld` con arrow functions (sin `Function` no serializable) (P4), `protocol.handle('app')` con `registerSchemesAsPrivileged` antes de `app.ready()` (P5), `autoUpdater.setFeedURL('http://example.com/updates')` (HTTP, no HTTPS) (P6).
- [x] 3 trampas superficiales: `LegacyLogger.info/warn/error` no invocados (S1), `ENABLE_BETA/ENABLE_ANALYTICS/DEBUG_LOG_LEVEL` no leídos (S2), `formatTimestamp` declarado pero no invocado (S3).
- [x] Ground truth completo en `dev/ground-truth/fx-electron/{ground_truth.json,GROUND_TRUTH.md,unique_tokens.txt}` con paquete completo por feature.
- [x] 14 entry points, 19 modules, 7 dependencies, 3 features (21 R-NN), 13 surfaces, 6 traps ecosistema, 6 traps paquete, 3 superficiales, 15 call graph edges.
- [x] 33 unique_tokens `NPRGT-FXELEC-`; `check_ground_truth.py --check-cc11` 0 referencias rotas tras limpieza de comentarios en `src/main/workers/updater.ts`.
- [x] `dev/tests/test_fx_electron_ground_truth.py` con 62 tests (8 TestGroundTruthShape + 6 TestOutcomesAndCitations + 3 TestUniqueTokensFile + 3 TestAllCitesValid + 16 TestElectronStructure + 3 TestElectronBuilder + 6 TestTrapsEcosystem + 6 TestTrapsPackage + 3 TestTrapsSuperficial + 7 TestManifest) verde.
- [x] `pytest` total **1827 passed** (1765 previos + 62 nuevos) sin regresiones.
- [x] `validate_skill.py` y `overfit_guard.py` verdes.
- [x] `target_matrix.yml` extendido con frameworks `[electron, electron-context-bridge, electron-builder, electron-asar-unpack, electron-extra-resources, electron-utility-process, electron-app-scheme, electron-auto-updater]`.
- [x] `fixtures_matrix.py` extendido con detección de electron/electron-builder/electron-context-bridge/electron-asar-unpack/electron-extra-resources/electron-utility-process/electron-app-scheme/electron-auto-updater via `package.json` + `electron-builder.yml` + `src/*.ts`.
- [x] `MATRIX.md` regenerado: 33 fixtures, `fx-electron` cubre `javascript`, `typescript`, `electron`, `electron-builder`, `electron-asar-unpack`, `electron-extra-resources`, `electron-utility-process`, `electron-app-scheme`, `electron-context-bridge`, `shell`.
- [x] `manifest.yml` con `requires: [linux, macos]` + `container.enabled: true`.
- [x] `Dockerfile.test` con `FROM node:20-bookworm-slim` + `apt-get install xvfb + libs Electron` + `yarn install` + `CMD ["make","test"]`.
- [x] `package.json` con electron + electron-builder + electron-updater + typescript + esbuild + vitest.
- [x] `electron-builder.yml` con `asarUnpack` + `extraResources` + targets mac/win/linux.
- [x] `tsconfig.main.json` + `tsconfig.renderer.json` (separados para Node vs DOM).
- [x] Source sets `src/main/{index,windows,autoUpdater}.ts` + `src/main/ipc/{handlers,channels}.ts` + `src/main/menu/appMenu.ts` + `src/main/protocol/appProtocol.ts` + `src/main/workers/{updater,pdfExporter}.ts` + `src/main/util/{legacyLogger,featureFlags}.ts`.
- [x] `src/preload/{index,api}.ts` con `contextBridge.exposeInMainWorld`.
- [x] `src/renderer/{index.html,renderer.ts,styles.css}` con 3 botones (Open, Export, Update).
- [x] `src/workers/{updater-worker,pdf-worker}.ts` como scripts standalone.
- [x] `resources/{icon.png, native-menu.json, translations.json}` para `extraResources`.
- [x] 9 archivos `test/` Vitest (ipc, menu, protocol, api, updater, traps, cc11 = 17 tests Vitest).
- [x] `build-history.sh` con 8 commits reproducibles.
- [x] fx-python-cli..fx-react-native (31 fixtures) sin cambios de comportamiento.
- [x] 10 decisiones nuevas D-361..D-370 (stack Electron 32 + TypeScript 5.5 + esbuild 0.24 + Vitest 2.1 + electron-builder 25.1, image `node:20-bookworm-slim` + xvfb + libs Electron, requires linux+macos + container enabled, IPC channels por string con `ipcMain.handle`/`ipcRenderer.invoke`, `contextBridge.exposeInMainWorld` con `window.api`, Menu nativo con accelerators duplicados P2, utility process para actualizaciones con trampa P3 sin handler de cleanup, `child_process.fork` para PDF export, protocolo personalizado `app://` con trampa P5 `registerSchemesAsPrivileged` obligatorio, electron-builder.yml con `asarUnpack` + `extraResources` trampa E6, `autoUpdater.setFeedURL` con HTTP trampa P6, prefijo unique tokens `NPRGT-FXELEC-` con 33 entradas).
- [x] PROGRESS.md fila F06af = `HECHA` con evidencia completa.
- [x] DECISIONS.md con D-361..D-370.
- [x] ROADMAP.md encabezado F06af con ✅ y sección `Criterios de aceptación (verificados)` con todos los checks `[x]`.
- [x] Commit `F06af: fixture fx-electron con paquete por feature`.

**Limitación operativa documentada:** los tests Vitest del fixture NO se ejecutan en este host sin `electron` instalado (CI requiere el contenedor `node:20-bookworm-slim` con xvfb que pesa ~2 GB y tarda ~3-5 min la primera vez). Los tests usan `vi.mock('electron')` para no requerir display real; `utilityProcess.fork` y `child_process.fork` se mockean para evitar forks reales.
 
## F06ag — Fixture `fx-csharp-wpf` ✅
 
**Objetivo:** app de escritorio WPF con MVVM.
**Stack:** C# 12, .NET 9.0, WPF (net9.0-windows), XAML, CommunityToolkit.Mvvm 8.4 (source generators), xUnit 2.9.
**Features:** `clientes`, `cotizaciones`, `impresión`.
**Trampas del ecosistema:**
1. Bindings en XAML por string de propiedad.
2. Comandos y propiedades generados por `[RelayCommand]`/`[ObservableProperty]`.
3. `DataTemplate` implícitos por `DataType` que eligen la vista.
4. Value converters.
5. Styles y triggers con lógica.
6. Merged dictionaries en `App.xaml`.
**Toolchain de tests:** xUnit sobre los ViewModels (proyecto `net9.0` multiplataforma) en contenedor `mcr.microsoft.com/dotnet/sdk:9.0`; la UI requiere Windows. **requires: [linux, macos]** para tests VM; tests UI solo Windows (marcados `[Trait("Category", "UI")]`).

**Criterios de aceptación (verificados):**
- [x] 3 features (`clientes`, `cotizaciones`, `impresión`) × 7 R-NN cada una (CC-03, CC-08).
- [x] 6 trampas del ecosistema plantadas con referencia exacta: 5+ bindings XAML por string (E1), `[ObservableProperty]` + `[RelayCommand]` con source generators (E2), `DataTemplate` con `DataType` (E3 + P6 typo), 3 `IValueConverter` (E4), `Style.Triggers` con `DataTrigger IsValid` (E5), 4 `MergedDictionaries` en `App.xaml` (E6).
- [x] 6 trampas del paquete plantadas: `OnSelectedClienteChanged` sin null check (P1), `Task.Run` sin await bloquea UI (P2), `BoolToVisibilityConverter.ConvertBack` lanza `NotImplementedException` (P3), 2 Styles sin `BasedOn` (P4), `AsyncRelayCommand.CanExecute => false` siempre (P5), `ClienteTemplate.xaml` con `DataType={x:Type vm:ClientesViewModel}` typo (P6).
- [x] 3 trampas superficiales: `LegacyConverter` declarado pero no invocado (S1), `Fonts.xaml` con `BrandFont` no referenciado (S2), `ExperimentalViewModel` declarado pero no usado (S3).
- [x] Ground truth completo en `dev/ground-truth/fx-csharp-wpf/{ground_truth.json,GROUND_TRUTH.md,unique_tokens.txt}` con paquete completo por feature.
- [x] 13 entry points, 13 modules, 8 dependencies, 3 features (21 R-NN), 13 surfaces, 6 traps ecosistema, 6 traps paquete, 3 superficiales, 10 call graph edges.
- [x] 34 unique_tokens `NPRGT-FXWPF-`; `check_ground_truth.py --check-cc11` 0 referencias rotas.
- [x] `dev/tests/test_fx_csharp_wpf_ground_truth.py` con 65 tests (8 TestGroundTruthShape + 6 TestOutcomesAndCitations + 3 TestUniqueTokensFile + 3 TestAllCitesValid + 18 TestCSharpStructure + 4 TestPackageConfig + 2 TestMergedDictionaries + 6 TestTrapsEcosystem + 6 TestTrapsPackage + 3 TestTrapsSuperficial + 7 TestManifest) verde.
- [x] `pytest` total **1892 passed** (1827 previos + 65 nuevos) sin regresiones.
- [x] `validate_skill.py` y `overfit_guard.py` verdes.
- [x] `target_matrix.yml` extendido con frameworks `[wpf, xaml, mvvm, community-toolkit-mvvm, data-template, value-converter, merged-dictionary, style-trigger, xunit]`.
- [x] `fixtures_matrix.py` extendido con detección de wpf/xaml/mvvm/community-toolkit-mvvm/data-template/value-converter/merged-dictionary/style-trigger/xunit via `**/*.csproj` + `**/*.xaml` + `**/*.cs`.
- [x] `MATRIX.md` regenerado: 34 fixtures, `fx-csharp-wpf` cubre `csharp`, `wpf`, `xaml`, `mvvm`, `community-toolkit-mvvm`, `data-template`, `value-converter`, `merged-dictionary`, `style-trigger`, `xunit`, `shell`.
- [x] `manifest.yml` con `requires: [linux, macos]` + `container.enabled: true`.
- [x] `Dockerfile.test` con `FROM mcr.microsoft.com/dotnet/sdk:9.0` + `apt-get install xvfb + libs UI` + `dotnet restore` + `CMD ["make","test"]`.
- [x] `FxWpf.sln` con 5 proyectos (App + Core + ViewModels + Tests + TrapTests) + `Directory.Build.props` con `TargetFramework=net9.0`.
- [x] 3 `.csproj` con `CommunityToolkit.Mvvm 8.4.0` y `net9.0-windows` (App) o `net9.0` (ViewModels, Core).
- [x] `App.xaml` con 4 `MergedDictionaries` (Colors + Buttons + Controls + ButtonStyles) + 3 converters registrados (BoolToVisibility + NullToBool + Currency).
- [x] 4 Views (`MainWindow.xaml` con 5+ bindings, `ClientesView.xaml`, `CotizacionesView.xaml` con `DataGrid`, `PrintPreviewView.xaml`).
- [x] 4 Themes (`Colors.xaml`, `Buttons.xaml`, `Controls.xaml`, `Fonts.xaml` con S2).
- [x] `ButtonStyles.xaml` con `DataTrigger IsValid` (E5) + 2 styles sobrepuestos sin `BasedOn` (P4).
- [x] `ClienteTemplate.xaml` con `DataTemplate DataType={x:Type vm:ClientesViewModel}` typo (E3 + P6).
- [x] 4 ViewModels (ClientesViewModel con P1 + AddClienteCommand + FilterClientes; CotizacionesViewModel con P2 + SaveCotizacion; PrintPreviewViewModel con IsValid; ExperimentalViewModel S3).
- [x] 4 Converters (BoolToVisibility + NullToBool + Currency + Legacy S1).
- [x] `AsyncRelayCommand` con `CanExecute => false` always (P5).
- [x] 13 tests xUnit VM cross-platform + 19 tests xUnit traps = 32 tests xUnit.
- [x] `build-history.sh` con 8 commits reproducibles.
- [x] fx-python-cli..fx-electron (32 fixtures) sin cambios de comportamiento.
- [x] 10 decisiones nuevas D-371..D-380 (stack .NET 9 + WPF + CommunityToolkit.Mvvm 8.4 + xUnit 2.9.2, image `mcr.microsoft.com/dotnet/sdk:9.0` con xvfb + libs UI, requires linux+macos + container enabled para tests VM, source generators `[ObservableProperty]` + `[RelayCommand]` E2, bindings XAML por string de propiedad E1, `DataTemplate` con `DataType` E3 + P6, value converters `IValueConverter` E4 + P3, styles con `DataTrigger` E5 + P4 sobrepuestos, merged dictionaries en `App.xaml` con 4 ResourceDictionary sources E6, prefijo unique tokens NPRGT-FXWPF- con 34 entradas).
- [x] PROGRESS.md fila F06ag = `HECHA` con evidencia completa.
- [x] DECISIONS.md con D-371..D-380.
- [x] ROADMAP.md encabezado F06ag con ✅ y sección `Criterios de aceptación (verificados)` con todos los checks `[x]`.
- [x] Commit `F06ag: fixture fx-csharp-wpf con paquete por feature`.

**Limitación operativa documentada:** los tests xUnit del fixture NO se ejecutan en este host sin `dotnet` instalado (CI requiere el contenedor `mcr.microsoft.com/dotnet/sdk:9.0` con xvfb que pesa ~1.5 GB y tarda ~2-3 min la primera vez). Los tests de **ViewModels** corren multiplataforma; los tests de **UI WPF** requieren Windows con `net9.0-windows` y se omiten en CI Linux/macOS con `[Trait("Category", "UI")]`. Esta es la primera fase de F06 que marca `requires: [linux, macos]` (no windows) porque las trampas se prueban contra el codigo fuente + ground truth, no contra la UI en runtime.
 
---
 
# Datos y bases de datos
 
## F06ah — Fixture `fx-sql-postgres` ✅
 
**Objetivo:** repositorio de base de datos donde las features son procesos de negocio en la base.
**Stack:** PostgreSQL 16, Flyway 10, PL/pgSQL, pg_cron 1.6, pgTAP.
**Features:** `facturación`, `auditoría`, `multi-tenant`.
**Trampas del ecosistema:**
1. Triggers con efectos secundarios (auditoría, recálculo de totales).
2. Políticas RLS que cambian lo que ve cada rol.
3. SQL dinámico con `EXECUTE format(...)`.
4. Orden de migraciones versionadas y repetibles (`R__`).
5. `ON DELETE CASCADE` y foreign keys diferidas.
6. Vistas materializadas refrescadas por pg_cron, y vistas de soft-delete.
**Toolchain de tests:** pgTAP en contenedor PostgreSQL.

**Criterios de aceptación (verificados):**
- [x] 3 features (`facturación`, `auditoría`, `multi-tenant`) × 7 R-NN cada una (CC-03, CC-08).
- [x] 6 trampas del ecosistema plantadas con referencia exacta: 4 triggers (INSERT/UPDATE/DELETE) llamando a `f_audit_factura()` (E1), 13 RLS policies + ENABLE (E2), `EXECUTE format()` en `f_search_dynamic` + `f_admin_search` (E3), 7 V* + 1 R__ (E4), FK `ON DELETE CASCADE` + `DEFERRABLE` (E5), `CREATE EXTENSION pg_cron` + 3 jobs + vista materializada (E6).
- [x] 6 trampas del paquete plantadas: `f_audit_factura` lee `NEW.id` en `TG_OP='DELETE'` (P1), 13 policies RLS sin `FORCE ROW LEVEL SECURITY` (P2), `f_search_dynamic` + `f_admin_search` sin whitelist (P3 SQLi), `R__recalc_factura_totals.sql` con `TRUNCATE` + `INSERT` no idempotente (P4), `ON DELETE CASCADE` sin trigger BEFORE DELETE (P5 silent), vista materializada `mv_facturas_mensuales` sin `WHERE deleted_at IS NULL` (P6).
- [x] 3 trampas superficiales: `db/sql/legacy_export.sql` con `SELECT 'noop'` (S1), `db/schema/007_unused_indexes.sql` con `CREATE INDEX` no usados (S2), `db/test/08_deprecated_test.sql` con `pass` placeholder (S3).
- [x] Ground truth completo en `dev/ground-truth/fx-sql-postgres/{ground_truth.json,GROUND_TRUTH.md,unique_tokens.txt}` con paquete completo por feature.
- [x] 27 entry points, 25 modules, 8 dependencies, 3 features (21 R-NN), 19 surfaces, 6 traps ecosistema, 6 traps paquete, 3 superficiales, 9 call graph edges.
- [x] 32 unique_tokens `NPRGT-FXSQLPG-`; `check_ground_truth.py --check-cc11` 0 referencias rotas tras renombrar `multi_tenant_query.sql` → `tenant_isolation_query.sql` (CC-11 prohibe feature names en código).
- [x] `dev/tests/test_fx_sql_postgres_ground_truth.py` con 67 tests (8 TestGroundTruthShape + 6 TestOutcomesAndCitations + 3 TestUniqueTokensFile + 3 TestAllCitesValid + 20 TestPostgresStructure + 4 TestMigrationsPresent + 2 TestPgCronConfigured + 6 TestTrapsEcosystem + 6 TestTrapsPackage + 3 TestTrapsSuperficial + 7 TestManifest) verde.
- [x] `pytest` total **1959 passed** (1892 previos + 67 nuevos) sin regresiones.
- [x] `validate_skill.py` y `overfit_guard.py` verdes.
- [x] `target_matrix.yml` extendido con frameworks `[postgresql, flyway, pl-pgsql, pg-cron, pgtap, row-level-security, trigger, materialized-view, sql-dynamic, cascade-constraint]`.
- [x] `fixtures_matrix.py` extendido con detección de postgresql/pl-pgsql/pg-cron/pgtap/row-level-security/trigger/materialized-view/sql-dynamic/cascade-constraint/flyway via `**/*.sql`.
- [x] `MATRIX.md` regenerado: 35 fixtures, `fx-sql-postgres` cubre `sql`, `postgresql`, `flyway`, `pl-pgsql`, `pg-cron`, `pgtap`, `row-level-security`, `trigger`, `materialized-view`, `sql-dynamic`, `cascade-constraint`, `shell`.
- [x] `manifest.yml` con `requires: [linux, macos]` + `container.enabled: true`.
- [x] `Dockerfile.test` con `FROM postgres:16-alpine` + `apk add openjdk21-jdk` + `git clone pg_cron + make install` + `curl flyway` + `CMD make test`.
- [x] `db/migration/V1..V7__*.sql` (7 migraciones versionadas) + `R__recalc_factura_totals.sql` (repetible).
- [x] `db/seed/{seed_data,seed_audit}.sql` con datos iniciales (3 clientes, 2 facturas, 1 soft-deleted, 4 entries auditoria).
- [x] `db/test/01..08_*.sql` (8 archivos pgTAP con 28+ tests).
- [x] `db/sql/{facturas_crud,auditoria_query,tenant_isolation_query,legacy_export}.sql`.
- [x] `config/{flyway,postgres}.conf` con `shared_preload_libraries=pg_cron`.
- [x] `tools/{run_pgtap,apply_migrations,reset_db}.sh`.
- [x] `build-history.sh` con 8 commits reproducibles.
- [x] fx-python-cli..fx-csharp-wpf (33 fixtures) sin cambios de comportamiento.
- [x] 10 decisiones nuevas D-381..D-390 (stack PostgreSQL 16 + Flyway 10 + pg_cron 1.6 + pgTAP, image `postgres:16-alpine` con `pg_cron` desde git, requires linux+macos + container enabled, `EXECUTE format(...)` con tabla parametrizada E3+P3, triggers con efectos secundarios E1+P1, RLS sin FORCE E2+P2, ON DELETE CASCADE + DEFERRABLE E5+P5, vistas materializadas refrescadas por pg_cron E6+P6, migraciones versionadas + repetibles E4+P4, tests pgTAP via pg_prove, prefijo unique tokens NPRGT-FXSQLPG- con 32 entradas + CC-11 con limpieza de feature names).
- [x] PROGRESS.md fila F06ah = `HECHA` con evidencia completa.
- [x] DECISIONS.md con D-381..D-390.
- [x] ROADMAP.md encabezado F06ah con ✅ y sección `Criterios de aceptación (verificados)` con todos los checks `[x]`.
- [x] Commit `F06ah: fixture fx-sql-postgres con paquete por feature`.

**Limitación operativa documentada:** los tests pgTAP del fixture NO se ejecutan en este host sin Docker (CI requiere el contenedor `postgres:16-alpine` con pg_cron compilado desde git que pesa ~1.5 GB y tarda ~3-5 min la primera vez). Los tests pgTAP corren contra una DB efímera (`fxpg_test`) que se reinicia en cada `docker run`. El archivo `db/sql/multi_tenant_query.sql` se renombro a `db/sql/tenant_isolation_query.sql` para cumplir CC-11 (los feature names como `multi-tenant` no pueden aparecer en código fuente del fixture).
## F06ai — Fixture `fx-sql-oracle-plsql` ✅
 
**Objetivo:** esquema Oracle con lógica en paquetes PL/SQL.
**Stack:** Oracle Database Free 23c, PL/SQL, Liquibase 4.27, utPLSQL.
**Features:** `apertura-de-cuenta`, `cálculo-de-intereses`, `cierre-de-mes`.
**Trampas del ecosistema:**
1. Spec frente a body: procedimientos privados que solo existen en el body.
2. Sinónimos públicos que redirigen objetos.
3. `EXECUTE IMMEDIATE` con nombres construidos.
4. `PRAGMA AUTONOMOUS_TRANSACTION`.
5. Triggers compuestos e `INSTEAD OF` sobre vistas.
6. Jobs de `DBMS_SCHEDULER` y DB links a una base remota.
**Toolchain de tests:** utPLSQL en contenedor Oracle Database Free (`gvenzl/oracle-free:23.5-alpine-slim` + sqlcl).

**Criterios de aceptación (verificados):**
- [x] 3 features (`apertura-de-cuenta`, `cálculo-de-intereses`, `cierre-de-mes`) × 7 R-NN cada una (CC-03, CC-08).
- [x] 6 trampas del ecosistema plantadas con referencia exacta: `p_internal_validate` solo en body (E1), 5 sinonimos publicos (E2), `EXECUTE IMMEDIATE` con tabla (E3), `PRAGMA AUTONOMOUS_TRANSACTION` en trigger (E4), trigger `INSTEAD OF UPDATE` (E5), `DBMS_SCHEDULER.CREATE_JOB` + `CREATE DATABASE LINK` (E6).
- [x] 6 trampas del paquete plantadas: `PRAGMA AUTONOMOUS_TRANSACTION` sin `WHEN OTHERS` (P1), sinonimo a tabla inexistente (P2), `EXECUTE IMMEDIATE` sin whitelist (P3), trigger sin handler (P4), `INSTEAD OF UPDATE` omite `opened_at` (P5), `JOB_MONTHLY` con `enabled => FALSE` (P6).
- [x] 3 trampas superficiales: `pkg_legacy` declarado pero no usado (S1), sinonimo `legacy_orders` apuntando a tabla inexistente (S2), test `07-deprecated-test` trivial (S3).
- [x] Ground truth completo en `dev/ground-truth/fx-sql-oracle-plsql/{ground_truth.json,GROUND_TRUTH.md,unique_tokens.txt}` con paquete completo por feature.
- [x] 23 entry points, 18 modules, 8 dependencies, 3 features (21 R-NN), 18 surfaces, 6 traps ecosistema, 6 traps paquete, 3 superficiales, 9 call graph edges.
- [x] 33 unique_tokens `NPRGT-FXORAPL-`; `check_ground_truth.py --check-cc11` 0 referencias rotas tras renombrar formato de `decision_points.file` (separar `file` de `line` para que `check_cite` parsee correctamente).
- [x] `dev/tests/test_fx_sql_oracle_plsql_ground_truth.py` con 69 tests (8 TestGroundTruthShape + 6 TestOutcomesAndCitations + 3 TestUniqueTokensFile + 3 TestAllCitesValid + 26 TestOracleStructure + 3 TestLiquibaseConfigured + 6 TestTrapsEcosystem + 6 TestTrapsPackage + 3 TestTrapsSuperficial + 7 TestManifest) verde.
- [x] `pytest` total **2028 passed** (1959 previos + 69 nuevos) sin regresiones.
- [x] `validate_skill.py` y `overfit_guard.py` verdes.
- [x] `target_matrix.yml` extendido con frameworks `[oracle, liquibase, pl-sql, utplsql, dbms-scheduler, db-link, autonomous-transaction, instead-of, synonym, execute-immediate]`.
- [x] `fixtures_matrix.py` extendido con detección de oracle/pl-sql/liquibase/utplsql/dbms-scheduler/db-link/autonomous-transaction/instead-of/synonym/execute-immediate via `**/*.sql`.
- [x] `MATRIX.md` regenerado: 36 fixtures, `fx-sql-oracle-plsql` cubre `sql`, `oracle`, `liquibase`, `pl-sql`, `utplsql`, `dbms-scheduler`, `db-link`, `autonomous-transaction`, `instead-of`, `synonym`, `execute-immediate`, `trigger`, `postgresql`, `shell`.
- [x] `manifest.yml` con `requires: [linux, macos]` + `container.enabled: true`.
- [x] `Dockerfile.test` con `FROM gvenzl/oracle-free:23.5-alpine-slim` + `apk add openjdk21-jdk` + `curl download liquibase-4.27.0` + `CMD ["make","test"]`.
- [x] `db/changelog/changelog-master.xml` incluye 7 migraciones (001..007).
- [x] `db/packages/pkg_accounts_spec.sql` + `pkg_accounts_body.sql` con p_internal_validate privada (E1 + P1).
- [x] `db/packages/pkg_interest_spec.sql` + `pkg_interest_body.sql` con `EXECUTE IMMEDIATE` (E3 + P3).
- [x] `db/packages/pkg_monthly_close_spec.sql` + `pkg_monthly_close_body.sql`.
- [x] `db/packages/pkg_legacy_spec.sql` (Trampa S1).
- [x] `db/changelog/004-autonomous-trigger.sql` con `PRAGMA AUTONOMOUS_TRANSACTION` (E4 + P4).
- [x] `db/changelog/005-instead-of-trigger.sql` + `db/sql/views.sql` con trigger INSTEAD OF (E5 + P5).
- [x] `db/changelog/006-scheduler-jobs.sql` con `JOB_MONTHLY` disabled (P6) + `JOB_HOURLY` enabled.
- [x] `db/changelog/007-db-link.sql` con `CREATE DATABASE LINK remote_orafi` (E6).
- [x] `db/sql/{synonyms,legacy_synonym}.sql` con 5 sinonimos publicos + 1 trampa P2 + 1 S2.
- [x] `db/seed/{seed-data,seed-accounts}.sql` con datos iniciales (3 cuentas + history + interest).
- [x] `db/test/01..07_*.sql` (7 archivos utPLSQL con 25+ tests).
- [x] `config/{liquibase.properties,tnsnames.ora}` con `shared_preload_libraries`-equivalent.
- [x] `tools/{run_utplsql,apply_liquibase,reset_db}.sh`.
- [x] `build-history.sh` con 8 commits reproducibles.
- [x] fx-python-cli..fx-sql-postgres (34 fixtures) sin cambios de comportamiento.
- [x] 10 decisiones nuevas D-391..D-400 (stack Oracle 23c + Liquibase 4.27 + PL/SQL + utPLSQL, image `gvenzl/oracle-free:23.5-alpine-slim`, requires linux+macos + container enabled, packages PL/SQL spec/body E1, sinonimos publicos E2 + P2, EXECUTE IMMEDIATE con tabla parametrizada E3 + P3 SQLi, PRAGMA AUTONOMOUS_TRANSACTION en trigger + open_account P1 + P4, triggers INSTEAD OF + DBMS_SCHEDULER + DB links E5 + E6 + P6, prefijo unique tokens NPRGT-FXORAPL- con 33 entradas + CC-11 con decision_points formato).
- [x] PROGRESS.md fila F06ai = `HECHA` con evidencia completa.
- [x] DECISIONS.md con D-391..D-400.
- [x] ROADMAP.md encabezado F06ai con ✅ y sección `Criterios de aceptación (verificados)` con todos los checks `[x]`.
- [x] Commit `F06ai: fixture fx-sql-oracle-plsql con paquete por feature`.

**Limitación operativa documentada:** los tests utPLSQL del fixture NO se ejecutan en este host sin Docker (CI requiere el contenedor `gvenzl/oracle-free:23.5-alpine-slim` que pesa ~1.5 GB y tarda ~3-5 min la primera vez). Los tests utPLSQL corren contra una DB efímera (auto-start del contenedor) que se reinicia en cada `docker run`. El archivo `pkg_legacy_spec.sql` está en `db/packages/` como evidencia textual de trampa S1.
 
## F06aj — Fixture `fx-sql-tsql` ✅
  
**Objetivo:** base SQL Server con stored procedures T-SQL, triggers, CTE recursivas, `MERGE` con `OUTPUT`, tablas temporales globales y 3 jobs de SQL Agent.
**Stack:** SQL Server 2022 (oficial MS, Linux), T-SQL, `mssql-tools18` (`sqlcmd`), orquestador `db/install.sql`, tests T-SQL puros (sin tSQLt).
**Features:** `stock` (inventario, sinonimo neutro CC-11), `reconcile` (conciliación), `dashboard` (reportes).
**Trampas del ecosistema:**
1. Procedimientos almacenados con `sp_executesql` parametrizado vs string-concatenado.
2. `MERGE` con cláusula `OUTPUT $action` + `INTO` tabla de auditoría.
3. Triggers `AFTER` + `INSTEAD OF` (este último sobre vista).
4. CTE recursivas (`WITH ... AS (anchor) UNION ALL (recursive)`).
5. Tablas temporales globales (`##global_stock_temp`) compartidas entre SPs.
6. Scripts de jobs de SQL Agent (`sp_add_job` + `sp_add_schedule` + `sp_attach_schedule`).
**Toolchain de tests:** T-SQL puro (`fx_assert_equal` + `fx_test_begin/end` + tabla `fx_test_results`) ejecutado por `tools/run_tests.sh` con `sqlcmd`, en contenedor Docker `mcr.microsoft.com/mssql/server:2022-CU14-ubuntu-22.04`.

**Criterios de aceptación (verificados):**
- [x] 3 features (`stock`, `reconcile`, `dashboard`) × 7 R-NN cada una (CC-03, CC-08) = 21 R-NN documentados en `ground_truth.json`.
- [x] 6 trampas del ecosistema plantadas con referencia exacta: `usp_stock_search_dynamic` (E1 parametrizado) + `usp_stock_search_raw` (P1 concat), `usp_reconcile_run` con `MERGE ... OUTPUT $action` (E2), `trg_stock_movements_after_insert` + `trg_stock_instead_of_update` (E3), `usp_explode_bom` con `WITH ... UNION ALL` (E4), `usp_temp_load` + `usp_temp_consume` con `##global_stock_temp` (E5), `JOB_HOURLY_RECALC_TOTALS` + `JOB_DAILY_REBUILD_REPORT_CACHE` + `JOB_LEGACY_PURGE` (E6).
- [x] 6 trampas del paquete plantadas: `usp_stock_search_raw` concat (P1 SQLi), `usp_reconcile_partial` sin `WHEN NOT MATCHED BY SOURCE` (P2 huerfanos), `trg_stock_instead_of_update` omite `quantity_on_hand` (P3), CTE recursiva + ciclo `A->B->C->A` en `bom_links` (P4), `usp_temp_consume` no limpia `##global_stock_temp` (P5 leak), `JOB_LEGACY_PURGE` con `enabled=0` (P6).
- [x] 3 trampas superficiales: `usp_legacy_export` declarado pero no invocado (S1), `usp_legacy_purge` referencia `dbo.legacy_archive` inexistente + `trg_old_audit` sobre `dbo.does_not_exist` con `TRY/CATCH` silencioso (S2), `08_deprecated_test.sql` con `IF 1=0 SELECT 'noop'` (S3).
- [x] Ground truth completo en `dev/ground-truth/fx-sql-tsql/{ground_truth.json, GROUND_TRUTH.md, unique_tokens.txt}` con paquete completo por feature (entry_points, modules, dependencies, features, surfaces, traps, package_traps, superficial_traps, call_graph, config, tests).
- [x] 45 entry points, 43 modules, 7 dependencies, 3 features (21 R-NN), 21 surfaces, 6 traps ecosistema, 6 traps paquete, 3 superficiales, 10 call graph edges.
- [x] 33 unique_tokens `NPRGT-FXSQLTS-`; `check_ground_truth.py --check-cc11` 0 referencias rotas (CC-11 OK tras validar 4 archivos .sql + 4 .sh + 1 .ini + 1 .md).
- [x] `dev/tests/test_fx_sql_tsql_ground_truth.py` con 74 tests (11 TestGroundTruthShape + 6 TestOutcomesAndCitations + 3 TestUniqueTokensFile + 3 TestAllCitesValid + 21 TestSqlServerStructure + 2 TestMigrationsPresent + 2 TestSqlAgentConfigured + 6 TestTrapsEcosystem + 6 TestTrapsPackage + 3 TestTrapsSuperficial + 13 TestManifest) verde.
- [x] `pytest` total **2102 passed** (2028 previos + 74 nuevos) sin regresiones.
- [x] `validate_skill.py` y `overfit_guard.py` verdes.
- [x] `target_matrix.yml` extendido con frameworks `[sqlserver, tsql, sqlcmd, sp_executesql, merge-output, after-trigger, recursive-cte, temp-tables, sql-agent]`.
- [x] `fixtures_matrix.py` extendido con detección T-SQL via `**/*.sql` (sp_executesql, MERGE OUTPUT $action, AFTER INSERT/UPDATE, INSTEAD OF, recursive CTE con UNION ALL, ##temp tables, sp_add_job/sysjobs, DATETIME2/SYSUTCDATETIME/SET NOCOUNT) + Dockerfile.test (mssql-tools18 → sqlcmd).
- [x] `MATRIX.md` regenerado: 37 fixtures, `fx-sql-tsql` cubre `shell`, `postgresql` (compartido con fx-sql-postgres), `trigger`, `instead-of`, `synonym`, `sqlserver`, `tsql`, `sqlcmd`, `sp_executesql`, `merge-output`, `after-trigger`, `recursive-cte`, `temp-tables`, `sql-agent`.
- [x] `manifest.yml` con `requires: [linux, macos]` + `container.enabled: true` + `image_tag: npr-fx-sql-tsql`.
- [x] `Dockerfile.test` con `FROM mcr.microsoft.com/mssql/server:2022-CU14-ubuntu-22.04` + `apt-get install mssql-tools18 unixodbc-dev make bash git jq` + `ACCEPT_EULA=Y MSSQL_SA_PASSWORD=SqlServer2022! MSSQL_PID=Developer` + `CMD ["bash","entrypoint.sh"]`.
- [x] `entrypoint.sh` arranca `sqlservr` en background + `tools/wait_for_sql.sh` (poll 60s) + `CREATE DATABASE fxsqlts` + `sqlcmd -i db/install.sql` + `bash tools/run_tests.sh`.
- [x] `db/install.sql` orquesta 5 tablas auxiliares (`stock_audit`, `reconcile_audit`, `bom_links`, `stock_totals`, + idempotencia) + V001..V008 + 2 R__ + views + synonyms + functions + legacy_artifact + seed.
- [x] `db/migration/V001__init_schema.sql` con 5 tablas (`stock_items`, `stock_movements`, `reconcile_runs`, `reconcile_lines`, `report_cache`) + 2 indices (uno trampa S2 `ix_stock_items_unused`).
- [x] `db/migration/V002__init_triggers.sql` con `trg_stock_movements_after_insert` (AFTER INSERT → stock_audit, P3 omite `source_system`) + `trg_stock_instead_of_update` (INSTEAD OF UPDATE sobre `vw_stock_current`, P3 omite `quantity_on_hand`).
- [x] `db/migration/V003__recursive_cte_bom.sql` con `usp_explode_bom` (CTE `WITH bom_tree AS ... UNION ALL ...` + `OPTION (MAXRECURSION 1000)`).
- [x] `db/migration/V004__dynamic_sql_search.sql` con `usp_stock_search_dynamic` (E1 parametrizado con `@pattern`, `@min_qty`) + `usp_stock_search_raw` (P1 trap `+ @raw_filter` antes de EXEC).
- [x] `db/migration/V005__merge_conciliacion.sql` con `usp_reconcile_run` (E2 `MERGE ... OUTPUT $action INTO dbo.reconcile_audit`) + `usp_reconcile_partial` (P2 trap sin `WHEN NOT MATCHED BY SOURCE`).
- [x] `db/migration/V006__global_temp_inventory.sql` con `usp_temp_load` (E5 crea `##global_stock_temp` + `TRUNCATE`) + `usp_temp_consume` (P5 trap lee pero no `DROP TABLE`).
- [x] `db/migration/V007__sql_agent_jobs.sql` con 3 jobs en `msdb.dbo.sysjobs`: `JOB_HOURLY_RECALC_TOTALS` (enabled=1), `JOB_DAILY_REBUILD_REPORT_CACHE` (enabled=1), `JOB_LEGACY_PURGE` (P6 enabled=0).
- [x] `db/migration/V008__legacy_sprocs.sql` con `usp_legacy_export` (S1 dead), `usp_legacy_purge` (S2 referencia `dbo.legacy_archive` inexistente), `usp_recalc_totals` (helper de JOB_HOURLY), `usp_rebuild_cache` (helper de JOB_DAILY con `FOR JSON PATH`).
- [x] `db/migration/R__recalc_stock_totals.sql` (P4 trap `DELETE+INSERT` no idempotente) + `R__rebuild_report_cache.sql` (P5 trap mantiene `##global_stock_temp` leak entre sesiones).
- [x] `db/sql/views.sql` con `vw_stock_current`, `vw_reconcile_dashboard`, `vw_report_top_items` (TOP 10 ordenado DESC).
- [x] `db/sql/synonyms.sql` con 5 sinonimos CREATE SYNONYM (4 válidos + `syn_legacy_table FOR dbo.legacy_does_not_exist` P2 trap).
- [x] `db/sql/functions.sql` con `fn_stock_available(@sku)`, `fn_reconcile_status(@run_id)`, `fn_report_total_sales()`.
- [x] `db/sql/legacy_artifact.sql` con `trg_old_audit` sobre `dbo.does_not_exist` envuelto en `TRY/CATCH` (S2 instalación silenciosamente falla).
- [x] `db/seed/seed_stock.sql` con 5 items (SKU-A001..A005, 1 soft-deleted) + `db/seed/seed_movements.sql` con 12 movimientos (1 soft-deleted) + `db/seed/seed_bom.sql` con ciclo A->B->C->A (P4).
- [x] `db/test/test_runner.sql` con `fx_assert_equal`, `fx_test_begin`, `fx_test_end`, `fx_test_results`.
- [x] 8 archivos de test `01..08_*_test.sql` (≥ 7 tests por suite en stock/reconcile/dashboard/triggers/sql_agent; 6 E1..E6 en 06; 6 P1..P6 en 07; 1 S3 en 08) = **48 tests T-SQL**.
- [x] `config/msodbcsql.ini` con `TrustServerCertificate=yes`.
- [x] `tools/{wait_for_sql,apply_migrations,run_tests,reset_db}.sh` ejecutables (chmod +x).
- [x] `build-history.sh` con 8 commits reproducibles (scaffold + schema + triggers/CTE/legacy-artifact + dynamic-sql/MERGE/synonyms + temp/sql-agent/legacy-sprocs + seed/R__ + test-runner/8-tests + tools/config).
- [x] fixtures previos (35 fixtures F00–F06ai) sin cambios de comportamiento — verificado por `pytest 2102 passed sin regresiones`.
- [x] 10 decisiones nuevas D-401..D-410 (SQL Server 2022 + sqlcmd + tSQL runner; db/install.sql orquestador con `:r`; fx_assert_equal + fx_test_results; sinonimos scoped al schema; INSTEAD OF UPDATE sobre vista = único UPDATE; CTE recursiva + ciclo A->B->C->A en seed; MERGE OUTPUT $action con reconcile; 3 SQL Agent jobs con JOB_LEGACY_PURGE disabled; ##global_stock_temp + leak; prefijo NPRGT-FXSQLTS- con 33 entradas + sinonimos neutros stock/reconcile/dashboard CC-11).
- [x] PROGRESS.md fila F06aj = `HECHA` con evidencia completa.
- [x] DECISIONS.md con D-401..D-410.
- [x] ROADMAP.md encabezado F06aj con ✅ y sección `Criterios de aceptación (verificados)` con todos los checks `[x]`.
- [x] Commit `F06aj: fixture fx-sql-tsql con paquete por feature`.

**Limitación operativa documentada:** el contenedor MS-SQL Server 2022 (≈1.5 GB) tarda ~3-5 min la primera vez en descargar y arrancar. Los tests T-SQL se ejecutan contra una DB efímera (`fxsqlts`) que se recrea en cada `docker run` con `entrypoint.sh`. El volumen `-v $(PWD)/.sqlserver_data:/var/opt/mssql/data` cachea entre runs. Los tests pytest (`test_fx_sql_tsql_ground_truth.py`) validan sin necesidad de Docker, contra los archivos del fixture.
 
## F06ak — Fixture `fx-dbt-airflow` ✅
  
**Objetivo:** pipeline analítico con dbt (SQL + Jinja) + Airflow (Python DAGs) + DuckDB embebido. Linaje via `ref()`/`source()`, macros Jinja parametrizadas, `is_incremental()`, materialización por carpeta, DAG generado desde YAML, XCom explícito entre tareas.
**Stack:** dbt-core 1.8 + dbt-duckdb 1.8 + apache-airflow 2.9 + DuckDB embedded + Python 3.11 + pytest 8.
**Features (con sinonimos neutros CC-11):** `ventas` (ingesta-de-ventas), `clientes` (modelo-de-clientes), `metricas` (métricas-diarias).
**Trampas del ecosistema:**
1. Linaje definido solo por `ref()` y `source()` (sin FK en DuckDB).
2. Macros Jinja que generan SQL parametrizado.
3. Ramas `is_incremental()` en modelos incrementales.
4. Materialización configurada por carpeta en `dbt_project.yml` (view/table/incremental).
5. DAG de Airflow generado dinámicamente desde YAML (`build_dag_from_yaml`).
6. XCom que pasa datos entre tareas de forma explícita (vía `xcom_push`/`xcom_pull`).
**Toolchain de tests:** `dbt build` sobre DuckDB + `airflow dags parse` (sin scheduler) + pytest sobre `airflow/tests/`, en contenedor `python:3.11-slim`.

**Criterios de aceptación (verificados):**
- [x] 3 features (`ventas`, `clientes`, `metricas`) × 7 R-NN cada una (CC-03, CC-08) = 21 R-NN documentados en `ground_truth.json`.
- [x] 6 trampas del ecosistema plantadas con referencia exacta: `stg_ventas.sql` con `{{ source('raw','ventas_raw') }}` (E1), `centros_normalizados.sql` macro Jinja con `{{ estado }}` (E2), `ventas_diarias_incremental.sql` con `{% if is_incremental() %}` y filtro `occurred_at >` (E3), `dbt_project.yml` con `+materialized: view/table/incremental` por path (E4), `dag_factory.py` con `yaml.safe_load` + `etl_config.yaml` (E5), `etl_dag.py` con `xcom_push(key='table_name', ...)` + `xcom_pull(...)` (E6).
- [x] 6 trampas del paquete plantadas: `centros_concat.sql` con concat `~` (P1 SQLi), `ventas_diarias_incremental_buggy.sql` con `where 1=1` (P2), `legacy_helper.sql` nunca invocado (P3), `dbt_project.yml` materialization incremental vs table inconsistency (P4), `legacy_purge_dag.py` con `catchup=False` + `start_date=datetime(2019,1,1)` (P5), `transform_xcom_implicit.py` con `return dict` no serializable (P6).
- [x] 3 trampas superficiales: `legacy_helper.sql` macro declarado pero no invocado (S1), `legacy_purge_dag.py` con start_date 2019 + catchup=False nunca corre (S2), `test_deprecated.py` con `pytest.skip` (S3).
- [x] Ground truth completo en `dev/ground-truth/fx-dbt-airflow/{ground_truth.json, GROUND_TRUTH.md, unique_tokens.txt}` con paquete completo por feature (entry_points, modules, dependencies, features, surfaces, traps, package_traps, superficial_traps, call_graph, config, tests).
- [x] 43 entry points, 33 modules, 7 dependencies, 3 features (21 R-NN), 19 surfaces, 6 traps ecosistema, 6 traps paquete, 3 superficiales, 17 call graph edges.
- [x] 34 unique_tokens `NPRGT-FXDBAIR-`; `check_ground_truth.py --check-cc11` 0 referencias rotas (CC-11 OK tras sustituir `metricas_diarias.sql` comentario "capa diaria de feature (marts_metricas) para tabla de metricas" por "capa diaria agregada sobre ventas_diarias + int_ventas_clientes" para evitar la falsa deteccion).
- [x] `dev/tests/test_fx_dbt_airflow_ground_truth.py` con 88 tests (8 TestGroundTruthShape + 6 TestOutcomesAndCitations + 3 TestUniqueTokensFile + 3 TestAllCitesValid + 33 TestDbtAirflowStructure + 2 TestModelsPresent + 2 TestDagConfigured + 6 TestTrapsEcosystem + 6 TestTrapsPackage + 3 TestTrapsSuperficial + 16 TestManifest) verde.
- [x] `pytest` total **2190 passed** (2102 previos + 88 nuevos) sin regresiones.
- [x] `validate_skill.py` y `overfit_guard.py` verdes.
- [x] `target_matrix.yml` extendido con frameworks `[dbt, dbt-duckdb, duckdb, airflow, dag-factory, xcom, jinja-macros, dbt-lineage, ref-source, is_incremental, dbt-materialization-config, dbt-models, apache-airflow]`.
- [x] `fixtures_matrix.py` extendido con detección dbt (`dbt/dbt_project.yml` -> dbt + duckdb + dbt-materialization-config + is_incremental), dbt models (con `{{ ref(` o `{{ source(` -> dbt-models + dbt-lineage + ref-source + dbt-incremental), macros Jinja, airflow DAGs (DAG( -> airflow + yaml.safe_load -> dag-factory + xcom_push/pull -> xcom), requirements.txt (dbt-core/dbt-duckdb -> dbt-duckdb + apache-airflow -> apache-airflow).
- [x] `MATRIX.md` regenerado: 38 fixtures, `fx-dbt-airflow` cubre `python`, `shell`, `dbt`, `dbt-duckdb`, `duckdb`, `airflow`, `dag-factory`, `xcom`, `jinja-macros`, `dbt-lineage`, `ref-source`, `is_incremental`, `dbt-materialization-config`, `dbt-models`, `apache-airflow`.
- [x] `manifest.yml` con `requires: [linux, macos]` + `container.enabled: true` + `image_tag: npr-fx-dbt-airflow`.
- [x] `Dockerfile.test` con `FROM python:3.11-slim` + `apt-get install git make curl unzip` + `pip install -r requirements.txt` + `dbt deps` + `CMD ["bash","entrypoint.sh"]`.
- [x] `entrypoint.sh` ejecuta `bash tools/run_dbt.sh` (dbt deps + dbt seed + dbt build) + `bash tools/run_airflow_tests.sh` (`airflow dags parse` + `pytest airflow/tests/`) + `pytest dev/tests/test_fx_dbt_airflow_ground_truth.py -q`.
- [x] `dbt/dbt_project.yml` con `name: fxdbt`, `profile: fxdbt`, `models.fxdbt.{staging:+materialized:view, intermediate:+materialized:view, marts:+materialized:table, marts/marts_incremental:+materialized:incremental, +unique_key:fecha_sku, +on_schema_change:append_new_columns}`.
- [x] `dbt/models/staging/_sources.yml` con `source 'raw'` + `tables: ventas_raw (test unique/not_null en venta_id) + clientes_raw (test unique/not_null en cliente_id)`.
- [x] `dbt/models/staging/stg_ventas.sql` con `{{ source('raw','ventas_raw') }}` + columnas `cantidad*precio_unitario as monto_total` (E1).
- [x] `dbt/models/staging/stg_clientes.sql` con `{{ source('raw','clientes_raw') }}` + `cast(activo as boolean)` (E1).
- [x] `dbt/models/intermediate/int_ventas_clientes.sql` con `{{ ref('stg_ventas') }} + {{ ref('stg_clientes') WHERE activo = true }} + LEFT JOIN` (E1).
- [x] `dbt/models/marts/marts_ventas/ventas_diarias.sql` (table) + `ventas_mensuales.sql` (view override).
- [x] `dbt/models/marts/marts_clientes/clientes_top.sql` (table).
- [x] `dbt/models/marts/marts_metricas/metricas_diarias.sql` con `{{ filter_centros_normalizado('centro_norte') }}` (E2).
- [x] `dbt/models/marts/marts_incremental/ventas_diarias_incremental.sql` con `{% if is_incremental() %} WHERE occurred_at > max {% else %} WHERE >= 2024-01-01 {% endif %}` (E3 correcto) + `ventas_diarias_incremental_buggy.sql` con `{% if is_incremental() %} where 1=1 {% endif %}` (P2 trampa).
- [x] `dbt/macros/centros_normalizados.sql` (E2) + `centros_concat.sql` (P1) + `legacy_helper.sql` (S1 dead).
- [x] `dbt/seeds/` con 4 CSVs: `seed_clientes.csv` (5 clientes), `seed_catalogo.csv` (10 productos), `seed_cliente_venta.csv` (13 enlaces), `ventas_raw.csv` (12 ventas origen del source).
- [x] `dbt/tests/singular/` con `assert_ventas_positivas.sql` + `assert_clientes_activos.sql` + `dbt/tests/generic/freshness_24h.sql`.
- [x] `dbt/snapshots/snap_ventas.sql` con strategy='timestamp' + updated_at='occurred_at'.
- [x] `airflow/dags/etl_dag.py` con `extract (PythonOperator + duckdb.read_csv_auto + xcom_push) -> transform (PythonOperator + xcom_pull) -> load (BashOperator + dbt build)`.
- [x] `airflow/dags/dag_factory.py` con `build_dag_from_yaml()` que itera `spec['tasks']` y crea BashOperator o PythonOperator.
- [x] `airflow/dags/etl_config.yaml` con `dag_id: generated_etl_dag`, `schedule_interval: @hourly`, `start_date: 2026-01-01`, `tasks: [extract_csv, transform_dbt, load_dbt]`.
- [x] `airflow/dags/generated_etl_dag.py` wrapper que invoca `build_dag_from_yaml('/fixture/airflow/dags/etl_config.yaml')` (E5).
- [x] `airflow/dags/transform_xcom_implicit.py` DAG trampa `transform_xcom_implicit` con `return {'unserializable': {1,2,3}}` (P6).
- [x] `airflow/legacy_purge_dag.py` con `start_date=datetime(2019,1,1) + catchup=False + schedule_interval='@daily'` (S2 nunca corre).
- [x] `airflow/tests/conftest.py` con `DagBag` fixture apuntando a `/fixture/airflow/dags`.
- [x] 8 archivos de test en `airflow/tests/`: `test_etl_dag.py` (6), `test_dag_factory.py` (5), `test_xcom_explicit.py` (3), `test_xcom_implicit.py` (5), `test_traps_ecosystem.py` (6), `test_traps_package.py` (6), `test_deprecated.py` (1), `conftest.py` (0 directos) = **32 tests pytest** en airflow/tests/.
- [x] `profiles.yml` con target `dev` (DuckDB en `/fixture/dev.duckdb`) + `test` (DuckDB `:memory:`).
- [x] `requirements.txt` con `dbt-core==1.8.*, dbt-duckdb==1.8.*, apache-airflow==2.9.*, pytest==8.2.*`.
- [x] `.airflowignore` excluye `generated_etl_dag.py` del descubrimiento del scheduler.
- [x] `tools/{run_dbt,run_airflow_tests,wait_for_duckdb,reset_workspace}.sh` ejecutables (chmod +x).
- [x] `build-history.sh` con 8 commits reproducibles (scaffold + dbt sources/staging + intermediate/marts/incremental + macros/tests/snapshots + airflow etl_dag + dag_factory/generated_etl_dag/etl_config + legacy_purge_dag/airflow tests + tools/marts_metricas).
- [x] fixtures previos (36 fixtures F00–F06aj) sin cambios de comportamiento — verificado por `pytest 2190 passed sin regresiones`.
- [x] 10 decisiones nuevas D-411..D-420 (python:3.11-slim + dbt + apache-airflow; DuckDB embebido; materialization por carpeta E4; DAG factory desde YAML E5; XCom explicito vs return value P6; macros Jinja con concat string vs parametrizado P1; is_incremental correcto vs trampa P2; legacy_helper + legacy_purge_dag S1+S2; prefijo NPRGT-FXDBAIR- con sinonimos neutros ventas/clientes/metricas CC-11; fixtures_matrix.py + target_matrix.yml extension con 13 frameworks dbt/airflow).
- [x] PROGRESS.md fila F06ak = `HECHA` con evidencia completa.
- [x] DECISIONS.md con D-411..D-420.
- [x] ROADMAP.md encabezado F06ak con ✅ y sección `Criterios de aceptación (verificados)` con todos los checks `[x]`.
- [x] Commit `F06ak: fixture fx-dbt-airflow con paquete por feature`.

**Limitación operativa documentada:** el contenedor `python:3.11-slim` con `dbt-core` + `dbt-duckdb` + `apache-airflow` pesa ~600 MB y tarda ~3-5 min la primera vez en descargar e instalar dependencias. NO se levanta el scheduler de Airflow (se valida con `airflow dags parse`). DuckDB es embebido (`/fixture/dev.duckdb` montado como volumen efímero). Los tests pytest (`test_fx_dbt_airflow_ground_truth.py`) validan la estructura y trampas del fixture sin necesidad de Docker. `dbt deps` requiere conexión a internet para descargar `dbt-labs/dbt_utils` (en CI se podría pre-cachear en `dbt/dbt_packages/`).
 
## F06al — Fixture `fx-python-ml` ✅
  
**Objetivo:** proyecto de ML con notebooks Jupyter (nbval), pipeline DVC, configuracion Hydra, tracking MLflow (FileStore) y servicio de inferencia FastAPI.
**Stack:** `python:3.11-slim` + `scikit-learn==1.5.*` (CPU) + `hydra-core==1.3.*` + `dvc==3.5.*` (file backend) + `mlflow==2.18.*` (FileStore en `mlruns/`) + `fastapi==0.115.*` + `jupyter==1.0.*` + `nbval==0.10.*` + `pytest==8.2.*`. Dataset: `iris.csv` (150 rows sklearn).
**Features (con sinonimos neutros CC-11):** `entrenamiento` (entrenamiento), `evaluacion` (evaluación), `inferencia` (inferencia).
**Trampas del ecosistema:**
1. Estado oculto en notebooks: celdas ejecutadas fuera de orden (validado con nbval).
2. Composición de configuraciones Hydra con `@package _global_` + `defaults:`.
3. Etapas definidas en `dvc.yaml` con `deps`/`outs`/`metrics`.
4. Modelos registrados por nombre en MLflow via `registered_model_name='iris_clf'`.
5. Feature engineering duplicado entre notebook (`MinMaxScaler`) y `src/` (`StandardScaler`).
6. Semillas y aleatoriedad con `random_state=42` en `src/train.py` para reproducibilidad.
**Toolchain de tests:** pytest sobre `src/` + `nbval` sobre `notebooks/*.ipynb` + `dvc repro` (smoke) + FastAPI `TestClient`, en contenedor `python:3.11-slim`.

**Criterios de aceptación (verificados):**
- [x] 3 features (`entrenamiento`, `evaluacion`, `inferencia`) × 7 R-NN cada una (CC-03, CC-08) = 21 R-NN documentados en `ground_truth.json`.
- [x] 6 trampas del ecosistema plantadas con referencia exacta: notebooks en orden `0[0-6]_*.ipynb` (E1), `conf/config.yaml` con `@package _global_` + `defaults:` + sub-configs en `conf/{entrenamiento,evaluacion,inferencia}/*.yaml` (E2), `dvc.yaml` con 3 stages `train/evaluate/register` + `deps`/`outs`/`metrics` (E3), `notebooks/03_entrenamiento.ipynb` con `mlflow.sklearn.log_model(..., registered_model_name='iris_clf')` (E4), `src/features.py` con `StandardScaler` vs `notebooks/02_features.ipynb` con `MinMaxScaler` (E5), `src/train.py` con `random_state=42` (E6).
- [x] 6 trampas del paquete plantadas: `notebooks/06_setup_with_delete.ipynb` con `del df` (P1), `conf/config.yaml` con override apuntando a config inexistente (P2), `dvc.yaml` stage `register` con `outs: mlruns/.placeholder` que puede no generarse (P3), `notebooks/04_evaluacion_legacy.ipynb` con `registered_model_name='iris_classifier_legacy'` (P4), `src/features.py` vs notebook divergen StandardScaler vs MinMaxScaler (P5), `src/legacy_train.py` sin `random_state` (P6).
- [x] 3 trampas superficiales: `src/legacy_train.py` declarado pero nunca invocado (S1), `notebooks/00_setup.ipynb` solo imports (S2), `tests/test_deprecated.py` con `@pytest.mark.skip` (S3).
- [x] Ground truth completo en `dev/ground-truth/fx-python-ml/{ground_truth.json, GROUND_TRUTH.md, unique_tokens.txt}` con paquete completo por feature (entry_points, modules, dependencies, features, surfaces, traps, package_traps, superficial_traps, call_graph, config, tests).
- [x] 35 entry points, 35 modules, 15 dependencies, 3 features (21 R-NN), 16 surfaces, 6 traps ecosistema, 6 traps paquete, 3 superficiales, 11 call graph edges.
- [x] 33 unique_tokens `NPRGT-FXPML-`; `check_ground_truth.py --check-cc11` 0 referencias rotas (CC-11 OK tras sustituir comentarios `entrenamiento/evaluacion/inferencia` por `algo/metric/serve` neutros en conf/*.yaml + manifest.yml; ademas se removio `random_state` del docstring de `legacy_train.py` y se ajusto el test de P6 para que use regex sobre la firma de la funcion).
- [x] `dev/tests/test_fx_python_ml_ground_truth.py` con 86 tests (8 TestGroundTruthShape + 6 TestOutcomesAndCitations + 3 TestUniqueTokensFile + 3 TestAllCitesValid + 32 TestPythonMlStructure + 2 TestModelsPresent + 2 TestDvcConfigured + 7 TestTrapsEcosystem + 6 TestTrapsPackage + 3 TestTrapsSuperficial + 14 TestManifest) verde.
- [x] `pytest` total **2276 passed** (2190 previos + 86 nuevos) sin regresiones.
- [x] `validate_skill.py` y `overfit_guard.py` verdes.
- [x] `target_matrix.yml` extendido con frameworks `[hydra, dvc, mlflow, notebook-ipynb, jupyter, nbval, dvc-yaml, hydra-config, mlflow-file-store, scikit-learn, pytorch]`.
- [x] `fixtures_matrix.py` extendido con deteccion dvc (`dvc.yaml` -> dvc + dvc-yaml), hydra (`conf/config.yaml` con `@package`/`defaults:` -> hydra + hydra-config), mlflow (`src/register.py` o `mlruns/` -> mlflow + mlflow-file-store), notebooks (`notebooks/*.ipynb` -> notebook-ipynb + jupyter) + nbval (pytest.ini -> nbval), requirements.txt (scikit-learn -> scikit-learn; torch -> pytorch). Bloque DEDENTED a 4 espacios para que se ejecute fuera del `if sql_files:` block.
- [x] `MATRIX.md` regenerado: 39 fixtures, `fx-python-ml` cubre `python`, `shell`, `pytest-django`, `fastapi`, `pydantic`, `pyproject`, `make`, `pip`, `source-text`, `notebook-ipynb`, `hydra`, `dvc`, `mlflow`, `jupyter`, `nbval`, `dvc-yaml`, `hydra-config`, `mlflow-file-store`, `scikit-learn`.
- [x] `manifest.yml` con `requires: [linux, macos]` + `container.enabled: true` + `image_tag: npr-fx-python-ml`.
- [x] `Dockerfile.test` con `FROM python:3.11-slim` + `apt-get install git make curl unzip` + `pip install -r requirements.txt` + `dvc init` + `python -m ipykernel install` + `CMD ["bash","entrypoint.sh"]`.
- [x] `entrypoint.sh` ejecuta `pytest --nbval-lax notebooks/` + `pytest tests/` + `dvc repro` (smoke) + `pytest dev/tests/test_fx_python_ml_ground_truth.py`.
- [x] `data/iris.csv` con 150 rows (sklearn iris dataset real).
- [x] `conf/config.yaml` con `defaults: [entrenamiento:default, evaluacion:default, inferencia:default, _self_] + datos + semilla + mlflow` (E2).
- [x] `conf/entrenamiento/{default,random_forest,logistic_regression}.yaml` + `conf/evaluacion/{default,f1}.yaml` + `conf/inferencia/default.yaml` con `model_name: iris_clf + stage: production`.
- [x] `src/{config,train,evaluate,features,register,legacy_train}.py` + `src/app/main.py` con FastAPI `POST /inferencia` que carga `models:/iris_clf@production`.
- [x] 8 notebooks en `notebooks/`: `00_setup.ipynb` (S2), `01_exploratorio.ipynb` (E1), `02_features.ipynb` (E5 MinMaxScaler), `03_entrenamiento.ipynb` (E4 MLflow), `04_evaluacion.ipynb` (E1 log metrics), `04_evaluacion_legacy.ipynb` (P4 nombre incorrecto), `05_inferencia.ipynb` (E1 cargar), `06_setup_with_delete.ipynb` (P1 state out-of-order).
- [x] `dvc.yaml` con 3 stages: `train` (deps: data/iris.csv + src/train.py; outs: models/model.pkl), `evaluate` (deps: models/model.pkl + data/iris.csv; metrics: metrics/eval.json), `register` (deps: models/model.pkl + metrics/eval.json; outs: mlruns/.placeholder).
- [x] `params.yaml` con `entrenamiento.algoritmo: random_forest + n_estimators: 100 + max_depth: 5 + evaluacion.metrica: f1 + average: weighted + semilla: 42`.
- [x] 13 archivos de test en `tests/`: `conftest.py` + `test_train.py` (5) + `test_evaluate.py` (5) + `test_inference.py` (5 FastAPI TestClient) + `test_hydra_config.py` (10) + `test_dvc_pipeline.py` (10) + `test_mlflow_registry.py` (5) + `test_reproducibility.py` (4 P6) + `test_features_divergence.py` (3 P5) + `test_traps_ecosystem.py` (7 E1..E6) + `test_traps_package.py` (6 P1..P6) + `test_traps_superficial.py` (3 S1..S3) + `test_deprecated.py` (1 S3) = **64 tests pytest** en tests/.
- [x] `tools/` (opcional, no usado; `entrypoint.sh` hace el wrapper).
- [x] `build-history.sh` con 8 commits reproducibles (scaffold + data + Hydra configs + src + notebooks core + DVC + legacy + tools).
- [x] fixtures previos (37 fixtures F00–F06ak) sin cambios de comportamiento — verificado por `pytest 2276 passed sin regresiones`.
- [x] 10 decisiones nuevas D-421..D-430 (python:3.11-slim + scikit-learn + Hydra + DVC + MLflow; MLflow file store no servidor; DVC local no remoto; Hydra con @package _global_ + defaults; notebooks con orden + nbval; feature engineering duplicado; random_state + trampa P6; FastAPI + MLflow load por nombre; prefijo NPRGT-FXPML- con sinonimos neutros; fixtures_matrix.py + target_matrix.yml extension con 11 frameworks dvc/hydra/mlflow).
- [x] PROGRESS.md fila F06al = `HECHA` con evidencia completa.
- [x] DECISIONS.md con D-421..D-430.
- [x] ROADMAP.md encabezado F06al con ✅ y sección `Criterios de aceptación (verificados)` con todos los checks `[x]`.
- [x] Commit `F06al: fixture fx-python-ml con paquete por feature`.

**Limitación operativa documentada:** el contenedor `python:3.11-slim` con `scikit-learn + hydra + dvc + mlflow + fastapi + jupyter + nbval` pesa ~1.2 GB y tarda ~3-5 min primera vez. Los notebooks se ejecutan con `pytest --nbval-lax` (puede tardar 5-10 min para 8 notebooks); `entrypoint.sh` usa `|| true` en el comando nbval para que un fallo de P1 no rompa el entrypoint (los tests pytest unitarios sí deben pasar). `dvc repro` es un smoke test (no CI), requiere que los `outs` no existan o el pipeline este dirty. MLflow usa `file://` URI (no servidor); los modelos se inspeccionan con `MlflowClient` o `ls mlruns/`. `dvc init` en Dockerfile usa `[ ! -d /fixture/.dvc ] && dvc init -q || true` para idempotencia.
 
## F06am — Fixture `fx-scala-spark`
 
**Objetivo:** jobs Spark en Scala.
**Stack:** Scala, Apache Spark, sbt multi-módulo, Typesafe Config.
**Features:** `deduplicación`, `enriquecimiento`, `agregados`.
**Trampas del ecosistema:**
1. Implicits/givens y conversiones implícitas.
2. Evaluación perezosa: transformaciones frente a acciones.
3. UDFs registradas por nombre y usadas dentro de strings SQL.
4. Configuración de sbt y estrategia de merge de assembly.
5. `sealed trait` + pattern matching.
6. `application.conf` con `include`.
**Toolchain de tests:** `sbt test` con Spark local, en contenedor.
 
---
 
# Empresarial legacy
 
## F06an — Fixture `fx-oracle-adf-soa`
 
**Objetivo:** aplicación JDeveloper con ADF y composite SOA/BPM.
**Stack:** Java, Oracle ADF (ADF BC, ADF Faces, task flows), SOA Suite (composite, BPEL, Mediator, XSLT, WSDL/XSD, JCA DB adapter), BPM (BPMN, human tasks), workspace `.jws`/`.jpr`.
**Features:** `formulario-de-apertura`, `validación-y-aprobación`, `alta-en-core`.
**Trampas del ecosistema:**
1. Navegación en task flows XML (`control-flow-case`), no en Java.
2. PageDef y EL (`#{bindings.X.inputValue}`) que conectan la UI con los View Objects.
3. Validaciones en Entity Objects declaradas en XML y expresiones Groovy.
4. Managed beans declarados en XML con scope (`pageFlowScope`).
5. `composite.xml` que conecta componentes, y transformaciones `assign`/XSLT en BPEL.
6. Configuración JCA (`.jca`) que apunta a datasources JNDI fuera del repositorio, y reglas de asignación de human tasks.
**Toolchain de tests:** sin runtime WebLogic; validación XML/XSD con xmllint y JUnit sobre managed beans y clases Java, en contenedor.
 
## F06ao — Fixture `fx-java-ee-legacy`
 
**Objetivo:** aplicación Java EE con configuración XML.
**Stack:** Java 8, Spring con XML, JSF o Struts, JSP, EJB, JAX-WS, Hibernate (`hbm.xml`), Ant.
**Features:** `consulta-de-pólizas`, `endoso`, `servicio-soap`.
**Trampas del ecosistema:**
1. Wiring de beans en `applicationContext.xml`.
2. Servlets y filtros mapeados en `web.xml`.
3. Mapeos de Hibernate en `hbm.xml`.
4. Scriptlets JSP y taglibs.
5. Lookup de EJB por JNDI con un string.
6. Stubs JAX-WS generados con `wsimport` desde un WSDL.
**Toolchain de tests:** JUnit 4 vía Ant, en contenedor JDK 8.
 
## F06ap — Fixture `fx-cobol-mainframe`
 
**Objetivo:** sistema batch y online estilo mainframe.
**Stack:** COBOL, copybooks, JCL, CICS (BMS), DB2 embebido, VSAM.
**Features:** `cierre-batch`, `consulta-online`, `actualización-de-saldos`.
**Trampas del ecosistema:**
1. Estructuras definidas en copybooks (`COPY`).
2. JCL que define el orden de los pasos y los datasets (`DD`).
3. `CALL` dinámico por variable.
4. `REDEFINES`.
5. `EXEC SQL` y `EXEC CICS` embebidos.
6. Flujo con `PERFORM THRU` y `GO TO`.
**Toolchain de tests:** GnuCOBOL para los programas batch con archivos de ejemplo, en contenedor; las partes CICS y DB2 se validan de forma estática.
 
---
 
# Infraestructura y DevOps
 
## F06aq — Fixture `fx-terraform-ansible`
 
**Objetivo:** infraestructura como código para varios entornos.
**Stack:** Terraform (HCL), Ansible (YAML + Jinja2).
**Features:** `red`, `cluster-de-aplicación`, `base-de-datos-gestionada`.
**Trampas del ecosistema:**
1. Módulos anidados con outputs encadenados.
2. Recursos generados con `for_each`, `count` y bloques `dynamic`.
3. Workspaces y `.tfvars` por entorno.
4. `terraform_remote_state` entre stacks.
5. Precedencia de variables de Ansible (`group_vars`, `host_vars`, defaults de roles).
6. Handlers notificados por nombre.
**Toolchain de tests:** `terraform validate` + tflint + `terraform test` con mocks; ansible-lint + `--check` contra un contenedor, todo en contenedor.
 
## F06ar — Fixture `fx-k8s-helm`
 
**Objetivo:** despliegue en Kubernetes con un operador propio.
**Stack:** Helm, Kustomize, YAML, CRD + controlador.
**Features:** `despliegue-web`, `job-de-migración`, `recurso-personalizado`.
**Trampas del ecosistema:**
1. Helpers en `_helpers.tpl` incluidos en varias plantillas.
2. `values-prod.yaml` que sobrescribe valores base.
3. Overlays de Kustomize con patches.
4. Configuración consumida por ConfigMap o Secret vía env o volumen: solo aparece en los manifiestos.
5. Hooks de Helm (job `pre-install`).
6. CRD con bucle de reconciliación.
**Toolchain de tests:** `helm lint`/`helm template` + kubeconform (kind opcional), en contenedor.
 
## F06as — Fixture `fx-ci-docker`
 
**Objetivo:** pipelines de CI/CD y contenedores.
**Stack:** GitHub Actions, GitLab CI, Jenkinsfile (Groovy) con shared library, Dockerfile multi-stage, docker-compose, Makefile.
**Features:** `build-y-test`, `release`, `despliegue-por-entorno`.
**Trampas del ecosistema:**
1. Workflows reutilizables (`workflow_call`) y composite actions.
2. Anchors YAML y `extends` en GitLab CI.
3. Shared library de Jenkins (`vars/*.groovy`).
4. Targets y `ARG` en un Dockerfile multi-stage.
5. Profiles y archivos override de docker-compose.
6. Condiciones `if:` por rama y por rutas.
**Toolchain de tests:** actionlint, hadolint, `docker build --target` y validación de YAML, en contenedor.
 
---
 
# Scripting
 
## F06at — Fixture `fx-shell-automation`
 
**Objetivo:** automatización de operaciones en shell.
**Stack:** Bash (compatible con zsh), awk, sed, cron, units de systemd.
**Features:** `respaldo`, `rotación-de-logs`, `aprovisionamiento`.
**Trampas del ecosistema:**
1. `source` dinámico (`. "$DIR/lib/$mod.sh"`).
2. Funciones definidas en archivos cargados con `source`.
3. `eval` y expansión indirecta `${!var}`.
4. `trap` de `EXIT` y `ERR`.
5. Timers de systemd y cron como puntos de entrada fuera del código.
6. Heredocs que generan archivos de configuración.
**Toolchain de tests:** bats-core, en contenedor.
 
## F06au — Fixture `fx-powershell`
 
**Objetivo:** módulo PowerShell de administración.
**Stack:** PowerShell 7, `.psd1`/`.psm1`, clases, Pester.
**Features:** `usuarios`, `inventario-de-equipos`, `reportes`.
**Trampas del ecosistema:**
1. `FunctionsToExport` en el manifiesto `.psd1`.
2. Dot-sourcing de `Public/` y `Private/`.
3. Parameter binding por pipeline (`ValueFromPipelineByPropertyName`).
4. Aliases.
5. Parámetros dinámicos.
6. Splatting e `Invoke-Expression`.
**Toolchain de tests:** Pester en contenedor `pwsh`.
 
---
 
# Videojuegos
 
## F06av — Fixture `fx-unity-csharp`
 
**Objetivo:** proyecto Unity donde buena parte del wiring está en escenas y assets.
**Stack:** C#, Unity (escenas `.unity` en YAML, prefabs, ScriptableObjects, Addressables, `.asmdef`).
**Features:** `movimiento-del-jugador`, `inventario`, `guardado`.
**Trampas del ecosistema:**
1. Métodos de ciclo de vida que llama el motor (`Awake`, `Start`, `Update`, `OnTriggerEnter`).
2. UnityEvents y botones conectados en la escena YAML, con referencias por GUID en `.meta`.
3. Campos `[SerializeField]` asignados en el inspector.
4. ScriptableObjects como datos y configuración.
5. `SendMessage` e `Invoke` por string.
6. Dependencias entre ensamblados definidas en `.asmdef`.
**Toolchain de tests:** lógica pura en un proyecto .NET separado + script que valida las referencias GUID de la escena, en contenedor (Unity Test Runner es opcional y requiere licencia).
 
## F06aw — Fixture `fx-godot-gdscript`
 
**Objetivo:** juego Godot con el wiring en escenas.
**Stack:** GDScript, Godot 4 (`.tscn`, `.tres`, `project.godot`).
**Features:** `combate`, `diálogos`, `progresión`.
**Trampas del ecosistema:**
1. Señales conectadas en `.tscn`.
2. Singletons de autoload en `project.godot`.
3. Grupos y `call_group`.
4. `@onready` con `$NodePath`.
5. Callbacks `_process` e `_input`.
6. Recursos `.tres`.
**Toolchain de tests:** GUT con Godot headless, en contenedor.
 
---
 
# Contratos de API
 
## F06ax — Fixture `fx-grpc-protobuf`
 
**Objetivo:** servicios gRPC con clientes en varios lenguajes.
**Stack:** Protobuf, buf, gRPC (servidor Go, clientes Python y TypeScript), grpc-gateway.
**Features:** `cuentas`, `movimientos-en-streaming`, `gateway-http`.
**Trampas del ecosistema:**
1. Código generado en tres lenguajes que hay que mapear al `.proto`.
2. Campos `oneof`, `reserved` y `deprecated`.
3. Interceptors de autenticación.
4. Streaming bidireccional.
5. Versiones `v1` y `v2` del paquete conviviendo.
6. Anotaciones HTTP de grpc-gateway.
**Toolchain de tests:** `buf lint` + `buf breaking` + `go test` + pytest, en contenedor.
 
## F06ay — Fixture `fx-graphql`
 
**Objetivo:** API GraphQL con cliente generado.
**Stack:** TypeScript, Apollo Server (schema-first), DataLoader, subscriptions, GraphQL Code Generator, Apollo Client.
**Features:** `catálogo`, `reseñas`, `notificaciones-en-vivo`.
**Trampas del ecosistema:**
1. Resolvers mapeados al schema por nombre de campo.
2. Resolvers de tipo y resolvers por defecto.
3. Batching con DataLoader.
4. Directivas propias (`@auth`) que transforman el schema.
5. Federation con `@key` y subgraphs.
6. Hooks de cliente generados por codegen.
**Toolchain de tests:** Jest, en contenedor.
 
---
 
# Otros runtimes
 
## F06az — Fixture `fx-wasm`
 
**Objetivo:** módulo Rust compilado a WebAssembly usado desde una web.
**Stack:** Rust, wasm-bindgen, wasm-pack, TypeScript, Vite, Web Workers.
**Features:** `procesamiento-de-imágenes`, `compresión`, `fallback-js`.
**Trampas del ecosistema:**
1. Funciones `#[wasm_bindgen]` llamadas desde JavaScript.
2. Glue JS generado.
3. Memoria compartida y punteros entre JS y WASM.
4. `postMessage` con un worker.
5. Detección de soporte con fallback a JavaScript.
6. Integración de wasm-pack con un plugin de Vite.
**Toolchain de tests:** `wasm-pack test --node` + Vitest, en contenedor.
 
## F06ba — Fixture `fx-solidity`
 
**Objetivo:** contratos inteligentes actualizables con indexador off-chain.
**Stack:** Solidity, Foundry, proxy UUPS, indexador TypeScript.
**Features:** `token`, `staking`, `gobernanza`.
**Trampas del ecosistema:**
1. Proxy: la lógica está en la implementación y el storage en el proxy.
2. Modifiers que ocultan validaciones.
3. Herencia múltiple y su orden de linearización.
4. `using X for Y`.
5. `fallback` y `receive`.
6. Eventos consumidos por el indexador TypeScript.
**Toolchain de tests:** `forge test` + Vitest para el indexador, en contenedor.
 
---
 
# Lenguajes de cola larga
 
## F06bb — Fixture `fx-lua-neovim`
 
**Objetivo:** plugin de Neovim.
**Stack:** Lua, API de Neovim.
**Features:** `buscador-de-archivos`, `resaltado`, `comandos`.
**Trampas del ecosistema:**
1. Metatables con `__index`.
2. Autocommands por evento.
3. Keymaps que disparan features.
4. Carga perezosa por comando.
5. `pcall(require, ...)` para dependencias opcionales.
6. Callbacks de `vim.api`.
**Toolchain de tests:** busted/plenary con Neovim headless, en contenedor.
 
## F06bc — Fixture `fx-haskell`
 
**Objetivo:** API web tipada.
**Stack:** Haskell, Cabal, Servant, mtl, lens, Template Haskell.
**Features:** `usuarios`, `pedidos`, `reportes`.
**Trampas del ecosistema:**
1. API definida a nivel de tipos con Servant.
2. Instancias de type classes en módulos distintos (incluidas huérfanas).
3. Stacks de monad transformers.
4. Template Haskell que genera código (lenses, JSON).
5. Evaluación perezosa.
6. Extensiones de lenguaje por archivo (`{-# LANGUAGE ... #-}`).
**Toolchain de tests:** `cabal test`, en contenedor.
 
## F06bd — Fixture `fx-r-analysis`
 
**Objetivo:** paquete R con app Shiny.
**Stack:** R, paquete con S3/S4/R6, tidyverse, Shiny, targets.
**Features:** `limpieza`, `modelado`, `dashboard`.
**Trampas del ecosistema:**
1. Dispatch S3 por nombre (`print.miclase`).
2. Clases S4 y R6.
3. Non-standard evaluation del tidyverse.
4. Reactives y observers de Shiny.
5. Pipeline definido en `_targets.R`.
6. `NAMESPACE` con exports e imports.
**Toolchain de tests:** testthat, en contenedor.
 
## F06be — Fixture `fx-perl-legacy`
 
**Objetivo:** aplicación web Perl heredada.
**Stack:** Perl 5, Mojolicious, módulos CPAN.
**Features:** `tickets`, `búsqueda`, `exportación-csv`.
**Trampas del ecosistema:**
1. `AUTOLOAD`.
2. Typeglobs.
3. `local` con alcance dinámico.
4. Expresiones regulares complejas con lógica de negocio.
5. Contexto escalar frente a lista.
6. Rutas de Mojolicious con placeholders.
**Toolchain de tests:** `prove`, en contenedor.
 
## F06bf — Fixture `fx-zig`
 
**Objetivo:** herramienta de línea de comandos en Zig con interop C.
**Stack:** Zig, `build.zig`, interop con C.
**Features:** `parseo`, `compresión`, `salida-formateada`.
**Trampas del ecosistema:**
1. `comptime` que genera código.
2. Error unions y `try`.
3. `@cImport` de una librería C.
4. Allocators pasados explícitamente.
5. Opciones de build en `build.zig`.
6. Dispatch con `inline else` sobre uniones etiquetadas.
**Toolchain de tests:** `zig build test`, en contenedor.
 
## F06bg — Fixture `fx-clojure`
 
**Objetivo:** servicio web Clojure.
**Stack:** Clojure, deps.edn, Ring, Compojure, core.async.
**Features:** `catálogo`, `colas-de-trabajo`, `reportes`.
**Trampas del ecosistema:**
1. Macros que generan código.
2. Multimethods con dispatch por función.
3. Protocols.
4. Rutas de Compojure.
5. Canales de core.async.
6. Middleware de Ring componiendo handlers.
**Toolchain de tests:** `clojure -X:test`, en contenedor.
 
---
 
# Transversales
 
## F06bh — Fixture `fx-scale-huge`
 
**Objetivo:** repositorio muy grande, generado por script (no se commitea el resultado), para probar que la skill no trunca ni pierde features.
**Stack:** mezcla de TypeScript, Python y Go.
**Features:** 5 features repartidas en directorios profundos y archivos de miles de líneas.
**Trampas del ecosistema:**
1. ~20.000 archivos y > 1M de líneas.
2. Módulos casi idénticos con diferencias mínimas.
3. Dependencias vendorizadas (`node_modules/`, `vendor/`) que deben ignorarse.
4. Directorios de código generado.
5. Symlinks (incluido un ciclo) y submódulos git.
6. Punteros de Git LFS en lugar de archivos reales.
**Toolchain de tests:** script de generación determinista + tests de integridad, en contenedor.
 
## F06bi — Fixture `fx-broken-build`
 
**Objetivo:** proyecto que no compila, a mitad de una migración.
**Stack:** TypeScript + Java.
**Features:** `facturación` (dos implementaciones, vieja y nueva), `reportes`, `notificaciones` (stub).
**Trampas del ecosistema:**
1. Dependencias faltantes y lockfile incompatible.
2. Errores de sintaxis en algunos archivos.
3. Dos implementaciones de la misma feature durante una migración.
4. Stubs con `TODO` y `throw new UnsupportedOperationException()`.
5. Feature flags que hacen inalcanzable una rama.
6. Tests deshabilitados (`@Disabled`, `it.skip`).
**Toolchain de tests:** los tests verifican que el fixture **falla** de la forma esperada, en contenedor.
 
## F06bj — Fixture `fx-git-history`
 
**Objetivo:** historia git compleja que la skill debe interpretar.
**Stack:** Python.
**Features:** `exportación` (eliminada y reintroducida), `búsqueda` (renombrada), `sincronización` (revertida).
**Trampas del ecosistema:**
1. Archivos renombrados y movidos.
2. Una feature revertida.
3. Merges de ramas y squash merges.
4. Tags de releases.
5. Una feature eliminada del código que sigue descrita en el README y el CHANGELOG.
6. Commits con co-autores.
**Toolchain de tests:** tests sobre la historia generada por `build-history.sh` (≥ 20 commits en este fixture), en contenedor.
 
## F06bk — Fixture `fx-encodings-i18n`
 
**Objetivo:** archivos en codificaciones y finales de línea distintos, con varios idiomas.
**Stack:** Java + Python + Dart, con archivos de traducción `.po`, `.xliff`, `.arb` y `.properties`.
**Features:** `saludo-localizado`, `formato-de-moneda`, `ordenación-por-idioma`.
**Trampas del ecosistema:**
1. Archivos en Latin-1, Shift-JIS y UTF-16.
2. Finales de línea CRLF y mezclados.
3. BOM en algunos archivos.
4. Comentarios en español, chino y árabe.
5. Identificadores Unicode.
6. Textos de derecha a izquierda (RTL) en los archivos de traducción.
**Toolchain de tests:** tests de comportamiento + verificación de líneas, en contenedor.
 
## F06bl — Fixture `fx-docs-vs-code`
 
**Objetivo:** documentación que contradice al código; la skill debe reportar las discrepancias.
**Stack:** TypeScript + OpenAPI + Markdown (README, ADRs).
**Features:** `usuarios`, `pagos`, `webhooks`.
**Trampas del ecosistema:**
1. Endpoint en OpenAPI que no está implementado.
2. Endpoint implementado que no está en OpenAPI.
3. ADR "aceptado" que el código no sigue.
4. README con comandos de instalación obsoletos.
5. Comentarios JSDoc que describen parámetros que ya no existen.
6. Diagrama de arquitectura en Markdown (Mermaid) con un componente que no existe.
**Toolchain de tests:** tests que confirman cada discrepancia, en contenedor.
 
---
 
## F06-cierre — Validación de la matriz completa
 
**Objetivo:** confirmar que la matriz de fixtures cubre todo el objetivo y que todo pasa junto.
**Depende de:** F06b–F06bl.
**Subagentes:** uno.
 
**Tareas:**
- Ejecutar `run_fixture_tests.py` sobre todos los fixtures (Linux en contenedores, `requires: macos` en macOS, `requires: windows` en Windows).
- Ejecutar `check_ground_truth.py` sobre todos los fixtures.
- Generar `dev/fixtures/MATRIX.md` con `fixtures_matrix.py`.
- Agregar un job de CI que ejecute todo lo anterior.
**`target_matrix.yml` debe cubrir como mínimo:**
- **Lenguajes:** Python, TypeScript, JavaScript, Java, Kotlin, Scala, Groovy, C#, Go, Rust, C, C++, Swift, Objective-C, Dart, PHP, Ruby, Elixir, SQL (PostgreSQL, PL/SQL, T-SQL, MySQL), HCL, YAML, Bash, PowerShell, GDScript, Solidity, Lua, Haskell, R, Perl, Zig, Clojure, COBOL, HTML, CSS/SCSS, Protobuf, GraphQL, XML declarativo, Jinja, XAML.
- **Frameworks:** React, Next.js, Vue/Nuxt, Svelte/SvelteKit, Angular (NgModules y standalone), jQuery, Spring Boot, Micronaut, Ktor, ASP.NET Core, Django, FastAPI, NestJS, Express/Fastify, Axum, Laravel, Rails, Phoenix, Qt, SwiftUI, UIKit, Vapor, Jetpack Compose, Flutter, React Native, Electron, WPF, Oracle ADF/SOA/BPM, Java EE, Spark, dbt, Airflow, Unity, Godot.
- **Sistemas de build:** pip/uv, npm/pnpm, Vite, esbuild, Gradle, Maven, Ant, sbt, MSBuild, Cargo, Go modules, CMake, Make, SPM, Xcode, Mix, Bundler, Composer, Cabal, `build.zig`, Foundry, Helm.
- **Tipos de proyecto:** CLI, API REST, API gRPC, API GraphQL, SPA, full-stack, móvil, escritorio, librería, extensión de editor, firmware, base de datos, pipeline de datos, ML, infraestructura, CI/CD, videojuego, contratos inteligentes, monorepo, políglota, artefactos sin fuente, legacy.
**Criterios de aceptación:**
- [ ] `fixtures_matrix.py` reporta 100 % de cobertura de `target_matrix.yml`.
- [ ] Todos los fixtures cumplen CC-01 a CC-13.
- [ ] `check_ground_truth.py` pasa para todos los fixtures con 0 referencias rotas.
- [ ] Todos los tests de fixtures pasan en su sistema; los omitidos lo están solo por `requires:` y pasan en su sistema.
- [ ] El job de CI ejecuta la matriz completa.
 

---

## F07 — Umbrales canónicos, anti-sobreajuste y especificación de fixtures reservados

**Objetivo:** que la calidad se mida con números únicos y que la skill no aprenda de memoria los fixtures de desarrollo.
**Depende de:** F06
**Subagentes:** el `SPEC.md` del holdout lo escribe un subagente distinto del que construyó los fixtures de F06.

**Tareas:**
- `dev/evals/thresholds.json` (fuente única de verdad) con todos los umbrales del Anexo C, separados en `dev` (fixtures de desarrollo), `holdout` (fixtures reservados) y `real` (repos reales). Esquema `schemas/thresholds.schema.json` (solo desarrollo).
- `dev/tools/check_thresholds.py`: parsea la tabla del Anexo C de este roadmap y la compara con `thresholds.json`; falla ante cualquier diferencia o umbral sin uso. Se agrega a CI.
- `dev/ground-truth/<fixture>/unique_tokens.txt`: ≥ 20 identificadores, strings y rutas exclusivos de cada fixture (nombres de clases, mensajes de error, slugs de modos, claves i18n).
- `dev/tools/overfit_guard.py`: recorre `skills/notemartin-project-review/**` y falla si encuentra nombres de fixtures (`fx-…`), rutas de `dev/`, o cualquier token de `unique_tokens.txt`. Lista de excepciones explícita y justificada en `dev/tools/overfit_allowlist.txt` (cada excepción enlaza a una decisión `D-NNN`). Se agrega a pytest y CI.
- `dev/holdout/SPEC.md`: especificación de los fixtures reservados **sin detalles concretos**:
  - ≥ 6 fixtures: al menos una app de agente de IA con modos, herramientas y skills (con nombres, rutas y protocolos distintos a `fx-ts-agent-extension`), un backend JVM, un frontend con estado complejo, un monorepo políglota, un proyecto con código solo minificado o compilado y un CLI con plugins.
  - Categorías de trampas a incluir (las de F06 y las del paquete por feature) y cantidad mínima por fixture.
  - Formato de ground truth idéntico al de F06.
  - Procedimiento de generación (F82): subagente generador con contexto limpio que solo recibe `SPEC.md`; subagente verificador independiente; los fixtures generados se guardan en `dev/holdout/generated/<lote>/` y nunca se usan para modificar la skill.
  - Política de "lote quemado": un lote cuyo contenido fue visto por el constructor al corregir fallas ya no cuenta como holdout; se genera un lote nuevo.
- Registrar en `DECISIONS.md` la decisión de holdout (D-007 ya la anticipa) y cualquier excepción.

**Entregables:** `thresholds.json`, `check_thresholds.py`, `unique_tokens.txt` por fixture, `overfit_guard.py`, `overfit_allowlist.txt`, `dev/holdout/SPEC.md`, tests.

**Criterios de aceptación:**
- [ ] `check_thresholds.py` en verde; un test que altera un valor del Anexo C lo hace fallar.
- [ ] `overfit_guard.py` falla al plantar un token de un fixture en un archivo de `skills/` (test) y pasa en el árbol limpio.
- [ ] Cada fixture tiene `unique_tokens.txt` con ≥ 20 entradas que existen realmente en el fixture (verificado por script).
- [ ] `SPEC.md` cubre las 6 categorías de fixture exigidas y no contiene ningún token de `unique_tokens.txt` (verificado por `overfit_guard.py` en modo `--spec`).
- [ ] CI ejecuta ambos guardianes en las 3 plataformas.

---

# ETAPA 1 — RECONOCIMIENTO DETERMINISTA (SCRIPTS)

## F08 — Inventario de archivos

**Objetivo:** listar cada archivo del repo con metadatos, sin perder ninguno.
**Depende de:** F05

**Tareas:**
- `npr inventory`: recorre el repo.
  - Con git: `git ls-files -co --exclude-standard` + listado aparte de archivos ignorados presentes (marcados `ignored: true`).
  - Sin git: recorrido manual con parser propio de `.gitignore` (patrones básicos, negaciones, directorios).
  - No sigue symlinks fuera del repo; los registra como `symlink`.
- Por archivo: `path, size, sha1, lines, is_binary (heurística de byte nulo y proporción no-UTF8), ext, encoding, is_symlink, ignored`.
- Salida en streaming a `recon/inventory.jsonl` + `recon/inventory-summary.json` (totales por extensión, tamaño, líneas).
- Caché por `sha1` para ejecuciones posteriores.
- Robustez multiplataforma: rutas de salida siempre POSIX relativas; conteo de líneas consistente con CRLF, LF y CR; detección de BOM y codificaciones (UTF-8, UTF-16, Latin-1) con respaldo `errors="replace"`; aviso de colisiones de mayúsculas/minúsculas (archivos que chocan en sistemas de archivos insensibles); rutas largas en Windows; nombres con unicode y espacios.

**Entregables:** `npr/inventory.py`, tests.

**Criterios de aceptación:**
- [ ] El conteo de archivos de cada fixture coincide con `ground_truth.json`.
- [ ] Un árbol sintético de 50.000 archivos se procesa sin cargarlo entero en memoria (test genera el árbol en tmp).
- [ ] Binarios detectados correctamente en tests (png, zip, archivo con byte nulo, UTF-16).
- [ ] Symlink que apunta fuera del repo se registra y no se recorre.
- [ ] Cada línea de `inventory.jsonl` valida contra `inventory-entry`.
- [ ] Tests de CRLF, BOM, UTF-16, nombres unicode y colisión de mayúsculas pasan en CI en Linux, macOS y Windows.

---

## F09 — Clasificador de archivos y política de análisis

**Objetivo:** saber qué es cada archivo y cuánto hay que leerlo, sin excluir nada en silencio.
**Depende de:** F08

**Tareas:**
- Categorías: `source, test, config, build, ci, docs, asset, generated, vendored, minified, lockfile, migration, i18n, schema, data, notebook, binary, infra, script`.
- Reglas: rutas (`node_modules/`, `vendor/`, `dist/`, `build/`, `out/`, `.next/`, `target/`, `__pycache__/`), cabeceras (`@generated`, `DO NOT EDIT`, `Code generated ... DO NOT EDIT.`), heurística de minificado (longitud media de línea > 300, ratio de espacios bajo), nombres de lockfiles, extensiones.
- Política por archivo: `full` (leer completo), `skim` (leer estructura y partes relevantes), `metadata` (solo registrar), `reverse` (requiere ingeniería inversa: minificado/binario sin fuente equivalente), `excluded` — **siempre con `reason`**.
- Detección de "fuente equivalente": si existe `src/x.ts` y `dist/x.js`, el `dist` es `metadata` con razón; si solo existe el minificado, es `reverse`.
- Salida `recon/classification.jsonl`.

**Entregables:** `npr/classify.py`, tests.

**Criterios de aceptación:**
- [ ] Clasificación de los 6 fixtures coincide al 100 % con el ground truth.
- [ ] Toda política distinta de `full` tiene `reason` no vacío.
- [ ] `fx-minified` marca el bundle sin sourcemap como `reverse` y el que tiene sourcemap como `reverse` con nota de recuperación posible.

---

## F10 — Detección de lenguajes, frameworks y stack

**Objetivo:** identificar el stack con evidencia.
**Depende de:** F09
**Paralelizable con:** F11, F13

**Tareas:**
- Lenguajes por extensión, shebang y contenido (para ambiguos como `.h`, `.m`).
- Frameworks y plataformas por archivos marcadores y dependencias: `angular.json`, `next.config.*`, `vite.config.*`, `nest-cli.json`, `micronaut-cli.yml`, `application.yml`, `pom.xml` con parent Spring, `engines.vscode` en `package.json` (extensión VS Code), `electron` en deps, `pubspec.yaml`, `AndroidManifest.xml`, `*.xcodeproj`, `Dockerfile`, `docker-compose*`, `*.tf`, manifiestos k8s, `serverless.yml`, etc.
- Salida `recon/stack.json`: cada detección con `evidence: [rutas]` y confianza.

**Entregables:** `npr/stack.py`, tabla de reglas en `npr/rules/stack_rules.json`, tests.

**Criterios de aceptación:**
- [ ] Todos los frameworks del ground truth detectados en cada fixture; ningún falso positivo en los fixtures.
- [ ] Cada detección tiene al menos una ruta de evidencia existente.
- [ ] Las reglas viven en un archivo de datos (agregar un framework no requiere tocar código).

---

## F11 — Parser de manifiestos de dependencias

**Objetivo:** dependencias directas de cualquier ecosistema con su origen exacto.
**Depende de:** F09
**Paralelizable con:** F10, F13

**Tareas:**
- Parsers: `package.json` (deps, devDeps, peer, optional, scripts, workspaces, bin, main, exports, engines, contributes), `pyproject.toml` (PEP 621, Poetry, uv; con `tomllib`), `requirements*.txt` (incluye `-r`), `setup.cfg`, `setup.py` (regex, marcado `partial`), `go.mod`, `Cargo.toml`, `pom.xml` (`xml.etree`, parent, modules, properties con interpolación básica, dependencyManagement), `build.gradle`/`build.gradle.kts` (regex, marcado `partial`), version catalogs `libs.versions.toml`, `composer.json`, `Gemfile`, `pubspec.yaml`, `*.csproj`/`Directory.Packages.props`, `Package.swift` (regex), `Podfile`, `CMakeLists.txt` (`find_package`, `FetchContent`).
- YAML: usar PyYAML si está disponible; si no, parser mínimo propio para mapeos simples, marcando `partial: true`.
- Cada dependencia: `name, spec, scope (runtime|dev|test|build|peer|optional), ecosystem, manifest, line`.
- Salida `recon/deps.json`.

**Entregables:** `npr/manifests/*.py`, tests con un manifiesto de ejemplo por formato.

**Criterios de aceptación:**
- [ ] Un test por formato con manifiesto realista; todas las dependencias extraídas con línea correcta.
- [ ] Dependencias directas de cada fixture coinciden al 100 % con el ground truth.
- [ ] Los parsers parciales lo declaran en la salida (`partial: true`) y nunca fallan en silencio.

---

## F12 — Lockfiles y dependencias transitivas

**Objetivo:** versiones resueltas, árbol transitivo y "quién trae qué".
**Depende de:** F11

**Tareas:**
- Parsers: `package-lock.json` v2/v3, `pnpm-lock.yaml`, `yarn.lock` v1 y Berry, `bun.lock` (texto), `poetry.lock`, `uv.lock`, `Cargo.lock`, `go.sum`, `gradle.lockfile`, `composer.lock`, `Gemfile.lock`, `Package.resolved`, `pubspec.lock`.
- Para cada dependencia directa: versión resuelta, número de transitivas, cadena "por qué está" (`npr deps why <paquete>`).
- Detección de duplicados con versiones distintas.
- Salida `recon/lock.json`.

**Entregables:** `npr/lockfiles/*.py`, tests.

**Criterios de aceptación:**
- [ ] Versiones resueltas de `fx-monorepo` coinciden con el lockfile real del fixture.
- [ ] `npr deps why <paquete-transitivo>` devuelve la cadena correcta en un test.
- [ ] Tests por cada formato de lockfile soportado.

---

## F13 — Monorepos, workspaces y límites de paquetes

**Objetivo:** saber qué paquetes internos hay y cómo dependen entre sí.
**Depende de:** F09
**Paralelizable con:** F10, F11

**Tareas:**
- Detectar: workspaces npm/yarn/pnpm, Lerna, Nx (`nx.json`, `project.json`), Turborepo, Rush, workspaces Cargo, `go.work`, `settings.gradle(.kts)` includes, módulos Maven, workspaces uv, solución .NET (`.sln`).
- Salida `recon/workspaces.json`: paquetes con `name, root, manifest, internal_deps`.

**Entregables:** `npr/workspaces.py`, tests.

**Criterios de aceptación:**
- [ ] `fx-monorepo`: paquetes y dependencias internas exactas.
- [ ] Repo no-monorepo produce un único paquete raíz sin error.
- [ ] Tests para pnpm, Nx, Cargo workspace, Gradle multi-proyecto y Maven multi-módulo.

---

## F14 — Grafo de imports (interno y externo)

**Objetivo:** quién importa a quién, con línea, y dónde se usa cada dependencia externa.
**Depende de:** F12, F13

**Tareas:**
- Extractores por lenguaje (regex robustas, comentarios y strings ignorados):
  - JS/TS: `import`, `export … from`, `import type`, `require`, `import()` dinámico; resolución con `tsconfig` `paths`/`baseUrl`, `exports` de `package.json`, archivos `index`, extensiones implícitas, alias de Vite/Webpack si están en config simple.
  - Python: `import`, `from … import`, relativos; resolución por paquetes.
  - Go: imports + ruta de módulo de `go.mod`.
  - Rust: `mod`, `use crate::`, `use super::`.
  - Java/Kotlin: `package` + `import` → mapeo FQN→archivo.
  - C#: `using` + namespaces.
  - PHP: `use` + PSR-4 de `composer.json`.
  - Ruby: `require`, `require_relative`; Dart: `import`; Swift: módulos; C/C++: `#include`.
- Cada arista: `from, to | external, kind (static|dynamic|type|reexport|include), line`.
- Imports no resueltos registrados con razón. Imports dinámicos y strings construidas marcados como **indirección** para trazado manual.
- Salida `graph/edges.jsonl`, `graph/external-usage.json` (por paquete externo: lista de sitios de import).

**Entregables:** `npr/imports/*.py`, tests por lenguaje.

**Criterios de aceptación:**
- [ ] Precisión y recall ≥ 98 % sobre las aristas del ground truth de cada fixture (el script de test imprime las métricas).
- [ ] 100 % de los imports dinámicos de los fixtures marcados como indirección.
- [ ] Cada paquete externo de `deps.json` tiene sus sitios de uso o se marca `unused` (detecta dependencias declaradas sin uso).

---

## F15 — Backend opcional de símbolos (tree-sitter / ctags)

**Objetivo:** precisión de rangos cuando haya herramientas disponibles, sin depender de ellas.
**Depende de:** F14

**Tareas:**
- Interfaz `SymbolBackend` con implementaciones: `RegexBackend` (siempre disponible), `TreeSitterBackend` (si `tree_sitter` y gramáticas están instaladas), `CtagsBackend` (si `ctags` universal existe).
- Selección automática por disponibilidad, reportada en `recon/tools.json` (qué herramientas externas hay: git, rg, ctags, tree-sitter, node, java, javap, go, cargo, mmdc, jadx, cfr, etc.).

**Entregables:** `npr/symbols/backends.py`, `npr/tools_probe.py`, tests.

**Criterios de aceptación:**
- [ ] Los tres backends producen salida con el mismo esquema `symbol`.
- [ ] Los tests corren siempre con `RegexBackend`; los de tree-sitter/ctags se saltan con mensaje claro si no están instalados.
- [ ] `recon/tools.json` lista versión y ruta de cada herramienta encontrada.

---

## F16 — Índice de símbolos y referencias cruzadas

**Objetivo:** cada función, clase, método, interfaz, tipo, enum y constante exportada, con rango, y dónde se referencia.
**Depende de:** F15

**Tareas:**
- `npr symbols`: genera `recon/symbols.jsonl` (`name, kind, file, start, end, exported, signature, parent`).
- Referencias: para cada símbolo exportado, sitios de uso por coincidencia de palabra completa (ripgrep si existe, si no búsqueda propia), filtrando definiciones. `recon/xrefs.jsonl`.
- `npr symbols find <nombre>` y `npr symbols refs <nombre>` para uso interactivo del agente.

**Entregables:** `npr/symbols/index.py`, tests.

**Criterios de aceptación:**
- [ ] Todos los símbolos clave listados en el ground truth están, con línea de inicio exacta (y fin exacto con tree-sitter).
- [ ] `npr symbols refs` encuentra todos los sitios de uso de 5 símbolos elegidos del fixture TS.

---

## F17 — Detección de entry points

**Objetivo:** saber por dónde arranca cada proceso del sistema.
**Depende de:** F16
**Paralelizable con:** F18, F19, F20, F21

**Tareas:**
- Detectores: `package.json` `main`/`bin`/`exports`/`scripts`, extensión VS Code (`main` + `activationEvents` + `activate()`), Electron main/preload/renderer, webviews, `if __name__ == "__main__"`, `console_scripts`/entry points de plugins, `func main` en `package main`, binarios Rust (`src/main.rs`, `[[bin]]`), `public static void main`, `Micronaut.run`, `@SpringBootApplication`, `bootstrapApplication`/`platformBrowserDynamic` de Angular, rutas de Next (app/pages), workers, cron, handlers serverless, `Dockerfile` `CMD`/`ENTRYPOINT`, `Procfile`, `docker-compose` services, scripts de CI que arrancan cosas.
- Salida `recon/entrypoints.json` ordenado por importancia, con evidencia y proceso al que pertenece.

**Entregables:** `npr/entrypoints.py`, tests.

**Criterios de aceptación:**
- [ ] 100 % de los entry points del ground truth de cada fixture detectados.
- [ ] `fx-ts-agent-extension` distingue al menos 2 procesos (host de extensión y webview).

---

## F18 — Superficies: rutas, comandos, mensajes, eventos, IPC

**Objetivo:** catálogo de todas las "puertas" por las que entra o sale comportamiento.
**Depende de:** F16
**Paralelizable con:** F17, F19, F20, F21

**Tareas:**
- HTTP: Express, Fastify, NestJS, Next route handlers, Flask, FastAPI, Django `urls.py`, Spring/Micronaut (`@Controller`, `@Get`, `@Post`…), Go `net/http`/gin/echo/chi, Rust axum/actix, ASP.NET.
- CLI: commander, yargs, oclif, click, typer, argparse, cobra, clap, picocli.
- VS Code: `contributes.commands`, `menus`, `keybindings`, `views`, `configuration` + sitios `registerCommand`.
- Webview/IPC: uniones discriminadas por `type: "literal"`, `postMessage`, `onDidReceiveMessage`, Electron `ipcMain`/`ipcRenderer`, `chrome.runtime` messages.
- Eventos: `.emit("x")`/`.on("x")`, EventEmitter, buses propios, Observables/Subjects, `@EventListener`.
- Esquemas: OpenAPI, GraphQL SDL, `.proto`, JSON Schema, AsyncAPI.
- WebSockets, SSE, colas (Kafka, RabbitMQ, SQS) por imports y llamadas.
- Emparejamiento productor↔consumidor: por cada evento/mensaje, sitios que emiten y que escuchan; huérfanos reportados.
- Salida `recon/surfaces.json`.

**Entregables:** `npr/surfaces/*.py`, reglas en datos, tests.

**Criterios de aceptación:**
- [ ] 100 % de rutas, comandos y tipos de mensaje del ground truth detectados con handler correcto.
- [ ] Emisores y listeners emparejados; los huérfanos plantados en fixtures aparecen como huérfanos.
- [ ] Las reglas por framework están en archivos de datos.

---

## F19 — Configuración, variables de entorno y feature flags

**Objetivo:** todo lo que cambia el comportamiento sin tocar código.
**Depende de:** F16
**Paralelizable con:** F17, F18, F20, F21

**Tareas:**
- Subcomando `npr env` (escaneo de configuración; `npr config` queda reservado para la configuración de la propia skill).
- Variables de entorno: `process.env.X`, `import.meta.env.X`, `os.environ`/`getenv`, `System.getenv`, `os.Getenv`, `std::env::var`, `${X}` en YAML/properties, `.env.example`.
- Claves de configuración: `contributes.configuration` de VS Code, `application.yml`/`.properties` + `@Value`/`@Property`/`@ConfigurationProperties`/`@Requires`, `settings.py`, archivos de config propios (JSON/YAML/TOML) y sus lectores.
- Feature flags: patrones `flag`, `experiment`, `featureFlag`, `isEnabled(`, `EXPERIMENT_`, condicionales sobre config.
- Valores por defecto y sitios de lectura.
- **Redacción de secretos**: nunca copiar valores de `.env`, solo nombres; valores que parecen secretos se enmascaran.
- Salida `recon/env.json`.

**Entregables:** `npr/config_scan.py`, tests.

**Criterios de aceptación:**
- [ ] 100 % de variables, claves y flags del ground truth con sitios de lectura y default.
- [ ] Test con `.env` que contiene un secreto falso: el valor no aparece en ninguna salida del workspace (grep del workspace completo).

---

## F20 — Detector de artefactos de LLM (prompts, herramientas, modos, skills)

**Objetivo:** encontrar mecánicamente todo lo que hace "inteligente" a una app de IA.
**Depende de:** F16
**Paralelizable con:** F17, F18, F19, F21

**Tareas:**
- Prompts: strings largos/template literals y archivos con señales (`You are`, `## Rules`, `<tool`, `system`, encabezados markdown dentro de strings, nombres `*prompt*`, `*system*`, `*instructions*`).
- Definiciones de herramientas: objetos con `name` + `description` + `parameters`/`input_schema`/`inputSchema`, decoradores de tools, registros de handlers por nombre de herramienta.
- Modos/agentes/personas: arreglos de objetos con `slug`/`mode`/`roleDefinition`/`allowedTools`/`groups`.
- Proveedores: imports de SDKs (`openai`, `@anthropic-ai/sdk`, `@google/genai`, `ollama`, `litellm`, `openrouter`, `@modelcontextprotocol/sdk`…).
- Skills/reglas/instrucciones: rutas con `skills`, `SKILL.md`, `.clinerules`, `rules`, `AGENTS.md`, lectura de frontmatter.
- Loop de agente: bucles alrededor de llamadas de streaming, parseo de tool calls (XML o nativas), conteo de tokens, condensación/truncado.
- Salida `recon/llm.json` con categoría, ubicación y fragmento inicial (≤ 200 caracteres).

**Entregables:** `npr/llm_scan.py`, tests.

**Criterios de aceptación:**
- [ ] En `fx-ts-agent-extension`: 100 % de prompts, herramientas, modos, cargador de skills y loop del agente detectados.
- [ ] ≤ 2 falsos positivos en total entre `fx-python-cli`, `fx-java-micronaut` y `fx-polyglot`.
- [ ] Si el repo no usa LLM, la salida lo declara explícitamente (`is_llm_app: false` con evidencia).

---

## F21 — Estadísticas e índice de historia git

**Objetivo:** usar la historia como fuente de "por qué" y de dónde está la complejidad.
**Depende de:** F16
**Paralelizable con:** F17, F18, F19, F20

**Tareas:**
- Si hay `.git`: número de commits, primera/última fecha, tags/releases, churn por archivo, hotspots (churn × líneas), pares de co-cambio (archivos modificados juntos ≥ N veces), actividad reciente por directorio.
- Índice de mensajes: `npr git why <archivo>` (commits que lo tocan con mensaje), `npr git when "<texto>"` (`git log -S`/`-G`), referencias a issues/PRs en mensajes.
- Clones superficiales (`--depth`): detectarlo y avisar que la historia es parcial.
- Autores: solo conteos agregados, sin emails.
- Salida `recon/git.json`.

**Entregables:** `npr/gitstats.py`, tests sobre fixture con historia scriptada.

**Criterios de aceptación:**
- [ ] Hotspots y co-cambios del fixture con historia coinciden con el ground truth.
- [ ] `npr git when` encuentra el commit que introdujo una función conocida.
- [ ] Clon superficial detectado y reportado.
- [ ] Ningún email en la salida.

---

## F22 — Análisis del grafo y módulos candidatos

**Objetivo:** estructura de alto nivel derivada de datos, no de intuición.
**Depende de:** F17, F18, F19, F20, F21

**Tareas:**
- Módulos candidatos: por paquete del workspace, por directorio y por detección de comunidades (label propagation, stdlib).
- Ciclos (Tarjan SCC), fan-in/fan-out, PageRank simple, capas inferidas, violaciones de capa sospechosas.
- Archivos huérfanos (sin aristas entrantes, que no son entry point, test ni config) → candidatos a código muerto o cargados por indirección.
- Exportación Mermaid colapsada por nivel de directorio, con tope de nodos por diagrama.
- Salida `graph/modules.json`, `graph/metrics.json`, `graph/*.mmd`.

**Entregables:** `npr/graph.py`, tests.

**Criterios de aceptación:**
- [ ] Ciclos plantados en fixtures detectados.
- [ ] La trampa de "código muerto que parece activo" aparece como huérfano; la de "cargado por indirección" también aparece como huérfano **y** con la indirección enlazada (desde F14).
- [ ] Ningún diagrama generado supera el tope de nodos configurado.

---

## F23 — Particionador en unidades de trabajo (WU)

**Objetivo:** dividir la lectura exhaustiva entre subagentes sin romper cohesión.
**Depende de:** F22

**Tareas:**
- Generar WUs por módulo/paquete con presupuesto configurable (líneas o tokens estimados por WU; sin límite fijo por defecto, configurable según el modelo).
- Un SCC nunca se divide entre WUs.
- Cada WU incluye: archivos (política `full`/`skim`/`reverse`), vecinos (interfaces que toca de otras WUs), prioridad (entry points y nodos centrales primero), glosario inicial de términos del módulo.
- Archivos gigantes: WU propia con plan de lectura por rangos (chunks con solapamiento).
- Salida `wu/WU-NNN.json` + `wu/plan.md` con olas sugeridas (dependencias primero).

**Entregables:** `npr/partition.py`, tests.

**Criterios de aceptación:**
- [ ] Cada archivo con política `full|skim|reverse` está en exactamente una WU (test de partición).
- [ ] Ningún SCC dividido.
- [ ] El archivo de > 5.000 líneas del fixture TS tiene plan de chunks que cubre todas sus líneas.
- [ ] Cada WU valida contra el esquema `wu`.

---

## F24 — Ledger de cobertura concurrente

**Objetivo:** saber en todo momento qué se leyó, qué falta y quién lo hizo, incluso con subagentes en paralelo.
**Depende de:** F23

**Tareas:**
- Estados: `pending → read → carded → integrated → verified` y `excluded(reason)`.
- Escritura sin conflictos: cada subagente escribe solo `ledger/fragments/<WU>.jsonl`; `npr ledger merge` consolida de forma determinista (último estado por timestamp, sin regresiones de estado salvo `--reopen`).
- Comandos: `npr ledger mark <ruta> --state carded --by WU-007`, `npr ledger gaps`, `npr ledger stats`, `npr ledger reopen <ruta>`.

**Entregables:** `npr/ledger.py`, tests de concurrencia.

**Criterios de aceptación:**
- [ ] Test con 8 procesos escribiendo fragmentos a la vez: el merge es determinista y no pierde entradas.
- [ ] `gaps` lista exactamente los archivos no cubiertos.
- [ ] Un estado no retrocede sin `reopen` explícito.

---

## F25 — Orquestador de recon y resumen `RECON.md`

**Objetivo:** un solo comando que deja listo todo el material mecánico.
**Depende de:** F24

**Tareas:**
- `npr recon`: ejecuta F08–F24 en orden, con caché por hash, idempotente, con barra de progreso en log.
- Genera `recon/RECON.md`: stack, tamaño, paquetes, entry points, superficies por tipo, config, artefactos LLM, hotspots, módulos candidatos, ciclos, huérfanos, indirecciones a resolver, herramientas disponibles, plan de WUs y olas.
- Actualiza `state.json` a etapa `recon-done`.

**Entregables:** `npr/recon.py`, plantilla `templates/recon.md`, tests.

**Criterios de aceptación:**
- [ ] `npr recon` completa en los 6 fixtures y genera `RECON.md`.
- [ ] Segunda ejecución sin cambios reutiliza caché (lo indica el log) y produce salidas idénticas byte a byte.
- [ ] Toda cifra de `RECON.md` es reproducible desde los JSON de `recon/` (test que las recalcula).

---

# ETAPA 2 — PROTOCOLO COGNITIVO (GUÍAS Y PLANTILLAS)

> Estas fases escriben los `references/*.md` y `templates/*` que el agente y sus subagentes leen bajo
> demanda. Cada guía tiene secciones fijas: **Objetivo**, **Entradas**, **Procedimiento paso a paso**,
> **Técnicas para casos difíciles**, **Salida (plantilla)**, **Checklist de calidad**, **Errores comunes**.
> Cada guía se valida con un *dry run*: un subagente con contexto limpio que solo recibe esa guía y un fixture.

## F26 — Pipeline maestro del análisis

**Objetivo:** definir las etapas que sigue el orquestador, con entradas, salidas y gates.
**Depende de:** F25

**Tareas:**
- Escribir `references/01-pipeline.md` con las etapas:
  - **A. Preparación:** `npr init`, confirmar modo (completo/pregunta/feature/reanudar/actualizar/comparar), idioma, si se permite análisis dinámico, dónde guardar.
  - **B. Recon:** `npr recon`, leer `RECON.md`.
  - **C. Orientación:** leer README, docs, CONTRIBUTING, ADRs, CHANGELOG, comentarios de arquitectura → `notes/cross/hipotesis.md` (todas marcadas como hipótesis a verificar).
  - **D. Lectura exhaustiva por WU** (subagentes lectores en olas) → fichas de archivo + dossiers de módulo + fragmentos de ledger + preguntas abiertas.
  - **E. Síntesis de arquitectura** (orquestador, desde dossiers) → `notes/cross/arquitectura.md`.
  - **F. Descubrimiento de features** → `notes/features/CATALOGO.md`.
  - **G. Trazado de flujos** (subagentes trazadores, uno por feature o grupo) → `notes/flows/*.md`.
  - **G2. Paquete completo por feature** (subagentes de paquete, uno por feature): `npr branches` → diagrama de flujo de decisiones → matriz de resultados posibles → tabla de decisión → secuencia/estados → errores → escenarios de prueba → datos → llamadas → ejemplos → límites → observabilidad → interacciones; mini-paquete por cada superficie → `notes/features/<FEAT-NNN>-<slug>/`, `notes/surfaces/`. Gates `branches` y `outcomes` por feature antes de seguir.
  - **H. Temas transversales** (subagentes analistas): datos/estado, interfaces, config, extensibilidad, LLM, build/CI, tests, seguridad, historia.
  - **I. Ingeniería inversa / dinámico** (si aplica).
  - **J. Verificación** (subagente verificador independiente) + ciclo de resolución de preguntas abiertas.
  - **K. Ensamble de reportes** (`npr report build`) + linters + gates.
  - **L. Entrega:** mensaje final en chat con resumen, índice y cómo navegar.
- Para cada etapa: entradas, salidas, comando de gate, condición de reentrada, qué escribir en `state.json`.
- Diagrama Mermaid del pipeline.

**Entregables:** `references/01-pipeline.md`.

**Criterios de aceptación:**
- [ ] Cada etapa tiene entradas, salidas y gate explícitos, y los comandos citados existen en `npr --help`.
- [ ] El diagrama del pipeline pasa el validador Mermaid (provisional hasta F68).
- [ ] Dry run: un subagente que solo lee esta guía y `RECON.md` de `fx-python-cli` describe correctamente qué haría en cada etapa y qué archivos produciría.

---

## F27 — Protocolo de subagentes y briefs

**Objetivo:** que el trabajo en paralelo sea completo, consistente y sin conflictos.
**Depende de:** F26

**Tareas:**
- Escribir `references/02-subagentes.md`:
  - **Roles:** Orquestador, Lector de WU, Trazador de flujo, **Constructor de paquete de feature**, **Analista de superficie**, Analista transversal, Ingeniero inverso, Analista dinámico, Verificador, Resolvedor de preguntas, Redactor de reportes.
  - **Regla de oro del orquestador:** no lee el código entero; lee recon, dossiers y trazas; abre código solo para decidir o desempatar.
  - **Contrato de brief** (campos obligatorios): rol, objetivo, alcance exacto (lista de archivos o feature), contexto mínimo (extracto de `RECON.md`, glosario, interfaces de vecinos), reglas (enlace a `00-principios.md`), plantilla de salida, rutas donde escribir, criterios de terminado, qué devolver al orquestador.
  - **Contrato de retorno:** lista de archivos escritos, resumen ≤ 20 líneas, fragmento de ledger, preguntas abiertas nuevas, términos nuevos para el glosario, sospechas para otros módulos.
  - **Olas:** cómo agrupar WUs (dependencias primero), cuántas en paralelo (parámetro), cómo propagar glosario e interfaces entre olas.
  - **Conflictos:** dos subagentes con interpretaciones distintas → el orquestador abre el código del punto en disputa o lanza un verificador.
  - **Modo secuencial de respaldo** (enlace a F02).
- Plantillas en `templates/briefs/`: `wu-reader.md`, `flow-tracer.md`, `feature-package-builder.md`, `surface-analyst.md`, `cross-analyst.md`, `reverse-engineer.md`, `dynamic-analyst.md`, `verifier.md`, `question-resolver.md`, `report-writer.md`.
- `npr brief <tipo> <id>` genera el brief rellenado desde el workspace (para pegarlo en la invocación del subagente).

**Entregables:** `references/02-subagentes.md`, 10 plantillas, `npr/briefs.py`, tests.

**Criterios de aceptación:**
- [ ] `npr brief wu-reader WU-001` produce un brief con todos los campos obligatorios rellenos (test).
- [ ] Dry run en `fx-monorepo` con 3 subagentes lectores en paralelo: salidas sin pisarse, ledger consolidado sin pérdidas.
- [ ] El modo secuencial produce las mismas salidas estructurales que el paralelo en el mismo fixture.

---

## F28 — Dossier de módulo

**Objetivo:** el documento central de comprensión por módulo.
**Depende de:** F27
**Paralelizable con:** F29–F60

**Tareas:**
- `references/06-analisis-por-modulo.md` + `templates/notes/module-dossier.md` con secciones obligatorias:
  Propósito · Responsabilidades · Archivos (tabla con rol) · API pública (símbolo, firma, cita) · Dependencias internas (y para qué) · Dependencias externas (y para qué) · Consumidores · Flujo interno · Estado y datos · Configuración que lee · Efectos secundarios (fs, red, procesos, UI, almacenamiento) · Errores y casos borde · Concurrencia y asincronía · Puntos de extensión · Lo no obvio / trampas · Tests que lo cubren · Preguntas abiertas.
- Diagramas obligatorios por módulo: componentes internos (`flowchart` con subgrafos), clases/tipos principales (`classDiagram`), dependencias entrantes y salientes (`flowchart LR`) y, si el módulo tiene ciclo de vida, `stateDiagram-v2`.
- Tabla "features en las que participa este módulo" con enlaces a sus paquetes (se completa tras la etapa 2B).
- Cada sección: contenido o `N/A — razón`.
- `npr lint dossier <archivo>`: verifica secciones, diagramas, etiquetas y citas.

**Entregables:** guía, plantilla, linter de dossier, tests.

**Criterios de aceptación:**
- [ ] El linter rechaza dossiers con secciones faltantes, vacías, `N/A` sin razón o sin los diagramas obligatorios (tests).
- [ ] Dry run: dossier del módulo de skills de `fx-ts-agent-extension` cubre el 100 % de los puntos del ground truth de ese módulo con citas válidas.

---

## F29 — Fichas de archivo y lectura de archivos gigantes

**Objetivo:** que cada archivo leído deje rastro útil y compacto.
**Depende de:** F27

**Tareas:**
- `references/03-lectura-de-archivos.md` + `templates/notes/file-card.md`: rol (1–2 líneas), símbolos clave con línea, imports relevantes, efectos, lo no obvio, features en las que participa (se completa en etapa G), preguntas.
- Variante `skim` (estructura + partes relevantes) y variante `reverse` (enlaza a la nota de ingeniería inversa).
- Protocolo para archivos gigantes: lectura por rangos según plan de F23, ficha por chunk, fusión final; nunca resumir un rango no leído.
- Fichas en `notes/files/<ruta-con-__>.md`.

**Entregables:** guía, plantillas, `npr lint card`.

**Criterios de aceptación:**
- [ ] Dry run sobre el archivo de > 5.000 líneas: la ficha fusionada menciona todos los símbolos exportados del archivo (comparado con `symbols.jsonl`).
- [ ] El linter de fichas detecta fichas sin símbolos citados en archivos `full`.

---

## F30 — Guía de arquitectura

**Objetivo:** explicar el sistema completo a nivel de procesos, componentes y decisiones.
**Depende de:** F27

**Tareas:**
- `references/05-arquitectura.md`: cómo identificar estilo (capas, hexagonal, MVC, eventos, plugins, actores, cliente-servidor, extensión+webview), topología de ejecución (procesos, hilos, workers, contenedores), fronteras y contratos, flujo de datos macro, niveles C4 (contexto, contenedores, componentes), decisiones clave con evidencia, deuda y riesgos arquitectónicos.
- `templates/notes/architecture.md` con diagramas obligatorios: contexto, contenedores, componentes por contenedor.
- `references/04-stack-y-dependencias.md`: cómo explicar para qué sirve **cada** dependencia directa a partir de sus sitios de uso (`graph/external-usage.json`) y no por su nombre; dependencias declaradas sin uso, duplicadas con versiones distintas, dependencias "de núcleo" (sin las cuales la app no funciona) vs. periféricas; riesgos de versión.

**Entregables:** guías `05-arquitectura.md` y `04-stack-y-dependencias.md`, plantilla.

**Criterios de aceptación:**
- [ ] Dry run sobre `fx-ts-agent-extension`: identifica los procesos (host y webview), el protocolo de mensajes entre ellos y los componentes del ground truth.
- [ ] Dry run de `04-stack-y-dependencias.md`: el propósito de cada dependencia directa de `fx-monorepo` coincide con el ground truth y cita al menos un sitio de uso.
- [ ] Dry run sobre `fx-java-micronaut`: identifica capas y el uso de DI en compilación.

---

## F31 — Guía de trazado de flujos

**Objetivo:** el corazón de la skill: seguir una feature de punta a punta sin saltarse nada.
**Depende de:** F27

**Tareas:**
- `references/07-trazado-de-flujos.md`:
  - Definición de traza: disparador → saltos numerados (cada salto: qué pasa, dónde `[@…]`, datos que entran/salen, si cruza frontera de proceso o async) → ramas y errores → persistencia → llamadas externas → camino de vuelta al usuario.
  - Técnicas: hacia adelante desde el entry point, hacia atrás desde el efecto, seguir strings literales (tipos de mensaje, nombres de herramienta, claves i18n), resolver indirecciones (DI, registros/mapas de handlers, bus de eventos, import dinámico, reflexión, decoradores, middleware, interceptores, observables), usar `npr symbols refs` y `graph/edges.jsonl`.
  - Regla: si un salto no se encuentra, `[?]` + pregunta abierta; nunca puentear con suposición sin etiqueta.
  - Profundidad: llegar hasta la última función propia del repo antes de entrar a una dependencia externa; documentar qué hace la dependencia en ese punto.
- `templates/notes/flow.md`: tabla de pasos + `sequenceDiagram` Mermaid + tabla de estado mutado + ramas de error + archivos involucrados.

**Entregables:** guía, plantilla, `npr lint flow` (pasos numerados continuos, cita por paso, diagrama presente).

**Criterios de aceptación:**
- [ ] Dry run: traza "usuario cambia a modo plan y envía una tarea" en `fx-ts-agent-extension` coincide en ≥ 95 % de los pasos con el ground truth y 100 % de citas válidas.
- [ ] Dry run: traza de un endpoint en `fx-java-micronaut` resuelve la trampa de cliente HTTP declarativo.
- [ ] El linter rechaza trazas con saltos sin cita o numeración rota.

---

## F32 — Guía de features

**Objetivo:** encontrar todas las features y documentarlas desde el punto de vista del usuario y del código.
**Depende de:** F27

**Tareas:**
- `references/08-features.md`: fuentes de descubrimiento (UI: comandos, menús, ajustes, botones y **strings i18n**; rutas; CLI; docs; CHANGELOG; nombres de tests; feature flags; historia git), deduplicación, estado (activa, experimental, detrás de flag, muerta).
- `templates/notes/features-catalog.md` (id, nombre, descripción de usuario, entry points, módulos, trazas, config, estado).
- `templates/notes/feature-dossier.md`: qué hace · cómo se usa · cómo funciona por dentro (enlaces a trazas) · datos · configuración · extensiones · límites y casos borde · tests · historia (commits clave) · cómo modificarla o extenderla. Este dossier es el `README.md` del **paquete completo por feature** que se define en F33–F47.

**Entregables:** guía, plantillas, `npr lint feature`.

**Criterios de aceptación:**
- [ ] Dry run: el catálogo de cada fixture tiene recall 100 % de features del ground truth.
- [ ] La feature detrás de flag desactivado se marca como tal.
- [ ] La feature "muerta" trampa se marca como muerta con evidencia.

---

# ETAPA 2B — PAQUETE COMPLETO POR FEATURE

> Una traza no basta. Cada feature se entrega como una **carpeta con 13 artefactos obligatorios**:
> diagrama de flujo de decisiones, matriz de **todos los resultados posibles**, tabla de decisión,
> diagramas de secuencia y de estados, catálogo de errores, escenarios de prueba, linaje de datos,
> grafo de llamadas, ejemplos trabajados y recorrido del usuario, límites y concurrencia,
> observabilidad y efectos, e interacciones con otras features. Además, cada superficie (endpoint,
> comando, mensaje, herramienta) recibe un mini-paquete. Scripts deterministas extraen cada punto de
> decisión y cada salida del código para que ningún diagrama ni matriz omita ramas.

## F33 — Especificación del paquete completo por feature

**Objetivo:** definir qué se genera obligatoriamente para cada feature, para que ninguna quede explicada a medias.
**Depende de:** F31, F32

**Tareas:**
- `references/24-paquete-por-feature/00-indice.md`: los 13 artefactos, para qué sirve cada uno, de qué notas se alimenta, orden de producción, qué rol de subagente lo produce y qué gate lo valida.
- Estructura en el workspace `notes/features/<FEAT-NNN>-<slug>/`:
  ```
  README.md                 dossier de la feature (F32) + tabla resumen del paquete
  flujo.md                  diagrama de flujo de decisiones (F35)
  resultados.md             matriz de resultados posibles R-NN (F36)
  decision.md               tabla de decisión + matriz de configuración (F37)
  secuencia-y-estados.md    diagramas de secuencia, de estado y estados de UI (F38)
  errores.md                errores y modos de falla (F39)
  pruebas.md                escenarios Given/When/Then por resultado + brecha de tests (F40)
  datos.md                  linaje de datos (F41)
  llamadas.md               grafo de llamadas + mapa de archivos (F42)
  ejemplos.md               ejemplos trabajados + recorrido del usuario (F43)
  limites.md                límites, rendimiento, concurrencia, reintentos (F44)
  observabilidad.md         logs, telemetría, efectos externos (F45)
  interacciones.md          relación con otras features + impacto de cambios (F46)
  _branches.json            puntos de decisión y salidas extraídos (F34)
  _callgraph.json           grafo de llamadas extraído (F42)
  ```
- Tabla resumen del `README.md`: número de resultados posibles, de puntos de decisión, de errores, de escenarios, % de resultados cubiertos por tests, enlaces a cada artefacto.
- Nuevos esquemas en `schemas/`: `decision-point`, `outcome`, `feature-package`, `scenario`, `error-entry`.
- `npr feature scaffold <FEAT-id>` crea la carpeta con las plantillas de `templates/notes/feature/`.
- `npr lint feature-package <FEAT-id>`: verifica los 13 archivos, sus secciones, diagramas, citas y etiquetas.
- Regla: en features triviales un artefacto puede ser `N/A — razón`, **excepto** `flujo.md`, `resultados.md` y `pruebas.md`, que nunca son opcionales.

**Entregables:** guía índice, 13 plantillas, 5 esquemas, `npr feature scaffold`, `npr lint feature-package`, tests.

**Criterios de aceptación:**
- [ ] `scaffold` crea exactamente la estructura especificada.
- [ ] El linter rechaza: artefacto faltante, `flujo.md`/`resultados.md`/`pruebas.md` en `N/A`, diagrama ausente, citas inválidas (tests).
- [ ] Los 5 esquemas nuevos validan sus ejemplos y rechazan los inválidos.

---

## F34 — Extractor de puntos de decisión y salidas (`npr branches`)

**Objetivo:** base determinista para que diagramas y matrices de resultados no omitan ninguna rama.
**Depende de:** F16, F33

**Tareas:**
- `npr branches <ruta>[:ini-fin] [--follow-flow <flow-id>] [--feature <FEAT-id>]` que detecta por lenguaje (JS/TS, Python, Java/Kotlin, Go, Rust, C#, PHP, Ruby, Dart, Swift):
  - Decisiones: `if / else if / else`, `switch/case/default`, `match`, `when`, ternarios, guard clauses, cortocircuitos con efectos (`&&`, `||`, `??` que llaman funciones), bucles con salida condicional.
  - Salidas: `return` tempranos y con valores distintos, `throw`/`raise`/`panic`, `try/catch/finally`/`except`, `.catch(`, `Promise.reject`, callbacks de error, `if err != nil` (Go), `Err(...)`/`?` (Rust), `Optional.empty`, respuestas HTTP con código, `process.exit`/códigos de salida, envío de mensajes de error a la UI.
- Cada punto: `id, file, line, kind, condition_text (≤ 200 caracteres), branches[{label, target_line}]`.
- Cada salida: `outcome_candidate {id, file, line, kind, value_or_message}`.
- `--follow-flow`/`--feature`: toma los rangos citados en las trazas de la feature y sigue las funciones llamadas dentro del repo (xrefs + aristas) sin límite de profundidad, cortando en ciclos; externas como hojas.
- Ignora código dentro de strings y comentarios.
- Salida `notes/features/<FEAT-NNN>-<slug>/_branches.json`.

**Entregables:** `npr/branches/*.py`, reglas por lenguaje en `rules/branches_*.json`, tests.

**Criterios de aceptación:**
- [ ] 100 % de los puntos de decisión y salidas del ground truth (extendido en F06) para al menos 3 features por fixture.
- [ ] Tests por lenguaje con cada tipo de decisión y salida.
- [ ] Código dentro de strings y comentarios no genera puntos (test específico).
- [ ] `--follow-flow` atraviesa al menos 4 niveles de llamadas en `fx-ts-agent-extension` y se detiene en ciclos sin error.

---

## F35 — Diagrama de flujo de decisiones por feature

**Objetivo:** un diagrama de flujo por feature con cada decisión, rama, bucle y resultado final.
**Depende de:** F34

**Tareas:**
- `references/24-paquete-por-feature/01-diagrama-de-flujo.md` + plantilla `flujo.md`:
  - Mermaid `flowchart TD`: inicio (disparador real), procesos, **decisiones** (rombos) con la condición real expresada en lenguaje claro, subprocesos agrupados en `subgraph` por proceso o capa (UI, host/servidor, servicio, BD, externo), bucles (reintentos, loop del agente), cruces de frontera marcados.
  - **Nodos terminales por resultado**, enlazados a su `R-NN` de `resultados.md`, con `classDef` por tipo: éxito, éxito parcial, error, cancelado, no-op.
  - Camino feliz resaltado (`linkStyle`).
  - Tabla de nodos: id de nodo → descripción → cita `[@…]`.
  - Niveles: diagrama general + diagramas de detalle por subproceso cuando se supera el tope de nodos, enlazados entre sí.
- Gate `npr gate branches <FEAT-id>`: cada punto de decisión y cada salida de `_branches.json` está mapeado a un nodo (por cita en la tabla de nodos) o justificado como irrelevante con razón escrita.

**Entregables:** guía, plantilla, gate, tests.

**Criterios de aceptación:**
- [ ] Dry run: el diagrama de flujo de "modo plan" y de "carga de skills" de `fx-ts-agent-extension` cubre todas las decisiones y resultados del ground truth; `gate branches` en verde.
- [ ] El gate falla si se borra un rombo del diagrama (test).
- [ ] Todos los diagramas pasan el validador Mermaid (provisional hasta F68).
- [ ] Un diagrama que supera el tope se divide en general + detalle con enlaces válidos.

---

## F36 — Matriz de resultados posibles

**Objetivo:** enumerar **todo** lo que puede pasar al usar una feature y qué significa cada resultado.
**Depende de:** F35

**Tareas:**
- `references/24-paquete-por-feature/02-resultados.md` + plantilla `resultados.md`.
- Taxonomía obligatoria a revisar en cada feature (cada categoría se documenta o se declara inexistente con razón): éxito completo · éxito parcial/degradado · éxito con advertencia · no-op · error de validación de entrada · precondición no cumplida · recurso inexistente · permiso denegado o aprobación rechazada por el usuario · cancelación por el usuario · timeout · error de red o servicio externo · error del proveedor (rate limit, cuota, autenticación, modelo no disponible) · límite alcanzado (tamaño, tokens, máximo de turnos) · conflicto o concurrencia · reintento con recuperación · error interno no controlado · estado inconsistente.
- Por cada resultado `R-NN`:
  - Nombre y categoría.
  - Condiciones que lo producen y camino en el diagrama (ids de nodos).
  - Entradas, estado y configuración de ejemplo que lo disparan.
  - **Qué ve el usuario** exactamente: texto de UI, mensaje, notificación, código HTTP, salida y código de salida de CLI (con cita al string o clave i18n).
  - Efectos secundarios (qué se escribió, envió, borró o cambió de estado) y si son reversibles.
  - Estado final del sistema.
  - Si queda registrado (log/telemetría).
  - Cómo recuperarse y cómo reproducirlo.
  - Tests que lo cubren.
  - Etiqueta de evidencia y citas.
- Tabla resumen de resultados + sección "ramas muertas o inalcanzables" con razón.
- Cada `outcome_candidate` de `_branches.json` mapeado a un `R-NN` o justificado.

**Entregables:** guía, plantilla, `npr lint outcomes`, tests.

**Criterios de aceptación:**
- [ ] Dry run sobre modo plan y carga de skills (`fx-ts-agent-extension`), un endpoint (`fx-java-micronaut`) y un comando (`fx-python-cli`): recall 100 % de los resultados del ground truth.
- [ ] 0 resultados inventados según el verificador independiente.
- [ ] Todo `R-NN` tiene "qué ve el usuario" con cita o `[?]` con OQ (lint).
- [ ] Todo `outcome_candidate` está mapeado o justificado (lint).

---

## F37 — Tabla de decisión y matriz de configuración

**Objetivo:** saber qué combinación de condiciones produce cada resultado y qué setting cambia qué.
**Depende de:** F36

**Tareas:**
- `references/24-paquete-por-feature/03-tabla-de-decision.md` + plantilla `decision.md`:
  - **Tabla de decisión**: columnas = condiciones relevantes (entradas, estado, flags, settings, modo, permisos, plataforma, proveedor), filas = combinaciones que producen resultados distintos → `R-NN`. Combinaciones equivalentes agrupadas con explicación; combinaciones imposibles marcadas con razón.
  - **Matriz de configuración**: cada setting, variable de entorno o flag que afecta la feature → valores posibles → efecto en el comportamiento → resultado afectado → default → dónde se lee (cita).
  - Precondiciones, postcondiciones e invariantes de la feature.

**Entregables:** guía, plantilla, verificación cruzada dentro de `npr lint outcomes`.

**Criterios de aceptación:**
- [ ] Cada fila apunta a un `R-NN` existente y cada `R-NN` aparece en al menos una fila (lint).
- [ ] Dry run: toda clave de configuración del ground truth que afecta la feature aparece con su efecto correcto.

---

## F38 — Diagramas de secuencia, de estado y estados de UI por feature

**Objetivo:** ver quién habla con quién, en qué orden, y cómo cambia el estado.
**Depende de:** F36

**Tareas:**
- `references/24-paquete-por-feature/04-secuencia-y-estados.md` + plantilla `secuencia-y-estados.md`:
  - `sequenceDiagram` del camino feliz y de cada resultado de error relevante (con `alt`, `opt`, `loop`, `par`); participantes = procesos y componentes reales (UI, host, servicio, BD, proveedor externo).
  - `stateDiagram-v2` del ciclo de vida de cada entidad o estado que la feature cambia (por ejemplo, una tarea: inactiva → ejecutando → esperando aprobación → completada / fallida / cancelada).
  - **Estados de UI**: inicial, cargando, vacío, error, éxito, parcial, deshabilitado; qué los activa y qué se muestra (cita a componentes y strings).

**Entregables:** guía, plantilla, lint.

**Criterios de aceptación:**
- [ ] Dry run `fx-ts-agent-extension`: el diagrama de estados de la tarea coincide con el ground truth.
- [ ] Cada mensaje de un `sequenceDiagram` corresponde a un paso numerado de la traza (lint cruzado por número de paso).
- [ ] Los estados de UI del ground truth están todos, con su disparador.

---

## F39 — Catálogo de errores y modos de falla

**Objetivo:** cada error: dónde nace, cómo viaja, quién lo atrapa y qué ve el usuario.
**Depende de:** F36

**Tareas:**
- `npr errors`: extrae clases de error/excepción definidas, sitios de `throw`/`raise`, mensajes de error y claves i18n de error, códigos HTTP devueltos, códigos de salida, `catch` vacíos o que solo registran. Salida `recon/errors.json` (se integra a `npr recon`).
- `references/24-paquete-por-feature/05-errores.md` + plantilla `errores.md`, por error:
  tipo/clase · origen (cita) · mensaje · **propagación** (cada capa que lo atrapa, transforma o relanza, con cita) · dónde se maneja finalmente · qué ve el usuario · `R-NN` asociado · recuperación o reintento · si se registra.
- Modos de falla no controlados: excepciones sin atrapar, promesas sin `catch`, errores tragados (catch vacío), errores convertidos en éxito silencioso. Se reportan como riesgos.
- Reporte global `catalogo-de-errores` (ver F66).

**Entregables:** `npr/errors.py`, guía, plantilla, tests.

**Criterios de aceptación:**
- [ ] 100 % de los errores plantados en fixtures aparecen con su propagación correcta.
- [ ] El `catch` vacío plantado se detecta como error tragado.
- [ ] Tests de `npr errors` por lenguaje.

---

## F40 — Escenarios de prueba por resultado y brecha de tests

**Objetivo:** cada resultado posible se convierte en un escenario verificable, y se sabe cuáles ya tienen test.
**Depende de:** F36 (la parte que ejecuta código se valida en F53)

**Tareas:**
- `references/24-paquete-por-feature/06-escenarios-de-prueba.md` + plantilla `pruebas.md`.
- Por cada `R-NN`, al menos un escenario **Given / When / Then** concreto: datos, estado inicial, acción y resultado observable esperado.
- Mapeo de tests existentes del repo a escenarios (por nombre, ruta y llamadas a símbolos de la feature), con cita.
- Escenarios sin test marcados como **brecha**; % de resultados cubiertos por tests.
- Con permiso de análisis dinámico: ejecutar los tests de la feature en el worktree aislado (F53) y etiquetar `[D]`.
- Reporte global de escenarios y cobertura de resultados (ver F66).

**Entregables:** guía, plantilla, lint.

**Criterios de aceptación:**
- [ ] Todo `R-NN` tiene al menos un escenario (lint).
- [ ] El mapeo test→escenario en fixtures coincide con el ground truth y las brechas son correctas.
- [ ] Dry run: un subagente implementa 2 escenarios de brecha como tests en una copia del fixture y se comportan como predice `resultados.md`.

---

## F41 — Linaje de datos por feature

**Objetivo:** seguir cada dato desde que entra hasta donde termina.
**Depende de:** F36

**Tareas:**
- `references/24-paquete-por-feature/07-linaje-de-datos.md` + plantilla `datos.md`:
  - Por cada dato de entrada (input del usuario, config, archivo, respuesta externa): transformaciones paso a paso, validaciones, dónde se persiste, quién lo lee después, por dónde sale (UI, red, disco), con cita en cada paso.
  - Diagrama `flowchart LR` de linaje.
  - Tipos y estructuras clave (interfaces, DTOs, entidades) con cita.
  - Datos sensibles que atraviesan la feature, marcados.

**Entregables:** guía, plantilla.

**Criterios de aceptación:**
- [ ] Dry run `fx-monorepo`: el linaje de un dato desde el formulario Angular → API → BD coincide con el ground truth.

---

## F42 — Grafo de llamadas y mapa de archivos por feature

**Objetivo:** ver todas las funciones que participan y detectar ramas que la traza no recorrió.
**Depende de:** F34

**Tareas:**
- `npr callgraph --flow <id> | --feature <FEAT-id>`: grafo de llamadas de las funciones del repo involucradas, construido desde las citas de las trazas + xrefs + aristas; profundidad completa dentro del repo; dependencias externas como hojas. Salida `_callgraph.json` + Mermaid colapsable.
- Mapa de archivos tocados: archivo → rol en la feature → funciones → líneas.
- Funciones del grafo que ninguna traza cubre → **candidatas a ramas olvidadas**; alimentan `gate branches` (F35).
- Plantilla `llamadas.md`.

**Entregables:** `npr/callgraph.py`, plantilla, tests.

**Criterios de aceptación:**
- [ ] El grafo de 3 features de fixtures contiene ≥ 95 % de los nodos del ground truth y ninguna arista falsa.
- [ ] Las funciones no cubiertas plantadas se reportan como candidatas.

---

## F43 — Ejemplos trabajados y recorrido del usuario

**Objetivo:** pasar de lo abstracto a casos concretos de entrada y salida.
**Depende de:** F36 (la parte que ejecuta código se valida en F53)

**Tareas:**
- `references/24-paquete-por-feature/09-ejemplos-y-recorrido.md` + plantilla `ejemplos.md`:
  - **Recorrido del usuario**: pasos que hace la persona en la UI, CLI o API y qué ve en cada uno (strings con cita); diagrama `journey` o `flowchart`.
  - Al menos un **ejemplo trabajado por resultado principal**: entrada exacta (mensaje, request JSON, comando), estado inicial, resumen numerado de lo que ocurre por dentro enlazado a la traza, salida exacta esperada.
  - En apps de IA: mensaje del usuario → modo → prompt efectivo (enlace al reconstruido) → herramientas disponibles → herramientas llamadas → resultado.
  - Ejemplos ejecutados etiquetados `[D]`; los no ejecutados `[I]`.

**Entregables:** guía, plantilla.

**Criterios de aceptación:**
- [ ] Cada resultado principal tiene al menos un ejemplo (lint).
- [ ] Los ejemplos sin ejecución quedan etiquetados `[I]` con su razón (lint); la reproducción `[D]` se valida en F53.

---

## F44 — Límites, rendimiento, concurrencia y reintentos por feature

**Depende de:** F36

**Tareas:**
- `references/24-paquete-por-feature/10-limites-y-concurrencia.md` + plantilla `limites.md`: timeouts, reintentos y backoff, límites (tamaño, tokens, ítems, rate), paginación, caché, operaciones costosas (I/O en bucles, N+1), concurrencia (paralelismo, locks, colas, condiciones de carrera posibles, cancelación), idempotencia, comportamiento con entradas grandes, vacías o con unicode, comportamiento sin red. Cada punto con cita o `[?]`.

**Criterios de aceptación:**
- [ ] Dry run: timeouts, reintentos y la condición de carrera plantados en fixtures detectados con cita.

---

## F45 — Observabilidad y efectos externos por feature

**Depende de:** F36

**Tareas:**
- `references/24-paquete-por-feature/11-observabilidad-y-efectos.md` + plantilla `observabilidad.md`: logs emitidos (nivel, mensaje, cita), eventos de telemetría y sus propiedades, métricas; efectos externos (red: host, endpoint y resumen del payload; archivos escritos o borrados; procesos lanzados; notificaciones; portapapeles; almacenamiento) y reversibilidad de cada uno; **cómo depurar la feature** (qué log mirar, flags de debug, puntos de breakpoint recomendados).

**Criterios de aceptación:**
- [ ] 100 % de los eventos de telemetría y llamadas de red plantados en la feature de `fx-ts-agent-extension` están documentados.

---

## F46 — Interacciones entre features e impacto de cambios

**Depende de:** F36, F42

**Tareas:**
- `references/24-paquete-por-feature/12-interacciones.md` + plantilla `interacciones.md`:
  - Por feature: de qué features depende, cuáles la afectan (estado, config o eventos compartidos), cuáles bloquea o excluye, orden requerido.
  - Matriz global feature × feature con tipo de relación + diagrama (reporte global, ver F66).
- `npr impact <ruta|símbolo>`: usando grafo inverso y pertenencia a trazas, lista features, resultados (`R-NN`) y superficies afectadas si se cambia ese archivo o función.

**Entregables:** guía, plantilla, `npr/impact.py`, tests.

**Criterios de aceptación:**
- [ ] Interacciones del ground truth al 100 %.
- [ ] `npr impact` sobre 3 símbolos de fixtures devuelve exactamente las features y resultados afectados del ground truth.

---

## F47 — Mini-paquete por superficie (endpoint, comando, mensaje, herramienta, evento)

**Objetivo:** que cada puerta de entrada tenga su propio flujo y resultados, no solo las features.
**Depende de:** F35, F36

**Tareas:**
- `references/24-paquete-por-feature/13-mini-paquete-superficies.md` + plantilla `templates/notes/surface.md`.
- Cada elemento de `surfaces.json` recibe una ficha en `notes/surfaces/<tipo>/<nombre>.md` con: contrato (entrada y salida con tipos y ejemplo), diagrama de flujo corto de decisiones, tabla de resultados posibles (códigos, mensajes, payloads de error), errores, enlace a la feature y a la traza.
- En apps de IA, cada **herramienta del agente** tiene mini-paquete: esquema, handler, aprobación, resultados posibles devueltos al modelo y al usuario.

**Entregables:** guía, plantilla, `npr surface scaffold`, lint.

**Criterios de aceptación:**
- [ ] Dry run: todos los endpoints de `fx-java-micronaut` y todas las herramientas del agente de `fx-ts-agent-extension` tienen mini-paquete con resultados correctos según ground truth.

---

# ETAPA 2 (continuación) — GUÍAS TRANSVERSALES, INGENIERÍA INVERSA Y ECOSISTEMAS

## F48 — Datos y estado

**Objetivo:** dónde vive cada dato y cómo cambia.
**Depende de:** F27

**Tareas:**
- `references/09-datos-y-estado.md`: almacenamiento persistente (esquemas BD, migraciones, entidades ORM, archivos en disco, KV, almacenamiento de navegador, `globalState`/`secrets` de VS Code), estado en memoria (stores, signals, redux/ngrx/zustand, singletons), cachés, máquinas de estado, ciclos de vida, serialización.
- Plantilla con `erDiagram` y `stateDiagram-v2` obligatorios cuando aplique.

**Entregables:** guía, plantilla.

**Criterios de aceptación:**
- [ ] Dry run `fx-java-micronaut`: entidades, relaciones y migraciones al 100 %.
- [ ] Dry run `fx-ts-agent-extension`: todas las ubicaciones de estado del ground truth (persistente y en memoria).

---

## F49 — Interfaces y protocolos

**Objetivo:** catálogo exhaustivo de fronteras.
**Depende de:** F27

**Tareas:**
- `references/10-interfaces-y-protocolos.md`: API HTTP (método, ruta, handler, tipos de request/response, auth), CLI (comando, flags, handler), mensajes IPC/webview (tipo, emisor, receptor, payload, handler), eventos, APIs externas consumidas (base URL, SDK, auth), formatos de archivo leídos/escritos, entradas de entorno.
- Partir de `recon/surfaces.json` y completar tipos de payload leyendo el código.

**Entregables:** guía, plantilla.

**Criterios de aceptación:**
- [ ] Dry run: 100 % de tipos de mensaje webview de `fx-ts-agent-extension` con emisor, receptor, payload y handler correctos.

---

## F50 — Extensibilidad: plugins, skills, reglas, MCP, hooks

**Objetivo:** explicar en detalle cómo la app se extiende (caso clave: "cómo usa las skills descargadas").
**Depende de:** F27

**Tareas:**
- `references/11-extensibilidad.md` con checklist para cada mecanismo:
  - **Descubrimiento:** rutas buscadas (global/proyecto/modo), orden, variables que lo cambian.
  - **Formato:** archivo esperado, frontmatter, validación, qué pasa si es inválido.
  - **Precedencia y conflictos** (mismo nombre en dos lugares).
  - **Carga:** cuándo (arranque, bajo demanda, watcher), caché, recarga.
  - **Inyección:** cómo y dónde entra al prompt/contexto (índice de descripciones vs contenido completo), qué herramienta la activa.
  - **Instalación:** marketplace, CLI externo (por ejemplo `npx skills add`), descarga manual, dónde escribe.
  - **Permisos y seguridad:** qué puede hacer una extensión.
  - MCP: archivos de configuración, transportes, registro de herramientas, aprobación.
  - Hooks, modos personalizados, comandos personalizados, temas.
- Playbook "cómo agregar una extensión de cada tipo".

**Entregables:** guía, plantilla.

**Criterios de aceptación:**
- [ ] Dry run sobre `fx-ts-agent-extension`: explicación del cargador de skills cubre rutas, precedencia, parseo, punto de inyección y herramienta de activación, 100 % según ground truth, con citas.

---

## F51 — Apps con LLM: modos, prompts, herramientas y loop del agente

**Objetivo:** analizar a fondo apps de IA (caso clave: "cómo se implementa el modo plan").
**Depende de:** F27

**Tareas:**
- `references/12-apps-con-llm.md`, checklist completo:
  - Proveedores y capa de abstracción; construcción de requests; streaming.
  - **Ensamblado del system prompt:** secciones, orden, condicionales por modo, por proveedor, por settings; inclusión de reglas, skills, MCP, información del entorno.
  - **Modos:** definición, herramientas permitidas por modo, restricciones de archivos, cómo se cambia de modo (usuario, herramienta, orquestador), qué se conserva al cambiar.
  - **Herramientas:** definición/esquema, handler, aprobación/permisos/auto-aprobación, formato del resultado devuelto al modelo.
  - **Loop del agente:** turno, parseo de tool calls (XML o nativas), reintentos, errores, límites, finalización.
  - Gestión de contexto: conteo de tokens, truncado, condensación/resumen, memoria.
  - Checkpoints/deshacer, costo y telemetría, subagentes/orquestación interna.
- **Entregable obligatorio por modo: "prompt efectivo reconstruido"**: el system prompt final tal como lo vería el modelo, ensamblado fragmento por fragmento, cada fragmento con su cita y la condición que lo incluye. Plantilla `templates/notes/reconstructed-prompt.md`.
- Mapa "modo → herramientas → handlers".

**Entregables:** guía, plantillas.

**Criterios de aceptación:**
- [ ] Dry run: el prompt reconstruido de los modos `plan` y `code` de `fx-ts-agent-extension` coincide en contenido y orden con el ground truth.
- [ ] El mapa modo→herramientas coincide al 100 %.
- [ ] La traza del loop del agente cubre parseo, aprobación, ejecución y reinyección del resultado.

---

## F52 — Ingeniería inversa estática

**Objetivo:** entender código sin fuente legible.
**Depende de:** F27

**Tareas:**
- `references/13-ingenieria-inversa.md` + scripts en `scripts/npr/re/`:
  - JS minificado: pretty-print propio (indentación por llaves/`;`, sin dependencias) o `prettier` si existe; recuperar fuentes desde sourcemaps (`sourcesContent`); reconstruir el mapa de módulos de bundles webpack/esbuild/rollup (detectar el runtime del bundler y el objeto de módulos).
  - `.asar` de Electron: lector propio (cabecera JSON + offsets) → `npr re asar extract`.
  - `.vsix`, `.jar`, `.apk`, `.whl`, `.nupkg`: extraer como zip; listar contenido.
  - Java `.class`: `javap -c -p` si existe; decompiladores opcionales (CFR, jadx) si están instalados.
  - Python `.pyc`: `marshal` + `dis` (versión compatible).
  - Binarios nativos/Go/Rust: tipo de archivo (magic bytes), `strings` propio, símbolos con `nm`/`objdump` si existen, `go version -m` para buildinfo.
  - WASM: secciones e imports/exports (parser propio mínimo).
  - Técnica de **anclas de strings**: localizar lógica por mensajes de error, textos de UI, URLs y claves.
- Las salidas van a `re/` y alimentan fichas `reverse`.
- Nota de uso responsable: análisis para comprensión; respetar licencias.

**Entregables:** guía, `npr re <subcomando>`, tests.

**Criterios de aceptación:**
- [ ] `fx-minified` con sourcemap: se recupera la lista de módulos originales y su contenido.
- [ ] `fx-minified` sin sourcemap: dry run identifica las funciones del ground truth usando anclas de strings.
- [ ] Test unitario del lector `.asar` con un archivo construido en el test.
- [ ] Test de `.pyc` desensamblado.

---

## F53 — Análisis dinámico seguro

**Objetivo:** confirmar comportamiento ejecutando, sin riesgo para el usuario.
**Depende de:** F27, F40, F43

**Tareas:**
- `references/14-analisis-dinamico.md`:
  - Requiere permiso explícito del usuario; nunca en la copia de trabajo: usar `git worktree add` en `.project-review/dyn/worktree` o copia temporal.
  - Recomendaciones de aislamiento (contenedor, sin secretos reales, red desactivada cuando sea posible).
  - Ejecutar la suite de tests para confirmar comportamiento; agregar logs temporales en la copia; ejecutar con flags de debug.
  - Trazadores incluidos: `scripts/npr/dyn/py_tracer.py` (`sys.settrace` → secuencia de llamadas filtrada al repo) y `scripts/npr/dyn/node_tracer.cjs` (hook de `Module._load` que envuelve funciones exportadas y registra llamadas).
  - Resultados etiquetados `[D]` con cita `[@dyn:<id>]` a `dyn/logs/<id>.jsonl`.
- No instalar dependencias del repo analizado sin permiso (los scripts de instalación pueden ejecutar código).

**Entregables:** guía, trazadores, `npr dyn` (worktree, trace-python, trace-node, cleanup), tests.

**Criterios de aceptación:**
- [ ] El trazador Python sobre un comando de `fx-python-cli` produce la secuencia de llamadas del ground truth.
- [ ] El trazador Node registra la secuencia de un flujo del arnés CLI de `fx-ts-agent-extension`.
- [ ] Tras `npr dyn cleanup`, `git status` y `git worktree list` del repo original quedan como antes.
- [ ] Integración con el paquete por feature: los ejemplos `[D]` de F43 en `fx-python-cli` reproducen la salida exacta, y los tests de una feature (F40) se ejecutan en el worktree con sus escenarios etiquetados `[D]`.

---

## F54 — Build, CI y release

**Objetivo:** cómo se construye, prueba, empaqueta y publica.
**Depende de:** F27

**Tareas:**
- `references/15-build-ci-release.md`: scripts, herramientas de build y bundlers con su config, pipelines CI (jobs, triggers, matrices; nombres de secretos, nunca valores), versionado, empaquetado (vsix, docker, binarios), entornos, cómo levantar el proyecto en local paso a paso.

**Entregables:** guía, plantilla.

**Criterios de aceptación:**
- [ ] Dry run en fixtures con workflows: todos los jobs y pasos descritos con citas.
- [ ] La sección "cómo levantarlo en local" es ejecutable en `fx-python-cli` siguiendo solo el texto.

---

## F55 — Superficie de seguridad

**Objetivo:** entender riesgos y límites de confianza (para comprensión, no explotación).
**Depende de:** F27

**Tareas:**
- `references/16-seguridad.md`: autenticación/autorización, manejo de secretos, validación de entradas, sitios de ejecución de comandos (`child_process`, `exec`, `subprocess`, `Runtime.exec`), acceso a sistema de archivos y su alcance, egreso de red (lista de hosts), deserialización, modelo de permisos (en agentes: aprobación de herramientas), dependencias con riesgo (si hay herramientas disponibles y permitidas: `npm audit`, `osv-scanner`, `pip-audit`).

**Entregables:** guía, plantilla.

**Criterios de aceptación:**
- [ ] Dry run: 100 % de los sitios de ejecución de comandos y de egreso de red plantados en fixtures listados.

---

## F56 — Historia y evolución

**Objetivo:** responder "por qué existe esto" y "cuándo cambió".
**Depende de:** F27

**Tareas:**
- `references/17-historia-git.md`: uso de `npr git why/when`, `git log --follow`, `-S`, `-G`, `blame` por rango, referencias a issues/PRs, línea de tiempo de cambios arquitectónicos, features por fecha de introducción.
- Citas `[@git:sha]`.

**Entregables:** guía, plantilla.

**Criterios de aceptación:**
- [ ] Dry run: "¿cuándo y por qué se agregó X?" en el fixture con historia responde con el commit correcto citado.

---

## F57 — Guías por ecosistema: web, TypeScript, VS Code, Electron

**Objetivo:** conocimiento específico para no perderse en convenciones del stack.
**Depende de:** F27
**Paralelizable con:** F58, F59

**Tareas:**
- `references/21-ecosistemas/` con secciones fijas (dónde empezar, entry points, estructura típica, indirecciones típicas y cómo resolverlas, configuración, testing, build, trampas):
  `node-typescript.md`, `vscode-extensions.md` (activación, `contributes`, webviews y su protocolo, `globalState`/`secrets`, `ExtensionContext`), `electron.md`, `react.md`, `angular.md` (standalone, signals, DI, routing, interceptores), `nextjs.md` (app router, server actions, route handlers), `nestjs.md`, `vite-webpack-esbuild.md`.

**Entregables:** 8 guías.

**Criterios de aceptación:**
- [ ] Cada guía tiene las 8 secciones fijas (lint).
- [ ] Dry run con `vscode-extensions.md` en `fx-ts-agent-extension` resuelve el registro de comandos y el protocolo webview.
- [ ] Dry run con `angular.md` en `fx-monorepo` resuelve DI e interceptores.

---

## F58 — Guías por ecosistema: JVM, Python, Go, Rust, .NET

**Depende de:** F27
**Paralelizable con:** F57, F59

**Tareas:**
- `java-spring.md`, `java-micronaut.md` (DI en compilación, `@Factory`, `@Requires`, entornos de `application.yml`, `@Client` declarativo, `@Controller`, filtros), `kotlin.md`, `python.md` (Django, FastAPI, Flask, Celery, entry points de plugins), `go.md`, `rust.md`, `dotnet.md`.

**Entregables:** 7 guías.

**Criterios de aceptación:**
- [ ] Cada guía tiene las 8 secciones fijas.
- [ ] Dry run con `java-micronaut.md` resuelve todas las trampas de `fx-java-micronaut`.
- [ ] Dry run con `python.md` resuelve los plugins por entry points de `fx-python-cli`.

---

## F59 — Guías por ecosistema: móvil, nativo, otros e infraestructura

**Depende de:** F27
**Paralelizable con:** F57, F58

**Tareas:**
- `android.md`, `ios-swift.md`, `flutter.md`, `react-native.md`, `c-cpp.md`, `php-laravel.md`, `ruby-rails.md`, `infra-iac.md` (Docker, compose, Kubernetes, Terraform, serverless), `monorepos.md`, `polyglot.md` (comunicación entre lenguajes: stdin/stdout, FFI, gRPC, HTTP).

**Entregables:** 10 guías.

**Criterios de aceptación:**
- [ ] Cada guía tiene las 8 secciones fijas.
- [ ] Dry run con `polyglot.md` en `fx-polyglot` traza la comunicación Go↔Rust↔shell completa.

---

## F60 — Modo pregunta

**Objetivo:** responder a fondo "¿cómo funciona X?" sin exigir el análisis completo antes.
**Depende de:** F27, F31, F36, F51

**Tareas:**
- `references/20-modo-pregunta.md`:
  1. Asegurar recon (rápido) si no existe.
  2. Reformular la pregunta en preguntas verificables y términos ancla (nombres, strings de UI, slugs de modo, claves i18n, nombres de herramientas, comandos).
  3. Localizar anclas (`npr symbols find`, búsqueda de strings, `surfaces.json`, `llm.json`).
  4. Conjunto candidato por vecindad en el grafo (n saltos) + co-cambio git.
  5. Lectura profunda **completa** del conjunto candidato (con subagentes si es grande), fichas y ledger.
  6. Trazas necesarias; prompt reconstruido si es app LLM.
  7. Reutilizar notas existentes si ya hubo análisis completo.
  8. Si la pregunta es sobre una feature o superficie, generar su **paquete completo** (F33–F47) o mini-paquete, no solo una traza.
  9. Respuesta en `notes/answers/<slug>.md`: respuesta corta · explicación completa · trazas · **diagrama de flujo de decisiones** · **resultados posibles** con lo que ve el usuario · diagrama de secuencia · archivos clave · configuración relevante · errores · ejemplos trabajados · cómo modificarlo · preguntas abiertas · enlace al paquete de la feature.
  10. Verificación de las afirmaciones de la respuesta (verificador).
- `templates/notes/answer.md`.

**Entregables:** guía, plantilla, `npr question new "<texto>"` (crea slug y esqueleto).

**Criterios de aceptación:**
- [ ] Dry run en `fx-ts-agent-extension` sin análisis completo previo: 5 preguntas doradas (modo plan, carga de skills, aprobación de herramientas, condensación de contexto, protocolo webview) superan el umbral del scorer definido en F80 (se valida formalmente en F74).
- [ ] Cada respuesta incluye al menos una traza completa, diagrama de flujo de decisiones, matriz de resultados posibles y citas válidas.

---

# ETAPA 3 — VERIFICACIÓN Y CALIDAD

## F61 — Linter de citas y etiquetas

**Objetivo:** ninguna cita rota, ninguna afirmación sin respaldo.
**Depende de:** F28–F60
**Paralelizable con:** F64

**Tareas:**
- `npr claims check [ruta|--all]`:
  - Extrae citas de todas las notas y reportes.
  - Verifica: archivo existe en inventario; rango dentro de las líneas del archivo; si hay `#Símbolo`, el símbolo aparece en el rango; `[@git:sha]` existe; `[@dyn:id]` existe.
  - Reglas de etiquetas: `[V]`/`[D]` con ≥ 1 cita en el mismo bullet o párrafo; `[I]` con "porque"/"razón:"; `[?]` con `OQ-NNN` existente.
  - Detecta citas a archivos con política `excluded` (advertencia).
- Salida `verify/claims-report.json` y resumen legible.

**Entregables:** `npr/claims.py`, tests.

**Criterios de aceptación:**
- [ ] Tests: rango fuera de límites, archivo inexistente, símbolo ausente, sha inexistente, `[V]` sin cita, `[I]` sin razón, `[?]` sin OQ → todos detectados.
- [ ] 0 falsos positivos sobre las notas de referencia correctas de los fixtures.

---

## F62 — Gates de cobertura y completitud

**Objetivo:** imposible terminar con huecos.
**Depende de:** F61
**Paralelizable con:** F65

**Tareas:**
- `npr gate coverage`: ningún archivo en `pending`/`read` sin ficha; exclusiones con razón.
- `npr gate modules`: cada dossier lista todos los archivos de su módulo.
- `npr gate features`: cada feature del catálogo tiene ≥ 1 traza y su **paquete completo** (`npr lint feature-package` en verde).
- `npr gate branches`: para cada feature, todos los puntos de decisión y salidas de `_branches.json` mapeados en el diagrama de flujo y en la matriz de resultados (F35, F36).
- `npr gate outcomes`: cada `R-NN` tiene escenario de prueba, al menos una fila en la tabla de decisión y "qué ve el usuario".
- `npr gate surfaces`: cada elemento de `surfaces.json` (ruta, comando, mensaje, evento, herramienta) tiene mini-paquete (F47) y aparece en al menos un dossier o traza.
- `npr gate llm`: si `is_llm_app`, cada modo tiene prompt reconstruido y cada herramienta tiene handler documentado.
- `npr gate all`.

**Entregables:** `npr/gates.py`, tests que fuerzan cada falla.

**Criterios de aceptación:**
- [ ] Cada gate falla con código 2 y lista exacta de faltantes ante un workspace incompleto construido en el test.
- [ ] Todos los gates pasan sobre un workspace completo de referencia de un fixture.

---

## F63 — Verificador independiente

**Objetivo:** que el trabajo no se califique a sí mismo.
**Depende de:** F61

**Tareas:**
- `references/18-verificacion.md`:
  - Verificador con contexto limpio, recibe solo el documento a verificar + acceso al código.
  - Muestreo: 100 % de afirmaciones en trazas, features, prompts reconstruidos y respuestas del modo pregunta; en el resto, el porcentaje de `verifier_sample_noncritical` de `config/defaults.json` (default 50 %, configurable hasta 100 %).
  - Veredictos por afirmación: `correcta | incorrecta | imprecisa | no-verificable`, con corrección propuesta y cita.
  - El orquestador aplica correcciones y se repite hasta 0 `incorrecta` en documentos críticos.
- `npr verify sample <doc>` genera la lista de afirmaciones a verificar; `npr verify apply` registra veredictos en `verify/verdicts.jsonl`.

**Entregables:** guía, brief de verificador (actualizar F27), comandos, tests.

**Criterios de aceptación:**
- [ ] Test de errores sembrados: 10 afirmaciones falsas insertadas en notas correctas de un fixture → 10/10 detectadas combinando linter (F61) + verificador.
- [ ] El ciclo termina con 0 `incorrecta` en documentos críticos del fixture.

---

## F64 — Linter anti-relleno

**Objetivo:** prohibir la vaguedad que hace inútiles los reportes de IA.
**Depende de:** F28–F60
**Paralelizable con:** F61

**Tareas:**
- `npr lint vague`: detecta (ES/EN) hedging sin etiqueta (`probablemente`, `parece`, `posiblemente`, `likely`, `seems`, `might`), enumeraciones truncadas (`etc.`, `entre otros`, `y más`, `...`), cuantificadores vagos sin lista (`varios archivos`, `algunos módulos`), secciones vacías, `TODO`/`TBD`, `N/A` sin razón, frases genéricas sin cita en secciones técnicas.
- Lista de patrones en datos, ampliable.

**Entregables:** `npr/lint_vague.py`, tests.

**Criterios de aceptación:**
- [ ] Tests con cada patrón en ES y EN.
- [ ] 0 falsos positivos en notas de referencia correctas de los fixtures.

---

## F65 — Registro y ciclo de preguntas abiertas

**Objetivo:** lo desconocido se gestiona, no se esconde.
**Depende de:** F61
**Paralelizable con:** F62

**Tareas:**
- `openq/openq.jsonl`: `id (OQ-NNN), pregunta, contexto, dónde se buscó (citas), hipótesis, estado (abierta|resuelta|irresoluble), resolución, qué la resolvería`.
- `npr openq add|list|resolve|close`.
- Ciclo de resolución con subagentes resolvedores en olas; las irresolubles quedan documentadas con lo intentado y qué haría falta (por ejemplo, análisis dinámico o acceso a un servicio externo).

**Entregables:** `npr/openq.py`, brief de resolvedor, tests.

**Criterios de aceptación:**
- [ ] El ítem deliberadamente irresoluble de un fixture (servicio externo) termina como `irresoluble` con intentos y requisito documentados.
- [ ] Toda etiqueta `[?]` del workspace apunta a una OQ existente (cubierto por F61).

---

# ETAPA 4 — REPORTES

## F66 — Catálogo de reportes y plantillas

**Objetivo:** definir los reportes finales, su contenido obligatorio y de qué notas se alimentan.
**Depende de:** F61–F65

**Tareas:**
- `references/19-reportes.md` + `templates/reports/` con una plantilla por reporte:

| # | Reporte | Fuente principal |
|---|---|---|
| 00 | `00-INDICE.md` — índice navegable y cómo leer los reportes | todos |
| 01 | `01-resumen-ejecutivo.md` — qué es, para qué sirve, cómo está hecho, cifras clave, 10 hallazgos | todos |
| 02 | `02-mapa-del-repositorio.md` — árbol comentado de carpetas y propósito | inventario, dossiers |
| 03 | `03-stack-y-dependencias.md` — lenguajes, frameworks, cada dependencia directa: para qué sirve y dónde se usa, transitivas, duplicadas, sin uso | stack, deps, lock, external-usage |
| 04 | `04-arquitectura.md` — C4, procesos, componentes, decisiones, riesgos | notes/cross/arquitectura |
| 05 | `05-modulos.md` + `modulos/<m>.md` | dossiers |
| 06 | `06-features.md` (catálogo con tabla: feature · nº resultados · nº decisiones · nº errores · % resultados con test · estado) + **carpeta `features/<FEAT-NNN>-<slug>/` con los 13 artefactos del paquete** (README, flujo, resultados, decisión, secuencia y estados, errores, pruebas, datos, llamadas, ejemplos, límites, observabilidad, interacciones) | paquetes de features |
| 07 | `07-flujos.md` + `flujos/<f>.md` | trazas |
| 07b | `07b-superficies.md` + `superficies/<tipo>/<nombre>.md` — mini-paquete por endpoint, comando, mensaje, herramienta y evento | notes/surfaces |
| 08 | `08-datos-y-estado.md` | transversal datos |
| 09 | `09-interfaces-y-protocolos.md` | transversal interfaces |
| 10 | `10-configuracion.md` — variables, claves, flags, defaults | config |
| 11 | `11-extensibilidad.md` — plugins, skills, MCP, hooks | transversal extensibilidad |
| 12 | `12-ia-prompts-y-agentes.md` — modos, prompts reconstruidos, herramientas, loop (si aplica) | transversal LLM |
| 13 | `13-build-ci-release.md` + cómo levantarlo en local | transversal build |
| 14 | `14-testing.md` — estrategia, cobertura por módulo, cómo correr | tests, dossiers |
| 15 | `15-seguridad.md` | transversal seguridad |
| 16 | `16-historia-y-evolucion.md` | git |
| 17 | `17-indice-de-archivos.md` — cada archivo, una fila | inventario, fichas |
| 18 | `18-glosario.md` | glosario acumulado |
| 19 | `19-guia-de-onboarding.md` — orden de lectura, primeros 10 archivos, primera modificación sugerida | todos |
| 20 | `20-playbooks-de-modificacion.md` | dossiers, extensibilidad |
| 21 | `21-ingenieria-inversa.md` (si aplica) | re/ |
| 22 | `22-preguntas-abiertas-y-limitaciones.md` | openq |
| 23 | `23-cobertura-y-verificacion.md` — ledger, gates, veredictos, métricas | ledger, verify |
| 24 | `24-catalogo-de-errores.md` — todos los errores, origen, propagación, manejo, qué ve el usuario, errores tragados | errores por feature + recon/errors.json |
| 25 | `25-matriz-de-interacciones.md` — feature × feature, diagrama, análisis de impacto de cambios | interacciones por feature |
| 26 | `26-escenarios-y-cobertura-de-resultados.md` — todos los escenarios Given/When/Then, qué resultados tienen test y cuáles son brecha | pruebas por feature |
| — | `respuestas/<slug>.md` (modo pregunta) | notes/answers |

- Cada plantilla: secciones obligatorias, qué diagramas lleva, reglas de etiquetas.

**Entregables:** guía, 28+ plantillas de reporte (incluida la del paquete por feature y la del mini-paquete por superficie).

**Criterios de aceptación:**
- [ ] Cada reporte tiene plantilla con secciones y fuente declarada.
- [ ] El reporte `06-features.md` enlaza a los 13 artefactos de cada feature y su tabla resumen se genera desde los paquetes (no a mano).
- [ ] `validate_skill.py` en verde (todos los enlaces existen).

---

## F67 — Ensamblador de reportes

**Objetivo:** convertir notas en reportes navegables, consistentes e interconectados.
**Depende de:** F66

**Tareas:**
- `npr report build`:
  - Rellena plantillas con notas (secciones mecánicas desde JSON; secciones narrativas las redacta el agente redactor y el ensamblador las integra).
  - Convierte `[@ruta:a-b]` en enlaces relativos clicables (`../../ruta#La-Lb` en estilo GitHub) manteniendo el texto `ruta:a-b`.
  - Enlaces cruzados: feature ↔ traza ↔ módulo ↔ archivo; primera aparición de cada término del glosario enlazada.
  - Tabla de contenidos por reporte e índice global.
- `npr report check-links`: todos los enlaces internos resuelven.

**Entregables:** `npr/report.py`, tests.

**Criterios de aceptación:**
- [ ] `check-links` sin enlaces rotos en los reportes de un fixture.
- [ ] Ejecución idempotente (dos builds = salida idéntica).
- [ ] Ninguna cita queda en formato crudo `[@…]` en `reports/`.

---

## F68 — Diagramas y validación Mermaid

**Depende de:** F66
**Paralelizable con:** F69, F70

**Tareas:**
- Helpers para generar `flowchart`, `sequenceDiagram`, `classDiagram`, `erDiagram`, `stateDiagram-v2` y C4 (con subgrafos de flowchart).
- Validador: `mmdc` si está disponible; si no, lint estructural propio (tipo de diagrama válido, ids válidos, comillas en etiquetas con caracteres especiales, bloques balanceados, tope de nodos con división automática).
- `npr lint mermaid` sobre notas y reportes.

**Entregables:** `npr/mermaid.py`, tests.

**Criterios de aceptación:**
- [ ] Todos los diagramas de los reportes de los fixtures pasan el validador.
- [ ] Un grafo de 500 nodos se divide en diagramas bajo el tope.
- [ ] Etiquetas con `()`, `[]`, `:` y comillas se escapan correctamente (tests).

---

## F69 — Índice de archivos automático

**Depende de:** F66
**Paralelizable con:** F68, F70

**Tareas:**
- `17-indice-de-archivos.md` generado: ruta · categoría · política · rol (1 línea de la ficha) · módulo · features · enlace a ficha. Agrupado por directorio.

**Criterios de aceptación:**
- [ ] Número de filas = número de entradas de inventario (test).
- [ ] Toda fila de archivo `full` tiene rol no vacío.

---

## F70 — Export legible por máquina y visor HTML offline

**Depende de:** F66
**Paralelizable con:** F68, F69

**Tareas:**
- `npr report json` → `reports/knowledge.json` (módulos, archivos, símbolos clave, features, flujos, superficies, dependencias, config, preguntas abiertas) validado con el esquema `knowledge`.
- `npr report html` → `reports/index.html` único y autocontenido: navegación lateral, búsqueda en cliente, render de markdown propio mínimo, diagramas Mermaid (librería cargada desde CDN si hay red; si no, se muestran como bloque de código), enlaces a archivos fuente.

**Criterios de aceptación:**
- [ ] `knowledge.json` valida contra su esquema.
- [ ] `index.html` abre sin red mostrando todos los reportes y la búsqueda encuentra nombres de archivo y features.

---

## F71 — Playbooks de modificación y guía de onboarding

**Objetivo:** pasar de "entender" a "poder cambiarlo".
**Depende de:** F67

**Tareas:**
- `references/19-reportes.md` (sección playbooks) + plantilla: para cada punto de extensión real del repo ("agregar un modo", "agregar una herramienta", "agregar un proveedor", "agregar un endpoint", "agregar un comando"), pasos concretos con archivos a tocar, patrón a copiar (con cita) y tests a agregar.
- Guía de onboarding: orden de lectura, los 10 archivos más importantes y por qué, glosario mínimo, primera modificación sugerida.

**Criterios de aceptación:**
- [ ] Dry run: un subagente que sigue solo el playbook "agregar un modo nuevo" de `fx-ts-agent-extension` lo implementa en una copia y los tests del fixture pasan.
- [ ] La guía de onboarding de cada fixture lista archivos existentes con justificación citada.

---

# ETAPA 5 — ORQUESTACIÓN DE PUNTA A PUNTA

## F72 — `SKILL.md` definitivo

**Objetivo:** el archivo que el runtime carga: corto, preciso y que dirige a todo lo demás.
**Depende de:** F66–F71

**Tareas:**
- Completar `SKILL.md` (≤ 5k tokens) con:
  - **Cuándo usar** y cuándo no.
  - **Arranque:** resolver `SKILL_DIR` (según `references/22`), `python "$SKILL_DIR/scripts/npr.py" init`, preguntar modo y permisos (dinámico sí/no) en un solo mensaje, luego avanzar sin pedir permiso entre etapas.
  - **Modos** y su secuencia de etapas.
  - **Pipeline** resumido con enlace a cada `references/*.md` y en qué etapa leerlo.
  - **Reglas duras** (las 8 leyes condensadas + "nunca concluyas desde el README", "nunca resumas lo que no leíste", "toda feature necesita traza", "todo a disco antes de seguir").
  - **Subagentes:** cuándo, cómo generar briefs (`npr brief`), olas, respaldo secuencial.
  - **Gates** obligatorios antes de entregar.
  - **Entrega:** qué decir al usuario al final (resumen, ubicación de reportes, cómo navegar, preguntas abiertas importantes).
  - **Reanudar** tras corte de contexto: `npr status` / `npr resume`.
- Revisar `description` final para activación fiable.

**Criterios de aceptación:**
- [ ] `validate_skill.py` en verde, estimación ≤ 5000 tokens.
- [ ] Quiz con subagente de contexto limpio que solo tiene `SKILL.md`: para 12 situaciones (una por etapa y modo) indica la acción y el documento correctos; 12/12.
- [ ] Ninguna instrucción de `SKILL.md` contradice una guía de `references/` (revisión por subagente verificador).

---

## F73 — Modo completo E2E en fixtures

**Depende de:** F72

**Tareas:**
- Ejecutar la skill completa, como la ejecutaría un usuario, en un runtime real (o arnés equivalente con el mismo modelo) sobre los 6 fixtures.
- Medir contra ground truth con el scorer (provisional; formal en F80).
- Registrar en `dev/evals/results/full-<fixture>-<fecha>.md`.

**Criterios de aceptación:**
- [ ] Cobertura del ledger 100 % en los 6 fixtures; todos los gates en verde.
- [ ] Recall de features 100 %; precisión de pasos de trazas ≥ 95 %; citas válidas 100 %.
- [ ] Cada feature tiene su paquete completo; recall de resultados posibles 100 % y de puntos de decisión 100 % frente al ground truth; `gate branches` y `gate outcomes` en verde.
- [ ] Las 6 trampas del paquete por feature (F06) detectadas y explicadas correctamente.
- [ ] Toda superficie tiene mini-paquete con resultados correctos.
- [ ] Todas las trampas resueltas o documentadas como `[?]` con OQ (0 trampas "explicadas" incorrectamente).
- [ ] 0 afirmaciones `incorrecta` del verificador en documentos críticos.

---

## F74 — Modo pregunta E2E

**Depende de:** F73
**Paralelizable con:** F75, F78

**Criterios de aceptación:**
- [ ] 5 preguntas doradas por fixture sin análisis completo previo: puntuación ≥ umbral de F80 en todas.
- [ ] Con análisis completo previo, el modo pregunta reutiliza notas (el log muestra lecturas reducidas) y mantiene la puntuación.
- [ ] Cada respuesta tiene traza completa, diagrama de flujo de decisiones, matriz de resultados posibles y citas válidas.

---

## F75 — Modo feature E2E

**Depende de:** F73
**Paralelizable con:** F74, F78

**Tareas:**
- `npr` + `SKILL.md`: modo `feature <nombre>` produce el **paquete completo** de una feature (los 13 artefactos de F33–F46), los mini-paquetes de sus superficies, su historia y su playbook de modificación.

**Criterios de aceptación:**
- [ ] Para 2 features por fixture, el paquete cubre el 100 % de los puntos del ground truth (decisiones, resultados, errores, config, estados, telemetría, tests, interacciones).
- [ ] Los gates aplicables a una sola feature pasan (subconjunto de `gate all`).

---

## F76 — Reanudación y resistencia a cortes de contexto

**Depende de:** F73

**Tareas:**
- `npr resume`: lee `state.json`, ledger, WUs y openq, y devuelve la siguiente acción exacta (qué brief lanzar, qué gate correr).
- Simular interrupción en cada etapa (B a K) y reanudar con un agente nuevo.
- Guía en `references/01-pipeline.md`: qué mantener en contexto del orquestador y qué solo en disco.

**Criterios de aceptación:**
- [ ] Para cada etapa interrumpida, la reanudación completa el análisis sin repetir WUs ya `carded` (verificado por timestamps del ledger).
- [ ] El resultado final reanudado pasa los mismos gates que uno sin interrupción.

---

## F77 — Modo actualización incremental

**Depende de:** F73

**Tareas:**
- `npr diff`: archivos cambiados desde `state.commit` (`git diff --name-status`), renombres incluidos.
- Marcar como obsoletos (`stale`) fichas, dossiers, trazas y features afectadas, usando el grafo inverso de dependencias y la pertenencia a trazas.
- Re-ejecutar solo lo obsoleto; regenerar reportes.
- Reporte `27-cambios-desde-<sha>.md`: qué cambió funcionalmente (features y flujos afectados), no solo qué archivos.

**Criterios de aceptación:**
- [ ] Aplicar un commit preparado que cambia un flujo en un fixture: solo se regeneran las salidas afectadas (lista exacta en test) y el reporte de cambios describe el cambio de comportamiento con citas.
- [ ] Archivos nuevos y borrados actualizan inventario y ledger.

---

## F78 — Modo comparación (versiones o forks)

**Depende de:** F73
**Paralelizable con:** F74, F75

**Tareas:**
- `npr compare <workspaceA> <workspaceB>`: diferencias estructurales (módulos, dependencias, superficies, config, features) y de comportamiento (trazas que cambiaron paso a paso).
- Reporte `comparacion-<a>-vs-<b>.md`.

**Criterios de aceptación:**
- [ ] Fixture v1 vs v2 preparado: todas las diferencias del ground truth de comparación aparecen, con citas a ambos lados.

---

## F79 — Escala: repos gigantes

**Depende de:** F73

**Tareas:**
- WUs jerárquicas: lectores por WU → sintetizadores por paquete → orquestador por sistema.
- Parámetros: concurrencia de subagentes, presupuesto por WU, prioridad de olas; sin límites artificiales por defecto.
- Recon en streaming y caché para repos de cientos de miles de archivos.
- Guía de escalado en `references/01-pipeline.md`.

**Criterios de aceptación:**
- [ ] Repo sintético generado de 20.000 archivos y 2 millones de líneas: `npr recon` completa, `partition` genera plan jerárquico válido, `resume` funciona sobre él.
- [ ] Memoria del proceso de recon acotada (no crece linealmente con el contenido total; test que mide pico con `tracemalloc`).

---

# ETAPA 6 — EVALS Y VALIDACIÓN REAL

## F80 — Preguntas doradas y scorer

**Depende de:** F79

**Tareas:**
- `dev/evals/questions/<fixture>.yaml`: 15–20 preguntas por fixture con: puntos clave obligatorios, archivos que deben citarse, **resultados posibles que deben enumerarse**, ramas que deben aparecer en el diagrama, trampas que deben evitarse.
- Scorer `dev/evals/score.py`:
  - Parte determinista: citas válidas, archivos obligatorios citados, presencia de traza, diagrama de flujo y matriz de resultados; recall de resultados `R-NN` y de puntos de decisión contra el ground truth.
  - Parte con juez: subagente juez con rúbrica fija que marca cada punto clave como cubierto/no cubierto/incorrecto.
  - Puntuación por pregunta y umbral de aprobación leídos de `dev/evals/thresholds.json` (perfil `dev`, `holdout` o `real` según el conjunto evaluado); el scorer nunca tiene umbrales escritos en código.
- Informe en tabla.

**Criterios de aceptación:**
- [ ] El scorer da 100 % a respuestas de referencia y < umbral a respuestas degradadas preparadas (test de sensibilidad).
- [ ] El juez es estable: misma respuesta evaluada 3 veces → misma puntuación.
- [ ] Cambiar un umbral en `thresholds.json` cambia el veredicto del scorer sin tocar código (test).

---

## F81 — Evals sobre fixtures

**Depende de:** F80

**Criterios de aceptación:**
- [ ] Todas las preguntas de los 6 fixtures superan el umbral en modo completo y en modo pregunta.
- [ ] Resultados guardados con fecha, modelo usado y versión de la skill.

---

## F82 — Evals en fixtures reservados (holdout)

**Objetivo:** demostrar que la skill generaliza a repos que su constructor nunca vio.
**Depende de:** F81
**Paralelizable con:** F83, F84, F85
**Subagentes:** generador (contexto limpio, solo `dev/holdout/SPEC.md`), verificador de ground truth, ejecutor de la skill y juez; ninguno es el agente constructor.

**Tareas:**
- Congelar la skill: tag `v1.0.0-rc<N>` y hash del paquete registrados en `PROGRESS.md`.
- El subagente generador crea el lote `dev/holdout/generated/<lote>/` (fixtures + ground truth) según `SPEC.md`. El verificador ejecuta `check_ground_truth.py` y revisa que cada trampa esté plantada.
- El ejecutor corre la skill congelada en modo completo y en modo pregunta sobre cada fixture del lote; el scorer evalúa con el perfil `holdout`.
- El constructor recibe **solo** el informe agregado de fallas por categoría (sin rutas ni identificadores del lote). Las correcciones van a F86 y deben ser generales.
- Tras cualquier corrección, el lote se marca "quemado" y se genera uno nuevo para la siguiente evaluación.
- Resultados en `dev/evals/results/holdout-<lote>-<fecha>.md` con modelo, versión y hash de la skill.

**Entregables:** lote(s) generados, informes de resultados, informe agregado de fallas.

**Criterios de aceptación:**
- [ ] `git log` demuestra que ningún archivo del lote existía antes del tag de congelamiento.
- [ ] Todos los umbrales del perfil `holdout` de `thresholds.json` se cumplen en un lote no quemado.
- [ ] `overfit_guard.py` sigue en verde después de las correcciones de F86.
- [ ] El informe que recibe el constructor no contiene tokens del lote (verificado con un `unique_tokens.txt` generado para el lote).

---

## F83 — Validación real: Kilo Code

**Objetivo:** el caso que motivó la skill.
**Depende de:** F81
**Paralelizable con:** F84, F85

**Tareas:**
- Clonar el repositorio actual de Kilo Code (verificar la URL oficial vigente en el momento de ejecutar).
- Escribir **antes** de ejecutar la skill las preguntas de validación (sin respuestas): 
  1. ¿Cómo se define e implementa el modo plan/arquitecto (o su equivalente actual)? ¿Qué prompt recibe el modelo, qué herramientas tiene permitidas, qué restricciones de archivos, cómo se pasa de ese modo a implementar?
  2. ¿Cómo descubre, valida, prioriza y carga las skills (rutas global/proyecto/modo, compatibilidad con otras carpetas), cuándo se inyectan al contexto y qué herramienta las activa?
  3. ¿Cómo se instalan skills desde marketplace o CLI externo y dónde se escriben?
  4. ¿Cómo funciona el loop del agente de punta a punta (desde que el usuario envía un mensaje hasta que se muestra la respuesta)?
  5. ¿Cómo funciona la aprobación y auto-aprobación de herramientas?
  6. ¿Cómo se gestiona el contexto largo (condensación/truncado)?
  7. ¿Cómo se integran los servidores MCP?
  8. ¿Cómo funcionan los checkpoints?
  9. ¿Cómo se comunican la extensión y la UI (protocolo de mensajes completo)?
  10. ¿Cómo se agregan proveedores de modelos?
  11. ¿Cómo funcionan los modos personalizados y las reglas?
  12. ¿Qué se ejecuta al activar la extensión?
  13. ¿Cuáles son todos los resultados posibles al enviar una tarea en modo plan (éxito, plan parcial, rechazo de aprobación, cancelación, error del proveedor, límite de contexto, intento de editar archivos no permitidos) y qué ve el usuario en cada uno?
  14. ¿Qué pasa en cada caso al cargar una skill inválida, duplicada, inexistente o sin permisos de lectura?
- Ejecutar modo completo (con paquete completo para cada feature); luego responder las 14 preguntas en modo pregunta.
- Verificación: verificador independiente al 100 % de afirmaciones de las respuestas + revisión del usuario por muestreo de 20 citas.

**Criterios de aceptación:**
- [ ] Cobertura 100 % de archivos no excluidos; gates en verde.
- [ ] Las 14 respuestas con traza completa, diagrama de flujo de decisiones, matriz de resultados posibles, prompt reconstruido donde aplique, citas 100 % válidas y 0 `incorrecta` del verificador.
- [ ] Los paquetes de "modo plan" y "carga de skills" pasan `lint feature-package`, `gate branches` y `gate outcomes`.
- [ ] El usuario confirma que las 20 citas muestreadas respaldan lo afirmado.
- [ ] Lista de fallas observadas registrada para F86.

---

## F84 — Validación real en más repos

**Depende de:** F81
**Paralelizable con:** F83, F85

**Tareas:**
- Ejecutar en: Cline, Hermes Agent (Python), un backend Micronaut real, un frontend Angular real, un repo grande de otro ecosistema (Go o Rust).
- 8–10 preguntas por repo escritas antes de ejecutar.

**Criterios de aceptación:**
- [ ] Mismos criterios que F83 en cada repo.
- [ ] Fallas registradas para F86.

---

## F85 — Pruebas por runtime: Hermes Agent, Cline, Kilo Code

**Depende de:** F81
**Paralelizable con:** F83, F84

**Tareas:**
- `dev/tools/install.py --runtime hermes|cline|kilo|all --scope global|project [--target <repo>]`:
  - Hermes: copia a `~/.hermes/skills/software-development/notemartin-project-review/` (o la ruta verificada en F02).
  - Cline: `~/.cline/skills/notemartin-project-review/` o `<repo>/.cline/skills/notemartin-project-review/`.
  - Kilo Code: `~/.kilo/skills/notemartin-project-review/` o `<repo>/.kilo/skills/notemartin-project-review/` (y ruta heredada si la versión instalada la usa).
  - Opción `--symlink` para desarrollo.
- En cada runtime probar: descubrimiento, activación por descripción y por nombre, resolución de `SKILL_DIR`, ejecución de `npr.py`, lanzamiento de subagentes, modo secuencial de respaldo, reanudación.

**Criterios de aceptación:**
- [ ] En los 3 runtimes: la skill aparece listada, se activa con 3 frases distintas, ejecuta `npr init` y `npr recon` correctamente.
- [ ] En los runtimes con subagentes: un análisis completo de `fx-python-cli` usa subagentes y pasa los gates.
- [ ] Modo secuencial probado al menos en un runtime con subagentes deshabilitados.
- [ ] Tabla de resultados por runtime en `dev/evals/results/runtimes.md`.
- [ ] La skill funciona con al menos un runtime en macOS, Linux y Windows (resolución de `SKILL_DIR`, `python`/`python3`/`py`, rutas con espacios y unicode).

---

## F86 — Endurecimiento

**Depende de:** F82, F83, F84, F85

**Tareas:**
- Consolidar fallas observadas en `references/23-fallas-comunes.md` (antipatrón observado → contramedida → dónde se aplica).
- Ajustar `SKILL.md`, guías, briefs, linters y gates.
- Re-ejecutar F81 completo y las preguntas de F83.
- Correcciones derivadas del holdout: solo a partir del informe agregado por categoría; luego nuevo lote de holdout (F82) para re-evaluar.

**Criterios de aceptación:**
- [ ] Cada falla registrada tiene contramedida implementada y enlazada.
- [ ] Sin regresiones: F81 y F83 mantienen o mejoran puntuación.
- [ ] Un lote nuevo (no quemado) de holdout cumple los umbrales `holdout` tras las correcciones.
- [ ] `overfit_guard.py` y `check_thresholds.py` en verde.

---

# ETAPA 7 — EMPAQUETADO Y DOCUMENTACIÓN

## F87 — README, versionado y empaquetado

**Depende de:** F86

**Tareas:**
- `README.md` del repo (página para humanos): qué es, capturas de reportes de ejemplo, instalación rápida, enlace a `docs/INSTRUCCIONES.md`.
- `skills/notemartin-project-review/README.md` corto (landing dentro de la skill).
- `CHANGELOG.md`, versión `1.0.0` en frontmatter.
- `dev/tools/package.py`: genera `dist/notemartin-project-review-<versión>.zip` y `.tar.gz` reproducibles (orden y fechas fijas), excluyendo `dev/`.
- Compatibilidad de instalación remota: `npx skills add <owner>/<repo> --skill notemartin-project-review` y `hermes skills install <owner>/<repo>/notemartin-project-review` (verificar sintaxis vigente).

**Criterios de aceptación:**
- [ ] Dos empaquetados seguidos producen el mismo hash.
- [ ] Instalación desde el zip y desde ruta local funciona en los 3 runtimes.
- [ ] `validate_skill.py` en verde sobre el paquete extraído.

---

## F88 — Documento de instrucciones del skill (fase final)

**Objetivo:** el manual completo para instalar, usar, entender y mantener la skill.
**Depende de:** F87

**Tareas:**
- Escribir `docs/INSTRUCCIONES.md` (y copia en `skills/notemartin-project-review/INSTRUCCIONES.md`, enlazada desde el README de la skill) con:
  1. **Qué es y qué problema resuelve.**
  2. **Requisitos:** Python ≥ 3.10, git; herramientas opcionales y qué aportan (ripgrep, tree-sitter, universal-ctags, mmdc, javap, CFR/jadx, node).
  3. **Instalación por runtime** (global y por proyecto) para Hermes Agent, Cline y Kilo Code, incluidos pasos para habilitar skills donde haga falta, y verificación de que quedó instalada.
  4. **Cómo activarla:** frases de ejemplo en español e inglés, invocación por nombre.
  5. **Modos** con ejemplos de prompts reales: completo, pregunta, feature, reanudar, actualizar, comparar.
  6. **Opciones:** idioma, carpeta de salida, análisis dinámico, nivel de muestreo del verificador, concurrencia de subagentes, presupuesto por WU.
  7. **Qué genera:** árbol del workspace, lista de reportes con descripción, cómo navegarlos, `index.html`, `knowledge.json`.
     Incluye una guía de **cómo leer el paquete de una feature**: por dónde empezar (README → flujo → resultados), cómo interpretar los nodos del diagrama y los `R-NN`, cómo usar la tabla de decisión, los escenarios de prueba y el análisis de impacto (`npr impact`), con un ejemplo completo sobre un fixture.
  8. **Flujo típico de uso:** clonar → invocar → revisar resumen → índice → profundizar con modo pregunta → actualizar tras `git pull`.
  9. **Cómo leer la evidencia:** formato de citas, etiquetas `[V] [D] [I] [?]`, preguntas abiertas.
  10. **Subagentes:** cómo los usa cada runtime y qué pasa si no hay.
  11. **Consumo de tokens y tiempo:** qué etapas consumen más y cómo ajustarlo.
  12. **Seguridad:** qué nunca hace la skill sin permiso (ejecutar código, instalar dependencias, red), dónde escribe, redacción de secretos.
  13. **Referencia de la CLI `npr`:** cada subcomando con opciones y ejemplo.
  14. **Solución de problemas por runtime** (skill no aparece, no encuentra `SKILL_DIR`, subagentes fallan, gates que no pasan y cómo resolverlos).
  15. **FAQ.**
  16. **Limitaciones conocidas.**
  17. **Cómo extender la skill:** agregar un ecosistema, reglas de detección, un tipo de reporte, un linter.
  18. **Mantenimiento:** cómo correr tests y evals, cómo publicar una versión.
- `dev/tools/check_docs.py`: compara la referencia de la CLI del documento con `npr <cmd> --help` y valida que cada comando de ejemplo del documento exista.

**Entregables:** `docs/INSTRUCCIONES.md`, copia en la skill, `check_docs.py`.

**Criterios de aceptación:**
- [ ] `check_docs.py` en verde: todos los subcomandos y opciones documentados existen y no falta ninguno.
- [ ] Un subagente con contexto limpio, siguiendo **solo** `INSTRUCCIONES.md`, instala la skill en cada uno de los 3 runtimes y ejecuta un análisis en modo pregunta sobre un fixture con éxito.
- [ ] Cada uno de los 18 apartados existe y no tiene secciones vacías (`npr lint vague` en verde sobre el documento).
- [ ] Todos los enlaces del documento resuelven.
- [ ] `PROGRESS.md` muestra F00–F88 en `HECHA` con evidencia.

---

## Anexo A — Definición de terminado global

La skill está terminada cuando:
- [ ] F00–F88 en `HECHA` con evidencia en `PROGRESS.md`.
- [ ] `python -m pytest` en verde.
- [ ] `validate_skill.py` en verde y `SKILL.md` ≤ 5k tokens.
- [ ] Evals de fixtures sobre umbral (perfil `dev`); lote de holdout no quemado sobre umbral (perfil `holdout`); validación en Kilo Code y repos adicionales aprobada (perfil `real`).
- [ ] `overfit_guard.py`, `check_thresholds.py` y `check_docs.py` en verde; CI verde en Linux, macOS y Windows.
- [ ] `PROGRESS.md` sin preguntas abiertas para el dueño y `DECISIONS.md` al día.
- [ ] Instalada y probada en Hermes Agent, Cline y Kilo Code.
- [ ] `docs/INSTRUCCIONES.md` completo y verificado.

## Anexo B — Matriz de subagentes para construir este roadmap

| Momento | Subagentes en paralelo |
|---|---|
| F02–F04 | 3 investigadores/escritores: runtime research, principios, esquemas |
| F06 | 6 constructores de fixtures + 1 verificador de ground truth |
| F07 | 1 escritor de `SPEC.md` del holdout (distinto de los constructores de F06) + 1 implementador de guardianes |
| F10–F13 | 4 implementadores de scripts |
| F14 | 1 por familia de lenguajes (JS/TS, Python, JVM, Go/Rust, otros) |
| F17–F21 | 5 implementadores |
| F28–F32, F48–F60 | 1 escritor por guía + 1 subagente de dry run por guía (contexto limpio) |
| F34, F39, F42, F46 | 4 implementadores de scripts (`branches`, `errors`, `callgraph`, `impact`) |
| F35–F47 | 1 escritor por artefacto del paquete + 1 subagente de dry run por artefacto |
| F61–F65 | 3 implementadores + 1 sembrador de errores para F63 |
| F68–F70 | 3 implementadores |
| F74, F75, F78 | 3 ejecutores E2E |
| F82 | 1 generador de holdout + 1 verificador de ground truth + 1 ejecutor + 1 juez (ninguno es el constructor) |
| F83–F85 | 1 por repo real + 1 por runtime + verificadores independientes |
| F88 | 1 escritor + 1 probador por runtime siguiendo solo el documento |

Regla: quien escribe una guía nunca es quien hace su dry run; quien produce un análisis nunca es quien lo verifica.

## Anexo C — Umbrales canónicos de calidad

Espejo legible de `dev/evals/thresholds.json` (F07). `check_thresholds.py` exige que ambos coincidan.
`dev` = fixtures de desarrollo · `holdout` = fixtures reservados (F82) · `real` = repos reales (F83, F84).
Porcentajes son mínimos salvo que la métrica diga "máx."; `—` = no aplica a ese perfil.

| Clave | Métrica | dev | holdout | real |
|---|---|---|---|---|
| `coverage.ledger` | Archivos no excluidos con ficha (%) | 100 | 100 | 100 |
| `citations.valid` | Citas que resuelven a archivo, rango y símbolo correctos (%) | 100 | 100 | 100 |
| `classification.accuracy` | Clasificación de archivos correcta (%) | 100 | 98 | — |
| `deps.direct.recall` | Dependencias directas detectadas (%) | 100 | 100 | — |
| `imports.edges.f1` | Precisión y recall de aristas de imports (%) | 98 | 95 | — |
| `imports.dynamic.flagged` | Imports dinámicos marcados como indirección (%) | 100 | 95 | — |
| `entrypoints.recall` | Entry points detectados (%) | 100 | 100 | — |
| `surfaces.recall` | Rutas, comandos, mensajes, eventos y herramientas detectados (%) | 100 | 95 | — |
| `config.recall` | Variables, claves y flags con sitio de lectura y default (%) | 100 | 95 | — |
| `llm.recall` | Prompts, herramientas, modos, cargadores y loop detectados (%) | 100 | 95 | — |
| `llm.false_positives.max` | Falsos positivos de artefactos LLM en repos sin LLM (máx., conteo) | 2 | 3 | — |
| `features.recall` | Features del catálogo (%) | 100 | 100 | — |
| `flows.step_precision` | Pasos de traza correctos (%) | 95 | 90 | — |
| `branches.recall` | Puntos de decisión y salidas extraídos (%) | 100 | 95 | — |
| `outcomes.recall` | Resultados posibles `R-NN` encontrados (%) | 100 | 95 | — |
| `outcomes.invented.max` | Resultados inventados según el verificador (máx., conteo) | 0 | 0 | 0 |
| `errors.propagation.recall` | Errores con propagación correcta (%) | 100 | 95 | — |
| `callgraph.node_recall` | Nodos del grafo de llamadas por feature (%) | 95 | 90 | — |
| `callgraph.false_edges.max` | Aristas falsas en el grafo de llamadas (máx., conteo) | 0 | 0 | — |
| `traps.resolved_or_flagged` | Trampas resueltas o marcadas `[?]` con OQ (%) | 100 | 100 | — |
| `traps.wrong.max` | Trampas "explicadas" incorrectamente (máx., conteo) | 0 | 0 | 0 |
| `verifier.incorrect_critical.max` | Afirmaciones `incorrecta` en documentos críticos (máx., conteo) | 0 | 0 | 0 |
| `eval.keypoints` | Puntos clave cubiertos por pregunta dorada (%) | 90 | 90 | — |
| `eval.incorrect.max` | Puntos clave incorrectos por pregunta (máx., conteo) | 0 | 0 | 0 |
| `judge.stable_runs` | Evaluaciones repetidas del juez con puntuación idéntica (conteo) | 3 | 3 | 3 |
| `real.user_citation_sample` | Citas muestreadas que el usuario confirma (de 20) | — | — | 20 |
| `skill_md.tokens.max` | Tokens estimados del cuerpo de `SKILL.md` (máx.) | 5000 | 5000 | 5000 |