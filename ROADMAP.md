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
| 0 — Fundaciones | F00–F07 | Repo, SKILL.md esqueleto, adaptadores runtime, reglas de evidencia, esquemas, CLI, fixtures, umbrales canónicos, anti-sobreajuste, especificación de holdout | F02 ∥ F03 ∥ F04; F06 por fixture en paralelo |
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
F00 → F01 → F02,F03,F04 → F05 → F06 → F07
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

## F03 — Principios, reglas de evidencia y gramática de citas

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
- [ ] Los ejemplos válidos del documento parsean todos y los inválidos ninguno (test que lee el propio `.md`).
- [ ] `parse_citations` devuelve ruta, rango, símbolo y tipo correctos en ≥ 20 casos de prueba.
- [ ] Las 8 leyes están redactadas como reglas verificables (cada una dice qué gate o linter la hace cumplir).

---

## F04 — Esquemas de datos del workspace

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
- [ ] Todos los ejemplos válidos validan y todos los inválidos fallan con un mensaje que indica el campo.
- [ ] No hay dependencias fuera de la stdlib en `schema.py`.
- [ ] Cada esquema tiene `description` en cada propiedad.

---

## F05 — CLI `npr` y creación del workspace

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
- [ ] `npr init` es idempotente (segunda ejecución no duplica la línea en `.git/info/exclude` ni pisa estado sin `--force`).
- [ ] Funciona en un directorio sin git (sin SHA, con aviso).
- [ ] `git status` del repo analizado queda limpio tras `init`.
- [ ] `npr status --json` valida contra el esquema `state`.
- [ ] `npr --help` lista todos los subcomandos.
- [ ] `npr config show` refleja correctamente la precedencia en un test con los 4 niveles.
- [ ] Todo error de usuario devuelve un código `NPR-Exxx` documentado (test que recorre el catálogo).

---

## F06 — Fixtures sintéticos con ground truth y trampas

**Objetivo:** repos de prueba pequeños pero realistas, con respuestas correctas conocidas, para medir la skill.
**Depende de:** F05
**Subagentes:** uno por fixture, en paralelo.

**Tareas:**
- Crear en `dev/fixtures/`:
  1. `fx-ts-agent-extension`: extensión tipo VS Code (TypeScript) que imita la arquitectura de un agente de código: proceso de extensión + webview con protocolo de mensajes tipado, **modos** (`plan`, `code`, `ask`) con prompts distintos y grupos de herramientas permitidas, **carga de skills** desde `~/.fxagent/skills/` y `.fxagent/skills/` con precedencia y parseo de frontmatter, herramienta `use_skill`, loop de agente con llamadas a herramientas y aprobación, abstracción de proveedores LLM, cliente MCP simulado, condensación de contexto, i18n de la UI. Un archivo de > 5.000 líneas.
  2. `fx-python-cli`: CLI en Python (argparse o click) con plugins por entry points, SQLite, configuración por archivo y variables de entorno, historia git scriptada.
  3. `fx-java-micronaut`: servicio REST Micronaut (controladores, servicios, repositorios, cliente HTTP declarativo, `application.yml` con entornos, DI en tiempo de compilación, migraciones).
  4. `fx-monorepo`: workspace pnpm con frontend Angular (standalone + signals), API Node y librería compartida.
  5. `fx-minified`: un bundle JS minificado con sourcemap y otro sin sourcemap; un `.asar` pequeño; un `.pyc`.
  6. `fx-polyglot`: Go + Rust + script shell con comunicación por stdin/JSON.
- Cada fixture incluye **trampas** que derrotan el análisis superficial (≥ 3 por fixture): código muerto que parece activo, import dinámico, dispatch por string, registro de handlers en un mapa, bus de eventos, README que contradice el código, feature flag que desactiva una feature, nombres engañosos.
- Ground truth en `dev/ground-truth/<fixture>/` (fuera del fixture para que el agente analizador no lo vea):
  `ground_truth.json` (entry points, módulos, dependencias directas, features con sus trazas paso a paso con `archivo:línea`, superficies, config, prompts y su orden de composición, trampas y su resolución) y `GROUND_TRUTH.md` legible.
- Ground truth del **paquete por feature** (para al menos 3 features por fixture y todas las superficies): puntos de decisión y salidas con `archivo:línea`, resultados posibles `R-NN` con su condición y lo que ve el usuario (string exacto), errores y su propagación, efecto de cada clave de configuración, estados de la entidad principal y estados de UI, eventos de telemetría y llamadas de red, mapeo test→resultado y brechas, interacciones entre features, grafo de llamadas esperado.
- Trampas específicas del paquete por feature: un resultado de error que solo ocurre con una combinación de dos settings, un `catch` vacío que convierte un error en éxito silencioso, un timeout con reintento, una condición de carrera, una rama muerta, un resultado que solo se produce cuando el usuario rechaza una aprobación.
- `dev/tools/check_ground_truth.py`: verifica que cada `archivo:línea` del ground truth exista y que el símbolo esperado esté en ese rango.
- Scripts `dev/fixtures/<fx>/build-history.sh` para fixtures con historia git reproducible.

**Entregables:** 6 fixtures, ground truth, verificador.

**Criterios de aceptación:**
- [ ] `check_ground_truth.py` pasa para los 6 fixtures (0 referencias rotas).
- [ ] Cada fixture tiene ≥ 3 trampas documentadas con su resolución correcta.
- [ ] Los fixtures con tests propios los pasan (`npm test`, `pytest`, `./gradlew test` o el equivalente, si el toolchain está disponible; si no, documentado).
- [ ] Ningún archivo dentro de `dev/fixtures/` menciona el ground truth.
- [ ] `fx-ts-agent-extension` tiene al menos: 3 modos, 6 herramientas, 1 cargador de skills con 2 rutas y precedencia, 12 tipos de mensajes webview.
- [ ] Las features con ground truth de paquete tienen al menos 6 resultados posibles cada una (incluidos error, cancelación y permiso denegado cuando aplica) y las 6 trampas específicas del paquete están plantadas y documentadas.

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