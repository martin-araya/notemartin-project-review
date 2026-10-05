# AGENTS.md — Contexto para el agente que construye `notemartin-project-review`

Este archivo es el contexto permanente para cualquier agente de IA (y sus subagentes) que implemente
el `ROADMAP.md` de este repositorio. Léelo completo antes de cada sesión.

**Jerarquía de documentos:** el `ROADMAP.md` manda en *qué* se construye (fases, tareas, criterios);
este archivo manda en *cómo* se trabaja (convenciones, reglas, procesos). `dev/evals/thresholds.json`
manda en los números de calidad. Cualquier contradicción se registra como decisión `D-NNN` en
`DECISIONS.md` (§15).

---

## 0. Arranque

### 0.1 Primera sesión (antes de F00)

1. Leer este archivo completo y las secciones 0–3 y los anexos del `ROADMAP.md`.
2. Confirmar herramientas: `python --version` (≥ 3.10), `git --version`; anotar en el Relevo cuáles de las opcionales existen (ripgrep, universal-ctags, tree-sitter, node, java/javap, go, cargo, mmdc).
3. Ejecutar F00 completa (estructura, `PROGRESS.md`, `DECISIONS.md` con D-001 a D-014, CI).
4. Escribir el primer Relevo (§14) y hacer commit `F00: estructura base`.

### 0.2 Cada sesión

1. Leer este archivo, la sección `## Relevo` y `## Preguntas para el dueño` de `PROGRESS.md`, y `DECISIONS.md`.
2. Ejecutar los "comandos para verificar el estado" del Relevo (como mínimo `python -m pytest` y `python dev/tools/validate_skill.py skills/notemartin-project-review`).
3. Elegir la siguiente fase según §27 y continuar.
4. Antes de que el contexto llegue a su límite, al pausar y al terminar: actualizar el Relevo.

---

## 1. Qué estamos construyendo

Una **skill** en formato abierto Agent Skills (`SKILL.md` + `references/` + `scripts/` + `templates/` +
`schemas/` + `config/`) llamada **`notemartin-project-review`**, instalable en **Hermes Agent**,
**Cline** y **Kilo Code**. Su CLI interna se llama **`npr`**.

La skill permite que un agente de IA analice un repositorio clonado **por completo** y entienda cómo
funciona la aplicación **al revés y al derecho**: estructura, dependencias y para qué sirve cada una,
arquitectura, cada módulo, cada feature, cada flujo de punta a punta, datos y estado, protocolos,
configuración, extensibilidad (plugins, skills, MCP, hooks) y, en apps de IA, modos, prompts
efectivos, herramientas y loop del agente. Si no hay código legible, hace ingeniería inversa. Entrega
varios reportes verificables, enlazados y con citas `archivo:línea`.

Por **cada feature** la skill entrega un **paquete completo** (§7): diagrama de flujo con cada
decisión, todos los resultados posibles y lo que ve el usuario en cada uno, tabla de decisión,
diagramas de secuencia y de estados, errores, escenarios de prueba, linaje de datos, grafo de
llamadas, ejemplos, límites, observabilidad e interacciones. Cada endpoint, comando, mensaje,
herramienta del agente y evento recibe un mini-paquete propio.

**Caso motivador:** el usuario clona Kilo Code y pregunta cómo se implementa el modo plan y cómo usa
las skills descargadas. Las IAs actuales responden con generalidades sacadas del README. Esta skill
debe responder con la traza exacta, el diagrama de decisiones, todos los resultados posibles, el
prompt reconstruido, los archivos y las líneas.

---

## 2. Por qué fallan hoy las IAs (y cómo lo resuelve el diseño)

| Falla observada | Contramedida de diseño |
|---|---|
| Leen el README y extrapolan | Ley del README: la documentación es hipótesis; el código es la verdad. Las contradicciones se reportan. |
| Muestrean unos pocos archivos | Inventario completo + ledger de cobertura + gate `coverage`. |
| Olvidan lo leído por límite de contexto | Ley del disco: todo hallazgo se escribe en el workspace antes de seguir; el orquestador trabaja con notas, no con memoria. |
| Un solo agente intenta leer todo | Particionado en WUs y subagentes lectores en olas; síntesis jerárquica. |
| Confunden nombres con comportamiento | Trazado obligatorio salto por salto con cita por salto. |
| No siguen indirecciones (DI, registros, eventos, imports dinámicos) | Recon marca indirecciones; guías con técnicas específicas; `[?]` + pregunta abierta si no se resuelve. |
| Resumen en vez de explicar | Plantillas con secciones obligatorias; linter anti-relleno. |
| Describen solo el camino feliz | `npr branches` extrae cada decisión y salida del código; diagrama de flujo y matriz de resultados por feature; gates `branches` y `outcomes`. |
| Inventan con seguridad | Etiquetas de evidencia `[V] [D] [I] [?]`, linter de citas, verificador independiente. |
| No dicen lo que no saben | Registro de preguntas abiertas con lo intentado y qué haría falta. |
| Se pierden en repos grandes | Recon determinista por scripts (barato y exacto) antes de gastar tokens en lectura. |
| Funcionan solo en los ejemplos con que se probaron | Guardián anti-sobreajuste + fixtures reservados generados después de congelar la skill (§24). |

---

## 3. Preferencias del dueño del proyecto (obligatorias)

- **Sin límites artificiales**: no hay límite de fases, de líneas, de reportes, de subagentes ni de profundidad. Nunca recortes alcance "para simplificar".
- **Modelos frontier**: los modelos que ejecutan la skill y este roadmap (por ejemplo MiniMax M3 Thinking Max, Kimi K3 Thinking Max) son de nivel frontier. No simplifiques instrucciones, prompts ni plantillas pensando en un modelo menos capaz.
- **Subagentes siempre contemplados**: tanto al construir (§22) como dentro de la skill (§21).
- **Sin estimaciones de tiempo**: no escribas timelines en semanas o meses; el avance se mide en fases cumplidas.
- **Idioma**: documentación, guías, plantillas, reportes y mensajes de error en **español** por defecto (los reportes aceptan `--lang`). Identificadores de código, nombres de módulos de scripts y claves JSON en inglés. Nombres de archivos de `references/` y `templates/` en español.

---

## 4. Runtimes objetivo y reglas de compatibilidad

Datos de partida (verificarlos y actualizarlos en F02 con fuentes y fecha):

| Aspecto | Hermes Agent | Cline | Kilo Code |
|---|---|---|---|
| Ruta global | `~/.hermes/skills/<categoría>/notemartin-project-review/` (categoría propuesta: `software-development`) | `~/.cline/skills/notemartin-project-review/` | `~/.kilo/skills/notemartin-project-review/` (heredado: `~/.kilocode/skills/`) |
| Ruta proyecto | — (verificar en F02) | `.cline/skills/notemartin-project-review/` (también `.clinerules/skills/`) | `.kilo/skills/notemartin-project-review/` (también `.claude/skills/` con compatibilidad activada) |
| Activación | por descripción o nombre; `skill_view` para archivos de soporte | herramienta `use_skill` según `description`; Skills debe estar habilitado en ajustes | por descripción; variantes por modo `skills-<modo>/` |
| Instalación remota | `hermes skills install <owner>/<repo>/notemartin-project-review` | `npx skills add <owner>/<repo>` | `npx skills add <owner>/<repo>` o marketplace |

Reglas que la skill debe cumplir para funcionar en los tres:
1. `name: notemartin-project-review` = nombre de la carpeta (Kilo lo exige). Minúsculas, números y guiones; ≤ 64 caracteres.
2. `description` ≤ 1024 caracteres (límite de Cline), con disparadores en español e inglés.
3. Cuerpo de `SKILL.md` ≤ 5.000 tokens (recomendación de Cline); todo el detalle va en `references/` y se carga bajo demanda mediante enlaces relativos.
4. Frontmatter compatible con agentskills.io; metadatos de Hermes bajo `metadata.hermes`.
5. Sin rutas absolutas; toda ruta interna relativa a la carpeta de la skill.
6. Los scripts se invocan como `python "$SKILL_DIR/scripts/npr.py" …`; cómo obtener `SKILL_DIR` en cada runtime se documenta en `references/22-adaptadores-runtime.md` (F02) y se exporta como `NPR_HOME`. **Riesgo conocido:** si un runtime no expone la ruta de la skill, la skill la busca en las rutas de instalación conocidas y la valida con el archivo marcador `scripts/.npr-marker`.
7. Debe funcionar con subagentes (si el runtime los tiene) y en modo secuencial de respaldo (si no).
8. El lanzador de Python varía (`python`, `python3`, `py -3`); la skill prueba en ese orden y lo documenta.

---

## 5. Arquitectura de la skill

Tres capas:

1. **Capa determinista (scripts Python, `scripts/npr/`)** — todo lo mecánico, exacto y barato:
   inventario, clasificación, stack, manifiestos, lockfiles, workspaces, grafo de imports, símbolos,
   referencias, entry points, superficies, configuración, artefactos LLM, historia git, métricas de
   grafo, particionado, ledger, puntos de decisión, errores, grafo de llamadas, impacto, linters,
   gates, ensamblado de reportes, ingeniería inversa de formatos, trazadores dinámicos.
2. **Capa cognitiva (`SKILL.md` + `references/` + `templates/`)** — lo que requiere comprensión:
   leer código, escribir fichas y dossiers, sintetizar arquitectura, descubrir features, trazar flujos,
   construir paquetes de feature, reconstruir prompts, resolver indirecciones, redactar reportes.
3. **Capa de verificación** — linter de citas y etiquetas, linter anti-relleno, gates de cobertura y
   completitud, verificador independiente con contexto limpio, ciclo de preguntas abiertas.

**Workspace del análisis** (`.project-review/` dentro del repo analizado, excluido vía
`.git/info/exclude`, o donde indique `--out`):

```
.project-review/
├── state/state.json          etapa, modo, commit, configuración efectiva
├── config.json               ajustes del usuario para este análisis (opcional)
├── recon/                    salidas de scripts + RECON.md + errors.json
├── graph/                    edges.jsonl, external-usage.json, modules.json, metrics.json, *.mmd
├── wu/                       WU-NNN.json + plan.md
├── ledger/                   ledger.jsonl + fragments/<WU>.jsonl
├── notes/
│   ├── files/                fichas de archivo
│   ├── modules/              dossiers de módulo
│   ├── flows/                trazas
│   ├── features/             CATALOGO.md + una carpeta por feature con su paquete completo (§7)
│   ├── surfaces/             mini-paquete por endpoint, comando, mensaje, herramienta y evento
│   ├── cross/                hipótesis, arquitectura, datos, interfaces, config, extensibilidad, llm, build, tests, seguridad, historia, glosario
│   └── answers/              respuestas del modo pregunta
├── openq/openq.jsonl         preguntas abiertas
├── verify/                   claims-report.json, verdicts.jsonl
├── re/                       salidas de ingeniería inversa
├── dyn/                      worktree aislado + logs de trazas dinámicas
├── reports/                  reportes finales, knowledge.json, index.html
└── logs/npr.log
```

**Pipeline del orquestador** (detalle en `references/01-pipeline.md`, F26):
A Preparación → B Recon → C Orientación (hipótesis) → D Lectura exhaustiva por WU → E Síntesis de
arquitectura → F Features → G Trazas → G2 Paquete completo por feature y mini-paquetes de superficie →
H Transversales → I Ingeniería inversa / dinámico → J Verificación + preguntas abiertas → K Reportes +
gates → L Entrega.

**Modos:** `completo`, `pregunta`, `feature`, `reanudar`, `actualizar`, `comparar`.

---

## 6. Las 8 leyes (se aplican a la skill y también al agente constructor)

| # | Ley | Qué exige | Cómo se hace cumplir |
|---|---|---|---|
| 1 | Cobertura | Ningún archivo no excluido queda sin leer; toda exclusión tiene razón escrita. | Ledger + `npr gate coverage` |
| 2 | Evidencia | Toda afirmación no trivial lleva etiqueta; `[V]` y `[D]` llevan cita. | `npr claims check` |
| 3 | Trazado | Una feature no está explicada sin al menos una traza completa sin saltos y su paquete completo. | `npr lint flow`, `npr gate features` |
| 4 | README | La documentación es hipótesis; el código es la verdad; las contradicciones se reportan. | Guía de orientación (F26) + verificador |
| 5 | Disco | El contexto no es memoria; todo hallazgo se escribe en el workspace antes de seguir. | Contrato de retorno de subagentes + `npr resume` |
| 6 | Indirección | DI, registros, eventos, imports dinámicos, reflexión y string-dispatch se resuelven o quedan `[?]`. | Indirecciones marcadas en recon + `npr claims check` |
| 7 | Desconocido | Lo que no se sabe va a preguntas abiertas con lo intentado y lo que haría falta. | `npr openq` + regla `[?]`→`OQ-NNN` |
| 8 | No-relleno | Prohibidas enumeraciones truncadas, hedging sin etiqueta, secciones vacías y `N/A` sin razón. | `npr lint vague` |

Para el constructor, la Ley del disco se traduce en el Relevo (§14) y la Ley de evidencia en la
evidencia de cada criterio de aceptación en `PROGRESS.md`.

---

## 7. Paquete obligatorio por feature (etapa 2B del roadmap, F33–F47)

Cada feature produce `notes/features/<FEAT-NNN>-<slug>/` con:

| Archivo | Contenido | Fase |
|---|---|---|
| `README.md` | Dossier de la feature + tabla resumen (nº resultados, decisiones, errores, escenarios, % resultados con test) | F32, F33 |
| `flujo.md` | `flowchart TD` con cada decisión (condición real), rama, bucle, cruce de frontera y nodo terminal por resultado; camino feliz resaltado; tabla nodo → cita | F35 |
| `resultados.md` | Matriz `R-NN`: condición, camino en el diagrama, entradas de ejemplo, **qué ve el usuario** (string exacto citado), efectos y reversibilidad, estado final, registro, recuperación, reproducción, tests | F36 |
| `decision.md` | Tabla de decisión (condiciones → `R-NN`), matriz de configuración (setting → efecto), pre/postcondiciones, invariantes | F37 |
| `secuencia-y-estados.md` | `sequenceDiagram` camino feliz y errores, `stateDiagram-v2` de entidades, estados de UI | F38 |
| `errores.md` | Cada error: origen, propagación capa por capa, manejo final, qué ve el usuario, errores tragados | F39 |
| `pruebas.md` | Escenario Given/When/Then por cada `R-NN`, tests existentes mapeados, brechas | F40 |
| `datos.md` | Linaje de cada dato de entrada hasta su salida, tipos clave, datos sensibles | F41 |
| `llamadas.md` | Grafo de llamadas completo + mapa de archivos; funciones no cubiertas por trazas | F42 |
| `ejemplos.md` | Recorrido del usuario + un ejemplo trabajado por resultado principal (entrada exacta → salida exacta) | F43 |
| `limites.md` | Timeouts, reintentos, límites, paginación, caché, concurrencia, carreras, idempotencia | F44 |
| `observabilidad.md` | Logs, telemetría, métricas, efectos externos y cómo depurar la feature | F45 |
| `interacciones.md` | Dependencias con otras features, estado compartido, impacto de cambios | F46 |
| `_branches.json`, `_callgraph.json` | Extracciones deterministas que alimentan los gates | F34, F42 |

Taxonomía de resultados que se revisa en cada feature (cada categoría se documenta o se declara
inexistente con razón): éxito completo · éxito parcial/degradado · éxito con advertencia · no-op ·
validación de entrada · precondición no cumplida · recurso inexistente · permiso denegado o aprobación
rechazada · cancelación por el usuario · timeout · error de red o servicio externo · error del proveedor
(rate limit, cuota, autenticación, modelo no disponible) · límite alcanzado · conflicto o concurrencia ·
reintento con recuperación · error interno no controlado · estado inconsistente.

Reglas: `flujo.md`, `resultados.md` y `pruebas.md` nunca pueden ser `N/A`. Todo punto de decisión y
toda salida de `_branches.json` aparece en el diagrama y en la matriz de resultados o queda justificado
(`npr gate branches`). Todo `R-NN` tiene escenario, fila en la tabla de decisión y "qué ve el usuario"
(`npr gate outcomes`). Cada superficie de `surfaces.json` tiene mini-paquete en `notes/surfaces/` (F47).

---

## 8. Convenciones de identificadores

| Entidad | Formato | Alcance | Ejemplo |
|---|---|---|---|
| Fase del roadmap (solo constructor) | `FNN` | roadmap | `F35` |
| Feature | `FEAT-NNN` | análisis | `FEAT-007` |
| Resultado posible | `R-NN` (global: `FEAT-NNN/R-NN`) | por feature | `FEAT-007/R-04` |
| Punto de decisión | `DP-NNN` | por feature | `DP-012` |
| Escenario de prueba | `SC-NN` (enlazado a un `R-NN`) | por feature | `SC-04` |
| Error | `ERR-NNN` | análisis | `ERR-031` |
| Flujo (traza) | `FL-NNN` | análisis | `FL-015` |
| Unidad de trabajo | `WU-NNN` | análisis | `WU-003` |
| Pregunta abierta | `OQ-NNN` | análisis | `OQ-009` |
| Superficie | `SRF-<tipo>-<slug>` | análisis | `SRF-msg-switch-mode` |
| Módulo | `MOD-<slug>` | análisis | `MOD-skills-loader` |
| Decisión del constructor | `D-NNN` | repo de desarrollo | `D-015` |
| Código de error de la CLI | `NPR-Exxx` | skill | `NPR-E104` |

- Los ids se asignan en orden de descubrimiento, nunca se reutilizan y se conservan entre ejecuciones de `actualizar` (mapeo estable en `state/ids.json`).
- Carpetas de feature: `<FEAT-NNN>-<slug-en-kebab-case>`. Fichas de archivo: `notes/files/<ruta con "/" reemplazado por "__">.md`.
- Ids de nodos Mermaid: `dp_012` (decisión), `r_04` (resultado terminal), `p_<n>` (proceso), `s_<slug>` (subgrafo). Sin guiones ni espacios.

## 9. Convenciones de diagramas (Mermaid)

- Tipos permitidos: `flowchart`, `sequenceDiagram`, `classDiagram`, `erDiagram`, `stateDiagram-v2`, `journey`.
- Tope de nodos por diagrama: `mermaid.max_nodes` (§13). Si se supera: diagrama general + diagramas de detalle enlazados.
- Etiquetas siempre entre comillas cuando contienen `()[]{}:;,"`; las condiciones se escriben en lenguaje claro, no en código.
- `flowchart` de feature: `TD`; subgrafos por proceso o capa (UI, host/servidor, servicio, BD, externo); cruces de frontera con flecha punteada `-.->` y etiqueta del canal.
- Clases obligatorias para nodos terminales:
  ```
  classDef ok fill:#d1fae5,stroke:#047857,color:#064e3b
  classDef parcial fill:#fef3c7,stroke:#b45309,color:#78350f
  classDef error fill:#fee2e2,stroke:#b91c1c,color:#7f1d1d
  classDef cancelado fill:#e5e7eb,stroke:#4b5563,color:#111827
  classDef noop fill:#e0f2fe,stroke:#0369a1,color:#0c4a6e
  ```
- Camino feliz: `linkStyle <índices> stroke-width:3px`.
- Todo diagrama va acompañado de una tabla nodo → descripción → cita; el diagrama nunca es la única fuente de una afirmación.
- Validación: `npr lint mermaid` (F68) antes de cerrar cualquier nota o reporte.

---

## 10. Estructura del repositorio de desarrollo

```
notemartin-project-review-skill/
├── AGENTS.md                         (este archivo)
├── ROADMAP.md
├── PROGRESS.md                       (estado por fase + ## Relevo + ## Preguntas para el dueño)
├── DECISIONS.md                      (D-NNN)
├── README.md
├── CHANGELOG.md
├── LICENSE
├── pyproject.toml                    (solo config de pytest)
├── .github/workflows/ci.yml          (Linux, macOS, Windows)
├── skills/
│   └── notemartin-project-review/    ← LO QUE SE DISTRIBUYE
│       ├── SKILL.md
│       ├── README.md
│       ├── INSTRUCCIONES.md
│       ├── config/defaults.json
│       ├── references/
│       │   ├── 00-principios.md
│       │   ├── 01-pipeline.md
│       │   ├── 02-subagentes.md
│       │   ├── 03-lectura-de-archivos.md
│       │   ├── 04-stack-y-dependencias.md
│       │   ├── 05-arquitectura.md
│       │   ├── 06-analisis-por-modulo.md
│       │   ├── 07-trazado-de-flujos.md
│       │   ├── 08-features.md
│       │   ├── 09-datos-y-estado.md
│       │   ├── 10-interfaces-y-protocolos.md
│       │   ├── 11-extensibilidad.md
│       │   ├── 12-apps-con-llm.md
│       │   ├── 13-ingenieria-inversa.md
│       │   ├── 14-analisis-dinamico.md
│       │   ├── 15-build-ci-release.md
│       │   ├── 16-seguridad.md
│       │   ├── 17-historia-git.md
│       │   ├── 18-verificacion.md
│       │   ├── 19-reportes.md
│       │   ├── 20-modo-pregunta.md
│       │   ├── 21-ecosistemas/       (F57–F59)
│       │   ├── 22-adaptadores-runtime.md
│       │   ├── 23-fallas-comunes.md
│       │   └── 24-paquete-por-feature/  (00-indice + 13 guías, F33–F47)
│       ├── scripts/
│       │   ├── npr.py                (entrada de la CLI)
│       │   ├── .npr-marker
│       │   └── npr/                  (cli, workspace, config, errors_catalog, inventory, classify, stack,
│       │                              manifests/, lockfiles/, workspaces, imports/, symbols/, tools_probe,
│       │                              entrypoints, surfaces/, env_scan, llm_scan, gitstats, graph, partition,
│       │                              ledger, recon, briefs, citations, claims, gates, lint_vague, openq,
│       │                              branches/, errors, callgraph, impact, feature_package, report,
│       │                              mermaid, schema, re/, dyn/, rules/)
│       ├── schemas/                  (JSON Schemas, F04 y F33)
│       └── templates/
│           ├── recon.md
│           ├── briefs/               (10 plantillas de brief)
│           ├── notes/                (file-card, module-dossier, flow, feature-dossier, features-catalog,
│           │                          architecture, reconstructed-prompt, answer, surface, y feature/ con
│           │                          las 13 plantillas del paquete por feature)
│           └── reports/              (una plantilla por reporte, §20)
├── dev/
│   ├── tests/                        (pytest)
│   ├── fixtures/                     (fx-ts-agent-extension, fx-python-cli, fx-java-micronaut,
│   │                                  fx-monorepo, fx-minified, fx-polyglot)
│   ├── ground-truth/                 (por fixture: ground_truth.json, GROUND_TRUTH.md, unique_tokens.txt)
│   ├── holdout/                      (SPEC.md; generated/<lote>/ solo desde F82)
│   ├── evals/                        (questions/, score.py, thresholds.json, results/)
│   └── tools/                        (validate_skill.py, check_ground_truth.py, overfit_guard.py,
│                                      overfit_allowlist.txt, check_thresholds.py, check_docs.py,
│                                      install.py, package.py)
├── docs/INSTRUCCIONES.md
└── dist/
```

---

## 11. Mapa de la CLI `npr`

Todos los subcomandos aceptan `--json`, `--repo`, `--out`, `--verbose`, `--lang`, `--config`, `--set`.

| Subcomando | Qué hace | Fase |
|---|---|---|
| `init <repo>` | Crea el workspace y `state.json`; agrega exclusión en `.git/info/exclude` | F05 |
| `config show` | Configuración efectiva y origen de cada valor | F05 |
| `status` | Etapa, cobertura, WUs pendientes, OQ abiertas, siguiente acción | F05 |
| `resume` | Siguiente acción exacta tras una interrupción | F76 |
| `inventory` | Inventario de archivos | F08 |
| `classify` | Categoría y política de análisis por archivo | F09 |
| `stack` | Lenguajes, frameworks y plataformas | F10 |
| `deps` · `deps why <pkg>` | Dependencias directas · cadena de dependencia transitiva | F11, F12 |
| `lockfiles` | Versiones resueltas y transitivas | F12 |
| `workspaces` | Paquetes internos de monorepos | F13 |
| `imports` | Grafo de imports interno y externo | F14 |
| `symbols` · `symbols find` · `symbols refs` | Índice de símbolos y referencias | F15, F16 |
| `entrypoints` | Entry points por proceso | F17 |
| `surfaces` | Rutas, comandos, mensajes, eventos, IPC, herramientas | F18 |
| `env` | Variables de entorno, claves de configuración y flags del repo analizado | F19 |
| `llm` | Prompts, herramientas, modos, skills, loop del agente | F20 |
| `git` · `git why` · `git when` | Estadísticas e índice de historia | F21 |
| `graph` | Módulos candidatos, ciclos, métricas, Mermaid | F22 |
| `partition` | Plan de WUs y olas | F23 |
| `ledger mark|merge|gaps|stats|reopen` | Ledger de cobertura | F24 |
| `recon` | Ejecuta todo el reconocimiento y genera `RECON.md` | F25 |
| `brief <tipo> <id>` | Genera el brief de un subagente | F27 |
| `feature scaffold <FEAT-id>` | Crea la carpeta del paquete de una feature | F33 |
| `branches` | Puntos de decisión y salidas | F34 |
| `errors` | Clases, sitios y mensajes de error | F39 |
| `callgraph` | Grafo de llamadas por flujo o feature | F42 |
| `impact <ruta|símbolo>` | Features, resultados y superficies afectadas por un cambio | F46 |
| `surface scaffold` | Crea mini-paquetes de superficie | F47 |
| `re <subcomando>` | Ingeniería inversa (sourcemaps, bundles, asar, zip, class, pyc, binarios, wasm) | F52 |
| `dyn worktree|trace-python|trace-node|cleanup` | Análisis dinámico aislado | F53 |
| `question new "<texto>"` | Esqueleto de respuesta del modo pregunta | F60 |
| `claims check` | Linter de citas y etiquetas | F61 |
| `gate <nombre>` | Gates (§12) | F35, F62 |
| `verify sample|apply` | Muestreo y registro de veredictos del verificador | F63 |
| `lint dossier|card|flow|feature|feature-package|outcomes|mermaid|vague` | Linters de notas | F28, F29, F31, F32, F33, F36, F68, F64 |
| `openq add|list|resolve|close` | Preguntas abiertas | F65 |
| `report build|check-links|json|html` | Ensamblado y export de reportes | F67, F70 |
| `diff` | Cambios desde el último análisis (modo actualizar) | F77 |
| `compare <wsA> <wsB>` | Comparación de versiones o forks | F78 |

Códigos de salida: `0` ok · `1` error de uso · `2` gate o lint fallido · `3` error interno.

## 12. Gates

| Gate | Qué bloquea | Etapa del pipeline | Fase |
|---|---|---|---|
| `coverage` | Archivos no excluidos sin ficha; exclusiones sin razón | D → E | F62 |
| `modules` | Dossiers que no listan todos los archivos de su módulo | E | F62 |
| `features` | Features sin traza o sin paquete completo válido | G2 → H | F62 |
| `branches` | Decisiones o salidas de `_branches.json` sin nodo ni justificación | G2 (por feature) | F35, F62 |
| `outcomes` | `R-NN` sin escenario, sin fila en la tabla de decisión o sin "qué ve el usuario" | G2 (por feature) | F62 |
| `surfaces` | Superficies sin mini-paquete o sin aparecer en dossier o traza | G2 | F62 |
| `llm` | Modos sin prompt reconstruido; herramientas sin handler documentado (si es app LLM) | H | F62 |
| `all` | Todos los anteriores + `claims check` + `lint vague` + `lint mermaid` + `report check-links` | K | F62 |

Ningún reporte se entrega con `npr gate all` en rojo; las excepciones se documentan como `[?]` con OQ.

## 13. Configuración por defecto (`config/defaults.json`)

| Clave | Default | Significado |
|---|---|---|
| `lang` | `es` | Idioma de reportes |
| `workspace.dir` | `.project-review` | Carpeta del workspace dentro del repo |
| `subagents.mode` | `auto` | `auto` · `parallel` · `sequential` |
| `subagents.max_parallel` | `auto` | Máximo que permita el runtime |
| `wu.context_fraction` | `0.5` | Fracción del contexto del modelo lector que puede ocupar una WU |
| `files.giant_threshold_lines` | `2000` | Desde cuántas líneas un archivo se lee por rangos |
| `files.chunk_overlap_lines` | `40` | Solape entre rangos de lectura |
| `symbols.backend` | `auto` | `auto` · `regex` · `treesitter` · `ctags` |
| `branches.follow_depth` | `null` | Sin límite dentro del repo; se corta en ciclos |
| `question.graph_hops` | `2` | Saltos de vecindad en el grafo para el modo pregunta (se amplía si faltan anclas) |
| `git.cochange_min` | `3` | Co-cambios mínimos para relacionar archivos |
| `verifier.sample_critical` | `1.0` | Trazas, paquetes de feature, prompts reconstruidos y respuestas |
| `verifier.sample_noncritical` | `0.5` | Resto de documentos (configurable hasta `1.0`) |
| `mermaid.max_nodes` | `40` | Tope de nodos por diagrama |
| `dynamic.enabled` | `false` | Análisis dinámico solo con permiso explícito |
| `dynamic.network` | `false` | Red durante análisis dinámico |
| `report.formats` | `["md","json","html"]` | Formatos de salida |
| `report.snippets` | `true` | Incluir fragmentos de código en reportes |
| `report.snippet_max_lines` | `30` | Líneas máximas por fragmento |
| `secrets.redact` | `true` | No desactivable |

---

## 14. Relevo entre sesiones del constructor

La sección `## Relevo` de `PROGRESS.md` se **reemplaza completa** (no se acumula) en cada actualización.
El historial queda en git. Plantilla:

```
## Relevo
- Fecha y hora:
- Agente / modelo / runtime:
- Fase(s) en curso y estado:
- Hecho en esta sesión (con commits):
- A medias (archivo → estado exacto → qué falta):
- Subagentes en vuelo (id, ruta del brief, qué devolverán, dónde escribirán):
- Comandos para verificar el estado:
- Siguiente acción exacta (comando o archivo + qué hacer):
- Decisiones tomadas (D-NNN):
- Riesgos y bloqueos:
```

Cuándo actualizarlo: antes de que el contexto llegue a su límite o a una compactación, al pausar, al
terminar cada fase y al terminar la sesión. Un agente nuevo debe poder continuar leyendo solo
`AGENTS.md`, el Relevo y `DECISIONS.md`.

## 15. Decisiones y política de escalamiento

**Decide y registra (`D-NNN` en `DECISIONS.md`), sin detenerte:**
- Detalles de implementación, nombres internos, estructura de módulos, formatos intermedios.
- Elección entre alternativas equivalentes que no cambian el alcance ni las salidas públicas.
- Valores de configuración operativos dentro de §13.
- Corrección de un ground truth **con evidencia** de que estaba mal (la evidencia va en la decisión).
- Contradicciones entre `ROADMAP.md` y este archivo (resolver con la jerarquía del encabezado).

**Pregunta al dueño (`## Preguntas para el dueño` en `PROGRESS.md`) y sigue con otra fase no bloqueada:**
- Reducir alcance, eliminar un artefacto, reporte, modo o gate.
- Relajar cualquier umbral del Anexo C o de `thresholds.json`.
- Cambiar, después de F72, el nombre de la skill, de la CLI, la gramática de citas, la estructura del workspace o el formato de reportes.
- Agregar dependencias de runtime fuera de la stdlib, usar red, servicios pagos o credenciales.
- Ejecutar código de un repo real o instalar sus dependencias.
- Publicar (push a un remoto público, marketplace) o cualquier acción irreversible.

Formato de una pregunta: `- [ ] Q-NNN (fase FNN): pregunta · opciones · recomendación · qué queda bloqueado`.
Si no hay respuesta, solo la fase afectada queda `BLOQUEADA`.

## 16. Registro inicial de decisiones (copiar a `DECISIONS.md` en F00)

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

Plantilla para nuevas decisiones:

```
### D-NNN — Título
- Fecha · Fase · Estado: vigente | reemplazada por D-xxx
- Contexto:
- Decisión:
- Alternativas consideradas:
- Consecuencias:
```

---

## 17. Convenciones de código

- **Python ≥ 3.10, solo biblioteca estándar en runtime.** Dependencias opcionales (PyYAML, tree-sitter, etc.) se detectan en ejecución y siempre hay respaldo. `pytest` solo en desarrollo.
- Sin acceso a red desde los scripts de la skill.
- CLI con `argparse`; cada subcomando acepta `--json` y escribe JSON válido contra su esquema.
- Escrituras atómicas (archivo temporal + `os.replace`). Salidas grandes en JSONL y en streaming.
- Determinismo: mismas entradas → mismas salidas byte a byte (orden estable, sin timestamps en contenido salvo `state.json` y logs).
- Caché por `sha1` de archivo.
- Type hints en todo; funciones puras donde sea posible; un módulo por responsabilidad.
- Reglas por framework y lenguaje en **archivos de datos** (`scripts/npr/rules/*.json`), no en código.
- Nunca modificar el repo analizado: solo leer, salvo `.git/info/exclude` en `init` y el worktree aislado de análisis dinámico.
- Nunca copiar valores de secretos a ninguna salida ni log.
- **Errores:** mensajes en español con código `NPR-Exxx`, causa y acción sugerida (catálogo en `npr/errors_catalog.py`). Nunca un traceback crudo al usuario salvo con `--verbose`.
- **Logging:** `logs/npr.log`, una línea por evento `ISO-ts NIVEL módulo mensaje`; niveles `DEBUG` (solo `--verbose`), `INFO`, `WARN`, `ERROR`.
- **Multiplataforma:**
  - `pathlib` para todo; rutas en salidas siempre relativas a la raíz del repo y con `/`.
  - Abrir archivos con codificación explícita; detectar BOM; respaldo `errors="replace"`.
  - Conteo de líneas consistente con LF, CRLF y CR; las citas usan la numeración que mostraría un editor.
  - `subprocess` con lista de argumentos, nunca `shell=True`; manejar `git` ausente.
  - Detectar colisiones por mayúsculas/minúsculas, rutas largas en Windows, symlinks y nombres unicode.
  - CI en Linux, macOS y Windows desde F00.

## 18. Convenciones de documentación

- Guías (`references/`) con secciones fijas: **Objetivo · Entradas · Procedimiento paso a paso · Técnicas para casos difíciles · Salida (plantilla) · Checklist de calidad · Errores comunes**.
- Guías por ecosistema: **Dónde empezar · Entry points · Estructura típica · Indirecciones típicas y cómo resolverlas · Configuración · Testing · Build · Trampas**.
- Citas: `[@ruta:inicio-fin]`, `[@ruta:línea]`, `[@ruta:inicio-fin#Símbolo]`, `[@git:sha]`, `[@dyn:id]`.
- Etiquetas: `[V]` verificado leyendo código (con cita) · `[D]` observado ejecutando (con cita dyn) · `[I]` inferido (con "porque…") · `[?]` desconocido (con `OQ-NNN`).
- Diagramas según §9.
- Prohibido: "etc.", "entre otros", "y más", "...", hedging sin etiqueta, secciones vacías, `N/A` sin razón, `TODO`.

## 19. Esquemas clave (resumen)

| Esquema | Campos esenciales |
|---|---|
| `state` | repo, commit, branch, created_at, skill_version, mode, stage, config |
| `inventory-entry` | path, size, sha1, lines, is_binary, ext, encoding, is_symlink, ignored |
| `classification` | path, category, policy (full/skim/metadata/reverse/excluded), reason |
| `dependency` | name, spec, resolved, scope, ecosystem, manifest, line, partial |
| `edge` | from, to, external, kind (static/dynamic/type/reexport/include), line, unresolved_reason |
| `symbol` | name, kind, file, start, end, exported, signature, parent |
| `surface` | id, kind (http/cli/command/message/event/ipc/schema/ws/queue/tool), name, handler, file, line, pair |
| `wu` | id, files[{path, policy, chunks}], neighbors, priority, wave, glossary |
| `ledger-entry` | path, state, by, ts, note_path, reason |
| `open-question` | id, question, context, searched[], hypotheses, status, resolution, needs |
| `feature` | id, name, user_description, entrypoints, modules, flows, config, status |
| `flow` | id, feature, trigger, steps[{n, what, cite, data_in, data_out, boundary}], errors, effects |
| `decision-point` | id, file, line, kind, condition_text, branches[{label, target_line}], mapped_node, justification |
| `outcome` | id, category, conditions, diagram_path, example_inputs, user_sees, user_sees_cite, side_effects, reversible, final_state, logged, recovery, repro, tests |
| `scenario` | id, outcome, given, when, then, existing_tests[], gap |
| `error-entry` | id, type, origin, message, propagation[{layer, action, cite}], handled_at, user_sees, outcome, swallowed |
| `feature-package` | feature, artifacts{nombre: ruta}, counts{outcomes, decisions, errors, scenarios}, tested_outcomes_pct |
| `knowledge` | export completo para `knowledge.json` |

La fuente de verdad son los archivos de `schemas/` (F04, F33).

## 20. Catálogo de reportes (detalle en F66)

| # | Reporte | # | Reporte |
|---|---|---|---|
| 00 | Índice | 14 | Testing |
| 01 | Resumen ejecutivo | 15 | Seguridad |
| 02 | Mapa del repositorio | 16 | Historia y evolución |
| 03 | Stack y dependencias | 17 | Índice de archivos |
| 04 | Arquitectura | 18 | Glosario |
| 05 | Módulos + `modulos/` | 19 | Guía de onboarding |
| 06 | Features + `features/<FEAT>/` (13 artefactos) | 20 | Playbooks de modificación |
| 07 | Flujos + `flujos/` | 21 | Ingeniería inversa (si aplica) |
| 07b | Superficies + `superficies/` | 22 | Preguntas abiertas y limitaciones |
| 08 | Datos y estado | 23 | Cobertura y verificación |
| 09 | Interfaces y protocolos | 24 | Catálogo de errores |
| 10 | Configuración | 25 | Matriz de interacciones entre features |
| 11 | Extensibilidad | 26 | Escenarios y cobertura de resultados |
| 12 | IA, prompts y agentes (si aplica) | 27 | Cambios desde `<sha>` (modo actualizar) |
| 13 | Build, CI y release | — | `respuestas/<slug>.md`, `comparacion-<a>-vs-<b>.md`, `knowledge.json`, `index.html` |

---

## 21. Subagentes dentro de la skill (protocolo de F27)

| Rol | Produce |
|---|---|
| Orquestador | Plan, olas, síntesis de arquitectura, catálogo de features, decisiones de conflicto; no lee el código entero |
| Lector de WU | Fichas de archivo, dossier de módulo, fragmento de ledger |
| Trazador de flujo | Trazas `FL-NNN` |
| Constructor de paquete de feature | Los 13 artefactos de una feature |
| Analista de superficie | Mini-paquetes de superficie |
| Analista transversal | Notas de `notes/cross/` (datos, interfaces, config, extensibilidad, LLM, build, tests, seguridad, historia) |
| Ingeniero inverso | Salidas de `re/` y fichas `reverse` |
| Analista dinámico | Logs de `dyn/` y etiquetas `[D]` |
| Verificador | Veredictos por afirmación (contexto limpio) |
| Resolvedor de preguntas | Resolución o cierre de `OQ-NNN` |
| Redactor de reportes | Secciones narrativas de los reportes |

**Contrato de brief** (lo genera `npr brief`): rol · objetivo · alcance exacto · contexto mínimo
(extracto de `RECON.md`, glosario, interfaces de vecinos) · reglas (enlace a `00-principios.md`) ·
plantilla de salida · rutas donde escribir (exclusivas) · criterios de terminado · qué devolver.

**Contrato de retorno:** archivos escritos · resumen ≤ 20 líneas · fragmento de ledger · OQ nuevas ·
términos nuevos de glosario · sospechas para otros módulos o features.

## 22. Subagentes durante la construcción

- Delega en paralelo las fases que el roadmap marca como paralelizables (Anexo B del roadmap).
- Cada subagente recibe un brief con: fase(s), fragmento del roadmap, secciones relevantes de este archivo, archivos que puede tocar (exclusivos), criterios de aceptación y formato de reporte.
- **Propiedad exclusiva de archivos:** dos subagentes nunca editan el mismo archivo a la vez; los compartidos (`PROGRESS.md`, `DECISIONS.md`, `npr/cli.py`, `config/defaults.json`) los integra el agente principal.
- **Separación de roles:** quien escribe una guía no hace su dry run; quien produce un análisis no lo verifica; quien construye un fixture no valida su ground truth; quien construye la skill nunca genera ni ve el holdout.
- **Dry runs:** el subagente de prueba recibe solo el artefacto indicado y el fixture, nunca el ground truth ni el contexto de quien escribió el artefacto.
- Reporte de un subagente constructor: archivos creados o modificados · comandos ejecutados y salida resumida · criterios cumplidos con evidencia · criterios pendientes · decisiones propuestas (`D-NNN` sugeridas).
- El agente principal integra, ejecuta tests globales y actualiza `PROGRESS.md` y el Relevo.

---

## 23. Fixtures, ground truth y trampas

| Fixture | Para qué existe |
|---|---|
| `fx-ts-agent-extension` | Imita un agente de código tipo VS Code: host + webview, modos con prompts y herramientas, cargador de skills con precedencia, `use_skill`, loop con aprobación, proveedores, MCP simulado, condensación, i18n, archivo > 5.000 líneas |
| `fx-python-cli` | CLI con plugins por entry points, SQLite, config por archivo y entorno, historia git scriptada |
| `fx-java-micronaut` | REST con DI en compilación, cliente HTTP declarativo, entornos en `application.yml`, migraciones |
| `fx-monorepo` | pnpm con Angular (standalone + signals), API Node y librería compartida |
| `fx-minified` | Bundle con y sin sourcemap, `.asar`, `.pyc` |
| `fx-polyglot` | Go + Rust + shell comunicándose por stdin/JSON |

Trampas generales (≥ 3 por fixture): código muerto que parece activo · import dinámico · dispatch por
string · registro de handlers en un mapa · bus de eventos · README que contradice el código · feature
flag que desactiva una feature · nombres engañosos.

Trampas del paquete por feature: resultado de error que solo ocurre con dos settings combinados ·
`catch` vacío que convierte un error en éxito silencioso · timeout con reintento · condición de carrera ·
rama muerta · resultado que solo ocurre cuando el usuario rechaza una aprobación.

Ground truth (`dev/ground-truth/<fixture>/`): `ground_truth.json` (entry points, módulos, dependencias,
features con trazas, superficies, config, prompts, decisiones, resultados `R-NN` con lo que ve el
usuario, errores y propagación, estados, telemetría, mapeo test→resultado, interacciones, grafo de
llamadas, trampas y su resolución), `GROUND_TRUTH.md` y `unique_tokens.txt`.

## 24. Anti-sobreajuste y fixtures reservados (holdout)

1. Prohibido escribir en `skills/` nombres de fixtures, rutas de `dev/`, identificadores, strings o reglas específicas de un fixture. `dev/tools/overfit_guard.py` lo verifica en pytest y CI; las excepciones van en `overfit_allowlist.txt` con su `D-NNN`.
2. Prohibido modificar un ground truth para que un test pase. Solo se corrige con evidencia de que estaba mal, registrada como `D-NNN`.
3. Toda regla de detección debe justificarse por un patrón general del ecosistema (documentación del framework, convención común), no por un fixture.
4. Los fixtures reservados se generan **después** de congelar la skill (tag `v1.0.0-rc<N>`, F82) por un subagente que solo recibe `dev/holdout/SPEC.md`. El constructor nunca los lee.
5. El constructor recibe solo el informe agregado de fallas por categoría. Al corregir, el lote queda "quemado" y se genera uno nuevo para re-evaluar.
6. Los repos reales de validación (F83, F84) también cuentan como no vistos: las preguntas se escriben antes de ejecutar la skill.

## 25. Umbrales de calidad

La fuente única es `dev/evals/thresholds.json`, con su espejo legible en el **Anexo C** del roadmap
(perfiles `dev`, `holdout`, `real`). Resumen del perfil `dev`: cobertura 100 % · citas válidas 100 % ·
recall de features 100 % · precisión de pasos de traza ≥ 95 % · recall de decisiones y de resultados
100 % · 0 resultados inventados · 0 afirmaciones incorrectas en documentos críticos · 0 trampas mal
explicadas · eval ≥ 90 % de puntos clave por pregunta y 0 incorrectos. Ningún criterio de aceptación
puede usar un número distinto al del archivo; relajar un umbral requiere al dueño (§15).

## 26. Testing

- `pytest` sobre `dev/tests/`. Un archivo de test por módulo de `npr/`.
- Tests de esquema: cada salida JSON validada contra su esquema.
- Tests de determinismo: doble ejecución → salidas idénticas.
- Tests de no-modificación: tras cualquier comando, `git status` del fixture queda limpio.
- Tests de redacción: un secreto falso plantado nunca aparece en el workspace ni en logs.
- Tests multiplataforma: CRLF, BOM, UTF-16, unicode, rutas con espacios, colisión de mayúsculas.
- Tests opcionales (tree-sitter, ctags, mmdc, javap…) se saltan con mensaje claro si la herramienta falta.
- Guardianes en cada ejecución: `overfit_guard.py`, `check_thresholds.py`, `validate_skill.py`.
- Evals (etapa 6): preguntas doradas + scorer determinista + juez con rúbrica fija; perfiles `dev`, `holdout`, `real`.

---

## 27. Cómo trabajar con el roadmap

1. Al inicio de cada sesión: §0.2.
2. Elegir la siguiente fase cuyas dependencias estén `HECHA`. Si varias son paralelizables, delegarlas (§22).
3. Marcar la fase `EN CURSO` en `PROGRESS.md`.
4. Implementar **todas** las tareas de la fase. No dejar stubs salvo que el roadmap lo indique.
5. Ejecutar cada criterio de aceptación y pegar la evidencia (comando + salida resumida, rutas, resultados de tests) en `PROGRESS.md`.
6. Antes de cerrar: `python -m pytest`, `python dev/tools/validate_skill.py skills/notemartin-project-review`, `python dev/tools/overfit_guard.py`, `python dev/tools/check_thresholds.py` (estos dos últimos desde F07).
7. Commit y marca `HECHA`; actualizar el Relevo.
8. Si un criterio no se puede cumplir por una razón externa: `BLOQUEADA` con la razón exacta y lo que haría falta.
9. Si una fase posterior demuestra un defecto en una anterior: `REABIERTA`, corregir y volver a pasar sus criterios.

Formato de `PROGRESS.md`:

```
| Fase | Estado | Fecha | Evidencia | Notas |
|---|---|---|---|---|
| F08 | HECHA | 2026-10-06 | pytest dev/tests/test_inventory.py: 18 passed; conteos fixtures = GT | — |
```

**Flujo git del constructor:**
- Rama `main` siempre en verde; una rama por etapa `etapa-<n>` que se integra al cerrar la etapa.
- Commit por fase `F<NN>: <título>` con cuerpo que resume la evidencia; commits intermedios `F<NN> wip: <qué>`.
- Tags: `etapa-<n>-ok` al cerrar cada etapa, `v1.0.0-rc<N>` al congelar para holdout (F82), `v1.0.0` en F87.
- Nunca reescribir historia publicada; nunca commitear `dist/`, workspaces `.project-review/` ni lotes de holdout antes de su generación en F82.
- Las líneas de atribución de commits que exija el entorno de ejecución se respetan.

## 28. Reglas duras para el agente constructor

1. No avanzar de fase sin evidencia de todos los criterios.
2. No reducir el alcance de una fase; si algo parece imposible, `BLOQUEADA` con razón, no un atajo silencioso.
3. No introducir dependencias de runtime fuera de la stdlib sin respaldo.
4. No escribir el ground truth y la skill en el mismo contexto de subagente.
5. No exponer el ground truth a los dry runs ni a los evals; no ver el holdout.
6. No meter lógica específica de fixtures en `skills/` ni ajustar ground truth para pasar tests (§24).
7. No modificar repos analizados (salvo `.git/info/exclude` y worktree de análisis dinámico).
8. No ejecutar código de un repo analizado ni instalar sus dependencias sin permiso explícito del dueño.
9. No copiar secretos a ningún archivo.
10. No poner timelines ni estimaciones de esfuerzo en ningún documento.
11. No simplificar instrucciones de la skill "para modelos más débiles".
12. Toda afirmación sobre runtimes externos (rutas, herramientas, sintaxis de instalación) se verifica con documentación vigente y se cita con fecha (F02, F85, F87).
13. `SKILL.md` siempre ≤ 5k tokens; si crece, mover detalle a `references/`.
14. No usar un número de calidad distinto al de `thresholds.json`.
15. No terminar una sesión sin Relevo actualizado.

## 29. Seguridad, privacidad y ética de la skill

- La skill es de **comprensión** de software: la ingeniería inversa se usa para entender cómo funciona una app, respetando licencias.
- Nada sale de la máquina: los scripts no usan red, y la skill funciona igual con modelos locales. Las herramientas de auditoría de dependencias que consultan bases externas solo se ejecutan con permiso.
- El workspace y los reportes contienen fragmentos del código analizado: tienen la misma confidencialidad que el repo. Para reportes que se van a compartir existe `report.snippets=false`.
- El análisis dinámico requiere permiso, se hace en una copia aislada y se limpia al terminar.
- Los reportes listan nombres de secretos y variables, nunca sus valores.
- La historia git se reporta con conteos agregados de autores, sin emails.

## 30. Borrador inicial del frontmatter de `SKILL.md`

```yaml
---
name: notemartin-project-review
description: >-
  Análisis exhaustivo e ingeniería inversa de un repositorio de software clonado: lee todos los
  archivos, mapea dependencias y arquitectura, descubre cada feature, traza cada flujo de punta a punta
  con citas archivo:línea, genera por feature diagrama de flujo de decisiones y todos los resultados
  posibles, reconstruye prompts, modos y herramientas en apps de IA, y entrega reportes verificados.
  Úsala cuando pidan "analiza este repositorio", "cómo funciona esta app", "explícame el flujo de X",
  "qué pasa en cada caso", "ingeniería inversa de este proyecto", "documenta este repo". Also use for
  "how does this codebase work", "reverse engineer this project", "trace this feature end to end",
  "explain this repo in depth".
version: 0.1.0
license: MIT
metadata:
  hermes:
    tags: [code-analysis, reverse-engineering, architecture, documentation, codebase-understanding]
---
```

(Se ajusta en F72 y se valida con `validate_skill.py`.)

## 31. Glosario

| Término | Definición |
|---|---|
| Skill | Carpeta con `SKILL.md` que un runtime carga bajo demanda según su `description`. |
| Runtime | Hermes Agent, Cline o Kilo Code. |
| `npr` | CLI interna de la skill (notemartin project review). |
| Orquestador | Agente principal que ejecuta la skill y coordina subagentes. |
| Recon | Reconocimiento determinista por scripts. |
| WU | Unidad de trabajo asignada a un subagente lector. |
| Ficha | Nota condensada por archivo. |
| Dossier | Documento completo de un módulo o feature. |
| Traza | Secuencia de saltos citados desde un disparador hasta su efecto. |
| Indirección | Mecanismo donde el destino de una llamada no es visible estáticamente (DI, registro, evento, import dinámico, reflexión, string-dispatch). |
| Prompt reconstruido | System prompt final de un modo, ensamblado fragmento por fragmento con cita y condición. |
| Paquete de feature | Carpeta con los 13 artefactos obligatorios de una feature (§7). |
| Punto de decisión | Lugar del código donde el comportamiento se bifurca, extraído por `npr branches`. |
| Resultado (R-NN) | Desenlace posible de una feature o superficie, con lo que ve el usuario y los efectos que deja. |
| Mini-paquete de superficie | Ficha de un endpoint, comando, mensaje, herramienta o evento con contrato, flujo corto y resultados. |
| Brecha de tests | Resultado posible que ningún test existente del repo cubre. |
| Ledger | Registro de cobertura por archivo. |
| Gate | Comprobación automática que bloquea avanzar (§12). |
| Dry run | Prueba de una guía o plantilla con un subagente de contexto limpio sobre un fixture. |
| Ground truth | Respuestas correctas conocidas de un fixture. |
| Holdout | Fixtures reservados generados tras congelar la skill, nunca vistos por el constructor (§24). |
| Lote quemado | Lote de holdout cuyo contenido influyó en correcciones; ya no sirve para evaluar. |
| Relevo | Sección de `PROGRESS.md` que permite a otro agente continuar el trabajo (§14). |
| OQ | Pregunta abierta del análisis (`OQ-NNN`). |
| Q-NNN | Pregunta del constructor para el dueño del proyecto. |
| D-NNN | Decisión registrada del constructor. |

## 32. Definición de terminado

Ver Anexo A del `ROADMAP.md`. Resumen: F00–F88 `HECHA` con evidencia; tests, validadores y guardianes
en verde con CI en Linux, macOS y Windows; evals sobre umbral en los perfiles `dev`, `holdout` (lote no
quemado) y `real`; validación en Kilo Code y otros repos; probada en los tres runtimes; sin preguntas
abiertas para el dueño; y `docs/INSTRUCCIONES.md` completo y verificado por un subagente que lo sigue al
pie de la letra.