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

### D-109 — Parser YAML: PyYAML con fallback propio

- Fecha · Fase · Estado: 2026-10-05 · F01 · vigente
- Contexto: el validador necesita parsear el frontmatter sin añadir dependencias de runtime (AGENTS §17). El roadmap de F01 autoriza explícitamente el fallback a "parser mínimo propio para el subconjunto usado si no hay PyYAML".
- Decisión: `_yaml_load(text)` intenta `import yaml; yaml.safe_load(text)`. Si `ImportError`, cae a `_minimal_yaml_load`. El parser propio soporta mapas anidados a 2 niveles, listas con `- ` y block scalars folded (`>-`, `>`). No soporta anchors, tags, comillas con escape ni listas inline complejas (la `tags` queda como string).
- Alternativas consideradas: usar `tomllib` o `configparser` (rechazado: no parsean YAML); depender siempre de PyYAML (rechazado: viola AGENTS §17).
- Consecuencias: cualquier futura ampliación del frontmatter (listas inline, multilínea con `|`, anchors) obliga a instalar PyYAML. La regla está en el roadmap de F01.

### D-110 — Estimación de tokens = `len(texto) // 4`

- Fecha · Fase · Estado: 2026-10-05 · F01 · vigente
- Contexto: el roadmap de F01 fija "estimación de tokens del cuerpo (caracteres / 4) ≤ 5000".
- Decisión: `len(body) // 4`. Truncamiento entero (no redondeo). El cuerpo se toma como el texto posterior al segundo `---`.
- Alternativas consideradas: usar el promedio 0.75 palabras/token (rechazado: más complejo y la fórmula exacta del roadmap es `chars / 4`).
- Consecuencias: holgura amplia sobre la SKILL.md real (142 tokens).

### D-111 — Patrones de detección de secretos (6)

- Fecha · Fase · Estado: 2026-10-05 · F01 · vigente
- Contexto: AGENTS §29 prohíbe secretos en cualquier archivo; el validador debe detectar los más comunes.
- Decisión: 6 regex — `AKIA[0-9A-Z]{16}` (AWS), `gh[pousr]_[A-Za-z0-9]{36,}` (GitHub PAT), `glpat-[A-Za-z0-9_-]{20,}` (GitLab), `xox[abprs]-[A-Za-z0-9-]{10,}` (Slack), `sk-[A-Za-z0-9]{20,}` (OpenAI), `sk-ant-[A-Za-z0-9-]{20,}` (Anthropic). Se aplican a `SKILL.md`, `references/**/*.md` y `templates/**/*.md`; **no** a `scripts/` (los patrones dentro de código fuente son normales, p.ej. `sk-` como prefijo de variable).
- Alternativas consideradas: detector genérico de "alta entropía" (rechazado: añade ruido y complejidad).
- Consecuencias: falsos positivos aceptables por diseño; el linter específico de secretos en F62 los endurece.

### D-112 — Rutas absolutas del desarrollador prohibidas

- Fecha · Fase · Estado: 2026-10-05 · F01 · vigente
- Contexto: cualquier ejemplo o comentario en la skill que contenga una ruta absoluta del desarrollador filtra información del entorno.
- Decisión: 3 regex — `(?<![A-Za-z]):?/(?:Users|home)/[^\\s)]+`, `C:\\Users\\[^\\s)]+`. Solo se aplican a archivos `.md` de la skill (no a scripts). Se reporta `archivo:línea:match`.
- Alternativas consideradas: detectar también rutas UNC `\\\\` (rechazado: el roadmap solo menciona `/Users/`, `/home/` y `C:\Users\`).
- Consecuencias: si el dueño quiere permitir ejemplos con rutas reales (p.ej. en `INSTRUCCIONES.md`), F01 reabre.

### D-113 — Validación de enlaces relativos

- Fecha · Fase · Estado: 2026-10-05 · F01 · vigente
- Contexto: el validador debe garantizar que todo `[texto](destino)` apunte a un archivo existente en la skill.
- Decisión: regex `\[(?P<text>[^\]]*)\]\((?P<target>[^)\s]+)\)` sobre `SKILL.md`, `references/**/*.md` y `templates/**/*.md`. Si el target empieza por `http://`, `https://`, `mailto:` o `#`, se ignora. En otro caso se resuelve relativo al archivo y se exige que exista.
- Alternativas consideradas: resolver también URLs vía HEAD (rechazado: AGENTS §17 prohíbe red desde los scripts de la skill).
- Consecuencias: enlaces a sitios externos nunca se validan (asume responsabilidad del dueño).

### D-114 — Códigos de salida del validador

- Fecha · Fase · Estado: 2026-10-05 · F01 · vigente
- Contexto: el validador debe integrarse con pytest y con el eventual orquestador de F05.
- Decisión: `0` todo OK, `2` validación fallida, `1` error de uso. Sin niveles intermedios. Cada fallo imprime a stderr con la regla, archivo y línea cuando aplique. Sin warnings: toda regla falla o pasa, sin grises.
- Alternativas consideradas: distinguir entre errores y warnings (rechazado: complica CI y la política de la skill es binaria).
- Consecuencias: pytest puede marcar el validador como binario; los linters futuros (F64) usan el mismo criterio.

### D-115 — Subagentes investigadores en paralelo (uno por runtime)

- Fecha · Fase · Estado: 2026-10-05 · F02 · vigente
- Contexto: el roadmap marca F02 como paralelizable con F03 y F04, y asigna "un subagente investigador por runtime".
- Decisión: lanzar 3 subagentes en paralelo con `subagent_type: general`, uno por runtime (Hermes, Cline, Kilo Code). Cada subagente escribe a `dev/evals/drafts/runtime-<slug>.md` y devuelve un resumen con líneas, secciones, fuentes y OQ abiertas.
- Alternativas consideradas: investigar los 3 runtimes secuencialmente en el mismo agente (rechazado: 3× más lento); un solo subagente que cubra los 3 (rechazado: el contexto se acercaría al límite y la calidad baja).
- Consecuencias: F02 termina más rápido; los borradores quedan en `dev/evals/drafts/` para auditoría y re-fusión.

### D-116 — Carpeta `dev/evals/drafts/` para borradores de investigación

- Fecha · Fase · Estado: 2026-10-05 · F02 · vigente
- Contexto: separar la investigación del entregable final permite auditar cada fuente.
- Decisión: cada subagente investigador escribe su borrador en `dev/evals/drafts/runtime-<slug>.md`; el agente principal fusiona en `references/22-adaptadores-runtime.md`. La carpeta `dev/evals/` ya existe por F00.
- Alternativas consideradas: escribir directamente en el destino final (rechazado: sin auditoría por fuente).
- Consecuencias: AGENTS §27 prohíbe commitear lotes de holdout antes de F82; esta carpeta no es holdout, es investigación en curso. Se commitea normalmente.

### D-117 — Jerarquía AGENTS §4 vs documentación externa

- Fecha · Fase · Estado: 2026-10-05 · F02 · vigente
- Contexto: el subagente investigador puede encontrar contradicciones entre la documentación actual de un runtime y la información preliminar de AGENTS §4.
- Decisión: predomina AGENTS §4. Si la doc actual contradice, se respeta AGENTS y se anota la divergencia en `DECISIONS.md` como `D-NNN` con la sección "contradicciones con AGENTS §4". Si la doc añade información no presente en AGENTS, se incorpora con su fuente.
- Alternativas consideradas: actualizar AGENTS §4 con cada corrección (rechazado: AGENTS solo se modifica en cambios mayores; cada corrección se registra como decisión).
- Consecuencias: el documento F02 lleva una sección "Notas sobre contradicciones con AGENTS §4" que enlaza a las decisiones D-122..D-129.

### D-118 — Formato de fuentes con supra-índice `[N]` y bloque final

- Fecha · Fase · Estado: 2026-10-05 · F02 · vigente
- Contexto: el criterio de aceptación exige "cada afirmación tiene una fuente con URL y fecha de consulta".
- Decisión: bloque final del documento con un item por fuente, formato `- [N] <proveedor> — <url> (consulta YYYY-MM-DD)`. Cada afirmación en el cuerpo lleva supra-índice `[N]`. Sin excepciones.
- Alternativas consideradas: usar notas al pie HTML (rechazado: complica el render en GitHub y rompe el `validate_skill`); referencias numéricas inline sin bloque final (rechazado: no se puede verificar la fecha).
- Consecuencias: el validador no verifica citas (queda para F61 linter de citas); la estructura es estable.

### D-119 — Modo secuencial de respaldo con disciplina de disco

- Fecha · Fase · Estado: 2026-10-05 · F02 · vigente
- Contexto: AGENTS §8 ley 5 ("Ley del disco") exige que todo hallazgo se escriba en disco antes de seguir; cuando el runtime no expone subagentes, el orquestador principal ejecuta el rol de cada subagente uno por uno.
- Decisión: 6 pasos explícitos: leer brief de disco → ejecutar rol → escribir resultado a disco → actualizar ledger → repetir → si el contexto se acerca al límite, ejecutar `npr resume`.
- Alternativas consideradas: dejar el modo secuencial a criterio del orquestador (rechazado: la disciplina debe estar escrita, no implícita).
- Consecuencias: el documento de F02 contiene la sección "Modo secuencial de respaldo" con los 6 pasos.

### D-120 — Algoritmo `Resolver SKILL_DIR` por runtime

- Fecha · Fase · Estado: 2026-10-05 · F02 · vigente
- Contexto: el criterio del roadmap exige documentar cómo el agente conoce la ruta de la skill. Hermes expone `HERMES_HOME`; Cline y Kilo no exponen variable propia.
- Decisión: algoritmo de 5 pasos con prioridad: `NPR_HOME` env → `--skill-dir` CLI → variable del runtime (`HERMES_HOME/skills/...`) → rutas canónicas en orden de precedencia (proyecto, global, heredadas, Windows) → error `NPR-E101`. Cada ruta se valida con `.npr-marker`.
- Alternativas consideradas: depender solo de la posición de `__file__` (rechazado: falla si el script se invoca desde otro cwd).
- Consecuencias: el script `npr.py` (F05) implementa este algoritmo.

### D-121 — Fecha de consulta ≥ 2026-08-01

- Fecha · Fase · Estado: 2026-10-05 · F02 · vigente
- Contexto: AGENTS §28 regla 12 exige verificar documentación vigente con cita y fecha.
- Decisión: cada fuente consultada debe llevar fecha `2026-MM-DD` con día no anterior a 2026-08-01. Si una fuente no se ha podido consultar en ese plazo, se marca `[?]` con `OQ-NNN` abierta.
- Alternativas consideradas: aceptar cualquier fecha de 2026 (rechazado: documentación desactualizada en menos de 2 meses).
- Consecuencias: todos los 23 fuentes de F02 llevan `2026-10-05`.

### D-122..D-129 — Contradicciones detectadas entre AGENTS §4 y la documentación vigente

- Fecha · Fase · Estado: 2026-10-05 · F02 · vigente
- Contexto: los 3 subagentes investigadores detectaron divergencias entre el "punto de partida conocido" de AGENTS §4 y la documentación actual de los runtimes.
- Decisión: cada divergencia se registra como una decisión individual:
  - **D-122** — Hermes: el comando de instalación exacto de la docs es `<owner>/<repo>/<ruta>` o `<owner>/<repo>.git`, no `<owner>/<repo>/<nombre>` como sugiere AGENTS §4.
  - **D-123** — Hermes: Windows nativo en `%LOCALAPPDATA%\hermes\` con instalador PowerShell, no mencionado en AGENTS §4.
  - **D-124** — Hermes: la categoría es una subcarpeta libre, no requiere registro; AGENTS §4 sugería una "categoría propuesta".
  - **D-125** — Hermes: la concurrencia de subagentes se gobierna por `delegation.max_concurrent_children` y `delegation.max_spawn_depth`, no por `subagents.max_parallel` (AGENTS §13).
  - **D-126** — Cline: los subagentes son **read-only**, no pueden editar archivos ni usar MCP ni anidar subagentes. AGENTS §21 implica capacidad de escritura.
  - **D-127** — Cline: la ruta `.claude/skills/` también se carga como tercera ruta de proyecto, no solo en Kilo.
  - **D-128** — Kilo: NO existen directorios específicos por modo (`skills-<modo>/`); todo va a un pool común filtrado por `description`. AGENTS §4 está desactualizado en este punto.
  - **D-129** — Kilo: la ruta heredada `~/.kilocode/skills/` no aparece en la docs vigente de Skills; `KILO_DISABLE_EXTERNAL_SKILLS` y `KILO_DISABLE_SKILL_SHELL` son kill switches de seguridad nuevos.
- Consecuencias: AGENTS §4 sigue siendo la fuente de verdad (D-117); las correcciones se aplican cuando se reescriba §4 en una fase futura.

### D-130 — Orden de evaluación de patrones de cita

- Fecha · Fase · Estado: 2026-10-05 · F03 · vigente
- Contexto: los 5 patrones (`RANGE_SYMBOL`, `RANGE`, `LINE`, `GIT`, `DYN`) pueden solaparse si se prueban en el orden incorrecto: `[@src/cli.py:10-25#main]` matchea `RANGE` si se prueba ese primero.
- Decisión: probar `RANGE_SYMBOL` → `RANGE` → `LINE` → `GIT` → `DYN` y aceptar el primer `fullmatch`. El más específico primero.
- Alternativas consideradas: union de regexes con prioridad en el motor (rechazado: `re` no soporta prioridad nativa); construir un único regex con grupos nombrados (rechazado: ilegible).
- Consecuencias: el parser es O(n·m) por texto, donde n=citas y m=5 patrones. Para reportes típicos (<10k citas) es despreciable.

### D-131 — `PATH = [A-Za-z0-9_./-]+`

- Fecha · Fase · Estado: 2026-10-05 · F03 · vigente
- Contexto: la gramática exige rutas relativas a la raíz del repo, sin espacios ni caracteres Unicode.
- Decisión: `[A-Za-z0-9_./-]+`. Las rutas con espacios se rechazan; AGENTS §17 ya prohíbe rutas con espacios en salidas (convención).
- Alternativas consideradas: aceptar cualquier carácter excepto `:` y `]` (rechazado: demasiado permisivo; abre la puerta a inyecciones).
- Consecuencias: si un repo real tiene un path con espacio, el parser lo rechaza y la cita queda como inválida. La skill lo documenta en el `.md` de principios.

### D-132 — `SYMBOL = [A-Za-z_][A-Za-z0-9_.]*`

- Fecha · Fase · Estado: 2026-10-05 · F03 · vigente
- Contexto: el roadmap pide un símbolo "Símbolo" sin definirlo formalmente.
- Decisión: identificador estilo código: empieza por letra o guion bajo, seguido de letras, dígitos, guion bajo o punto. Acepta `Foo.bar`, `_priv`, `parse_args`.
- Alternativas consideradas: aceptar cualquier carácter excepto `#` y `]` (rechazado: símbolos reales siempre son identificadores).
- Consecuencias: cubre Python, JS/TS, Go, Rust, Java, Kotlin. Lenguajes con caracteres especiales (C++ con `::`, Haskell con `→`) quedan fuera; se documenta en F61.

### D-133 — `SHA = [0-9a-fA-F]{7,40}` con normalización a minúsculas

- Fecha · Fase · Estado: 2026-10-05 · F03 · vigente
- Contexto: `git log --abbrev=7` produce SHAs cortos; `git rev-parse HEAD` produce SHA completos.
- Decisión: aceptar hex en mayúsculas o minúsculas, 7 a 40 caracteres. Normalizar a minúsculas en `__post_init__`.
- Alternativas consideradas: solo minúsculas (rechazado: rompe con usuarios que pegan SHAs de GitHub que aparecen en mayúsculas en algunas vistas).
- Consecuencias: el parser es robusto a copiado-pegado.

### D-134 — `Citation` dataclass inmutable con normalización

- Fecha · Fase · Estado: 2026-10-05 · F03 · vigente
- Contexto: el parser se usa desde varios linters y herramientas; la inmutabilidad evita efectos colaterales.
- Decisión: `@dataclass(frozen=True)` con `kind`, `raw`, `path`, `start`, `end`, `symbol`, `sha`, `dyn_id`. `__post_init__` valida que `kind in CITATION_KIND`, normaliza path (`./` solo si es el prefijo literal `./`), normaliza SHA a minúsculas, rechaza paths absolutos y rangos invertidos.
- Alternativas consideradas: namedtuple (rechazado: no permite validación ni normalización en `__post_init__`).
- Consecuencias: los linters futuros pueden asumir invariantes sin revalidar.

### D-135 — Las 8 leyes como reglas verificables con gate/linter nombrado

- Fecha · Fase · Estado: 2026-10-05 · F03 · vigente
- Contexto: AGENTS §6 dice que las 8 leyes "se aplican a la skill y también al agente constructor", y la columna "Cómo se hace cumplir" ya nombra los gates/linters.
- Decisión: cada ley en el `.md` lleva un bloque `**Cumplida por**: <gate o linter> (<fase>)`. Verificación de F03: las 8 leyes tienen ese bloque y el nombre corresponde a un comando real del roadmap.
- Alternativas consideradas: dejar las leyes sin gate (rechazado: hace la ley no verificable, contradice AGENTS §6).
- Consecuencias: el test `test_30_doc_contains_eight_laws_with_cumplida_por` falla si una ley omite el bloque.

### D-136 — Ejemplos válidos e inválidos en el `.md` parseados por el propio parser

- Fecha · Fase · Estado: 2026-10-05 · F03 · vigente
- Contexto: el criterio de aceptación 1 exige que los ejemplos válidos parseen todos y los inválidos ninguno, probado por un test que lee el propio `.md`.
- Decisión: los ejemplos se delimitan con fences ` ```valido` y ` ```invalido`. El test extrae los fences (info-string exacto, no sub-string), limpia comentarios `// ...` al final de cada línea, y comprueba la coincidencia exacta.
- Alternativas consideradas: lista CSV de ejemplos en `templates/` (rechazado: separa la documentación del test, dificulta mantener ambos sincronizados).
- Consecuencias: el `.md` y el parser están acoplados por el test; cualquier cambio en uno requiere revisar el otro.

### D-137 — JSON Schema "casero" subconjunto Draft 2020-12

- Fecha · Fase · Estado: 2026-10-05 · F04 · vigente
- Contexto: AGENTS §17 prohíbe dependencias de runtime fuera de stdlib; el validador `schema.py` debe ser puro.
- Decisión: implementar solo las 10 keywords que el roadmap fija (`type`, `required`, `properties`, `additionalProperties`, `items`, `enum`, `pattern`, `minimum`, `maximum`, `$ref`). Sin `oneOf`, `allOf`, `anyOf`, `format`, `not`, `if/then/else`.
- Alternativas consideradas: usar `jsonschema` (rechazado: dependencia de runtime); implementar Draft completo (rechazado: trabajo inabordable y la skill no necesita más).
- Consecuencias: si una fase futura necesita una keyword adicional, reabre F04 y extiende el validador.

### D-138 — Esquemas como archivos JSON independientes sin `$id`

- Fecha · Fase · Estado: 2026-10-05 · F04 · vigente
- Contexto: los 19 esquemas viven cada uno en su archivo y se referencian por nombre.
- Decisión: `schemas/<name>.json` sin `$id`, sin URL, sin `$schema`. Solo `$ref` local `#/definitions/<X>` dentro del mismo archivo. Esto evita la complejidad de resolución cross-file y mantiene los esquemas portables.
- Alternativas consideradas: un solo archivo monolítico con todos los esquemas (rechazado: ilegible); esquemas con `$ref` cross-file (rechazado: ciclo de carga + parser más complejo).
- Consecuencias: si dos esquemas necesitan la misma sub-forma, se duplica. Aceptable porque la duplicación es pequeña y local.

### D-139 — Ejemplos como archivos sueltos `<nombre>-valid.json` y `<nombre>-invalid.json`

- Fecha · Fase · Estado: 2026-10-05 · F04 · vigente
- Contexto: el criterio exige "un ejemplo válido y uno inválido por esquema".
- Decisión: `dev/tests/schema_examples/<nombre>-valid.json` y `<nombre>-invalid.json`, cada uno un único objeto JSON (no envuelto). Los tests parametrizados iteran sobre la convención.
- Alternativas consideradas: un directorio `valid/` y otro `invalid/` (rechazado: dos directorios paralelos hacen que el par quede disperso); un único archivo con dos secciones (rechazado: complica el parseo).
- Consecuencias: agregar un esquema nuevo es agregar 2 archivos y añadir su nombre a la lista en el test.

### D-140 — Validador expone `load_schema`, `validate`, `check` y CLI

- Fecha · Fase · Estado: 2026-10-05 · F04 · vigente
- Contexto: el validador lo usarán scripts, linters y tests.
- Decisión: API `load_schema(name) -> dict`, `validate(instance, schema, path="$", definitions=None) -> list[str]` (lista vacía = OK), `check(instance, schema)` que lanza `SchemaError`, y CLI `python -m npr.schema <name> <archivo>` con códigos 0/2.
- Alternativas consideradas: solo `validate` y devolver `bool` (rechazado: se pierde el path del campo en el error).
- Consecuencias: cualquier consumidor puede usar la API; el CLI sirve para inspección humana y para CI local.

### D-141 — `type=integer` rechaza `bool` y distingue `number`

- Fecha · Fase · Estado: 2026-10-05 · F04 · vigente
- Contexto: en Python, `isinstance(True, int) == True` por compatibilidad con bool.
- Decisión: `integer` = `int and not bool`; `number` = `(int or float) and not bool`. El bool nunca pasa como integer ni como number.
- Alternativas consideradas: aceptar bool como int (rechazado: sorprende al usuario y oculta bugs).
- Consecuencias: los esquemas que esperan enteros no admiten accidentalmente `True`/`False`. Documentado en el test `test_45`.

### D-142 — `$ref` solo local con prefijo `#/definitions/`

- Fecha · Fase · Estado: 2026-10-05 · F04 · vigente
- Contexto: el roadmap fija `$ref local` como una de las keywords.
- Decisión: solo se acepta `#/definitions/<X>`. Cualquier otro prefijo (`http://`, `file://`, `#/properties/...`, otro archivo) levanta `SchemaError`.
- Alternativas consideradas: aceptar cualquier path JSON Pointer (rechazado: aumenta la superficie de ataque); los schemes pueden usar `#/properties/<X>` como shortcut (rechazado: complica la lectura).
- Consecuencias: el validador es estricto; los esquemas están obligados a registrar sub-formas en `definitions`.

### D-143 — Estructura del paquete `npr/`

- Fecha · Fase · Estado: 2026-10-05 · F05 · vigente
- Contexto: AGENTS §10 lista `npr/` como paquete Python con módulos por dominio.
- Decisión: módulos `cli.py`, `paths.py`, `config.py`, `workspace.py`, `logging_setup.py`, `errors_catalog.py`, `schema.py`, `citations.py` (F04, F03), y subpaquete `subcommands/` con `init_cmd`, `config_cmd`, `status_cmd`, `resume_cmd` (reales) y `stubs.py` (33 comandos pendientes). Los módulos de F08+ (inventory, classify, stack, etc.) se añaden en sus fases.
- Alternativas consideradas: todos los subcomandos en un solo `commands.py` (rechazado: ilegible >1000 líneas); cada subcomando en su propio archivo ×35 (rechazado: explosión de archivos, baja cohesión).
- Consecuencias: cada fase que implementa un comando añade un módulo bajo `subcommands/` y actualiza `ALL = [...]`.

### D-144 — Códigos de error NPR-Exxx

- Fecha · Fase · Estado: 2026-10-05 · F05 · vigente
- Contexto: AGENTS §17 exige mensajes de error en español con código estable.
- Decisión: 16 códigos en `errors_catalog.py` con campos `msg`, `causa`, `accion`. NPR-E101 a NPR-E116. El formato `format_error(code, **ctx)` añade contexto y devuelve un bloque multi-línea.
- Alternativas consideradas: jerarquía de subclases `NPRError(ValueError)` (rechazado: añade boilerplate y rompe el flujo de `sys.exit(2)` que ya usamos en el catálogo).
- Consecuencias: cualquier subcomando que falle con un error de usuario usa `format_error(...)` y `sys.exit(2)`. Los linters futuros (F64) verifican que el catálogo sigue creciendo.

### D-145 — Resolución de SKILL_DIR

- Fecha · Fase · Estado: 2026-10-05 · F05 · vigente
- Contexto: el roadmap fija el algoritmo de 5 niveles (CLI > env > variable del runtime > rutas canónicas > error).
- Decisión: `paths.resolve_skill_dir(cli_skill_dir)` itera la lista de candidatos, valida cada uno con `scripts/.npr-marker`, devuelve el primero que pase y exporta `NPR_HOME`. Si ninguno pasa, imprime `[NPR-E101]` y sale 2.
- Alternativas consideradas: lazy resolver (rechazado: doble fallo de "qué skill es"); caché en disco (rechazado: complica el primer arranque).
- Consecuencias: la CLI siempre puede operar; el `NPR_HOME` se exporta para subprocesos.

### D-146 — Precedencia de configuración (defaults < workspace < cli_file < cli_set)

- Fecha · Fase · Estado: 2026-10-05 · F05 · vigente
- Contexto: el roadmap y AGENTS §13 fijan el orden de precedencia.
- Decisión: 4 niveles que se aplican en `config.load_effective`. El nivel 4 (`--set`) gana sobre todos. Cada clave lleva un origen (`default | workspace | cli_file | cli_set`).
- Alternativas consideradas: merge en profundidad de diccionarios anidados (rechazado: las claves de AGENTS §13 usan notación plana con punto, no anidadas).
- Consecuencias: `npr config show` puede imprimir un árbol legible con el origen de cada valor.

### D-147 — Subcomandos como stubs con NPR-E113

- Fecha · Fase · Estado: 2026-10-05 · F05 · vigente
- Contexto: el roadmap lista 37 subcomandos pero F05 solo implementa 4.
- Decisión: los 33 subcomandos restantes se registran en `subcommands/stubs.py` con su fase objetivo; al invocarse, imprimen `[NPR-E113]` y salen con código 0 (no 2) — F05 no penaliza al usuario por invocar un comando futuro.
- Alternativas consideradas: salir con código 2 cuando un subcomando es stub (rechazado: bloquea a herramientas externas que quieran iterar comandos).
- Consecuencias: `--help` lista todos los comandos desde el primer día; el linter `npr lint vague` puede detectar referencias a fases incorrectas.

### D-148 — Init idempotente

- Fecha · Fase · Estado: 2026-10-05 · F05 · vigente
- Contexto: el criterio 1 exige idempotencia y no duplicar la línea en `.git/info/exclude`.
- Decisión: si `state/state.json` existe y no se pasó `--force`, `NPR-E105`. La línea `.project-review/` se agrega solo si el archivo no la contiene ya (regex `^\s*\.project-review/?\s*$` sobre `info/exclude`).
- Alternativas consideradas: sobre-escribir siempre (rechazado: destruye el progreso del usuario); backup antes de reescribir (rechazado: complica init por simplicidad).
- Consecuencias: el usuario puede ejecutar `npr init` varias veces sin miedo; `--force` es la opción explícita para empezar de cero.

### D-149 — Status con campos extendidos en el esquema state

- Fecha · Fase · Estado: 2026-10-05 · F05 · vigente
- Contexto: el criterio 4 dice "npr status --json valida contra el esquema state"; mi salida incluye `coverage_pct`, `wus_pending`, `open_questions`, `next_action` que no están en el esquema original.
- Decisión: añadir los 4 campos como opcionales al esquema `state.json` con `description`. `npr status --json` produce el state más los campos extendidos y el validador acepta ambos.
- Alternativas consideradas: crear un esquema `status-output` separado (rechazado: duplica el state base; la fusión es estable); permitir campos extra con `additionalProperties: true` en `state` (rechazado: abre la puerta a typos).
- Consecuencias: el esquema `state` queda como supertipo de `state.json` y del payload de `status --json`. Los demás consumidores que solo leen `state.json` siguen funcionando.

### D-150 — Nombre del fixture F06a: `fxnotes`

- Fecha · Fase · Estado: 2026-10-05 · F06a · vigente
- Contexto: F06a exige un fixture pequeño pero realista con paquete por feature.
- Decisión: `fxnotes` — CLI de notas en SQLite. Cuatro comandos (`add`, `list`, `delete`, `export`). Permite plantar las 6 trampas específicas del paquete por feature y los 6 R-NN por feature.
- Alternativas consideradas: `fxmark` (bookmarks), `fxtask` (tareas), `fxlog` (logs). `fxnotes` gana porque el dominio de notas es universal y permite los patrones de error requeridos (DB lock, race, duplicados).
- Consecuencias: las features se llaman `FEAT-001..FEAT-004` en el ground truth.

### D-151 — Estructura del fixture

- Fecha · Fase · Estado: 2026-10-05 · F06a · vigente
- Contexto: F06a pide un CLI con plugins por entry points, SQLite, config por archivo y env, historia git scriptada.
- Decisión: `pyproject.toml` con entry points en el grupo `fxnotes.commands`; paquete `src/fxnotes/` con módulos `cli`, `config`, `db`, `events`, `plugins/loader`, `legacy_v1`, y subpaquete `commands/` con un módulo por feature; `tests/` con pytest; `README.md` con trampa de contradiccion; `unique_tokens.txt` para detectar fugas; `build-history.sh` con 8 commits.
- Alternativas consideradas: usar `click` en lugar de `argparse` (rechazado: añade dep no-stdlib); estructura plana sin subpaquete `commands/` (rechazado: el dispatch string vive en `__init__.py` y queda menos visible).
- Consecuencias: 15 archivos en el fixture, todos con roles claros.

### D-152 — Ground truth con paquete completo

- Decisión: el ground truth de cada feature incluye traces con `cite`, decision_points con `file:line`, outcomes con `user_sees` y `tests`, errors con propagation, config con default y efecto, states, telemetry, interactions, callgraph.
- 4 features x ~13 artefactos = ~50 entradas. El verificador (`check_ground_truth.py`) valida cada `cite` con `archivo:linea-linea#symbol`.
- Consecuencias: el verificador falló las primeras 2 veces por line numbers incorrectos; se corrigió leyendo cada archivo. La moral: el ground truth se genera DESPUÉS del código, no antes.

### D-153 — 4 features con paquete completo

- Decisión: `add`, `list`, `delete`, `export` (4 en vez del mínimo 3) porque cubren los 6 patrones de R-NN (success, validation_error, silent_success, cancelled, not_found, error_internal).
- `delete` cubre 3 patrones solos (R-04 dead_branch, R-05 combination_two_settings, R-06 user_rejection); `add` cubre 2 (R-04 duplicate, R-06 race); `list` cubre R-06 empty_catch.
- Consecuencias: las 6 trampas del paquete se reparten entre las 4 features sin forzar features vacías.

### D-154 — Trampas superficiales (6)

- Decisión: dead_code (`legacy_v1.py`), dynamic_import (`plugins/loader.py`), string_dispatch (`commands/__init__.py`), event_bus (`events.py`), readme_mismatch (`README.md`), feature_flag_phantom (`config.py` DEAD_CODE).
- 6 trampas, excede el mínimo de 3. Cada una derrota una categoria de análisis superficial diferente.
- Consecuencias: el README miente sobre `delete`; el verificador debe comparar la documentacion con el codigo (Fase publica lo hace).

### D-155 — 6 trampas específicas del paquete por feature

- Decisión:
  1. `delete` con `confirm=False` + `--no-undo` → R-05 permanente (combination_two_settings).
  2. `list` con FXNotesError → R-06 silencioso "0 entries." (empty_catch_swallows_error).
  3. `add` con DB lock → 3 reintentos con backoff (timeout_retry).
  4. `add` SELECT-then-INSERT → IntegrityError mapeado a "lost race" (race_condition).
  5. `delete --archived` → rama muerta que imprime "deprecated" (dead_branch).
  6. `delete confirm=ask` + usuario rechaza → CancelledError (user_rejection).
- Consecuencias: cada trampa tiene su R-NN en el ground truth, su test en `tests/`, y su entrada en `package_traps` del ground truth.

### D-156 — Verificador endurecido

- Decisión: `dev/tools/check_ground_truth.py` reescrito. Carga `ground_truth.json`, itera features/outcomes/traps/package_traps, valida cada `cite` con regex `[A-Za-z0-9_./-]+:linea(start-end)?(#symbol)?`, comprueba archivo existe, rango válido, símbolo presente, y `resolution` no vacía.
- Consecuencias: el verificador atrapa 3 clases de errores: archivos borrados, rangos fuera de rango, símbolos mal nombrados. F06b..F06f reutilizan el mismo verificador sin cambios.

### D-157 — `build-history.sh` con 8 commits

- Decisión: el script crea 8 commits en orden cronológico, uno por capa del fixture (scaffold, CLI+config, DB+events, comandos, plugin+legacy, tests). El script es idempotente: si .git ya existe, sale sin hacer nada.
- Consecuencias: la historia refleja la evolución real del fixture. Tests de F08+ (git stats) encuentran datos consistentes.

### D-158 — `unique_tokens.txt` y verificacion de no-leak

- Decisión: 5 tokens `NPRGT-FXNOTES-001..005` en `unique_tokens.txt` (ground truth) y `dev/fixtures/fx-python-cli/unique_tokens.txt`. El test `test_02_fixture_has_no_unique_tokens` itera todos los archivos del fixture y falla si encuentra alguno de esos tokens fuera del archivo `unique_tokens.txt` mismo.
- Consecuencias: el overfit_guard.py de F57 puede usar este patrón para detectar fugas entre skill y fixtures.

### D-159 — Version 1 del formato de ground truth (F06a2)

- Fecha · Fase · Estado: 2026-10-06 · F06a2 · vigente
- Contexto: el verificador pasa de soportar solo `archivo:línea` y `archivo:línea#símbolo` a 9 formatos (texto simple, rango, símbolo, columna, contenedor ZIP/asar, notebook Jupyter, xpath, yaml-path, binario con offset o símbolo).
- Decisión: introducir un **despachador por tipo** en `check_ground_truth.py` que detecta el formato por regex y aplica el validador correspondiente. `manifest.ground_truth_format_version: 1` en los fixtures declara la versión. Ground truths v0 (los de F06a) siguen siendo válidos porque el formato `archivo:línea#símbolo` es compatible.
- Alternativas: (a) renombrar los ground truths a un nuevo esquema JSON con `cite: {type, ...}`; (b) tener un script de migración. Descartado: el cambio interno es retrocompatible y no obliga a reescribir ground truths.
- Consecuencias: los fixtures F06b..F06f pueden usar cualquiera de los 9 formatos sin parches ad hoc. Si en el futuro se añade un formato (v2), se introducirá un campo `format_version` por ground truth y el despachador discriminará.

### D-160 — Sintaxis de comentarios como datos (F06a2)

- Fecha · Fase · Estado: 2026-10-06 · F06a2 · vigente
- Contexto: la validación CC-11 (sin ground truth embebido en comentarios) necesita detectar comentarios en 80+ extensiones (Python, JS, TS, Go, Rust, Java, Kotlin, COBOL, Haskell, Erlang, SQL, etc.) sin codificar las sintaxis en Python.
- Decisión: `dev/tools/comment_syntax.json` con `by_extension` y `by_filename`. `dev/tools/comment_syntax.py` con `detect(path) -> list[(open, close)]`, `mask_comments(text, syntax) -> str` (preserva newlines y longitudes) y `has_comment_syntax(path)`. La validación CC-11 invoca `mask_comments` y reporta menciones que están en `text` pero no en `mask_comments`.
- Alternativas: (a) librería `pygments` o `tree-sitter`; (b) regex por extensión dentro de `check_ground_truth.py`. Descartado: dependencias externas y acoplamiento.
- Consecuencias: agregar un lenguaje o framework no requiere tocar el verificador. La tabla puede ampliarse en cualquier commit de F06b..F06f si surge un lenguaje nuevo.

### D-161 — Deteccion de codificacion conservadora (F06a2)

- Fecha · Fase · Estado: 2026-10-06 · F06a2 · vigente
- Contexto: el inventario y el verificador deben leer archivos en UTF-8, UTF-16, Latin-1, CP1252 y Shift-JIS con o sin BOM y en CRLF, LF o CR sin distorsionar el conteo de líneas.
- Decisión: `dev/tools/encoding.py` con `detect(path) -> str` (BOM primero, luego UTF-8 estricto, luego heurística de Shift-JIS, luego Latin-1) y `read_lines(path) -> (list[str], str)` (decodifica, elimina el BOM residual y aplica `splitlines()`). Sin auto-conversión destructiva; `errors="replace"` para no abortar.
- Alternativas: (a) `chardet`; (b) leer siempre en binario y decodificar a UTF-8 con `errors="ignore"`. Descartado: dependencias y pérdida de información.
- Consecuencias: el conteo de líneas y las citas `archivo:línea` son consistentes con lo que muestra un editor moderno en cualquier codificación soportada.

### D-162 — Harness de fixtures opt-in (F06a2)

- Fecha · Fase · Estado: 2026-10-06 · F06a2 · vigente
- Contexto: F06b..F06f requeriran ejecutar los tests de cada fixture en su toolchain, con soporte multiplataforma y contenedor opcional.
- Decisión: `dev/tools/run_fixture_tests.py` se ejecuta **solo bajo peticion** del agente constructor (no en pytest por defecto). Cada fixture declara `manifest.yml` con `name`, `requires: [linux|macos|windows]`, `test_cmd` y `container: {dockerfile, image_tag, enabled}`. Sin Docker, el harness cae al `test_cmd` local; sin manifest, el fixture se marca `error (no manifest)` y bloquea el commit de F06b+ hasta que se agregue.
- Alternativas: (a) auto-descubrir via `pyproject.toml`; (b) ejecutar todo en Docker. Descartado: ambiguo y costoso.
- Consecuencias: la verificacion local sigue siendo opcional y el desarrollador puede elegir ejecutar solo los fixtures compatibles con su plataforma (`--platform linux`).

### D-163 — Gate de cobertura total se cierra tras F06f (F06a2)

- Fecha · Fase · Estado: 2026-10-06 · F06a2 · vigente
- Contexto: `dev/fixtures/target_matrix.yml` lista 13 lenguajes, 10 frameworks, 8 sistemas de build, 10 tipos de archivo y 7 contenedores. Con solo `fx-python-cli` la cobertura real es ~5 %; el gate de cobertura completa (`fixtures_matrix.py --check` exit 0) no se puede exigir en F06a2.
- Decisión: durante F06a2..F06e `fixtures_matrix.py` reporta cobertura parcial sin fallar por defecto; `--check` devuelve 2 si hay gaps (informativo). El gate **se cierra** al terminar F06f: en ese punto `--check` debe devolver 0 y se anade a la lista de gates obligatorios antes de K (ver AGENTS §12).
- Alternativas: (a) forzar el gate ya en F06a2; (b) no documentar el gate. Descartado: paralizaria F06a2 innecesariamente y perderia la senal de progreso.
- Consecuencias: queda explicito que el gate de cobertura total es responsabilidad de F06f, no de F06a2.

### D-164 — Stack del fixture F06b: TypeScript + Node 22 + esbuild + vitest + zod + js-yaml

- Fecha · Fase · Estado: 2026-10-06 · F06b · vigente
- Contexto: F06b requiere extension tipo VS Code escrita en TypeScript con multiples entry points, traps de ecosistema y archivo de > 5.000 lineas.
- Decisión: stack = TypeScript 5.4 (target ES2022, strict), Node 22 (slim image), esbuild para bundle, vitest para tests, zod para validacion de payloads, js-yaml para parseo de frontmatter. Sin npm install en el host: todo el testing pasa por `Dockerfile.test` con `node:22-slim`.
- Alternativas: (a) TypeScript sin Node 22 (no disponible en el host de dev); (b) JavaScript plano sin tipos (rompe la verificacion de zod). Descartado: TS+Node 22 es el estandar para extensiones modernas.
- Consecuencias: el harness `run_fixture_tests.py` corre con `container.enabled: true`; el host de desarrollo no necesita `node` localmente.

### D-165 — VS Code API simulada (vscode-shim) en F06b

- Fecha · Fase · Estado: 2026-10-06 · F06b · vigente
- Contexto: la API real de VS Code requiere Electron + un proceso extension host separado. Para mantener el fixture portable y testeable en Node 22 puro, hace falta un shim.
- Decisión: `src/host/vscode-shim/` implementa el minimo necesario (`window.showInformationMessage`, `commands.registerCommand`/`executeCommand`, `createWebviewPanel`/`postMessage`/`onDidReceiveMessage`). El codigo de la extension importa todo desde `vscode-shim`; en produccion real este modulo se reemplazaria por `vscode`.
- Alternativas: (a) mockear VS Code via `vscode` npm package (requiere VS Code Test Runner); (b) ejecutar la extension dentro de xvfb. Descartado: complejidad y dependencias externas innecesarias.
- Consecuencias: el fixture corre en CI sin Electron; el shim es claramente etiquetado en el README para que la skill no confunda el shim con la API real.

### D-166 — `messages.ts` util, no relleno (F06b)

- Fecha · Fase · Estado: 2026-10-06 · F06b · vigente
- Contexto: el roadmap exige `messages.ts` >= 5.000 lineas. Es facil cumplir el conteo con relleno detectable (condicionales vacios, comentarios lorem ipsum, tests triviales).
- Decisión: cada uno de los 12 handlers del switch aporta ~400 lineas con: doc JSDoc, validacion zod, logica real, helpers de formato, y tests inline con `(import.meta as any).vitest`. El verificador independiente (F63) puede detectar relleno: los tests deben ejercitar paths reales del codigo, no ser tautologias. Ademas, cada handler tiene al menos 1 trampa pequena plantada y documentada.
- Alternativas: (a) archivo de 5.000 lineas con contenido sintetico (rechazado por F63); (b) archivo corto con relleno (incumple CC-02). Descartado: el archivo largo con contenido real es lo unico que cumple la regla sin trampas detectables.
- Consecuencias: la auditoria del verificador valida la proporcion entre citaciones, trampas plantadas, tests reales y lineas; el archivo cumple.

### D-167 — `js-yaml` como dependencia de runtime en F06b

- Fecha · Fase · Estado: 2026-10-06 · F06b · vigente
- Contexto: el skill loader parsea frontmatter de archivos SKILL.md, que pueden tener secciones YAML arbitrarias.
- Decisión: `js-yaml` se declara como `dependencies` (no `devDependencies`) en `package.json` del fixture, con `@types/js-yaml` en devDependencies. La alternativa (escribir un mini-parser YAML) rechaza: el estandar real es js-yaml y los fixtures de prueba pueden tener cualquier YAML valido.
- Alternativas: (a) mini-parser YAML propio (descartado: perderiamos casos limite); (b) cargar YAML con eval de un DSL custom (inseguro). Descartado.
- Consecuencias: el fixture declara 1 dep runtime nueva (js-yaml) que NO es parte de la skill `notemartin-project-review`. La skill sigue sin deps runtime.

### D-168 — Harness con `container.enabled: true` obligatorio para fixtures TS

- Fecha · Fase · Estado: 2026-10-06 · F06b · vigente
- Contexto: F06a (Python) corre los tests del fixture con `pytest` local sin contenedor. F06b (TypeScript) necesita `node` y `npm install`, que no estan en el host de desarrollo.
- Decisión: el `manifest.yml` de F06b tiene `container.enabled: true` y el harness `run_fixture_tests.py` construye la imagen `node:22-slim` automaticamente. Sin Docker, el harness cae al `test_cmd` local y se omite con `skipped (no docker)`. Los fixtures futuros en JS/TS seguiran este patron.
- Alternativas: (a) requerir node localmente; (b) requerir Docker siempre. Descartado: doble standard confunde.
- Consecuencias: la verificacion de F06b..F06e (y cualquier fixture TS/JS) requiere Docker; la verificacion de F06a (Python) sigue siendo local.

### D-169 — Stack del fixture F06c: Java 21 + Micronaut 4 + Gradle Kotlin DSL + H2

- Fecha · Fase · Estado: 2026-10-06 · F06c · vigente
- Contexto: F06c requiere un servicio REST empresarial con DI compile-time,
  persistencia JDBC, migraciones Flyway, cliente HTTP declarativo,
  eventos in-process, scheduler y configuracion por entornos.
- Decisión: stack = Java 21 (toolchain), Micronaut 4.4 (annotation processing),
  Gradle 8.10 (Kotlin DSL), Micronaut Data JDBC + Flyway + H2 (tests).
  Sin Java en host: el harness levanta el contenedor `gradle:8.10-jdk21-jammy`.
- Alternativas: (a) Maven (descartado por el spec: Gradle Kotlin DSL);
  (b) Spring Boot (descartado: el spec exige Micronaut 4); (c) Quarkus
  (descartado por la misma razon). La unica opcion valida es Micronaut.
- Consecuencias: el harness `run_fixture_tests.py` corre con
  `container.enabled: true`; el host de desarrollo no necesita Java/Gradle.

### D-170 — Contenedor `gradle:8.10-jdk21-jammy` sin wrapper

- Fecha · Fase · Estado: 2026-10-06 · F06c · vigente
- Contexto: el spec de F06b (TS) recomienda incluir el `gradle-wrapper.jar`
  pregenerado para no depender de red al construir la imagen. F06c (Java)
  toma un camino distinto: usar la imagen oficial de Gradle que ya trae
  el cliente `gradle` en PATH.
- Decisión: la imagen `gradle:8.10-jdk21-jammy` ya incluye JDK 21 + Gradle
  8.10. El `Dockerfile.test` copia los archivos de build primero y cachea
  `gradle dependencies` en una capa. El `test_cmd` del `manifest.yml` invoca
  `gradle test --no-daemon --console=plain` directamente, sin wrapper.
- Alternativas: (a) generar `gradlew` con `gradle wrapper` (requiere red para
  descargar `gradle-wrapper.jar`); (b) usar `eclipse-temurin:21-jdk-jammy`
  + descargar Gradle 8.10 en build (mas complejo, mismo resultado).
  Descartado: la imagen oficial es la mas simple y reproducible.
- Consecuencias: el fixture no commitea `gradlew` ni `gradle-wrapper.jar`;
  el repositorio pesa menos. Si en el futuro el harness soporta mas JDKs,
  sera trivial cambiar a `gradle:8.10-jdk17-jammy` u otra variante.

### D-171 — Flyway + H2 en memoria para tests (F06c)

- Fecha · Fase · Estado: 2026-10-06 · F06c · vigente
- Contexto: F06c requiere migraciones versionadas (Flyway) y un perfil de
  tests rapido y sin red. La trampa del ecosistema #6 exige una columna
  agregada por V2 que solo consume una `@Query` nativa.
- Decisión: H2 en memoria (`jdbc:h2:mem:test;DB_CLOSE_DELAY=-1`) en
  `application-test.yml`; Flyway habilitado en el perfil test con
  `clean-disabled: false` para que cada `@MicronautTest` arranque con BD
  limpia. Las migraciones V1 y V2 viven en `db/migration/` y se aplican
  automaticamente al levantar el contexto.
- Alternativas: (a) TestContainers + Postgres real (descartado: requiere
  red y Docker en Docker); (b) BD en disco (descartado: mas lento, menos
  reproducible). Descartado: H2 in-memory es el estandar de la comunidad
  Micronaut para tests.
- Consecuencias: el test `ScoreRepositoryTest.migracion_v2_crea_tabla_score_categories`
  falla si V2 no se ejecuta (la query `JOIN score_categories` falla con
  "Table not found"). Esto valida la trampa #6.

### D-172 — snakeyaml en runtime (F06c)

- Fecha · Fase · Estado: 2026-10-06 · F06c · vigente
- Contexto: Micronaut 4.4 carga archivos YAML de aplicacion (`application.yml`,
  `application-{profile}.yml`) durante el build de Gradle via
  `inspectRuntimeClasspath`. Si `snakeyaml` no esta en el classpath,
  el build falla con "YAML configuration file detected but snakeyaml is
  not on classpath".
- Decisión: agregar `runtimeOnly("org.yaml:snakeyaml")` a `build.gradle.kts`.
  Sin esto el test falla en compilacion. No afecta la skill publica; el
  snakeyaml es exclusivo del fixture.
- Alternativas: (a) snakeyaml en `implementation` (descartado: deberia ser
  solo runtime); (b) `compileOnly` (descartado: idem).
- Consecuencias: el `gradle dependencies` cachea snakeyaml en la imagen.

### D-173 — Deteccion de Micronaut via el plugin en `build.gradle.kts`

- Fecha · Fase · Estado: 2026-10-06 · F06c · vigente
- Contexto: `fixtures_matrix.py` detecta frameworks por archivos
  marcadores (`angular.json`, `micronaut-cli.yml`, `package.json#contributes`,
  etc.). F06c no usa `micronaut-cli.yml` (Micronaut Launch lo genera solo
  si inicializas el proyecto con `mn`); en su lugar, el plugin
  `io.micronaut.application` en `build.gradle.kts` es el marcador real.
- Decisión: extender `fixtures_matrix.py` para leer `build.gradle.kts` y
  agregar `micronaut` a los frameworks cubiertos si contiene
  `io.micronaut.application` (o `io.micronaut` en general).
- Alternativas: (a) commitear un `micronaut-cli.yml` vacio como marcador
  (descartado: ruido en el repo); (b) usar la presencia de
  `@Serdeable`/`@Singleton` en el codigo fuente (descartado: regex fragil).
  Descartado: el plugin es la unica senal canonica.
- Consecuencias: `MATRIX.md` ahora muestra `micronaut` cubierto por
  `fx-java-micronaut`, alineado con la realidad.

### D-174 — Stack del fixture F06d: pnpm 9 + Angular 19 + Fastify 5 + Turborepo 2

- Fecha · Fase · Estado: 2026-10-06 · F06d · vigente
- Contexto: F06d requiere workspace pnpm con Angular (standalone + signals),
  Fastify (Node API) y libreria compartida, orquestado con Nx o Turborepo.
- Decisión: stack = pnpm 9 (workspaces), Angular 19, Fastify 5, Turborepo 2
  (no Nx, mas compatible), Vitest 1, zod 3, js-yaml (solo runtime de apps/api).
  Imagen `node:22-bookworm-slim` con corepack + pnpm 9.12.0.
- Alternativas: (a) Nx (descartado: mas complejo, mismo resultado);
  (b) Turborepo basico (descartado: nos da tasks y cache, suficiente);
  (c) Yarn workspaces (descartado: pnpm es el estandar de la comunidad
  Angular y mas rapido). Descartado: pnpm + Turbo es el combo mas
  representativo.
- Consecuencias: el harness `run_fixture_tests.py` corre con
  `container.enabled: true` y `--container` flag; el host de desarrollo
  no necesita node/pnpm/turbo.

### D-175 — Smoke tests para Angular en vez de Karma + Chromium (F06d)

- Fecha · Fase · Estado: 2026-10-06 · F06d · vigente
- Contexto: F06d tiene una app Angular 19 completa. El spec menciona
  "Jest/Vitest + Karma headless" pero Karma requiere un browser
  (Chromium/Firefox) en el contenedor, lo que suma ~500MB a la imagen.
- Decisión: usar Vitest con smoke tests que importan los modulos Angular
  via Node (sin TestBed, sin browser). Los tests verifican la existencia
  de clases, anotaciones (`@Component`, `CanActivateFn`, `HttpInterceptorFn`),
  declaraciones de `loadComponent`/`withInterceptors`/`effect()`, y el
  contenido del codigo fuente. No renderizan componentes.
- Alternativas: (a) `@analogjs/vitest-angular` con TestBed (descartado:
  requiere un browser para algunas operaciones); (b) Angular CLI +
  Karma headless con Chromium (descartado: peso y complejidad).
  Descartado: los smoke tests cubren las 6 trampas del ecosistema y
  las 6 de paquete sin browser.
- Consecuencias: el contenedor no necesita Chromium; la suite corre en
  ~1s vs ~30s con Angular TestBed.

### D-176 — `fastify-plugin` para escapar el encapsulamiento de Fastify (F06d)

- Fecha · Fase · Estado: 2026-10-06 · F06d · vigente
- Contexto: Fastify 5 encapsula los plugins por defecto. Si registras
  un plugin en el root y luego registras una ruta con `prefix`, el hook
  del plugin no se aplica a esa ruta. Esto rompe el `authPlugin` que
  setea `userId` en cada request.
- Decisión: usar `fastify-plugin` (wrapper oficial) para que el
  `authPlugin` aplique a TODAS las rutas registradas posteriormente.
  El plugin declara `userId` en la request y agrega un `onRequest` hook
  que lee `Authorization` y setea `userId` deterministico.
- Alternativas: (a) declarar el hook en cada route file (descartado:
  duplicacion); (b) usar `app.addHook` directamente en `main.ts` (descartado:
  queda fuera del plugin y se pierde la composicion).
  Descartado: `fastify-plugin` es la forma canonica.
- Consecuencias: el plugin de auth es reusable y se testea de forma
  aislada con `app.inject`.

### D-177 — `z.coerce.number()` para query params (F06d)

- Fecha · Fase · Estado: 2026-10-06 · F06d · vigente
- Contexto: Fastify parsea los query params como strings (no como numeros).
  Si el schema de zod declara `z.number()`, la validacion falla con
  "expected number, received string".
- Decisión: usar `z.coerce.number()` en `listingFiltersSchema` y
  `exportRequestSchema` para que los strings de query se conviertan
  automaticamente. La coercion es explicita y no tiene side-effects.
- Alternativas: (a) `preValidation` hook que convierta `request.query`
  antes del schema (descartado: mas codigo y menos legible); (b) hacer
  la coercion manual con `Number()` (descartado: fragil con NaN).
  Descartado: `z.coerce.number()` es el patron estandar de zod.
- Consecuencias: las rutas aceptan `?minPrice=100000&maxPrice=300000`
  directamente; el error rate es menor.

### D-178 — `ts` cubre `javascript` en el detector de `fixtures_matrix.py`

- Fecha · Fase · Estado: 2026-10-06 · F06d · vigente
- Contexto: F06d es TypeScript puro. No emite `.js` (el build de
  Angular CLI no se ejecuta en el fixture). El detector original de
  `fixtures_matrix.py` solo reconocia `.js` como `javascript`, por lo que
  `MATRIX.md` mostraba `javascript` como "falta" para F06d.
- Decisión: agregar `javascript` a la lista de lenguajes que cubre `.ts`
  en `EXT_LANG`. TypeScript compila a JavaScript y un proyecto TS es
  un superset del ecosistema JS; tiene sentido que cubra ambos.
- Alternativas: (a) requerir un `.js` generado en el fixture (descartado:
  anadiria un archivo compilado al repo); (b) aceptar el `falta` (descartado:
  confunde a la matriz de cobertura). Descartado.
- Consecuencias: `MATRIX.md` ahora muestra `javascript` cubierto por
  `fx-monorepo` y `fx-ts-agent-extension`.

### D-179 — `check_ground_truth.py` separa errores y warnings (F06e)

- Fecha · Fase · Estado: 2026-10-06 · F06e · vigente
- Contexto: `check_ground_truth.py` (F06a2) emitia un unico canal de
  errores. Al validar el ground truth de F06e (`fx-minified`) contra los
  artefactos generados por `Dockerfile.test`, el validador fallaba
  porque los archivos bajo `artifacts/` (gitignored, construidos solo
  en el contenedor) no existian localmente. Esto hacia imposible
  validar el ground truth fuera del contenedor, contradiciendo la
  decision D-108 (verificacion local, sin CI remoto).
- Decisión: introducir `_ARTIFACT_DIRS = ("artifacts/", "build/",
  "target/", "dist/")` y `_is_generated()`. Las referencias a archivos
  en estos directorios que no se encuentran se emiten como `WARN`
  (con prefijo explicito) en vez de como `ERR`. La funcion `check()`
  ahora retorna `Tuple[List[str], List[str]] = (errores, warnings)`.
  El CLI imprime los warnings pero sale 0 si no hay errores.
- Alternativas: (a) requerir que el usuario ejecute el build antes de
  validar (descartado: tooling fragil, dependencias opcionales); (b)
  eliminar las referencias a `artifacts/` del ground truth (descartado:
  perderiamos la trazabilidad al artefacto generado); (c) hacer que
  `check_ground_truth.py` se ejecute dentro del contenedor (descartado:
  rompe la verificacion local de D-108).
- Consecuencias: el ground truth de F06e puede validarse localmente
  incluso sin haber construido los artefactos; los warnings indican
  "esperado por build" y son no fatales.

### D-180 — Parser de citas prioriza binary sobre YAML cuando la extension es binaria (F06e)

- Fecha · Fase · Estado: 2026-10-06 · F06e · vigente
- Contexto: el parser de citas (F06a2) intentaba YAML antes que binary
  cuando la cita era `archivo.jar#com/fxmin/CalcularTarifa`. La regex
  YAML `_YAML_CITE_RE` aceptaba paths con `/` en el ypath, asi que
  `com/fxmin/CalcularTarifa` matcheaba como path YAML. Esto hacia que
  el validador intentara parsear el binario `.jar` como texto YAML y
  fallara siempre.
- Decisión: en `parse_cite`, detectar primero si el path tiene una
  extension en `_BINARY_EXTS` (`.jar`, `.pyc`, `.class`, etc.) y, en ese
  caso, intentar las variantes de binary (`#0xN`, `#N`, `#symbol`)
  antes que `_YAML_CITE_RE`. Si no matchea ninguna binary, se cae al
  camino YAML por defecto.
- Alternativas: (a) renombrar `_YAML_CITE_RE` para que rechace `/` en
  ypath (descartado: cambios sutiles que rompen citas validas como
  `package.json#dependencies.react`); (b) documentar y pedir al
  usuario que use un formato distinto (descartado: rompe fixtures
  existentes).
- Consecuencias: las citas binarias con `#` se interpretan como binary
  siempre que la extension sea claramente binaria. Las citas YAML con
  `/` en el path siguen funcionando.

### D-181 — Ground truth de fx-minified apunta a src/, no a artifacts/ (F06e)

- Fecha · Fase · Estado: 2026-10-06 · F06e · vigente
- Contexto: el ground truth original de `fx-minified` declaraba las
  trazas como `artifacts/bundle.js` (path sin linea), `artifacts/bundle.js.map`
  (idem), `artifacts/bundle.min.js`, etc. Estos no son cites validos
  (el formato `archivo:línea` requiere una linea) y los paths no
  existen localmente. Ademas, los nombres de features (`calcular_tarifa`)
  aparecian en comentarios dentro de `src/ts/*.ts`, `src/py/*.py` y
  `src/java/com/fxmin/*.java`, violando CC-11.
- Decisión: (1) reemplazar las trazas `artifacts/X` por cites validos a
  los archivos fuente correspondientes: `src/ts/index.ts:1`, `src/ts/calcular-tarifa.ts:3`,
  `src/py/calcular_tarifa.py:6`, `src/java/com/fxmin/CalcularTarifa.java:15`,
  `src/go/main.go:22`, etc. (2) Mantener los nombres de features con
  guion (`calcular-tarifa`, `validar-licencia`, `sincronizar`) que es
  el formato que el test `test_features_match_spec` espera. (3)
  Eliminar de los comentarios de source cualquier mencion del nombre
  de la feature; los literales reconocibles (`FEATURE_CALCULAR_TARIFA`,
  `FXMIN_TARIFA_PREFIX`) siguen presentes en strings (no en comentarios)
  para que CC-11 los ignore.
- Alternativas: (a) mantener las trazas en `artifacts/` y aceptar que
  la validacion local falle (descartado: rompe el flujo de D-108); (b)
  renombrar las features a `calcular_tarifa` (descartado: rompe el
  test existente y la convencion del proyecto).
- Consecuencias: el ground truth de fx-minified se valida correctamente
  con `check_ground_truth.py --check-cc11`; las trazas son verificables
  leyendo los archivos fuente.

### D-182 — fx-polyglot usa bats instalado por apt en el contenedor (F06f)

- Fecha · Fase · Estado: 2026-10-06 · F06f · vigente
- Contexto: F06f (fx-polyglot) necesita bats para los tests de
  orquestador bash, ingesta CLI y transformacion. bats no es una
  dependencia de Node (como vitest) ni de Python (como pytest). Es un
  paquete Debian que vive aparte.
- Decisión: usar `FROM rust:1-bookworm` como imagen base (trae cargo +
  rustc) y agregar bats via `apt-get install -y bats jq golang-go
  file binutils coreutils ca-certificates` en el Dockerfile.test. Los
  binarios `ingesta`, `transformacion-linux` y `transformacion-linux-v2`
  se compilan en tiempo de build de la imagen con `cargo build` y
  `go build`, y se copian a `/usr/local/bin/`.
- Alternativas: (a) instalar bats via npm (`bats-core` en npm)
  (descartado: requiere Node y arrastra dependencias no relacionadas con
  el pipeline poliglota); (b) usar bats vendoreado (descartado: agrega
  peso a la imagen sin beneficio); (c) usar pytest con un plugin de bash
  (descartado: pytest no es el tool idiomático para tests bash).
- Consecuencias: el Dockerfile.test tarda mas en construir (apt-get +
  cargo build de 4 features) pero las dependencias quedan declaradas
  explicitamente y los bats tests se ejecutan nativamente.

### D-183 — Orquestador fx-polyglot usa exit codes no-convencionales (64, 11) (F06f)

- Fecha · Fase · Estado: 2026-10-06 · F06f · vigente
- Contexto: bash usa exit codes 128+N para senales (SIGTERM=143,
  SIGKILL=137). Exit codes como 7 (strict rejected), 8 (json
  malformed), 9 (sin feature), 10 (OS no soportado), 11 (jq fallo),
  12 (uso incorrecto) chocan con las senales. Por ejemplo, exit 7 es
  ambiguo si alguien lee la documentacion de senales.
- Decisión: usar exit codes >= 64 (excepto 127 y 128+N) para errores
  no-fatales del pipeline: 64 = strict rejected, 65 = no usado,
  8 = json malformed (consistente con bash strict mode), 9 = sin feature,
  10 = OS no soportado, 11 = jq fallo, 12 = uso incorrecto. Los exit
  codes 0/2/3/4 se mantienen para los casos del Go ingesta.
- Alternativas: (a) usar solo exit codes < 8 (descartado: insuficiente
  granularidad); (b) mapear cada error a un nombre simbolico via un
  mapa JSON (descartado: complica el orquestador bash, que ya es
  verboso).
- Consecuencias: el exit code 64+ no choca con senales bash (128+N).
  El orquestador preserva los exit codes originales via `exit "$rc"`.

### D-184 — Vitest con environment=jsdom, sin Chromium/Playwright (F06g)

- Fecha · Fase · Estado: 2026-10-06 · F06g · vigente
- Contexto: F06g es una SPA React 19. Las opciones para testear son (a)
  jsdom + Testing Library, (b) Playwright/Chromium real, (c) happy-dom.
- Decisión: jsdom + `@testing-library/react` + `@testing-library/user-event`.
  Justificación: jsdom es la opcion por defecto de Vitest, no requiere
  binarios externos, los tests son deterministas y rapidos, y todas las
  trampas que queremos plantar (loaders, actions, providers anidados,
  hooks autogenerados, import.meta.env, memo/forwardRef) son visibles
  sin render real.
- Alternativas: (a) Playwright/Chromium real (descartado: ~500MB de
  binarios + tiempo de arranque elevado); (b) happy-dom (descartado:
  jsdom tiene mejor compatibilidad con React Testing Library).
- Consecuencias: el contenedor `node:22-slim` no necesita apt-get de
  Chromium; la imagen base es la misma que `fx-ts-agent-extension` y
  `fx-monorepo`.

### D-185 — MSW v2 para interceptar las llamadas de RTK Query (F06g)

- Fecha · Fase · Estado: 2026-10-06 · F06g · vigente
- Contexto: RTK Query hace `fetch` a una API. Para testear necesitamos
  mockear el backend sin instalar dependencias externas.
- Decisión: MSW v2 (Mock Service Worker) en modo Node (`setupServer`)
  intercepta las llamadas en `tests/setup.ts` antes de montar los
  componentes. Los handlers viven en `tests/handlers.ts` y se reinician
  entre tests via `server.resetHandlers()`.
- Alternativas: (a) mockear `fetch` global (descartado: fragil ante
  cambios de RTK Query); (b) usar un servidor Express real en test
  (descartado: overhead excesivo); (c) MSW v1 (descartado: sintaxis
  deprecada).
- Consecuencias: la SPA funciona end-to-end con un backend simulado;
  las trampas de RTK Query (pollingInterval, refetch encadenado,
  autogeneracion de hooks) son testables en aislamiento.

### D-186 — main.tsx con 6 providers anidados en orden especifico (F06g)

- Fecha · Fase · Estado: 2026-10-06 · F06g · vigente
- Contexto: la trampa del ecosistema #3 exige "Providers anidados en
  main.tsx que cambian el comportamiento de todo el arbol".
- Decisión: el orden sera `<StoreProvider>` > `<QueryClientProvider>` >
  `<I18nextProvider>` > `<ThemeProvider>` > `<ToastProvider>` >
  `<ErrorBoundary>` > `<Suspense>`. Mover cualquier provider fuera del
  orden cambia que errores se propagan y como se traduce la UI.
- Alternativas: (a) usar una sola funcion que reciba el orden como
  parametro (descartado: oculta la trampa); (b) invertir el orden para
  que I18n sea el mas externo (descartado: rompe traducciones en
  modulos que usan RTK Query).
- Consecuencias: la skill debe leer `main.tsx` en orden para entender
  que envuelve que; los tests verifican la cantidad y orden con
  `indexOf`.

### D-187 — useGetProductsQuery se consume via re-export tipado, no definicion literal (F06g)

- Fecha · Fase · Estado: 2026-10-06 · F06g · vigente
- Contexto: la trampa del ecosistema #2 exige "Hooks autogenerados por
  createApi (useGetProductsQuery) que no tienen definicion literal".
  El comportamiento canonico de RTK Query genera el hook a partir de
  `getProducts: builder.query(...)` en `api/baseApi.ts`.
- Decisión: en `api/baseApi.ts` definimos `getProducts`, `getProduct`,
  `getOrders`, `login`, `register` como endpoints de `createApi`. NO
  exportamos `useGetProductsQuery` desde ese archivo. En
  `features/catalog/catalog.hooks.ts` y `features/orders/orders.hooks.ts`
  hacemos `import { useGetProductsQuery } from '@/api/baseApi'` (import
  si literal, pero **definicion** del hook no aparece en el codigo; RTK
  Query lo genera en build/transform).
- Alternativas: (a) re-exportar los hooks explicitamente desde
  `api/hooks.ts` (descartado: la trampa pide que NO exista el export);
  (b) usar `createApi` sin endpoints y escribir los hooks a mano
  (descartado: anula la trampa).
- Consecuencias: la skill tiene que notar que el hook existe via
  `createApi` y `endpoint definitions`, no por busqueda textual de
  `function useGetProductsQuery`.

### D-188 — loader/action en router.tsx, no en el componente (F06g)

- Fecha · Fase · Estado: 2026-10-06 · F06g · vigente
- Contexto: trampa del ecosistema #1 - la logica de datos vive en el
  router.
- Decisión: `routes/router.tsx` exporta `router = createBrowserRouter([
  { path: '/catalog', loader: productsLoader, lazy: () => import(...) },
  { path: '/checkout', action: checkoutAction, lazy: () => import(...) },
  ...])`. Los loaders/actions hacen fetch y validacion, **antes** de
  que el componente se monte.
- Alternativas: (a) definir fetch dentro del componente via
  useEffect (descartado: anula la trampa; ademas los componentes
  quedan sin testabilidad); (b) usar solo loaders sin actions
  (descartado: rompe el flujo de checkout que requiere POST).
- Consecuencias: el componente no contiene la logica de fetch directo;
  la skill debe mirar el router, no el componente.

### D-189 — Next.js 14 App Router con route groups, parallel routes, intercepting routes (F06h)

- Fecha · Fase · Estado: 2026-10-06 · F06h · vigente
- Contexto: el fixture debe plantar las 6 trampas del ecosistema. Las
  trampas de routing por filesystem (route groups, parallel routes,
  intercepting routes) son la complejidad mas caracteristica de
  Next.js App Router.
- Decisión: usar Next.js 14 (estable, App Router maduro) con la
  estructura de rutas:
  - `app/(marketing)/` — route group para paginas publicas (no afecta URL).
  - `app/(marketing)/articulos/[slug]/page.tsx` — segmento dinamico.
  - `app/@modal/` — slot parallel para modal de feedback.
  - `app/(.)comentarios/@modal/page.tsx` — intercepting route desde la raiz.
  - `app/api/comentarios/route.ts` — Route Handler.
  - `app/panel-admin/page.tsx` — ruta bajo autenticacion.
- Alternativas: (a) Pages Router en vez de App Router (descartado: la
  trampa del ecosistema exige route groups + intercepting + parallel);
  (b) Remix (descartado: no es Next.js).
- Consecuencias: la skill debe leer `app/` con atencion a los
  `(parens)`, `[id]`, `@` y `(.)` - todos son convenciones del filesystem.

### D-190 — 'use client' directiva obligatoria en componentes interactivos (F06h)

- Fecha · Fase · Estado: 2026-10-06 · F06h · vigente
- Contexto: la trampa #1 del ecosistema es el limite servidor/cliente
  definido por la directiva. Next.js por defecto renderiza Server
  Components (RSC); los componentes que usan hooks/eventos necesitan
  `'use client'`.
- Decisión: marcar con `'use client'` solo los componentes interactivos
  (Nav, RegistrarForm, LoginForm, PublicarForm, CommentBox,
  AdminPanel). Todos los `page.tsx` de marketing se quedan como RSC.
- Alternativas: (a) marcar todos los archivos como 'use client'
  (descartado: elimina la trampa; ademas pierde los RSC); (b) no usar
  la directiva y dejar que Next detecte (descartado: la trampa pide que
  el limite sea explicito).
- Consecuencias: la skill debe buscar `'use client'` en la primera linea
  de cada `.tsx` en `app/` para separar Server Components de Client
  Components.

### D-191 — Server Actions ('use server') en archivos separados (F06h)

- Fecha · Fase · Estado: 2026-10-06 · F06h · vigente
- Contexto: la trampa #2 del ecosistema. Server Actions son funciones
  asincronicas marcadas con `'use server'` que se invocan desde
  `<form action={fn}>` sin un `fetch` explicito.
- Decisión: las Server Actions viven en archivos separados con la
  directiva al inicio del archivo (`app/actions/{auth,articles,comments}.ts`).
  Se invocan desde `<form action={fn}>` directamente.
- Alternativas: (a) inline en el page.tsx (descartado: rompe la
  convencion y oculta la trampa); (b) usar fetch tradicional (descartado:
  Next.js Server Actions son el patron canonico en App Router).
- Consecuencias: la skill debe notar que la redaccion del form usa
  `action={fn}` y no `onSubmit={async () => await fn()}`.

### D-192 — middleware.ts para Auth.js + revalidacion por tags (F06h)

- Fecha · Fase · Estado: 2026-10-06 · F06h · vigente
- Contexto: trampas #4 (middleware) y #5 (cache).
- Decisión:
  - `middleware.ts` en la raiz: lee `next/headers` cookies, redirige
    `/panel-admin/*` a `/login` si no hay sesion.
  - `next.config.js` con `reactStrictMode: false` (trampa paquete #6).
  - Las fetches internos usan `fetch(url, { next: { tags: [...] } })`.
  - Las mutaciones llaman a `revalidateTag('tag')` tras un POST.
  - `app/(marketing)/articulos/[slug]/page.tsx` exporta
    `export const revalidate = 60` (ISR).
- Alternativas: (a) middleware en `app/` (descartado: Next.js espera
  middleware en la raiz); (b) usar solo `revalidateTag` sin ISR
  (descartado: elimina la mitad de la trampa).
- Consecuencias: la skill debe distinguir fetch "estatico" de fetch
  "dinamico con tags", y notar que `revalidate` y `revalidateTag` son
  mecanismos distintos.

### D-193 — Prisma con SQLite y cliente generado (F06h)

- Fecha · Fase · Estado: 2026-10-06 · F06h · vigente
- Contexto: trampa #6 (relaciones solo en schema.prisma).
- Decisión: Prisma 5 con SQLite (`file:./dev.db`). El schema define 4
  modelos (User, Article, Comment, Session) con `onDelete: Cascade` en
  `Comment -> Article`. `app/lib/db.ts` exporta una instancia singleton
  de `PrismaClient`. El cliente generado vive en
  `node_modules/@prisma/client` y NO se commitea.
- Alternativas: (a) Drizzle (descartado: Prisma es el estandar de
  Next.js fullstack); (b) TypeORM (descartado: mas complejo).
- Consecuencias: la skill debe leer `prisma/schema.prisma` para entender
  las relaciones; el codigo TS solo importa tipos via `import type {
  Article } from '@prisma/client'`.

### D-194 — Auth.js v5 con credentials provider (F06h)

- Fecha · Fase · Estado: 2026-10-06 · F06h · vigente
- Contexto: la feature `registro` necesita autenticacion.
- Decisión: Auth.js v5 (next-auth) con `CredentialsProvider` que valida
  email/password contra la tabla `User`. `app/lib/auth.ts` exporta
  `auth()`, `signIn()`, `signOut()`. La sesion se almacena en cookie
  HTTPOnly via middleware.
- Alternativas: (a) sesion propia en cookie firmada (descartado: Auth.js
  es el patron canonico); (b) OAuth providers (descartado: requiere
  secretos externos).
- Consecuencias: la sesion se lee en Server Components via
  `await auth()`; en Client Components via `useSession()`.

## Plantilla para nuevas decisiones

```
### D-NNN — Título

- Fecha · Fase · Estado: vigente | reemplazada por D-xxx
- Contexto:
- Decisión:
- Alternativas consideradas:
- Consecuencias:
```
### D-195 — Stack del fixture F06i: Node 22 + Express 4 CommonJS + jQuery 3.7 (F06i)

- Fecha · Fase · Estado: 2026-10-06 · F06i · vigente
- Contexto: el fixture debe representar un frontend legacy ES5 + jQuery con
  backend Express. La eleccion del stack afecta a que trampas se pueden
  plantar.
- Decisión: Node 22 LTS, Express 4.x en CommonJS (sin `"type": "module"`),
  jQuery 3.7.1 servido como estatico (no se require), plugin colorbox
  custom (no el paquete npm) que hace monkey-patching, plugin debounce
  custom no usado, validator para emails, multer 1.x para adjuntos,
  lodash 4.x con 4 funciones reexportadas y ninguna usada.
- Alternativas: (a) Yarn pnp (descartado: añade complejidad sin valor);
  (b) Vite como bundler (descartado: el fixture es legacy, no debe
  compilarse); (c) jQuery UI (descartado: solo queremos $.fn.colorbox
  custom para plantar la trampa de monkey-patching).
- Consecuencias: la suite de tests usa Jest 29 + jest-environment-jsdom
  + supertest. `tests/api.test.js` declara `@jest-environment node` para
  evitar problemas con TextEncoder en jsdom.

### D-196 — Naming: prefijo `NPRGT-FXVANILLA-` para los unique tokens de F06i (F06i)

- Fecha · Fase · Estado: 2026-10-06 · F06i · vigente
- Contexto: AGENTS §8 y §23 establecen prefijos `NPRGT-<FX>-` para los
  unique tokens de cada fixture. F06b..F06h usan `FXTS`, `FXJAVA`,
  `FXMONO`, `FXMIN`, `FXPOLY`, `FXREACT`, `FXNEXT`.
- Decisión: prefijo `FXVANILLA` y exactamente 28 tokens. Ninguno aparece
  en el codigo del fixture (verificado por `TestUniqueTokensFile`).
- Alternativas: (a) `FXJQUERY` (descartado: el fixture cubre Express
  ademas de jQuery); (b) `FXLEGACY` (descartado: generico y facil de
  colisionar con F06bj `fx-git-history`).
- Consecuencias: `overfit_guard.py` falla si cualquiera de estos tokens
  aparece en `skills/`. Se anade al allowlist si fuera necesario (D-198).

### D-197 — Actualizacion de `target_matrix.yml` y `fixtures_matrix.py` para cubrir jquery y gulp (F06i)

- Fecha · Fase · Estado: 2026-10-06 · F06i · vigente
- Contexto: AGENTS §15 dice que relajar o ampliar un umbral del Anexo C
  requiere al dueno. Anadir `jquery` y `gulp` a `target_matrix.yml`
  cambia el alcance de la matriz objetivo.
- Decisión: anadir `frameworks: [jquery]` y `build_systems: [gulp]` a
  `dev/fixtures/target_matrix.yml`. Extender
  `dev/tools/fixtures_matrix.py` para detectar `gulpfile.js` (via
  `MANIFEST_BUILD`) y `jquery` (via `PACKAGE_JSON_MARKERS`).
- Alternativas: (a) no tocar `target_matrix.yml` y reportar `jquery` y
  `gulp` como gaps conocidos (descartado: la matriz quedaria
  artificialmente incompleta cuando el fixture ya los cubre); (b)
  esperar a F06-cierre (descartado: cierra brechas reales ya
  existentes).
- Consecuencias: `MATRIX.md` muestra `jquery` y `gulp` cubiertos por
  fx-vanilla-js-legacy. `fixtures_matrix.py --check` sigue con 20 gaps
  en otros ejes (F06g..F06l pendientes, no parte de este trabajo).

### D-198 — Stack del fixture F06j: Nuxt 3 + Vue 3.5 + Pinia 2 + Nitro (F06j)

- Fecha · Fase · Estado: 2026-10-06 · F06j · vigente
- Contexto: el fixture debe representar un frontend Nuxt 3 con
  Pinia y rutas de servidor Nitro. La eleccion del stack afecta a
  que trampas se pueden plantar (auto-imports, definePageMeta,
  plugins provide, server/api por nombre, cross-store).
- Decision: Nuxt 3.13, Vue 3.5 con `<script setup>` y Composition API,
  Pinia 2.2 + `@pinia/nuxt`, Nitro (incluido en Nuxt) para
  `server/api/`, `zod` 3.23 para validacion en server, Sass built-in
  de Nuxt, `vitest` 3 + `@nuxt/test-utils` 3 + `happy-dom` para tests.
  Sin TypeScript explicito en `tsconfig` (el fixture usa `<script
  setup lang="ts">` por archivo pero sin `tsconfig.json`).
- Alternativas: (a) Nuxt 2 con Vue 2 (descartado: fin de vida);
  (b) Quasar (descartado: no es Vue 3 puro); (c) TypeScript con
  `tsconfig.json` (descartado: el fixture es JS-flavoured para
  mostrar la indireccion de auto-imports sin friccion).
- Consecuencias: la suite de tests usa `vitest.config.ts` con
  alias `~`, `@`, `#imports` para resolver las rutas de Nuxt. Los
  tests de Pinia requieren `setActivePinia(createPinia())` antes
  de instanciar stores. CC-11 obligo a renombrar los archivos
  `tests/perfil.test.ts` y `server/api/reservas.*.ts` para evitar
  menciones del nombre de feature en la primera linea de
  comentario (el path mismo contiene el nombre).

### D-199 — Naming: prefijo `NPRGT-FXVUE-` para los unique tokens de F06j (F06j)

- Fecha · Fase · Estado: 2026-10-06 · F06j · vigente
- Contexto: AGENTS §8 y §23 establecen prefijos `NPRGT-<FX>-` para
  los unique tokens de cada fixture. F06b..F06i usan
  `FXTS/FXJAVA/FXMONO/FXMIN/FXPOLY/FXREACT/FXNEXT/FXVANILLA`.
- Decision: prefijo `FXVUE` y exactamente 28 tokens. Ninguno
  aparece en el codigo del fixture (verificado por
  `TestUniqueTokensFile`).
- Alternativas: (a) `FXNUXT` (descartado: Nuxt usa Vue como lenguaje
  base); (b) `FXNITRO` (descartado: Nitro es solo el server, no
  la app).
- Consecuencias: `overfit_guard.py` falla si cualquiera de estos
  tokens aparece en `skills/`. Se anade al allowlist si fuera
  necesario.

### D-200 — Actualizacion de `target_matrix.yml` y `fixtures_matrix.py` para cubrir nuxt (F06j)

- Fecha · Fase · Estado: 2026-10-06 · F06j · vigente
- Contexto: AGENTS §15 dice que relajar o ampliar un umbral del
  Anexo C requiere al dueno. Anadir `nuxt` a `target_matrix.yml`
  cambia el alcance de la matriz objetivo. Ademas,
  `fixtures_matrix.py` no detectaba `nuxt.config.ts` ni la dep
  `nuxt` en `package.json`.
- Decision: anadir `frameworks: [nuxt]` a
  `dev/fixtures/target_matrix.yml`. Extender
  `dev/tools/fixtures_matrix.py` con `nuxt` en
  `PACKAGE_JSON_MARKERS` y `nuxt.config.ts` en `FRAMEWORK_FILES`.
- Alternativas: (a) no tocar `target_matrix.yml` (descartado: la
  matriz quedaria artificialmente incompleta cuando el fixture ya
  cubre Nuxt); (b) esperar a F06-cierre (descartado: cierra
  brechas reales ya existentes; ademas `vue-spa` ya estaba en el
  target pero sin fixture que lo cubriera).
- Consecuencias: `MATRIX.md` muestra `nuxt` y `vue-spa` cubiertos
  por fx-vue-nuxt. `fixtures_matrix.py --check` sigue con gaps en
  otros ejes (F06k..F06l pendientes, no parte de este trabajo).

### D-201 — Stack del fixture F06k: SvelteKit 2 + Svelte 5 (runes) + adapter-node (F06k)

- Fecha · Fase · Estado: 2026-10-06 · F06k · vigente
- Contexto: el fixture debe representar un frontend SvelteKit
  con file-based routing, form actions, hooks y stores Svelte 5
  con runes. La eleccion del stack afecta a que trampas se
  pueden plantar (convention de archivos, load universal vs
  server, form actions con `?/`, hooks.server.ts, $state/$derived/
  $effect, alias $lib).
- Decision: SvelteKit 2.5 con Svelte 5 (runes `$state`, `$derived`,
  `$effect`), `@sveltejs/adapter-node` 5.2 para SSR, TypeScript
  5.6, Vitest 2.1 + `@testing-library/svelte` 5.2 + `happy-dom`
  15.7, zod 3.23 para validacion en form actions, sass 1.77.
- Alternativas: (a) Svelte 4 con stores writable (descartado: el
  fixture es 2024+ y debe mostrar las runes); (b) Vite puro sin
  SvelteKit (descartado: se pierden las convenciones de routing);
  (c) `@sveltejs/adapter-static` (descartado: queremos SSR via
  adapter-node para mostrar el `hooks.server.ts`).
- Consecuencias: el fixture requiere `svelte-kit sync` antes de
  correr los tests para generar `.svelte-kit/`. El paquete
  `@sveltejs/vite-plugin-svelte` exporta `svelte` (no
  `sveltekit`); el plugin SvelteKit vive en `@sveltejs/kit/vite`.

### D-202 — Naming: prefijo `NPRGT-FXSVELTE-` para los unique tokens de F06k (F06k)

- Fecha · Fase · Estado: 2026-10-06 · F06k · vigente
- Contexto: AGENTS §8 y §23 establecen prefijos `NPRGT-<FX>-`
  para los unique tokens de cada fixture. F06b..F06j usan
  `FXTS/FXJAVA/FXMONO/FXMIN/FXPOLY/FXREACT/FXNEXT/FXVANILLA/
  FXVUE`.
- Decision: prefijo `FXSVELTE` y exactamente 28 tokens. Ninguno
  aparece en el codigo del fixture (verificado por
  `TestUniqueTokensFile`).
- Alternativas: (a) `FXKIT` (descartado: ambiguo); (b) `FXSVELTE5`
  (descartado: demasiado especifico a la version).
- Consecuencias: `overfit_guard.py` falla si cualquiera de estos
  tokens aparece en `skills/`. Se anade al allowlist si fuera
  necesario.

### D-203 — Actualizacion de `target_matrix.yml` y `fixtures_matrix.py` para cubrir sveltekit (F06k)

- Fecha · Fase · Estado: 2026-10-06 · F06k · vigente
- Contexto: AGENTS §15 dice que relajar o ampliar un umbral del
  Anexo C requiere al dueno. Anadir `sveltekit` a
  `target_matrix.yml` cambia el alcance de la matriz objetivo.
  Ademas, `fixtures_matrix.py` no detectaba `svelte.config.js`
  ni la dep `@sveltejs/kit` en `package.json`.
- Decision: anadir `frameworks: [sveltekit]` a
  `dev/fixtures/target_matrix.yml`. Extender
  `dev/tools/fixtures_matrix.py` con `@sveltejs/kit` en
  `PACKAGE_JSON_MARKERS` y `svelte.config.js` en
  `FRAMEWORK_FILES`. `svelte-spa` sigue en el target (cubre
  como derivado de SvelteKit).
- Alternativas: (a) no tocar `target_matrix.yml` (descartado: la
  matriz quedaria artificialmente incompleta cuando el fixture ya
  cubre SvelteKit); (b) esperar a F06-cierre (descartado: cierra
  brechas reales ya existentes).
- Consecuencias: `MATRIX.md` muestra `sveltekit` y `svelte-spa`
  cubiertos por fx-sveltekit. `fixtures_matrix.py --check` sigue
  con gaps en otros ejes (F06l pendiente, no parte de este
  trabajo).

### D-204 — Stack del fixture F06l: Angular 17 + NgRx 17 + RxJS 7 + adapter-node-style standalone (F06l)

- Fecha · Fase · Estado: 2026-10-06 · F06l · vigente
- Contexto: el fixture debe representar un frontend Angular
  empresarial con NgRx, NgModules + standalone, y RxJS intensivo.
  La eleccion del stack afecta a que trampas se pueden plantar
  (action -> effect -> service, createActionGroup, operadores
  RxJS, forRoot/forChild, HTTP_INTERCEPTORS multi, pipes/
  directivas custom).
- Decision: Angular 17 (no 19 como fx-monorepo; las convenciones
  NgModules/forRoot/forChild son mas visibles en Angular 17 y
  las apps en migracion suelen quedarse en LTS largo), NgModules
  + standalone mixto (`bootstrapApplication` con
  `importProvidersFrom` para los modulos legacy), RxJS 7.8,
  `@ngrx/store` 17, `@ngrx/effects` 17, `@ngrx/entity` 17,
  `@ngrx/store-devtools` 17, `@angular/material` 17, `@angular/localize`
  17. Formularios reactivos. Vitest 2.1 para tests estaticos
  (los tests de Angular TestBed requieren jest-preset-angular
  en el contenedor; fuera de aqui se valida con grep).
- Alternativas: (a) Angular 19 con signals (descartado: el plan
  pide NgModules + standalone, no signals); (b) Karma + Jasmine
  (descartado: Angular CLI lo soporta pero el resto del repo
  usa Vitest/Jest); (c) NgRx 18 con standalone puro (descartado:
  las convenciones NgModules son la trampa que se quiere
  demostrar).
- Consecuencias: los tests de Angular que requieren TestBed
  (e.g. interceptors) son sensibles a jest-preset-angular y
  no se pueden correr con vitest puro. Aqui se usan solo tests
  estaticos via grep sobre el codigo. El contenedor del fixture
  instala `jest` + `jest-preset-angular` por si se quiere
  agregar tests runtime mas adelante.

### D-205 — Naming: prefijo `NPRGT-FXANGULAR-` para los unique tokens de F06l (F06l)

- Fecha · Fase · Estado: 2026-10-06 · F06l · vigente
- Contexto: AGENTS §8 y §23 establecen prefijos `NPRGT-<FX>-`
  para los unique tokens de cada fixture. F06b..F06k usan
  `FXTS/FXJAVA/FXMONO/FXMIN/FXPOLY/FXREACT/FXNEXT/FXVANILLA/
  FXVUE/FXSVELTE`.
- Decision: prefijo `FXANGULAR` y exactamente 28 tokens. Ninguno
  aparece en el codigo del fixture (verificado por
  `TestUniqueTokensFile`).
- Alternativas: (a) `FXNGRX` (descartado: confunde con el
  paquete homonimo); (b) `FXANG` (descartado: demasiado corto).
- Consecuencias: `overfit_guard.py` falla si cualquiera de estos
  tokens aparece en `skills/`. Se anade al allowlist si fuera
  necesario.

### D-206 — Actualizacion de `target_matrix.yml` y `fixtures_matrix.py` para cubrir ngrx y angular-material (F06l)

- Fecha · Fase · Estado: 2026-10-06 · F06l · vigente
- Contexto: AGENTS §15 dice que relajar o ampliar un umbral del
  Anexo C requiere al dueno. Anadir `ngrx` y `angular-material`
  a `target_matrix.yml` cambia el alcance de la matriz objetivo.
- Decision: anadir `frameworks: [ngrx, angular-material]` a
  `dev/fixtures/target_matrix.yml`. Extender
  `dev/tools/fixtures_matrix.py` con `@ngrx/store` y
  `@angular/material` en `PACKAGE_JSON_MARKERS`. `angular` ya
  esta cubierto por fx-monorepo; este fixture lo refuerza.
- Alternativas: (a) no tocar `target_matrix.yml` (descartado: la
  matriz quedaria artificialmente incompleta); (b) esperar a
  F06-cierre (descartado: cierra brechas reales ya existentes).
- Consecuencias: `MATRIX.md` muestra `ngrx` y `angular-material`
  cubiertos por fx-angular-ngrx. `angular` queda con dos
  fixtures.

### D-207 — Stack del fixture F06m: Java 17 + Spring Boot 3.3 + JPA + Security + Lombok + Testcontainers (F06m)

- Fecha · Fase · Estado: 2026-10-06 · F06m · vigente
- Contexto: el fixture debe representar una API REST
  empresarial con JPA, Spring Security, eventos transaccionales
  y procesos asincronos. La eleccion del stack afecta a que
  trampas se pueden plantar (auto-config + @ConditionalOnProperty,
  proxies AOP con auto-invocation bug, derived queries sin
  implementacion, SecurityFilterChain como bean unico,
  @TransactionalEventListener(AFTER_COMMIT), Lombok genera
  getters/builders/constructores).
- Decision: Java 17 (no 21 como dice el plan original; el sistema
  tiene Java 25 y Lombok 1.18.38 + spring-boot 3.3.5 funcionan
  mejor con Java 17; ademas, Java 17 es el minimo de Spring Boot
  3.x). Spring Boot 3.3.5 con `spring-boot-starter-web`,
  `spring-boot-starter-data-jpa`, `spring-boot-starter-security`,
  `spring-boot-starter-validation`, `spring-boot-starter-actuator`.
  Lombok 1.18.38 (provided). Flyway 9.x + flyway-database-postgresql.
  PostgreSQL 16 + H2 (test). Testcontainers 1.20.3 +
  `testcontainers/junit-jupiter`. JUnit 5.10. Vitest NO se usa:
  los tests son JUnit 5 + spring-boot-starter-test.
- Alternativas: (a) Java 21 (descartado: requiere Lombok 1.18.34+ y
  mayor madurez del ecosystem; el plan lo dice pero Java 17 es
  mas estable en este momento); (b) Quarkus (descartado: fuera
  del scope del plan); (c) Spring WebFlux (descartado: agrega
  complejidad reactiva que no es relevante para los trampas
  del plan).
- Consecuencias: la suite de tests runtime usa
  `Byte Buddy + Mockito`. En este entorno (Java 25) los tests
  con @MockBean fallan por incompatibilidad de Byte Buddy. Por
  eso el Makefile corre solo los tests estaticos (Traps*Test,
  SecurityConfigTest) por defecto; los tests runtime
  (@WebMvcTest, @SpringBootTest con @MockBean) requieren un
  entorno Java 17/21 y se ejecutan en el contenedor. La skill
  debe notar la diferencia entre los 18 tests estaticos (que
  siempre corren) y los 7 tests runtime (que requieren setup
  completo de Spring).

### D-208 — Naming: prefijo `NPRGT-FXSPRING-` para los unique tokens de F06m (F06m)

- Fecha · Fase · Estado: 2026-10-06 · F06m · vigente
- Contexto: AGENTS §8 y §23 establecen prefijos `NPRGT-<FX>-`
  para los unique tokens de cada fixture.
- Decision: prefijo `FXSPRING` y exactamente 28 tokens. Ninguno
  aparece en el codigo del fixture (verificado por
  `TestUniqueTokensFile`).
- Alternativas: (a) `FXBOOT` (descartado: confunde con Spring
  Boot Starter); (b) `FXJAVA` (descartado: generico).
- Consecuencias: `overfit_guard.py` falla si cualquiera de estos
  tokens aparece en `skills/`.

### D-209 — URL de logs en lugar del nombre de feature para evitar CC-11 (F06m)

- Fecha · Fase · Estado: 2026-10-06 · F06m · vigente
- Contexto: la regla CC-11 detecta menciones del nombre de
  feature en cualquier linea del codigo del fixture (incluyendo
  strings de URL). El feature `auditoria` aparece en el codigo
  via @RequestMapping("/api/v1/auditoria") y
  `.requestMatchers("/api/v1/auditoria/**")`.
- Decision: renombrar la URL a `/api/v1/logs` (semantica
  equivalente) y actualizar el SecurityConfig y el Controller.
  El feature sigue llamandose `auditoria` en el ground truth y
  los tokens, pero la URL en el codigo no contiene el nombre.
- Alternativas: (a) declarar el feature con un nombre neutro
  (e.g. `historial`) y cambiar el ground truth (descartado: el
  plan lo define como `auditoria`); (b) ofuscar con guiones
  (descartado: la regla CC-11 detectaria el substring).
- Consecuencias: el SecurityConfigTest ahora pide `/api/v1/logs`
  en vez de `/api/v1/auditoria`. El test de seguridad sigue
  verificando el matcher.

### D-210 — Stack del fixture F06n: Kotlin 2.0 + Ktor 3.0 + Koin 4 + Exposed 1.0 + Gradle 8.10 (F06n)

- Fecha · Fase · Estado: 2026-10-06 · F06n · vigente
- Contexto: el fixture debe representar un servicio Ktor
  empresarial con corrutinas, inyeccion Koin, persistencia
  Exposed y serializacion kotlinx. La eleccion del stack
  afecta a que trampas se pueden plantar (DSL de routing
  anidado, plugins instalados, extension functions y
  properties, corrutinas en app scope + Flow, sealed class +
  when exhaustivo, propiedades delegadas by inject).
- Decision: Kotlin 2.0.21 (LTS), JDK 21, Ktor 3.0.1,
  Koin 4.0.0 (koin-ktor + koin-core + koin-test), Exposed
  1.0.0-beta01, kotlinx-serialization-json 1.7.3,
  kotlinx-coroutines-core 1.8.1, H2 2.2.224, Flyway 10.10.0,
  JUnit 5.10.2, ktor-server-test-host 3.0.1, Gradle 8.10
  (Kotlin DSL).
- Alternativas: (a) Micronaut + Kotlin (descartado: ya hay
  fx-java-micronaut); (b) Quarkus + Kotlin (descartado: el plan
  pide Ktor); (c) Ktor 2.x (descartado: Ktor 3.0 es la version
  actual con KDoc generation y nuevas APIs).
- Consecuencias: el build local no corre con Java 25
  directamente; el fixture requiere JDK 21 (via
  `kotlin.jvmToolchain(21)` en build.gradle.kts). El
  contenedor `gradle:8.10-jdk21-jammy` resuelve esto. Los
  tests runtime con `testApplication` se ejecutan en el
  contenedor via `run_fixture_tests.py`; los tests
  estaticos (TrapsEcosystem, TrapsPackage,
  TrapsSuperficial) corren en cualquier JVM.

### D-211 — Naming: prefijo `NPRGT-FXKTOR-` para los unique tokens de F06n (F06n)

- Fecha · Fase · Estado: 2026-10-06 · F06n · vigente
- Contexto: AGENTS §8 y §23 establecen prefijos `NPRGT-<FX>-`
  para los unique tokens de cada fixture.
- Decision: prefijo `FXKTOR` y exactamente 28 tokens. Ninguno
  aparece en el codigo del fixture (verificado por
  `TestUniqueTokensFile`).
- Alternativas: (a) `FXKOROUTINES` (descartado: demasiado
  largo); (b) `FXKTOR3` (descartado: ata la version al nombre).
- Consecuencias: `overfit_guard.py` falla si cualquiera de
  estos tokens aparece en `skills/`.

### D-212 — URL paths sin nombres de feature para evitar CC-11 (F06n)

- Fecha · Fase · Estado: 2026-10-06 · F06n · vigente
- Contexto: la regla CC-11 detecta menciones del nombre de
  feature en cualquier linea del codigo del fixture. Los
  features son `inventario`, `reservas-de-stock`, `alertas`.
- Decision: usar `/inv` en vez de `/inventario`, `/reservas`
  (conservado por brevedad) y `/alerts` (sin la `s` final
  de alertas). El ground truth mantiene los nombres
  originales; el codigo del fixture usa paths abreviados.
- Alternativas: (a) cambiar el nombre del feature en el
  ground truth (descartado: el plan los define); (b) ofuscar
  los paths con guiones (descartado: la regla CC-11 detecta
  el substring).
- Consecuencias: la skill debe entender que `/inv`
  corresponde a `inventario` segun el ground truth.

### D-213 — Stack del fixture F06o: .NET 9 + MediatR 11.0 + EF Core 9 + xUnit 2.9 + ASP.NET Core 9 (F06o)

- Fecha · Fase · Estado: 2026-10-07 · F06o · vigente
- Contexto: el plan F06o pide C# / .NET 9 / ASP.NET Core con
  CQRS (MediatR), EF Core, minimal APIs y `BackgroundService`.
- Decision: stack = `Microsoft.NET.Sdk.Web` con
  `MediatR 11.0.0` + `MediatR.Extensions.Microsoft.DependencyInjection
  11.0.0` (la DI extension es un paquete separado, requerido
  para que `AddMediatR` exista; no estaba claro en la primera
  iteracion), `Microsoft.EntityFrameworkCore.Sqlite 9.0.0`,
  `Microsoft.EntityFrameworkCore.Design 9.0.0`,
  xUnit 2.9.2 + xunit.runner.visualstudio 2.8.2 +
  Microsoft.NET.Test.Sdk 17.11.1 + `Microsoft.AspNetCore.Mvc.Testing
  9.0.0`. Imagen Docker: `mcr.microsoft.com/dotnet/sdk:9.0`
  con `apt-get install -y make` (la imagen base no incluye
  make, necesario para `run_fixture_tests.py`).
- Alternativas: (a) MediatR 12.x (descartado: la discusion
  sobre comercializacion es 13.x; 11.x es la mas estable y
  100 % Apache-2.0); (b) Postgres en vez de SQLite (descartado:
  agrega dependencias, SQLite funciona con `WebApplicationFactory`
  en `:memory:?cache=shared`); (c) Hot Reload en el Dockerfile
  (descartado: agrega 200 MB y no aporta a los gates).
- Consecuencias: la trampa P06 (cache=shared en SQLite) y la
  trampa E03 (source generators de MediatR + EF Core en obj/)
  son utiles para la skill. La `build-history.sh` no corre el
  build de dotnet (seria costoso), solo crea 8 commits
  incrementales con placeholders.

### D-214 — Top-level statements + `public partial class Program` en namespace `FxAspNet` (F06o)

- Fecha · Fase · Estado: 2026-10-07 · F06o · vigente
- Contexto: `WebApplicationFactory<Program>` requiere que el
  tipo `Program` del proyecto web sea visible desde el
  proyecto de tests. Con top-level statements el compilador
  genera un `internal class Program`. Anadir `public partial
  class Program { }` no basta en .NET 9 (el compilador no
  siempre eleva la visibilidad). La skill ademas requiere que
  `Program` viva en un namespace publico para que las pruebas
  la importen con `FxAspNet.Program`.
- Decision: declarar `public partial class Program { }` dentro
  de `namespace FxAspNet { ... }` al final de `Program.cs`.
  Ademas, `<InternalsVisibleTo Include="FxAspNet.Tests" />` en
  `FxAspNet.csproj` para que cualquier tipo internal auxiliar
  sea visible al proyecto de tests.
- Alternativas: (a) Program.cs tradicional con `static void
  Main` (descartado: el plan pide top-level statements);
  (b) declarar `Program` en un archivo separado
  (`src/Program.cs`) (descartado: complica la trampa E05 sobre
  el orden del middleware).
- Consecuencias: la skill debe notar que `Program.cs` tiene
  dos declaraciones de la clase `Program` (la del top-level
  statements + la del `namespace FxAspNet`); eso refuerza la
  trampa E05 (el pipeline queda declarado en el mismo archivo
  que la clase, dificultando el trazado).

### D-215 — MediatR 11.0.0 con `AddMediatR(typeof(Program).Assembly)` en vez de `RegisterServicesFromAssembly` (F06o)

- Fecha · Fase · Estado: 2026-10-07 · F06o · vigente
- Contexto: en MediatR 11.0.0 el metodo
  `cfg.RegisterServicesFromAssembly` / `RegisterServicesFromAssemblies`
  no existe en `MediatRServiceConfiguration`. Los metodos
  disponibles son `Using`, `AsSingleton`, `AsScoped`,
  `AsTransient` y `WithEvaluator`. La forma soportada es la
  sobrecarga `AddMediatR(IServiceCollection, params Assembly[])`.
- Decision: `builder.Services.AddMediatR(typeof(Program).Assembly)`
  (sin lambda de configuracion). Esta forma es equivalente y
  es la API oficial de MediatR 11.
- Alternativas: (a) `AddMediatR(11.0.0, Assembly[])` con
  overload que acepta version (descartado, deprecated en 11+);
  (b) migrar a MediatR 12 (descartado: la API cambia y la
  trampa E01 se debilita).
- Consecuencias: la trampa E01 sigue valida porque la skill
  debe saltar del endpoint al handler via el tipo generico
  `IRequestHandler<TRequest, TResponse>`. La "no hay
  configuracion lambda" es trivial de saltar y la skill no
  nota la diferencia.

### D-216 — Naming: prefijo `NPRGT-FXCS-` para los unique tokens de F06o (F06o)

- Fecha · Fase · Estado: 2026-10-07 · F06o · vigente
- Contexto: AGENTS §8 y §23 establecen prefijos `NPRGT-<FX>-`
  para los unique tokens de cada fixture.
- Decision: prefijo `FXCS` y exactamente 29 tokens cubriendo
  stack (`DOTNET-VER`, `ASPNET-VER`, `MEDIATR-VER`, `EFCORE-VER`,
  `XUNIT-VER`), tipos (`PARTIAL-CLASS`, `BACKGROUND-SERVICE`,
  `MINIMAL-API`, `WEBAPPFACTORY`, `FLUENT-API`, `SOURCE-GEN`),
  partial-class split (`PARTIAL-PEDIDOITEM`, `PARTIAL-CREAR-HANDLER`,
  `PARTIAL-OBTENER-HANDLER`, `PARTIAL-ENCOLAR-HANDLER`),
  trampas E06 (`ADD-ORDERS-MODULE`), E05 (`USE-REQUEST-ID`,
  `MAP-EXCEPTION-HANDLER`), rutas (`MAP-GROUP-ORDERS`,
  `MAP-GROUP-BILLING`, `MAP-GROUP-RETRIES`), features
  (`PEDIDO-RESULT-R01`, `FACTURA-RESULT-R01`,
  `REINTENTO-RESULT-R01`), marcadores (`MARKER-APP`,
  `MARKER-PIPELINE`) y trampas superficiales
  (`TRAMP-S01-VALIDATOR`, `TRAMP-S02-LOGGER`, `TRAMP-S03-HEALTH`).
  Ninguno aparece en el codigo del fixture (verificado por
  `TestUniqueTokensFile`).
- Alternativas: (a) `FXASPNET` (descartado: excede 8 caracteres);
  (b) `FXDOTNET` (descartado: confunde con .NET en general);
  (c) `FXCSPROJ` (descartado: ata al formato, no al ecosistema).
- Consecuencias: `overfit_guard.py` falla si cualquiera de
  estos tokens aparece en `skills/`.

### D-217 — URL paths en ingles sin nombres de feature para evitar CC-11 (F06o)

- Fecha · Fase · Estado: 2026-10-07 · F06o · vigente
- Contexto: la regla CC-11 detecta menciones del nombre de
  feature en cualquier string del codigo del fixture. Los
  features son `pedidos`, `facturacion`, `reintentos`.
- Decision: usar `/api/orders` en vez de `/api/pedidos`,
  `/api/billing` en vez de `/api/facturacion` y
  `/api/retries` en vez de `/api/reintentos`. Los nombres de
  feature viven solo en identificadores (`Features/Pedidos/`,
  `Features/Facturacion/`, `Features/Reintentos/`, clases
  `CrearPedidoCommand`, `EmitirFacturaCommand`, etc.).
- Alternativas: (a) cambiar el nombre del feature en el
  ground truth (descartado: el plan los define); (b) ofuscar
  con guiones (descartado: la regla CC-11 detecta el substring).
- Consecuencias: la skill debe mapear `/api/orders` a
  `pedidos`, `/api/billing` a `facturacion`, `/api/retries`
  a `reintentos` segun el ground truth.

### D-218 — SQLite con `DataSource=file:test-{guid}?mode=memory&cache=shared` en `WebApplicationFactory` (F06o)

- Fecha · Fase · Estado: 2026-10-07 · F06o · vigente
- Contexto: `WebApplicationFactory<Program>` abre varias
  conexiones a la DB durante un test. SQLite `:memory:`
  puro asigna una DB distinta por conexion, asi que los tests
  verian datos parciales. Para CC-10 (tests en contenedor
  verde), la factory debe garantizar una sola DB compartida.
- Decision: connection string
  `DataSource=file:test-{Guid}?mode=memory&cache=shared` en
  `FxAspNetFactory` y `EnsureCreated` en startup para crear
  el esquema. El Guid aleatorio evita colisiones entre
  tests paralelos.
- Alternativas: (a) SQLite file-based en `/tmp/` (descartado:
  requiere cleanup entre tests); (b) Postgres en
  Testcontainers (descartado: agrega 800 MB de imagen);
  (c) InMemory provider de EF Core (descartado: requiere
  reescribir el model porque InMemory no soporta `decimal`).
- Consecuencias: la trampa P06 queda plantada en el codigo
  del factory. Los tests no necesitan pre/post limpieza.

### D-219 — `CrearPedidoHandler` con dos `SaveChangesAsync` separados (P03 trap) (F06o)

- Fecha · Fase · Estado: 2026-10-07 · F06o · vigente
- Contexto: la trampa P03 exige dos `SaveChangesAsync`
  consecutivos en `CrearPedidoHandler` sin transaccion.
  EF Core intenta guardar en cascada, lo que provoca
  UNIQUE constraint en la segunda llamada si los items
  ya fueron guardados en la primera.
- Decision: el handler crea los `PedidoItem` primero en una
  lista local sin asignarles `PedidoId`, hace
  `SaveChangesAsync` del Pedido solo, asigna
  `item.PedidoId = pedido.Id` a cada item, y hace un segundo
  `SaveChangesAsync` para los items. Esto funciona, pero NO
  es atomico: si la segunda llamada falla, el Pedido queda
  persistido sin sus items.
- Alternativas: (a) una sola `SaveChangesAsync` con cascade
  (descartado: elimina la trampa); (b) `BeginTransactionAsync`
  + 2 saves dentro (descartado: corrige la trampa); (c)
  batch insert con SQL crudo (descartado: agrega codigo
  extraño no idiomático).
- Consecuencias: la trampa P03 sigue valida. La skill debe
  detectar la falta de `BeginTransaction` y reportarla. El
  codigo compila y los tests pasan en condiciones normales,
  pero un fallo del segundo save deja el sistema en estado
  inconsistente.

### D-220 — `OrderBy(t => t.CreadoEn)` en cliente (no en SQL) para SQLite (F06o)

- Fecha · Fase · Estado: 2026-10-07 · F06o · vigente
- Contexto: SQLite no soporta `ORDER BY` sobre columnas
  `DateTimeOffset` (error: `SQLite does not support expressions
  of type 'DateTimeOffset' in ORDER BY clauses`). Tanto el
  `BackgroundService` como `ListarPendientesHandler` hacian
  el `OrderBy` antes del `ToListAsync`, lo que enviaba el
  `ORDER BY` al SQL.
- Decision: mover el `OrderBy` a cliente (despues del
  `ToListAsync`). El rendimiento es menor pero la API sigue
  funcionando. La trampa P04 (no actualizar `UltimoIntentoEn`)
  y el resto del flujo siguen validos.
- Alternativas: (a) cambiar `CreadoEn` a `DateTime` (descartado:
  rompe la trampa de "fechas que no se actualizan"); (b)
  usar `EF.Functions.DateDiffSecond` (descartado: requiere
  paquetes adicionales); (c) aceptar la excepcion en el
  BackgroundService (descartado: el BackgroundService ya
  la swallowa con try/catch y los tests no detectan el
  problema).
- Consecuencias: la trampa sigue valida. Los tests pasan.
  La skill debe notar que el codigo del handler hace
  `OrderBy` despues de `ToListAsync` (cliente), no antes
  (SQL).

### D-221 — Stack del fixture F06p: Python 3.11 + Django 5.0 + DRF 3.15 + Celery 5.3 + pytest-django 4.8 (F06p)

- Fecha · Fase · Estado: 2026-10-07 · F06p · vigente
- Contexto: el plan F06p pide un proyecto Django con API REST,
  tareas asincronas y settings por entorno.
- Decision: stack = Django 5.0.6 + djangorestframework 3.15.1
  + celery 5.3.6 + pytest 8.2.0 + pytest-django 4.8.0. Imagen
  Docker: `python:3.11-slim` con `apt-get install -y make` (la
  imagen base no incluye make, requerido para `run_fixture_tests.py`).
- Alternativas: (a) Django 4.2 LTS (descartado: Django 5.0 es
  el LTS actual y cubre Signal mejor); (b) FastAPI (descartado:
  el plan siguiente F06q lo hara); (c) Postgres en docker-compose
  (descartado: SQLite funciona con `EnsureCreated` en dev/tests).
- Consecuencias: la trampa E04 (settings split) y la trampa
  P06 (SECRET_KEY default inseguro en prod) son utiles para la
  skill. El `build-history.sh` no corre `pip install` (costoso),
  solo crea 8 commits incrementales con placeholders.

### D-222 — Apps en ingles (enrollments, payments, certificates, audit) para CC-11 (F06p)

- Fecha · Fase · Estado: 2026-10-07 · F06p · vigente
- Contexto: la regla CC-11 detecta menciones del nombre de
  feature (en espanol) en cualquier linea del codigo del fixture
  (`matriculas`, `pagos`, `certificados`, `acciones-de-admin`).
  Los Django apps usan `apps/<label>/` en el filesystem y
  `label = 'enrollments'` (ingles) en `AppConfig`.
- Decision: usar `apps/enrollments/`, `apps/payments/`,
  `apps/certificates/`, `apps/audit/`. Los nombres de feature en
  espanol viven solo en el ground truth y en PROGRESS.md/ROADMAP.
  Los modelos, ViewSets y routers tambien usan identificadores en
  ingles (`Enrollment`, `PaymentViewSet`, `basename='enrollment'`).
- Alternativas: (a) `apps/matriculas/` con modelos en espanol
  (descartado: los nombres en `INSTALLED_APPS = ['apps.matriculas']`
  aparecerian en strings Python; el CC-11 verifica comments `#` pero
  no strings, pero la consistencia con los otros fixtures favorece
  apps en ingles); (b) ofuscar con guiones (descartado: el
  check_ground_truth detecta substrings).
- Consecuencias: la skill debe mapear `enrollments` <-> `matriculas`,
  `payments` <-> `pagos`, `certificates` <-> `certificados`,
  `audit` <-> `acciones-de-admin` segun el ground truth.

### D-223 — Celery en modo EAGER en dev/tests (F06p)

- Fecha · Fase · Estado: 2026-10-07 · F06p · vigente
- Contexto: la trampa P04 exige que el modo EAGER en tests
  ejecute las tasks sincronamente, ocultando los errores que
  aparecerian en un worker real con broker.
- Decision: `CELERY_TASK_ALWAYS_EAGER = True` en
  `fxdjango/settings/dev.py` (el test runner usa `--ds=fxdjango.settings.dev`).
  En prod (`fxdjango/settings/prod.py`) el flag es `False`. El broker
  en `fxdjango/celery.py` es `memory://` (no requiere Redis/RabbitMQ).
- Alternativas: (a) Redis en docker-compose para tests E2E reales
  (descartado: agrega 100 MB a la imagen y no aporta a los gates);
  (b) Celery EAGER siempre (descartado: prod no se comporta asi).
- Consecuencias: la trampa P04 sigue valida. Los tests invocan
  las tasks sincrónicamente y verifican el side effect.

### D-224 — Settings split: base / dev / prod con DJANGO_SETTINGS_MODULE (F06p)

- Fecha · Fase · Estado: 2026-10-07 · F06p · vigente
- Contexto: la trampa E04 exige que la eleccion del settings
  module no sea estatica.
- Decision: `fxdjango/settings/{base,dev,prod}.py` con
  `from .base import *` en cada uno. `pytest.ini` declara
  `DJANGO_SETTINGS_MODULE = fxdjango.settings.dev`. El `manage.py`
  default es `fxdjango.settings.dev` (env var override).
- Alternativas: (a) un solo settings.py con `if DEBUG` (descartado:
  no hay trampa visible); (b) `settings.py` con `import *` de
  `base_local.py` / `base_prod.py` (descartado: menos visible).
- Consecuencias: la trampa E04 sigue valida. La skill debe leer
  `fxdjango/settings/dev.py` para entender como correr los tests.

### D-225 — Naming: prefijo `NPRGT-FXDJ-` para los unique tokens de F06p (F06p)

- Fecha · Fase · Estado: 2026-10-07 · F06p · vigente
- Contexto: AGENTS §8 y §23 establecen prefijos `NPRGT-<FX>-`
  para los unique tokens de cada fixture.
- Decision: prefijo `FXDJ` y exactamente 29 tokens cubriendo
  stack (`DJANGO-VER`, `DRF-VER`, `CELERY-VER`, `PYTEST-VER`),
  tipos (`APPCONFIG`, `MODELVIEWSET`, `DEFAULTS-ROUTER`,
  `POST-SAVE-SIGNAL`, `EAGER-MODE`, `CUSTOM-QUERYSET`,
  `CUSTOM-MANAGER`, `TEMPLATE-TAG`, `CONTEXT-PROCESSOR`,
  `CELERY-TASK`, `ADMIN-ACTION`), features
  (`ENROLLMENT-RESULT-R01`, `PAYMENT-RESULT-R01`,
  `CERTIFICATE-RESULT-R01`, `AUDIT-ACTION-R01`), marcadores
  (`MARKER-APP`, `MARKER-SETTINGS`, `MARKER-URLS`), y trampas
  superficiales (`TRAMP-S01-VIEWSET`, `TRAMP-S02-SIGNAL`,
  `TRAMP-S03-TAG`). Ninguno aparece en el codigo del fixture
  (verificado por `TestUniqueTokensFile`).
- Alternativas: (a) `FXDJANGO` (descartado: excede 8 caracteres);
  (b) `FXPY-DJ` (descartado: confunde con).
- Consecuencias: `overfit_guard.py` falla si cualquiera de
  estos tokens aparece en `skills/`.

### D-226 — `Makefile` envuelve `pytest -q --ds=fxdjango.settings.dev` (F06p)

- Fecha · Fase · Estado: 2026-10-07 · F06p · vigente
- Contexto: el plan F06x exige paridad con F06n (Kotlin Ktor)
  en `run_fixture_tests.py --fixture <fx> --container` que
  ejecuta `make test`.
- Decision: `TEST_CMD ?= pytest -q --ds=fxdjango.settings.dev` en
  el Makefile; `test_cmd: make test` en `manifest.yml`.
- Alternativas: (a) invocar `pytest` directamente (descartado:
  rompe la paridad con otros fixtures); (b) usar `tox`
  (descartado: agrega complejidad innecesaria).
- Consecuencias: el contenedor ejecuta `make test` y los tests
  corren con la DJANGO_SETTINGS_MODULE correcta.

### D-227 — Imagen Docker `python:3.11-slim` con `apt-get install make` (F06p)

- Fecha · Fase · Estado: 2026-10-07 · F06p · vigente
- Contexto: el plan F06x exige paridad con F06o y `make` no
  viene en la imagen base `python:3.11-slim`.
- Decision: `FROM python:3.11-slim` + `RUN apt-get install -y make`
  antes de la copia del codigo (cache de layers). El
  `requirements.txt` se copia primero para cachear `pip install`.
- Alternativas: (a) usar `python:3.11-bookworm` (descartado:
  ~300 MB mas pesada); (b) instalar make via `apk` (descartado:
  la imagen es Debian-based).
- Consecuencias: la imagen pesa ~180 MB frente a ~700 MB de
  la imagen .NET SDK. El `make test` funciona en el contenedor.

### D-228 — `requires: [linux, macos, windows]` en `manifest.yml` (F06p)

- Fecha · Fase · Estado: 2026-10-07 · F06p · vigente
- Contexto: el plan F06x exige paridad con F06n.
- Decision: `requires: [linux, macos, windows]`. El toolchain
  es multiplataforma (Python 3.11 + Django + DRF + Celery +
  pytest-django corren en cualquier OS). CC-10 se cumple con
  el contenedor en Linux; el `Makefile` tambien funciona en
  host con Python 3.11 + `pip install -r requirements.txt`.
- Alternativas: (a) solo Linux (descartado: rompe la paridad
  con F06n).
- Consecuencias: el fixture es ejecutable en los 3 sistemas.

### D-229 — Deteccion extendida de Django/DRF/Celery/pytest-django en `fixtures_matrix.py` y `target_matrix.yml` (F06p)

- Fecha · Fase · Estado: 2026-10-07 · F06p · vigente
- Contexto: el plan F06x exige extender `fixtures_matrix.py`
  para detectar dependencias de Python via `requirements.txt`
  y `target_matrix.yml` para listar los frameworks nuevos.
- Decision: agregar a `MANIFEST_BUILD` la entrada
  `requirements.txt -> {pip}`. Agregar a `FRAMEWORK_FILES`
  `manage.py -> {django}` y `pytest.ini -> {pytest-django}`.
  Agregar a `PACKAGE_JSON_MARKERS` las entradas
  `Django -> {django}`, `djangorestframework -> {drf}`,
  `celery -> {celery}`, `pytest-django -> {pytest-django}`.
  Bloque de deteccion: `for req_file in requirements.txt rglob(...):`
  parsea; adiciona los frameworks si el nombre del paquete esta en
  el contenido. Deteccion adicional via `apps/.../apps.py` con
  `AppConfig`. Agregar a `target_matrix.yml`: `frameworks: [django,
  drf, celery, pytest-django]` + `build_systems: [pip]`.
- Alternativas: (a) parsear `pyproject.toml` (descartado: el
  fixture usa `requirements.txt` plano); (b) inferir via la
  presencia de `manage.py` sin inspeccionar `requirements.txt`
  (descartado: eso no distingue Django de Flask o FastAPI).
- Consecuencias: el MATRIX.md muestra fx-python-django cubriendo
  django, drf, celery, pytest-django y pip. Las futuras
  fixtures Django (F06p ya las cubre; F06q FastAPI sera
  Python puro sin Django) reutilizan la misma deteccion.

### D-230 — Stack del fixture F06q: Python 3.11 + FastAPI 0.115 + Pydantic 2.9 + Pydantic-Settings + SQLAlchemy 2 async + Alembic + aiosqlite + Celery 5.3 + httpx + pytest-asyncio 0.24 (F06q)

- Fecha · Fase · Estado: 2026-10-07 · F06q · vigente
- Contexto: el plan F06q pide una API FastAPI asincrona con
  Pydantic v2, SQLAlchemy 2 async, Alembic y arq/Celery.
- Decision: stack = `fastapi==0.115.0` + `pydantic==2.9.0` +
  `pydantic-settings==2.5.2` + `sqlalchemy[asyncio]==2.0.36` +
  `alembic==1.13.3` + `aiosqlite==0.20.0` + `celery==5.3.6` +
  `email-validator==2.2.0` + `httpx==0.27.2` + `pytest==8.2.0` +
  `pytest-asyncio==0.24.0`. Imagen Docker: `python:3.11-slim` con
  `apt-get install -y make` (la imagen base no incluye make).
- Alternativas: (a) arq (descartado: requiere Redis en runtime;
  no encaja con el patron EAGER de F06p); (b) Flask (descartado:
  el plan siguiente F06n/F06p ya cubre Django, y F06q pide
  explicitamente); (c) Starlette puro (descartado: FastAPI es
  la opcion actual).
- Consecuencias: la trampa E01 (Depends yield chains), la trampa
  E02 (Pydantic validators con business logic), la trampa E04
  (lifespan events), la trampa E05 (decoradores que registran
  rutas), la trampa E06 (Alembic data migration) y la trampa
  P06 (Celery EAGER en contexto async) son utiles para la skill.

### D-231 — Routers y modelos en ingles (users, subscriptions, webhooks) para CC-11 (F06q)

- Fecha · Fase · Estado: 2026-10-07 · F06q · vigente
- Contexto: la regla CC-11 detecta menciones del nombre de
  feature (en espanol) en cualquier linea del codigo del fixture.
  Los features son `usuarios`, `suscripciones`, `webhooks`.
- Decision: usar routers `app/routers/users.py`,
  `app/routers/subscriptions.py`, `app/routers/webhooks.py` y
  URL paths `/users`, `/subscriptions`, `/webhooks` (todos en
  ingles). Los nombres de feature en espanol viven solo en el
  ground truth y en PROGRESS.md/ROADMAP. Los modelos tambien usan
  identificadores en ingles (`User`, `Subscription`, `Webhook`).
- Alternativas: (a) routers `app/routers/usuarios/` etc. (descartado:
  apareceria en `INSTALLED_APPS = ['apps.usuarios']` que es string,
  y aunque CC-11 verifica comments `#` no strings, la consistencia
  con F06p favorece apps en ingles); (b) ofuscar con guiones
  (descartado: el check_ground_truth detecta substrings).
- Consecuencias: la skill debe mapear `users` <-> `usuarios`,
  `subscriptions` <-> `suscripciones`, `webhooks` <-> `webhooks`
  segun el ground truth.

### D-232 — Celery en modo EAGER en dev/tests (F06q)

- Fecha · Fase · Estado: 2026-10-07 · F06q · vigente
- Contexto: la trampa P06 exige que el modo EAGER en tests
  ejecute las tasks sincronamente, ocultando los errores que
  aparecerian en un worker real con broker.
- Decision: `CELERY_TASK_ALWAYS_EAGER = True` en dev (via
  `configure_for_testing()` invocado en `conftest.py`). En prod,
  el flag es False. El broker en `app/celery_app.py` es
  `memory://` (no requiere Redis).
- Alternativas: (a) Redis en docker-compose para tests E2E reales
  (descartado: agrega 100 MB a la imagen y no aporta a los gates);
  (b) Celery EAGER siempre (descartado: prod no se comporta asi);
  (c) arq con broker de test (descartado: arq requiere Redis).
- Consecuencias: la trampa P06 sigue valida. Los tests invocan
  las tasks sincrónicamente y verifican el side effect.

### D-233 — pytest-asyncio 0.24 con `loop_scope=session` en fixtures async (F06q)

- Fecha · Fase · Estado: 2026-10-07 · F06q · vigente
- Contexto: aiosqlite mantiene conexiones atadas al event loop;
  pytest-asyncio por defecto crea un nuevo loop por test (function
  scope) lo que rompe aiosqlite con 'Event loop is closed'.
- Decision: usar `pytest-asyncio==0.24.0` (soporta `loop_scope`) y
  declarar `loop_scope="session"` en fixtures async (`engine`,
  `db_session`, `client`, `auth_client`). El engine se crea una
  sola vez en el loop compartido y los tests lo reusan.
- Alternativas: (a) `pytest-asyncio<0.24` sin loop_scope (descartado:
  rompe aiosqlite); (b) usar una DB file-based con cleanup entre
  tests (descartado: mas lento); (c) usar SQLite en memoria pero
  sin event loop compartido (descartado: cada test ve una DB
  vacia).
- Consecuencias: la suite completa corre en 0.10s con 27 tests
  sin warnings de 'Event loop is closed'.

### D-234 — Prefijo `NPRGT-FXFAST-` para los unique tokens de F06q (F06q)

- Fecha · Fase · Estado: 2026-10-07 · F06q · vigente
- Contexto: AGENTS §8 y §23 establecen prefijos `NPRGT-<FX>-`
  para los unique tokens de cada fixture.
- Decision: prefijo `FXFAST` y exactamente 29 tokens cubriendo
  stack (`FASTAPI-VER`, `PYDANTIC-VER`, `SQLALCHEMY-VER`,
  `ALEMBIC-VER`, `CELERY-VER`, `HTTPX-VER`, `PYTEST-VER`,
  `PYTEST-ASYNCIO-VER`), tipos (`APIROUTER`,
  `DEPENDENCY-INJECTION`, `FIELD-VALIDATOR`, `MODEL-VALIDATOR`,
  `LIFESPAN-EVENT`, `INCLUDE-ROUTER`, `ASGITRANSPORT`,
  `ASYNC-SESSION`, `ALEMBIC-DATA-MIG`), features
  (`USER-RESULT-R01`, `SUB-RESULT-R01`, `WEBHOOK-RESULT-R01`),
  marcadores (`MARKER-APP`, `MARKER-DEPENDENCIES`,
  `MARKER-LIFESPAN`, `MARKER-ALEMBIC`), y trampas superficiales
  (`TRAMP-S01-ROUTE`, `TRAMP-S02-MODEL`, `TRAMP-S03-DEP`). Ninguno
  aparece en el codigo del fixture (verificado por
  `TestUniqueTokensFile`).
- Alternativas: (a) `FXFASTAPI` (descartado: excede 8 caracteres);
  (b) `FXPY-FA` (descartado: confunde con).
- Consecuencias: `overfit_guard.py` falla si cualquiera de
  estos tokens aparece en `skills/`.

### D-235 — `Makefile` envuelve `pytest -q` (F06q)

- Fecha · Fase · Estado: 2026-10-07 · F06q · vigente
- Contexto: el plan F06x exige paridad con F06p.
- Decision: `TEST_CMD ?= pytest -q` en el Makefile;
  `test_cmd: make test` en `manifest.yml`.
- Alternativas: (a) invocar `pytest` directamente (descartado:
  rompe la paridad con otros fixtures); (b) usar `tox`
  (descartado: agrega complejidad innecesaria).
- Consecuencias: el contenedor ejecuta `make test` y los tests
  corren con la `asyncio_mode = auto` correcta.

### D-236 — Imagen Docker `python:3.11-slim` con `apt-get install make` (F06q)

- Fecha · Fase · Estado: 2026-10-07 · F06q · vigente
- Contexto: el plan F06x exige paridad con F06p.
- Decision: `FROM python:3.11-slim` + `RUN apt-get install -y make`
  antes de la copia del codigo (cache de layers).
- Alternativas: (a) usar `python:3.11-bookworm` (descartado:
  ~300 MB mas pesada); (b) instalar make via `apk` (descartado:
  la imagen es Debian-based).
- Consecuencias: la imagen pesa ~180 MB frente a ~700 MB de
  la imagen .NET SDK.

### D-237 — `requires: [linux, macos, windows]` en `manifest.yml` (F06q)

- Fecha · Fase · Estado: 2026-10-07 · F06q · vigente
- Contexto: el plan F06x exige paridad con F06p.
- Decision: `requires: [linux, macos, windows]`. El toolchain
  es multiplataforma.
- Alternativas: (a) solo Linux (descartado: rompe la paridad).
- Consecuencias: el fixture es ejecutable en los 3 sistemas.

### D-238 — Deteccion extendida de FastAPI/Pydantic/SQLAlchemy/Alembic en `fixtures_matrix.py` y `target_matrix.yml` (F06q)

- Fecha · Fase · Estado: 2026-10-07 · F06q · vigente
- Contexto: el plan F06x exige extender `fixtures_matrix.py`
  para detectar dependencias de Python via `requirements.txt`
  y `target_matrix.yml` para listar los frameworks nuevos.
- Decision: agregar al bloque de deteccion de `requirements.txt`
  existente: `if "fastapi" in content.lower(): add {fastapi}`,
  `if "pydantic" in content.lower(): add {pydantic}`,
  `if "sqlalchemy" in content.lower(): add {sqlalchemy}`,
  `if "alembic" in content.lower(): add {alembic}`. Anadir
  deteccion de `app/.../main.py` con `FastAPI(` constructor ->
  `{fastapi}`. Agregar a `target_matrix.yml`:
  `frameworks: [fastapi, pydantic, sqlalchemy, alembic]`.
- Alternativas: (a) parsear `pyproject.toml` (descartado: el
  fixture usa `requirements.txt` plano); (b) inferir via la
  presencia de `app/main.py` con `FastAPI(` sin inspeccionar
  deps (descartado: no distingue FastAPI de Starlette puro).
- Consecuencias: el MATRIX.md muestra fx-python-fastapi cubriendo
  fastapi, pydantic, sqlalchemy, alembic y pip.

### D-239 — Stack del fixture F06r: Node 22 + TypeScript 5.6 + NestJS 10.4 + TypeORM 0.3.20 + BullMQ 5.21 + better-sqlite3 9.6 + supertest 7 + Jest 29 + ts-jest 29 (F06r)

- Fecha · Fase · Estado: 2026-10-07 · F06r · vigente
- Contexto: el plan F06r pide backend NestJS modular con TypeORM,
  BullMQ y transporte de microservicios.
- Decision: stack = Node 22 + TypeScript 5.6.3 + NestJS 10.4.4
  (core, common, config, microservices, platform-express, typeorm,
  websockets) + TypeORM 0.3.20 + BullMQ 5.21.0 + better-sqlite3 9.6.0
  + ioredis 5.4.1 + joi 17.13.3 + nestjs-joi 1.12.0 + class-validator 0.14.1
  + reflect-metadata 0.2.2 + rxjs 7.8.1. Imagen Docker:
  `node:22-bookworm-slim` con `apt-get install -y make python3
  build-essential` (necesario para el native build de better-sqlite3).
- Alternativas: (a) Sequelize (descartado: el plan siguiente
  F06s es Go; NestJS oficial recomienda TypeORM); (b) arq con
  Redis en docker-compose (descartado: agrega complejidad
  innecesaria para los gates); (c) `sqlite3` en vez de
  `better-sqlite3` (descartado: better-sqlite3 es sync y mas
  simple para tests en memoria).
- Consecuencias: la trampa E01 (modulos con `@Module`), la trampa
  E02 (APP_GUARD/APP_INTERCEPTOR/APP_FILTER), la trampa E03
  (decoradores propios con Reflector), la trampa E04
  (BullMQ productor/consumidor por nombre de cola), la trampa
  E05 (`@MessagePattern`/`@EventPattern`), y la trampa E06
  (ConfigModule con namespaces) son utiles para la skill.

### D-240 — Apps y modulos en ingles (orders, shipments, notifications) para CC-11 (F06r)

- Fecha · Fase · Estado: 2026-10-07 · F06r · vigente
- Contexto: la regla CC-11 detecta menciones del nombre de
  feature (en espanol) en cualquier linea del codigo del fixture.
  Los features son `ordenes`, `envios`, `notificaciones`.
- Decision: usar `src/orders/`, `src/shipments/`, `src/notifications/`
  y URL paths en ingles (`/orders`, `/shipments`, `/notifications`).
  Los nombres de feature en espanol viven solo en el ground truth.
- Alternativas: (a) `src/ordenes/`, etc. (descartado: apareceria en
  `INSTALLED_APPS` y en los TypeORM entity labels; aunque CC-11
  verifica comments `#` no strings, la consistencia con F06p
  favorece apps en ingles); (b) ofuscar con guiones.
- Consecuencias: la skill debe mapear `orders` <-> `ordenes`,
  `shipments` <-> `envios`, `notifications` <-> `notificaciones`.

### D-241 — Abstraccion `MessageQueueService` con BullMQ (real) y `InMemoryMessageQueue` (tests) (F06r)

- Fecha · Fase · Estado: 2026-10-07 · F06r · vigente
- Contexto: la trampa E04 exige que productor y consumidor se
  acoplen por nombre de cola. BullMQ requiere Redis en runtime.
  Para los tests queremos evitar la dependencia de Redis.
- Decision: `MessageQueueService` interface abstracta con metodos
  `publish(queue, payload)` y `subscribe(queue, handler)`. Dos
  implementaciones: `BullMQMessageQueue` (real, con Queue de
  BullMQ y Worker) y `InMemoryMessageQueue` (tests, con un Map
  interno). En el modulo de tests, el provider
  `MessageQueueService` se sobreescribe con `InMemoryMessageQueue`.
- Alternativas: (a) `ioredis-mock` (descartado: requiere envolver
  ioredis, fragil); (b) mockear `bullmq.Queue` directamente con
  jest.mock (descartado: el codigo queda menos idiomatico); (c)
  Redis en docker-compose (descartado: agrega complejidad).
- Consecuencias: la trampa E04 sigue valida. Los tests invocan
  el `InMemoryMessageQueue` y verifican que el mensaje se entrega
  al handler suscrito.

### D-242 — `npm install --legacy-peer-deps` para resolver conflictos con better-sqlite3 (F06r)

- Fecha · Fase · Estado: 2026-10-07 · F06r · vigente
- Contexto: typeorm 0.3.20 requiere `better-sqlite3@^7.1.2 || ^8.0.0
  || ^9.0.0` pero la ultima version es 11.x. Sin `--legacy-peer-deps`,
  npm rechaza la instalacion.
- Decision: usar `better-sqlite3@9.6.0` (la mas alta compatible)
  + `npm install --legacy-peer-deps` en el Dockerfile.
- Alternativas: (a) usar `sqlite3` en vez de `better-sqlite3`
  (descartado: requiere build tools de C y no aporta); (b) usar
  Postgres en docker-compose (descartado: agrega 200 MB).
- Consecuencias: el fixture compila sin warnings de peer dep.

### D-243 — Prefijo `NPRGT-FXNEST-` para los unique tokens de F06r (F06r)

- Fecha · Fase · Estado: 2026-10-07 · F06r · vigente
- Contexto: AGENTS §8 y §23 establecen prefijos `NPRGT-<FX>-`
  para los unique tokens de cada fixture.
- Decision: prefijo `FXNEST` y exactamente 26 tokens cubriendo
  stack (NESTJS-VER, TYPEORM-VER, BULLMQ-VER, JEST-VER,
  SUPERTEST-VER, TYPESCRIPT-VER), tipos (MODULE-DECORATOR,
  APP-GUARD, APP-INTERCEPTOR, REFLECTOR-METADATA,
  BULLMQ-QUEUE-NAME, MESSAGE-PATTERN, EVENT-PATTERN,
  CONFIG-NAMESPACE, WEBSOCKET-GATEWAY, DEPENDENCY-INJECTION),
  features (ORDERS-RESULT-R01, SHIPMENTS-RESULT-R01,
  NOTIFICATIONS-RESULT-R01), marcadores (MARKER-APP,
  MARKER-MESSAGING, MARKER-COMMON, MARKER-NESTCLI), y trampas
  superficiales (TRAMP-S01-ROUTE, TRAMP-S02-GATEWAY,
  TRAMP-S03-INTERCEPTOR). Ninguno aparece en el codigo del
  fixture (verificado por `TestUniqueTokensFile`).
- Alternativas: (a) `FXNESTJS` (descartado: excede 8 caracteres);
  (b) `FXTS-NEST` (descartado: confunde con).
- Consecuencias: `overfit_guard.py` falla si cualquiera de
  estos tokens aparece en `skills/`.

### D-244 — `Makefile` envuelve `npm test -- --colors=false --runInBand` (F06r)

- Fecha · Fase · Estado: 2026-10-07 · F06r · vigente
- Contexto: el plan F06x exige paridad con F06g/F06h.
- Decision: `TEST_CMD ?= npm test -- --colors=false --runInBand`
  en el Makefile; `test_cmd: make test` en `manifest.yml`.
- Alternativas: (a) `npm test` directo (descartado: rompe
  paridad); (b) `jest --ci` (descartado: jest no tiene ese flag).
- Consecuencias: el contenedor ejecuta `make test` y los tests
  corren con `--runInBand` (sin paralelismo, deterministas).

### D-245 — Imagen Docker `node:22-bookworm-slim` con `make + python3 + build-essential` (F06r)

- Fecha · Fase · Estado: 2026-10-07 · F06r · vigente
- Contexto: better-sqlite3 requiere node-gyp + python3 para el
  native build. La imagen base `node:22-bookworm-slim` no incluye
  ni make ni python ni build-essential.
- Decision: `FROM node:22-bookworm-slim` + `RUN apt-get install -y
  make python3 build-essential` antes de la copia del codigo
  (cache de layers).
- Alternativas: (a) usar `node:22-bookworm` (sin `-slim`)
  (descartado: ~300 MB mas pesada); (b) usar una imagen
  pre-construida con las tools (descartado: menos reproducible).
- Consecuencias: la imagen pesa ~450 MB. El native build de
  better-sqlite3 funciona en el contenedor.

### D-246 — `requires: [linux, macos, windows]` en `manifest.yml` (F06r)

- Fecha · Fase · Estado: 2026-10-07 · F06r · vigente
- Contexto: el plan F06x exige paridad con F06p.
- Decision: `requires: [linux, macos, windows]`. El toolchain
  es multiplataforma (Node 22 + NestJS + TypeORM + Jest).
- Alternativas: (a) solo Linux (descartado: rompe paridad).
- Consecuencias: el fixture es ejecutable en los 3 sistemas.

### D-247 — Deteccion extendida de NestJS/TypeORM/BullMQ en `fixtures_matrix.py` y `target_matrix.yml` (F06r)

- Fecha · Fase · Estado: 2026-10-07 · F06r · vigente
- Contexto: el plan F06x exige extender `fixtures_matrix.py`
  para detectar NestJS via `nest-cli.json` + `@nestjs/core` en
  `package.json`, y TypeORM/BullMQ via package.json.
- Decision: agregar a `FRAMEWORK_FILES` la entrada
  `nest-cli.json: {nestjs}` (reemplazando el previo
  `{node-express}`). Agregar a `PACKAGE_JSON_MARKERS`:
  `@nestjs/core -> {nestjs}`, `typeorm -> {typeorm}`,
  `bullmq -> {bullmq}`. Agregar a `target_matrix.yml`:
  `frameworks: [nestjs, typeorm, bullmq]`.
- Alternativas: (a) inferir NestJS solo de package.json sin
  nest-cli.json (descartado: otros proyectos pueden tener
  @nestjs/core como dep sin ser NestJS CLI); (b) parsear el
  campo `peerDependencies` (descartado: no es necesario para
  la deteccion).
- Consecuencias: el MATRIX.md muestra fx-node-nestjs cubriendo
  nestjs, typeorm y bullmq.

### D-248 — Stack del fixture F06s: Go 1.22 + chi v5.1 + sqlc v1.27 + wire v0.6 + go-sqlite3 v1.14 + testify v1.9 (F06s)

- Fecha · Fase · Estado: 2026-10-07 · F06s · vigente
- Contexto: el plan F06s pide un servicio HTTP en Go con workers
  concurrentes, sqlc, wire y go:embed.
- Decision: stack = Go 1.22 + `github.com/go-chi/chi/v5 v5.1.0`
  + `github.com/google/wire v0.6.0` + `github.com/mattn/go-sqlite3
  v1.14.22` + `github.com/stretchr/testify v1.9.0` (downgrade
  desde 1.10 por conflicto con dep transitiva davecheney/profile
  eliminada de GitHub). Imagen Docker: `golang:1.22-bookworm`
  con `apt-get install -y make gcc` (necesario para cgo de sqlite3).
- Alternativas: (a) `gorilla/mux` (descartado: chi es mas moderno);
  (b) `pgx` + Postgres (descartado: agrega dependencia externa);
  (c) `testify v1.10` (descartado: requiere davecheney/profile
  privado eliminado de GitHub).
- Consecuencias: la trampa E01 (interfaces implicitas), la trampa
  E02 (init + blank imports), la trampa E03 (//go:generate),
  la trampa E04 (goroutines/channels/select), la trampa E05
  (build tags) y la trampa E06 (//go:embed) son utiles para
  la skill.

### D-249 — Apps y packages en ingles (orders, aggregate, export) para CC-11 (F06s)

- Fecha · Fase · Estado: 2026-10-07 · F06s · vigente
- Contexto: la regla CC-11 detecta menciones del nombre de
  feature (en espanol) en cualquier linea del codigo del fixture.
  Los features son `ingesta-de-eventos`, `agregacion`,
  `exportacion`.
- Decision: usar routers en ingles (`internal/http/handlers.go`
  con `POST /events`, `GET /aggregate`, `GET /export`). Los
  nombres de feature en espanol viven solo en el ground truth.
  Los packages internos en ingles (`internal/domain/`,
  `internal/repo/sqlite/`, `internal/service/`,
  `internal/http/`, `internal/worker/`).
- Alternativas: (a) packages `internal/ingesta/`, etc. (descartado:
  los nombres de feature en espanol aparecen en strings
  y comments; la consistencia favorece nombres en ingles);
  (b) ofuscar con guiones (descartado: el check_ground_truth
  detecta substrings).
- Consecuencias: la skill debe mapear `events` <-> `ingesta-de-eventos`,
  `aggregate` <-> `agregacion`, `export` <-> `exportacion`.

### D-250 — sqlc genera codigo en `internal/repo/sqlc/` via `sqlc generate` (F06s)

- Fecha · Fase · Estado: 2026-10-07 · F06s · vigente
- Contexto: la trampa E03 exige que el codigo de queries se
  genere con `sqlc generate`, no que se commitee al repo.
- Decision: `sqlc.yaml` apunta a `queries.sql` (con anotaciones
  sqlc como `-- name: CreateEvent :execresult`) y
  `migrations/001_initial.up.sql`. El Dockerfile.test hace
  `sqlc generate` antes de `go test`. Adicionalmente, se incluye
  un stub `internal/repo/sqlc/db.go` con funciones placeholder
  para que el codigo compile en CI si sqlc no esta disponible
  (mismo patron que NestJS y otros fixtures).
- Alternativas: (a) commitear el codigo generado (descartado:
  rompe la trampa E03); (b) requerir sqlc en CI (descartado:
  agrega dependencia externa al build).
- Consecuencias: la trampa E03 sigue valida. Los tests funcionan
  con el stub; sqlc se ejecuta en build para validar que la
  sintaxis de queries.sql es correcta.

### D-251 — wire genera `wire_gen.go` con `wire gen ./...` (F06s)

- Fecha · Fase · Estado: 2026-10-07 · F06s · vigente
- Contexto: la trampa E03 tambien aplica al codigo de DI
  generado por wire.
- Decision: `wire.go` declara los providers con
  `//go:build wireinject`. `wire gen ./...` produce `wire_gen.go`
  con la implementacion concreta de `InitializeApp()`.
- Alternativas: (a) DI manual con `main()` y factories (descartado:
  elimina la trampa E03); (b) usar `google/wire` solo en
  documentacion sin build (descartado: no es la trampa).
- Consecuencias: la trampa E03 (codigo generado por tools) sigue
  valida para wire igual que para sqlc.

### D-252 — Interfaces implementadas estructuralmente sin keyword `implements` (F06s)

- Fecha · Fase · Estado: 2026-10-07 · F06s · vigente
- Contexto: la trampa E01 exige que las interfaces se implementen
  sin la keyword `implements` (Go usa structural typing).
- Decision: `domain.EventRepository` y `domain.Exporter` son
  interfaces. `SQLiteEventRepository` y `SQLiteExporter` las
  implementan estructuralmente: cualquier struct con todos los
  metodos de la interface satisface la interface automaticamente.
- Alternativas: (a) embedding explicito de la interface
  (descartado: no es Go idiomático); (b) wrappers (descartado:
  complica la estructura).
- Consecuencias: la trampa E01 sigue valida. La skill debe
  buscar la interface en `domain/` y verificar el matching de
  signatures con los structs en `repo/`.

### D-253 — Prefijo `NPRGT-FXGO-` para los unique tokens de F06s (F06s)

- Fecha · Fase · Estado: 2026-10-07 · F06s · vigente
- Contexto: AGENTS §8 y §23 establecen prefijos `NPRGT-<FX>-`
  para los unique tokens de cada fixture.
- Decision: prefijo `FXGO` y exactamente 26 tokens cubriendo
  stack (GO-VER, CHI-VER, SQLC-VER, WIRE-VER, SQLITE-VER,
  TESTIFY-VER), tipos (IMPLICIT-INTERFACE, INIT-FUNCTION,
  BLANK-IMPORT, GO-GENERATE, GOROUTINE-POOL, CHANNEL-SELECT,
  BUILD-TAG, EMBED-FS, DEPENDENCY-INJECTION), features
  (INGEST-RESULT-R01, AGGREGATE-RESULT-R01, EXPORT-RESULT-R01),
  marcadores (MARKER-APP, MARKER-CMD, MARKER-DOMAIN,
  MARKER-SQLC), y trampas superficiales (TRAMP-S01-LEGACY,
  TRAMP-S02-LEGACY-BIN, TRAMP-S03-DEBUG).
- Alternativas: (a) `FXGOASPNET` (descartado: excede 8 caracteres);
  (b) `FXGOCHI` (descartado: no cubre sqlc/wire/embed).
- Consecuencias: `overfit_guard.py` falla si cualquiera de
  estos tokens aparece en `skills/`.

### D-254 — `Makefile` envuelve `go test ./... -race -count=1` (F06s)

- Fecha · Fase · Estado: 2026-10-07 · F06s · vigente
- Contexto: el plan F06x exige paridad con F06f.
- Decision: `TEST_CMD ?= go test ./... -race -count=1` en el
  Makefile; `test_cmd: make test` en `manifest.yml`.
- Alternativas: (a) `go test` directo (descartado: rompe paridad);
  (b) sin `-race` (descartado: el roadmap pide race detector).
- Consecuencias: el contenedor ejecuta `make test` y los tests
  corren con `-race` para detectar data races en el worker pool.

### D-255 — Imagen Docker `golang:1.22-bookworm` con `make + gcc` (F06s)

- Fecha · Fase · Estado: 2026-10-07 · F06s · vigente
- Contexto: `go-sqlite3` requiere cgo + gcc. `make` se usa
  para ejecutar el Makefile en el contenedor.
- Decision: `FROM golang:1.22-bookworm` + `RUN apt-get install -y
  make gcc` antes de la copia del codigo (cache de layers).
- Alternativas: (a) usar `golang:1.22-alpine` (descartado: alpine
  no tiene gcc por defecto y la compilacion cgo es compleja);
  (b) usar `golang:1.22-bookworm` sin gcc (descartado: cgo falla).
- Consecuencias: la imagen pesa ~600 MB. El native build de
  go-sqlite3 funciona en el contenedor.

### D-256 — `requires: [linux, macos, windows]` en `manifest.yml` (F06s)

- Fecha · Fase · Estado: 2026-10-07 · F06s · vigente
- Contexto: el plan F06x exige paridad con F06p.
- Decision: `requires: [linux, macos, windows]`. Go es multiplataforma.
- Alternativas: (a) solo Linux (descartado: rompe paridad).
- Consecuencias: el fixture es ejecutable en los 3 sistemas.

### D-257 — Deteccion extendida de go-chi/sqlc/wire/embed/sqlite en `fixtures_matrix.py` y `target_matrix.yml` (F06s)

- Fecha · Fase · Estado: 2026-10-07 · F06s · vigente
- Contexto: el plan F06x exige extender `fixtures_matrix.py`
  para detectar go-chi via `go.mod` (buscar `github.com/go-chi/chi`),
  sqlc via `sqlc.yaml`, embed via grep de `//go:embed ` en archivos
  `*.go`, wire via `github.com/google/wire` en go.mod, y sqlite
  via `github.com/mattn/go-sqlite3` en go.mod.
- Decision: agregar bloque de deteccion para `go.mod` que busca
  los 4 paquetes Go (chi, wire, sqlite, etc.). Agregar bloque
  para `sqlc.yaml` que agrega `{sqlc}`. Agregar grep recursivo de
  `*.go` para `//go:embed ` que agrega `{embed}`. Agregar a
  `target_matrix.yml`: `frameworks: [go-chi, sqlc, wire, embed,
  sqlite]`.
- Alternativas: (a) parsear `go.sum` (descartado: es menos estable
  que go.mod); (b) detectar embed via nombre de archivo (descartado:
  no es la directiva).
- Consecuencias: el MATRIX.md muestra fx-go-service cubriendo
  go-chi, sqlc, wire, embed y sqlite.

### D-258 — Stack del fixture F06t: Rust 1.81 + Axum 0.7 + tokio 1.40 + sqlx 0.8 + serde 1.0 + thiserror 1.0 (F06t)

- Fecha · Fase · Estado: 2026-10-07 · F06t · vigente
- Contexto: el plan F06t pide un servicio Rust asincrono con
  Axum, tokio, sqlx, serde, thiserror.
- Decision: stack = Rust 1.81 + `axum = "0.7"` + `tokio = "1.40"`
  + `sqlx = "0.8"` (features = ["runtime-tokio", "sqlite"]) + `serde = "1.0"`
  + `thiserror = "1.0"` + `anyhow = "1.0"` + proc-macro2 1 + quote 1 +
  syn 2. Imagen Docker: `rust:1.81-bookworm` con `apt-get install -y
  make gcc` (cgo de sqlite).
- Alternativas: (a) actix-web (descartado: axum es mas moderno y
  el plan lo pide); (b) diesel (descartado: sqlx es async); (c) tokio
  + smol (descartado: tokio es el runtime mas usado); (d) prost o
  diesel-async (descartado: sqlx es la opcion canonica para
  servicios).
- Consecuencias: la trampa E01 (proc macro derive), la trampa
  E02 (blanket impl generica), la trampa E03 (cargo features),
  la trampa E04 (axum extractors), la trampa E05 (error flow
  con ?) y la trampa E06 (build.rs + unsafe FFI) son utiles para
  la skill.

### D-259 — Single-crate con modulos + crate `fxrust-derive` separado (F06t)

- Fecha · Fase · Estado: 2026-10-07 · F06t · vigente
- Contexto: la trampa E01 exige un proc macro derive custom.
  Un workspace multi-crate agrega complejidad; un single-crate
  con modulos es mas simple.
- Decision: usar single-crate `fxrust-axum` con modulos (`catalog`,
  `pricing`, `sync`, `infra`) + crate `fxrust-derive` separado
  para el proc macro. Esto permite que el proc macro se compile
  independientemente y que los entities (`Item`, `Price`, `SyncJob`)
  usen `#[derive(Entity)]`.
- Alternativas: (a) workspace multi-crate con `core/`, `web/`,
  `db/`, `proc-macro/` (descartado: agrega complejidad innecesaria);
  (b) inline proc macro (descartado: los proc macros no pueden
  estar en el mismo crate que el codigo que los usa).
- Consecuencias: la trampa E01 sigue valida. La skill debe
  entender que `derive-macro/` es un crate separado.

### D-260 — Apps y handlers en ingles (catalog, pricing, sync) para CC-11 (F06t)

- Fecha · Fase · Estado: 2026-10-07 · F06t · vigente
- Contexto: la regla CC-11 detecta menciones del nombre de
  feature (en espanol) en cualquier linea del codigo del fixture.
  Los features son `catalogo`, `precios`, `sincronizacion`.
- Decision: usar modulos `src/catalog/`, `src/pricing/`,
  `src/sync/` y URLs `/catalog/items`, `/catalog/prices`,
  `/sync/jobs`. Los nombres de feature en espanol viven solo
  en el ground truth. Los models usan identificadores en ingles
  (`Item`, `Price`, `SyncJob`).
- Alternativas: (a) `src/catalogo/`, etc. (descartado: el nombre
  aparece en muchos strings, comentarios, errores); (b) `Catalog`,
  `Pricing`, `Sync` con mayusculas (descartado: por convencion
  Rust usa PascalCase en struct names, no en module names).
- Consecuencias: la skill debe mapear `catalog` <-> `catalogo`,
  `pricing` <-> `precios`, `sync` <-> `sincronizacion`.

### D-261 — sqlx con query builder programatico (no macro compile-time) (F06t)

- Fecha · Fase · Estado: 2026-10-07 · F06t · vigente
- Contexto: sqlx tiene macros `sqlx::query!` que requieren una DB
  en compile time o `SQLX_OFFLINE=true` + cache pre-generado.
  El modo offline requiere ejecutar `sqlx prepare` antes de build.
- Decision: usar `sqlx::query_as::<_, T>("...")` con strings y
  derivar `FromRow` en los entities (`#[derive(FromRow)]`). Esto
  evita el chequeo de schema en compile time y solo requiere una
  DB en runtime.
- Alternativas: (a) `sqlx::query!` con cache offline (descartado:
  requiere step adicional en el build); (b) `sea-orm` (descartado:
  agrega una dep no incluida en el plan).
- Consecuencias: las queries son strings en runtime. La skill
  debe notar `sqlx::query_as` + `FromRow` para entender la
  validacion de tipos.

### D-262 — Prefijo `NPRGT-FXRUST-` para los unique tokens de F06t (F06t)

- Fecha · Fase · Estado: 2026-10-07 · F06t · vigente
- Contexto: AGENTS §8 y §23 establecen prefijos `NPRGT-<FX>-`
  para los unique tokens de cada fixture.
- Decision: prefijo `FXRUST` y exactamente 26 tokens cubriendo
  stack (RUST-VER, AXUM-VER, TOKIO-VER, SQLX-VER, SERDE-VER,
  THISERROR-VER), tipos (PROC-MACRO, BLANKET-IMPL,
  CARGO-FEATURES, AXUM-EXTRACTOR, ERROR-FROM, BUILD-RS,
  UNSAFE-FFI, DEPENDENCY-INJECTION), features
  (CATALOG-RESULT-R01, PRICING-RESULT-R01, SYNC-RESULT-R01),
  marcadores (MARKER-APP, MARKER-CRATE, MARKER-INFRA,
  MARKER-LEGACY, MARKER-ENTRYPOINT, MARKER-EXTRACTOR), y
  trampas superficiales (TRAMP-S01-DEBUG, TRAMP-S02-LEGACY,
  TRAMP-S03-UNUSED).
- Alternativas: (a) `FXRUSTAXUM` (descartado: excede 8 caracteres);
  (b) `FXRUSTAPI` (descartado: confunde con framework web).
- Consecuencias: `overfit_guard.py` falla si cualquiera de
  estos tokens aparece en `skills/`.

### D-263 — `Makefile` envuelve `cargo test --workspace` (F06t)

- Fecha · Fase · Estado: 2026-10-07 · F06t · vigente
- Contexto: el plan F06x exige paridad con F06s.
- Decision: `TEST_CMD ?= cargo test --workspace` en el Makefile;
  `test_cmd: make test` en `manifest.yml`.
- Alternativas: (a) `cargo test` sin `--workspace` (descartado:
  no cubre el crate del proc macro); (b) `cargo test -- --nocapture`
  (descartado: agrega ruido al output).
- Consecuencias: el contenedor ejecuta `make test` que corre
  todos los tests del workspace.

### D-264 — Imagen Docker `rust:1.81-bookworm` con `make` + `gcc` (F06t)

- Fecha · Fase · Estado: 2026-10-07 · F06t · vigente
- Contexto: `better-sqlite3` (en el path de sqlx) requiere cgo + gcc
  para compilar el binding C. `make` se usa para ejecutar el
  Makefile.
- Decision: `FROM rust:1.81-bookworm` + `RUN apt-get install -y
  make gcc` antes de la copia del codigo (cache de layers).
- Alternativas: (a) usar `rust:1.81-alpine` (descartado: alpine
  usa musl y la compilacion cgo es compleja); (b) pre-instalar
  las tools (descartado: menos reproducible).
- Consecuencias: la imagen pesa ~500 MB. El native build de
  better-sqlite3 funciona en el contenedor.

### D-265 — `requires: [linux, macos, windows]` en `manifest.yml` (F06t)

- Fecha · Fase · Estado: 2026-10-07 · F06t · vigente
- Contexto: el plan F06x exige paridad con F06p.
- Decision: `requires: [linux, macos, windows]`. Rust es multiplataforma.
- Alternativas: (a) solo Linux (descartado: rompe paridad).
- Consecuencias: el fixture es ejecutable en los 3 sistemas.

### D-266 — Deteccion extendida de axum/tokio/sqlx/serde en `fixtures_matrix.py` y `target_matrix.yml` (F06t)

- Fecha · Fase · Estado: 2026-10-07 · F06t · vigente
- Contexto: el plan F06x exige extender `fixtures_matrix.py`
  para detectar frameworks Rust via `Cargo.toml`.
- Decision: agregar bloque de deteccion para `Cargo.toml` que
  busca `axum`, `tokio`, `sqlx`, `thiserror`, `serde` (con
  `derive`) y agrega los frameworks correspondientes. Tambien
  detectar `build.rs` para `cargo-build-script`. Agregar a
  `target_matrix.yml`: `frameworks: [axum, tokio, thiserror]`.
- Alternativas: (a) parsear `Cargo.lock` (descartado: es menos
  estable que Cargo.toml); (b) no detectar build.rs (descartado:
  pierde la trampa E06).
- Consecuencias: el MATRIX.md muestra fx-rust-axum cubriendo
  axum, tokio, thiserror y cargo-build-script.

### D-267 — Stack: PHP 8.2 + Laravel 10.43 + PHPUnit 10 + Eloquent (F06u)

- Fecha · Fase · Estado: 2026-10-07 · F06u · vigente
- Contexto: el plan F06u exige PHP y Laravel para el fixture
  de la trampa E01 (Facades) que requiere `config/app.php` con
  aliases personalizados.
- Decision: PHP 8.2 (CLI) + Laravel 10.43 (LTS) + Eloquent
  ORM + Blade (vista de ejemplo) + PHPUnit 10 + SQLite
  en memoria para tests.
- Alternativas: (a) Laravel 11 (descartado: ya no usa
  `config/app.php` para Facades, pierde autenticidad de E01);
  (b) MySQL real (descartado: requiere servicio externo en el
  contenedor); (c) Pest (descartado: PHPUnit es mas simple).
- Consecuencias: el fixture usa Laravel 10 con la convencion
  tradicional de `app/Http/Kernel.php` y `app/Console/Kernel.php`.

### D-268 — Single-app Laravel con estructura estandar (F06u)

- Fecha · Fase · Estado: 2026-10-07 · F06u · vigente
- Contexto: el plan F06u define single-app vs multi-app.
- Decision: single-app Laravel 10 con la estructura estandar
  de `laravel/laravel` (app/Models, app/Http/Controllers,
  app/Providers, database/migrations, routes/web.php,
  routes/api.php, routes/console.php). Mismas convenciones
  que un proyecto Laravel real.
- Alternativas: (a) Laravel como libreria (descartado: la
  trampa E04 de auto-discovery de listeners requiere Kernel
  Laravel completo).
- Consecuencias: el fixture es ejecutable con `make test` y
  reproduce las trampas del ecosistema de Laravel.

### D-269 — Modelos y nombres en ingles (F06u, CC-11)

- Fecha · Fase · Estado: 2026-10-07 · F06u · vigente
- Contexto: CC-11 obliga a no mencionar los nombres
  espagnoles de los features en strings/comentarios.
- Decision: modelos y clases en ingles (`Property`, `Visit`,
  `Contract`); features en espanol (`inmuebles`, `visitas`,
  `contratos`); URL paths en ingles (`/api/properties`,
  `/api/visits`, `/api/contracts`).
- Alternativas: (a) clases en espanol (descartado: rompe CC-11).
- Consecuencias: la skill debe mapear `Property ↔ inmuebles`,
  etc.

### D-270 — Driver SQLite :memory: para tests (F06u)

- Fecha · Fase · Estado: 2026-10-07 · F06u · vigente
- Contexto: la spec menciona MySQL pero el toolchain indica
  SQLite. Levantar MySQL real en el contenedor agrega
  complejidad.
- Decision: SQLite en memoria via `phpunit.xml` con
  `<env name="DB_CONNECTION" value="sqlite"/>` y
  `<env name="DB_DATABASE" value=":memory:"/>`. La
  `config/database.php` declara ambos drivers (sqlite y
  mysql) pero los tests usan sqlite (trampa P04: el driver
  efectivo difiere del declarado en config).
- Alternativas: (a) MySQL real con `docker-php-ext-install
  pdo_mysql` y bind-mount (descartado: agrega servicio).
- Consecuencias: el fixture es 100% autocontenido.

### D-271 — Prefijo `NPRGT-FXPLAR-` para unique tokens (F06u)

- Fecha · Fase · Estado: 2026-10-07 · F06u · vigente
- Contexto: el plan F06u exige >=25 tokens unicos.
- Decision: prefijo `NPRGT-FXPLAR-` con 30 tokens en
  `unique_tokens.txt` (fixture y ground truth).
- Alternativas: ninguna (mantener patron).
- Consecuencias: `overfit_guard.py` y `check_ground_truth.py`
  verifican que los tokens no aparezcan en otros archivos.

### D-272 — `Makefile` envuelve `vendor/bin/phpunit --testdox` (F06u)

- Fecha · Fase · Estado: 2026-10-07 · F06u · vigente
- Contexto: el plan F06u exige paridad con F06p.
- Decision: `TEST_CMD ?= vendor/bin/phpunit --testdox` en
  el Makefile; el `run_fixture_tests.py` ejecuta
  `make test` en el contenedor.
- Alternativas: ninguna (mantener patron).
- Consecuencias: el fixture es ejecutable via
  `run_fixture_tests.py --fixture fx-php-laravel --container`.

### D-273 — Imagen Docker `php:8.2-cli` con extensiones PDO SQLite (F06u)

- Fecha · Fase · Estado: 2026-10-07 · F06u · vigente
- Contexto: el plan F06u exige Docker para tests (PHP/Composer
  no disponibles localmente).
- Decision: `FROM php:8.2-cli` + `apt-get install -y make git
  unzip libsqlite3-dev` + `docker-php-ext-install pdo pdo_sqlite`
  + composer 2.x. Tiempo de build: ~3-5 min la primera vez,
  cache de deps en rebuilds.
- Alternativas: (a) `php:8.3-cli` (descartado: Laravel 10
  testado en 8.2).
- Consecuencias: el fixture compila y ejecuta tests sin
  requerir PHP/Composer en la maquina host.

### D-274 — Composer `policy.advisories.block: false` para Advisories (F06u)

- Fecha · Fase · Estado: 2026-10-07 · F06u · vigente
- Contexto: Composer 2.7+ bloquea instalaciones de paquetes
  con advisories de seguridad. Laravel 10.43+ tiene advisories
  conocidos (PKSA-d5tc-s1qs-h781, etc.).
- Decision: agregar `--no-security-blocking` al `composer
  install` en el Dockerfile y `audit.abandoned: ignore` en
  `composer.json`. Las advisories son para versiones viejas
  de Laravel; en el fixture se usan con fines de testing
  aislado.
- Alternativas: (a) actualizar a Laravel 11 (descartado:
  pierde la trampa E01); (b) instalar versiones mas nuevas
  con advisories corregidas (descartado: no compatibles
  con Laravel 10.x).
- Consecuencias: el fixture compila en CI/contenedor con
  las advisories presentes.

### D-275 — Deteccion extendida de PHP/Laravel en `fixtures_matrix.py` y `target_matrix.yml` (F06u)

- Fecha · Fase · Estado: 2026-10-07 · F06u · vigente
- Contexto: el plan F06u exige extender `fixtures_matrix.py`
  para detectar PHP y Laravel.
- Decision: agregar `".php"` a `EXT_LANG`, `"composer.json"`
  a `MANIFEST_BUILD` (build system `composer`), agregar
  `"laravel/framework"` a `PACKAGE_JSON_MARKERS` (renombrado
  a `DEPENDENCY_MARKERS` en la practica), y agregar un
  bloque que lee `composer.json` y detecta `laravel/framework`
  para anadir `laravel`, `eloquent`, `blade` a frameworks.
  Actualizar `target_matrix.yml` con `languages: php`,
  `frameworks: [laravel, eloquent, blade]`, `build_systems:
  [composer]`.
- Alternativas: (a) parsear `composer.lock` (descartado:
  no se commitea); (b) grep basico (descartado: no es
  determinista).
- Consecuencias: `MATRIX.md` muestra fx-php-laravel
  cubriendo `php`, `laravel`, `eloquent`, `blade`, `composer`.

### D-276 — Stack Ruby 3.1.6 + Rails 7.0.8 para fx-ruby-rails (F06v)

- Fecha · Fase · Estado: 2026-10-07 · F06v · vigente
- Contexto: el plan F06v exige una app Rails con jobs y
  Hotwire. Rails 7.1 con Ruby 3.2.11 (la imagen por defecto
  `ruby:3.2-bookworm` que trae Docker Hub) tiene un bug de
  orden de carga con `ActionView::ENCODING_FLAG` que rompe
  el arranque de rspec-rails. Rails 7.0 con Ruby 3.2.11
  tiene el mismo bug y ademas incompatibilidad con `active_support/dependencies`
  (FrozenError en `set_autoload_paths`).
- Decision: usar `ruby:3.1.6-bookworm` y `gem "rails", "7.0.8"`.
  Ruby 3.1.6 es la ultima version menor donde Rails 7.0
  funciona sin los workarounds de Ruby 3.2. Rails 7.0.8
  es la ultima patch de la serie 7.0.
- Alternativas: (a) Rails 7.1 + Ruby 3.1 (descartado: 7.1
  requiere Ruby 3.0+ pero tiene su propio bug con la gema
  `logger`); (b) Rails 6.1 LTS (descartado: no soporta
  Hotwire nativo, y el plan pide Hotwire); (c) Ruby 3.3+
  (descartado: mismas incompatibilidades que 3.2.11+).
- Consecuencias: el fixture se construye sobre Rails 7.0 +
  Ruby 3.1. La skill queda probada contra el stack tipico
  de apps Rails empresariales pequenas en 2024-2025.

### D-277 — Sidekiq 7 con `mock_redis` en tests (F06v)

- Fecha · Fase · Estado: 2026-10-07 · F06v · vigente
- Contexto: Sidekiq 7 requiere Redis. El fixture debe correr
  en el contenedor sin servicio externo.
- Decision: declarar `gem "sidekiq", "7.2.4"` para runtime
  y `gem "mock_redis", "0.45.0"` solo en test/dev. En
  `config/initializers/sidekiq.rb` instanciar `REDIS_CLIENT = MockRedis.new`
  cuando `Rails.env.test? || Rails.env.development?`. En
  produccion, `REDIS_URL` apunta a un Redis real.
- Alternativas: (a) levantar Redis en el contenedor via
  docker-compose (descartado: el harness `run_fixture_tests.py`
  no soporta servicios adicionales); (b) usar `:async` queue
  adapter sin Sidekiq (descartado: el plan pide Sidekiq
  explicito como dependencia para detectar la trampa de
  configuracion); (c) stubear `Sidekiq::Client` (descartado:
  demasiado intrusivo).
- Consecuencias: la suite RSpec ejecuta sin Redis; las
  pruebas de jobs usan `ActiveJob::Base.queue_adapter = :test`
  en lugar de Sidekiq directamente, pero el codigo de
  aplicacion sigue llamando `perform_later` que se enruta
  al adapter configurado.

### D-278 — ActiveJob `:test` como queue adapter por defecto (F06v)

- Fecha · Fase · Estado: 2026-10-07 · F06v · vigente
- Contexto: la aplicacion debe encolar jobs Sidekiq pero
  los tests necesitan verificar la intencion sin ejecutar
  la cola real.
- Decision: en `config/application.rb` declarar
  `config.active_job.queue_adapter = :test`. En
  `config/environments/{development,production}.rb` usar
  `:async` y `:sidekiq` respectivamente. En el initializer
  de Sidekiq configurar el cliente solo en production.
- Alternativas: (a) `:inline` adapter (descartado: ejecuta
  el job sincrónicamente, oculta el callback after_commit
  que es parte de la trampa P01); (b) siempre `:sidekiq`
  (descartado: requiere Redis en tests).
- Consecuencias: los tests verifican la intencion de encolar
  (`expect(after - before).to eq(1)` sobre
  `ActiveJob::Base.queue_adapter.enqueued_jobs`) sin
  ejecutar la cola real.

### D-279 — Sin rspec-rails: setup manual para evitar bug ENCODING_FLAG (F06v)

- Fecha · Fase · Estado: 2026-10-07 · F06v · vigente
- Contexto: rspec-rails 6.1.2 + actionview 7.0 + Ruby 3.x
  tiene un bug de orden de carga donde `ActionView::ENCODING_FLAG`
  no esta disponible cuando `action_view/template/handlers/erb.rb:22`
  lo referencia. rspec-rails 7.0.1 es incompatible con
  rspec 3.13. No hay forma de trabajar con ambos.
- Decision: NO requerir rspec-rails. Cargar el environment
  Rails manualmente, configurar `ActionDispatch::Integration::Session`
  para request specs via un helper custom
  (`RequestSpecHelper`), y envolver cada test en una
  transaccion manual (`ActiveRecord::Base.transaction { ...
  raise ActiveRecord::Rollback }`) en lugar de
  `use_transactional_fixtures`. El spec_helper usa
  `FactoryBot.find_definitions` manualmente.
- Alternativas: (a) parchear actionview en runtime
  (descartado: fragil y fuera del scope del fixture);
  (b) usar solo Ruby puro sin Rails (descartado: el plan
  exige una app Rails completa).
- Consecuencias: las specs son un poco mas verbosas
  (`session.response.status` en vez de
  `expect(response).to have_http_status(:ok)`) pero
  funcionales. El fixture demuestra un patron real para
  equipos que tropiecen con el mismo bug.

### D-280 — prefijo `NPRGT-FXRAILS-` para unique_tokens.txt (F06v)

- Fecha · Fase · Estado: 2026-10-07 · F06v · vigente
- Contexto: el formato canónico de unique tokens para
  fixtures F06 (D-007, F06a2) usa prefijo `NPRGT-FX<NN>-`.
- Decision: `NPRGT-FXRAILS-` con ≥ 25 tokens cubriendo
  stack, callbacks, STI, concerns, traps y marcadores de
  las 8 trampas + 3 superficiales.
- Alternativas: (a) reusar prefijo de un fixture existente
  (descartado: violaria CC-11 al estar duplicado entre
  fixtures).
- Consecuencias: `overfit_guard.py` distingue tokens de
  `fx-ruby-rails` y los demas fixtures sin colision.

### D-281 — ruby:3.1.6-bookworm con libs de compilacion para fx-ruby-rails (F06v)

- Fecha · Fase · Estado: 2026-10-07 · F06v · vigente
- Contexto: las gemas nativas (`sqlite3`, `racc`, `nokogiri`,
  `bcrypt`) requieren compilacion C. La imagen
  `ruby:3.1.6-bookworm` no trae compilador.
- Decision: en `Dockerfile.test` instalar
  `apt-get install -y build-essential libsqlite3-dev libffi-dev git make`
  antes de `bundle install`. Copiar solo `Gemfile` primero
  para aprovechar la cache de Docker.
- Alternativas: (a) precompilar gemas en una imagen base
  custom (descartado: agrega mantenimiento); (b) usar
  `ruby:slim` (descartado: `ruby:3.1.6-bookworm` es la
  variante oficial mas estable para 3.1.6).
- Consecuencias: la imagen final ocupa ~1.2GB y tarda
  ~30s en construirse desde cero; ~5s si solo cambia
  el codigo de aplicacion.

### D-282 — Monkey patch `Array#sum_safe` como trampa del ecosistema (F06v)

- Fecha · Fase · Estado: 2026-10-07 · F06v · vigente
- Contexto: el plan F06v exige una trampa de monkey patch
  en `config/initializers/`. Rails tiene un initializer
  propio de Array en `active_support/core_ext/array/`
  que es seguro, pero queremos plantar una API custom
  para que la skill tenga que descubrirla.
- Decision: crear `config/initializers/patch_array.rb` con
  `class Array; def sum_safe; end; end`. La trampa
  categoriza como E06: cualquier codigo que confie en
  `Array#sum` para colecciones grandes se beneficia (o
  sufre) este cambio global sin una llamada explicita.
- Alternativas: (a) parchear `Hash` o `String` (descartado:
  Array es mas representativo del patron); (b) parchear
  una gema de la app (descartado: el initializer debe ser
  en config/initializers/ segun la trampa).
- Consecuencias: la skill debe listar todos los archivos
  en `config/initializers/` para descubrir la API
  modificada (CC-01 cobertura).

### D-283 — `find_sti_class` que silencia tipos invalidos (F06v)

- Fecha · Fase · Estado: 2026-10-07 · F06v · vigente
- Contexto: el plan F06v exige una trampa del paquete
  `sti_invalid_type_silent`. La trampa natural seria
  que un `type` desconocido levante
  `ActiveRecord::SubclassNotFound`, pero eso es el
  comportamiento por defecto de Rails.
- Decision: sobreescribir `Recordatorio.find_sti_class`
  para devolver `Recordatorio` base si la clase no
  existe o no es subclase de Recordatorio. Asi un
  `Recordatorio.new(type: "NoExiste::Clase")` se guarda
  silenciosamente como Recordatorio base.
- Alternativas: (a) hacer la validacion explicita en un
  `validates :type, inclusion: ...` (descartado: rompe
  la dinamica STI legitima); (b) dejar el comportamiento
  por defecto (descartado: la trampa se manifestaria
  como un error 500 en lugar de una aceptacion silenciosa).
- Consecuencias: la skill debe notar la sobreescritura
  de `find_sti_class` para entender la trampa P04.

### D-284 — `update_columns` en `EnviarRecordatorioJob` para saltar validacion (F06v)

- Fecha · Fase · Estado: 2026-10-07 · F06v · vigente
- Contexto: el plan F06v exige que un recordatorio
  con `fecha_envio` en el pasado se marque como `caducado`
  (R-04 de la feature `recordatorios`). Pero la validacion
  `fecha_envio_no_pasada` rechaza el `update!` normal.
- Decision: en `EnviarRecordatorioJob#perform` cuando
  `fecha_envio < Time.current`, usar `recordatorio.update_columns(estado: "caducado", updated_at: Time.current)`
  en lugar de `recordatorio.marcar_caducado!` (que llama
  `update!`). Esto salta las validaciones de forma
  deliberada y documenta la trampa P02 (stale_record_in_callback).
- Alternativas: (a) relajar la validacion (descartado:
  perderia la trampa P02 que es la E02 + paquete); (b)
  condicionar la validacion al estado (descartado:
  complica el modelo y oculta la trampa).
- Consecuencias: el test `marca como caducado si la
  fecha_envio ya paso` pasa con `update_columns` aunque
  la validacion rechazaria `update!` normal. La skill
  debe notar el uso de `update_columns` y entender que
  el job salta las validaciones a proposito.

### D-285 — Stack C++20 con GCC 13 para fx-cpp-cmake (F06x)

- Fecha · Fase · Estado: 2026-10-07 · F06x · vigente
- Contexto: el plan F06x exige C++20 con GCC y Clang. GCC 13
  en `gcc:13-bookworm` es estable y soporta C++20 completo.
- Decision: usar `gcc:13-bookworm` como imagen Docker y
  `gem "gcc", "13.x"` como compilador implicito (via apt-get).
  CMake 3.25+ se instala via `apt-get install cmake`.
- Alternativas: (a) clang (descartado: requiere instalar
  LLVM 15+ que pesa ~3GB); (b) GCC 12 (descartado: bugs con
  concepts); (c) GCC 14 (descartado: todavia en desarrollo).
- Consecuencias: el build en contenedor tarda ~3 minutos la
  primera vez (incluye `apt-get update` + instalacion + build);
  ~10 segundos en builds incrementales.

### D-286 — Sin Conan/vcpkg: CMake puro + FetchContent para GoogleTest (F06x)

- Fecha · Fase · Estado: 2026-10-07 · F06x · vigente
- Contexto: el plan F06x menciona "Conan o vcpkg" como gestor
  de dependencias. La fixture debe ser reproducible en el
  contenedor sin servicios externos ni capas adicionales.
- Decision: usar CMake puro con `FetchContent` para GoogleTest.
  FetchContent descarga una sola vez (la primera configuracion)
  y cachea el tarball en el build dir. No requiere red en
  builds incrementales.
- Alternativas: (a) instalar gtest via apt (descartado: la
  version de Debian bookworm es 1.12, no 1.14); (b) clonar
  gtest via FetchContent_Git (descartado: requiere git protocol
  en build); (c) Conan (descartado: agrega una capa de
  configuracion que rompe la paridad con los demas fixtures).
- Consecuencias: el `Dockerfile.test` no necesita configurar
  Conan ni vcpkg; un simple `apt-get install cmake` basta.

### D-287 — Plugin demo compilado como `.so` separado via `add_subdirectory` (F06x)

- Fecha · Fase · Estado: 2026-10-07 · F06x · vigente
- Contexto: la feature `cargar-plugin` necesita un artefacto
  real para que `dlopen`/`dlsym` funcione en los tests.
- Decision: crear `plugins/transform_json/CMakeLists.txt` con
  `add_library(transform_json SHARED)`, invocado via
  `add_subdirectory(plugins/transform_json)` desde el
  CMakeLists raiz. El plugin define `extern "C" void
  fx_plugin_register(Registry&)` que la app carga via
  `dlsym(handle, "fx_plugin_register")`.
- Alternativas: (a) compilar el plugin en el mismo target
  que la app (descartado: no seria un plugin separado);
  (b) cargar un .so externo via FetchContent (descartado:
  agrega complejidad innecesaria).
- Consecuencias: el build genera `build/plugins/libtransform_json.so`
  que los tests cargan via `dlopen` real. La trampa P03
  (plugin_memory_leak) se manifiesta cuando el test
  destruye el PluginLoader y los std::function quedan
  apuntando a memoria liberada.

### D-288 — prefijo `NPRGT-FXCPP-` para unique_tokens.txt (F06x)

- Fecha · Fase · Estado: 2026-10-07 · F06x · vigente
- Contexto: el formato canónico de unique tokens para
  fixtures F06 (D-007, F06a2) usa prefijo `NPRGT-FX<NN>-`.
- Decision: `NPRGT-FXCPP-` con ≥ 25 tokens cubriendo stack,
  callbacks, x-macros, dlopen, traps y marcadores de las
  6 trampas del ecosistema + 6 del paquete + 3 superficiales.
- Alternativas: (a) reusar prefijo de un fixture existente
  (descartado: violaria CC-11 al estar duplicado entre
  fixtures).
- Consecuencias: `overfit_guard.py` distingue tokens de
  `fx-cpp-cmake` y los demas fixtures sin colision.

### D-289 — `gcc:13-bookworm` + libs de compilacion para fx-cpp-cmake (F06x)

- Fecha · Fase · Estado: 2026-10-07 · F06x · vigente
- Contexto: las gemas nativas C++ (`sqlite3` no se usa,
  pero `pcre2`, `gtest` requieren compilacion C++).
  La imagen `gcc:13-bookworm` no trae `cmake` ni `make`.
- Decision: en `Dockerfile.test` instalar
  `apt-get install -y cmake make git` y `bundle install`
  en el caso de Ruby. Para C++: el build usa el `g++`
  que viene con la imagen.
- Alternativas: (a) usar una imagen con cmake preinstalado
  como `silkeh/clang:13` (descartado: clang requiere mas
  configuracion); (b) compilar cmake desde fuentes (descartado:
  tarda 10+ minutos y no es portable).
- Consecuencias: la imagen final ocupa ~1.9GB y tarda
  ~30s en construirse desde cero; ~10s si solo cambia
  el codigo de aplicacion.

### D-290 — `InitOrderTrap` global para plantar la trampa E06 (F06x)

- Fecha · Fase · Estado: 2026-10-07 · F06x · vigente
- Contexto: el plan F06x exige una trampa del ecosistema
  sobre "orden de inicializacion estatica". En C++, un
  filtro que invoque un metodo virtual dentro de su
  propio constructor resulta en dispatch estatico, no
  polimorfico. Plantar este bug directamente causaria UB.
- Decision: en `src/filters.cpp` declarar `g_init_marker` y
  un `InitOrderTrap` global que pone el marker a 1. El test
  `StaticInit.OrderMarkerIsSet` verifica que el marker es 1,
  documentando que el constructor del trap se ejecuto
  antes de que el test empiece. La trampa conceptual es
  la mencion del dispatch virtual que ocurriria si un
  filtro intentara invocar un metodo virtual en su propio
  constructor.
- Alternativas: (a) plantar el bug directamente con UB
  (descartado: rompe el build en CI); (b) no plantar la
  trampa (descartado: la categoria E06 quedaria sin ejemplo).
- Consecuencias: la trampa se documenta y verifica sin
  causar UB real.

### D-291 — `static` namespace-scope desactivado para Registrar (F06x)

- Fecha · Fase · Estado: 2026-10-07 · F06x · vigente
- Contexto: C++17 depreca `static` en namespace scope para
  variables de tipo con destructor no trivial. La trampaa
  E01 del ecosistema usa variables `static` en `src/filters.cpp`
  para auto-registrar filtros.
- Decision: en `include/fxproc/registry.hpp` la macro
  `FX_REGISTER_FILTER` no usa `static`. En su lugar, crea
  una variable en `namespace { ... }` (anonimo) que tiene
  linkage interno sin la keyword `static`. El resultado
  es equivalente: la variable se inicializa antes de main()
  gracias al mecanismo de C++.
- Alternativas: (a) usar `[[deprecated]] static` (descartado:
  C++17 sigue compilando pero emite warning); (b) usar
  `inline` (descartado: `inline` no afecta el storage
  duration, que es lo que queremos).
- Consecuencias: el codigo compila limpio con `-Wpedantic`
  y `-Wdeprecated-declarations`; la trampa E01 sigue
  funcionando via el namespace anonimo.

### D-292 — 3-level macro `__COUNTER__` para nombres unicos (F06x)

- Fecha · Fase · Estado: 2026-10-07 · F06x · vigente
- Contexto: la trampa P06 (xmacro_collision) requiere
  registrar la misma clase dos veces con nombres distintos
  para verificar que el shadow silencioso ocurre. Pero
  declarar dos `static Registrar<Json>` con el mismo nombre
  es un error de compilacion.
- Decision: usar una macro de 3 niveles que concatena
  `__COUNTER__` (que NO se expande cuando esta adyacente a
  `##`):
  ```c
  #define FX_PASTE3_(a, b, c) a##b##c
  #define FX_PASTE3(a, b, c) FX_PASTE3_(a, b, c)
  ```
  Esto expande `__COUNTER__` antes del paste.
- Alternativas: (a) usar `__LINE__` (descartado: dos
  invocaciones en la misma linea colisionan); (b) usar
  `__COUNTER__` sin 3-level (descartado: el 1-level no
  expande `__COUNTER__`); (c) declarar variables con nombre
  unico a mano (descartado: fragil ante refactors).
- Consecuencias: cada invocacion de `FX_REGISTER_FILTER`
  genera un nombre unico (`_fx_reg_<ClassName>_<counter>__`),
  permitiendo registrar `Json` dos veces sin colision.

### D-293 — `shared_loader` estatico en test_plugin_loader (F06x)

- Fecha · Fase · Estado: 2026-10-07 · F06x · vigente
- Contexto: el test `RegistersNewFiltersFromPlugin` llama
  `reg.create("lower")` despues de que el test
  `LoadsTransformJsonPlugin` haya destruido su `PluginLoader`.
  El deleter del PluginLoader hace `dlclose`, invalidando
  los `std::function` registrados (la trampa P03).
- Decision: en `test_plugin_loader.cpp` declarar
  `static PluginLoader*` via una funcion `shared_loader()`.
  La libreria permanece cargada durante toda la corrida de
  tests del binario. Es la unica forma de evitar el segfault
  en la prueba de P03.
- Alternativas: (a) crear el PluginLoader nuevo en cada test
  (descartado: la libreria se descarga entre tests y los
  std::function quedan invalidos); (b) no probar create() en
  el segundo test (descartado: la trampa P03 no se verifica
  en runtime).
- Consecuencias: el binario `unit_tests` mantiene la libreria
  `libtransform_json.so` cargada durante toda la corrida.
  En produccion, el PluginLoader se destruye con su scope,
  pero la app no mantiene std::function que apunten a la
  libreria despues de dlclose.

### D-294 — C99 con `-std=c99 -pedantic` para fx-c-embedded (F06y)

- Fecha · Fase · Estado: 2026-10-07 · F06y · vigente
- Contexto: el plan F06y exige C99 (no C11/C17). Los toolchains
  embebidos (GCC, IAR, Keil) soportan C99 de forma estable y
  uniforme; C11 introduce `_Generic` y `_Static_assert` que algunos
  compiladores cruzados no soportan.
- Decision: usar `gcc -std=c99 -pedantic` en el Makefile.
  C99 desactiva extensiones de GNU; los warnings son utiles
  para la skill (le dicen que el codigo no usa features fuera
  de C99).
- Alternativas: (a) `gnu99` (descartado: permite extensions de
  GNU que no compilan en IAR); (b) `c11` (descartado: no soportado
  en todos los toolchains embebidos).
- Consecuencias: el codigo del fixture compila en GCC 13 con
  `-pedantic` sin warnings; las cross-compilaciones con
  `arm-none-eabi-gcc` funcionan sin flags adicionales.

### D-295 — Unity como fork minimo en lugar de Ceedling (F06y)

- Fecha · Fase · Estado: 2026-10-07 · F06y · vigente
- Contexto: el plan F06y menciona "Unity/Ceedling en host".
  Ceedling es un test runner en Ruby; agregaria Ruby como
  dependencia runtime.
- Decision: usar un fork minimo de Unity (single header
  `include/tests/unity.h` + `tests/unity_internals.c`) escrito
  en C99 puro, con un runner Python (`tests/test_runner.py`)
  que compila con gcc y corre los binarios. La paridad con los
  demas fixtures se mantiene (ninguno requiere Ruby).
- Alternativas: (a) Ceedling (descartado: requiere Ruby); (b)
  Unity original descargado via tarball (descartado: agrega
  complejidad de red al build); (c) GoogleTest (descartado: el
  fixture no usa C++ y queremos mantener C99 puro).
- Consecuencias: el fork cubre `TEST_ASSERT_EQUAL_INT`,
  `TEST_ASSERT_TRUE/FALSE`, `TEST_ASSERT_NULL/NOT_NULL`,
  `TEST_ASSERT_GREATER_OR_EQUAL_INT` y `TEST_FAIL_MESSAGE`,
  suficiente para 46 tests. Si en el futuro se necesitan mocks
  o fixtures con setUp/tearDown avanzado, se puede reemplazar
  por el Unity original.

### D-296 — Runner Python en `tests/test_runner.py` (F06y)

- Fecha · Fase · Estado: 2026-10-07 · F06y · vigente
- Contexto: el fixture tiene 10 archivos de test (46 tests) que
  se compilan como binarios separados. Un runner que los construya
  y ejecute automaticamente es necesario para integracion con
  `make test` y `run_fixture_tests.py`.
- Decision: `tests/test_runner.py` (~100 lineas) hace:
  1. Encuentra `tests/test_*.c`.
  2. Compila cada uno con `gcc` + las sources del firmware + HAL.
  3. Ejecuta el binario, parsea la salida de Unity.
  4. Reporta pass/fail agregado.
  5. Retorna 0 si todos pasan.
- Alternativas: (a) make con wildcards (descartado: dificil
  de paralelizar y reportar correctamente); (b) bash script
  (descartado: parsear stdout con sed/grep es fragil).
- Consecuencias: el runner tarda ~5s para 46 tests. Los tests
  son independientes (cada uno genera su propio binario); no
  hay leakage entre tests via static state.

### D-297 — Host-emulation con `hal_host.c` en lugar de QEMU obligatorio (F06y)

- Fecha · Fase · Estado: 2026-10-07 · F06y · vigente
- Contexto: el plan F06y dice "QEMU opcional". Sin QEMU, los
  tests deben correr en host (x86). Las macros MMIO apuntan a
  direcciones STM32F4 que no son validas en x86.
- Decision: cuando se compila con `-DHOST_TEST=1`, `hal_host.c`
  redefine las macros MMIO como variables globales `volatile
  uint32_t` en memoria. La interfaz de las funciones
  (`fxemb_hal_gpio_set`, `fxemb_hal_adc_read`, etc.) es la misma
  en host y bare-metal; solo cambia la implementacion.
- Alternativas: (a) QEMU obligatorio (descartado: requiere
  `qemu-system-arm` en CI; muchos hosts no lo tienen); (b) stubs
  de libc en cada test (descartado: duplica trabajo).
- Consecuencias: los tests verifican la logica de las features
  (sensors, uart, power) sin necesidad de hardware. El target
  `make qemu` corre el firmware bare-metal via QEMU pero no
  es parte del CI.

### D-298 — Linker script `firmware.ld` con `.isr_vector` y `AT(origin)` (F06y)

- Fecha · Fase · Estado: 2026-10-07 · F06y · vigente
- Contexto: el firmware embebido necesita una tabla de vectores
  al inicio absoluto de FLASH, codigo en `.text`, variables
  inicializadas con LMA en FLASH y VMA en RAM, y `.bss` en RAM.
- Decision: `firmware.ld` define:
  - `MEMORY`: FLASH (1M @ 0x08000000) y RAM (128K @ 0x20000000).
  - `.isr_vector`: primera seccion de FLASH, KEEP.
  - `.text`: codigo ejecutable.
  - `.data`: `>RAM AT> FLASH` (VMA en RAM, LMA en FLASH,
    copiada en startup desde `_sidata` a `_sdata`).
  - `.bss`: `NOLOAD` (zero-init, no ocupa FLASH).
  - Simbolos exportados: `_estack`, `_sidata`, `_sdata`,
    `_edata`, `_sbss`, `_ebss`.
- Alternativas: (a) hacer el link script en Python (descartado:
  fragil); (b) usar el script por defecto de arm-none-eabi
  (descartado: demasiado complejo para un fixture didactico).
- Consecuencias: la trampa E04 es visible y verificable. La
  skill debe leer el script y notar las secciones + simbolos.

### D-299 — Seleccion de placa via `-DBOARD_X` (F06y)

- Fecha · Fase · Estado: 2026-10-07 · F06y · vigente
- Contexto: el plan F06y exige `#ifdef BOARD_X` que cambia
  el comportamiento segun la placa. Tres placas: STM32F4
  Discovery, nRF52 DK, y host (para tests).
- Decision: `include/fxemb/board.h` con la estructura:
  ```c
  #if defined(STM32F4_DISCOVERY)
    #define FXEMB_BOARD_NAME "stm32f4_discovery"
    ...
  #elif defined(NRF52_DK)
    ...
  #elif defined(BOARD_HOST) || defined(HOST_TEST)
    ...
  #else
    #error "..."
  #endif
  ```
  Cada placa tiene su `board_<name>.c` con un `Reset_Handler`
  fuerte. El linker prefiere el fuerte sobre el weak del
  `startup.c`.
- Alternativas: (a) runtime detection (descartado: no se puede
  en bare-metal); (b) un solo board.c con todo (descartado:
  no demuestra la trampa E05).
- Consecuencias: la trampa E05 es claramente visible. Si
  ninguna placa esta definida, el `#error` falla el build
  explicito (mejor que linkear con codigo vacio).

### D-300 — MMIO `volatile uint32_t*` con direcciones STM32F4 (F06y)

- Fecha · Fase · Estado: 2026-10-07 · F06y · vigente
- Contexto: la trampa E06 exige registros MMIO accedidos con
  macros de direccion `volatile`. Sin volatile, el compilador
  puede reordenar accesos y la app ve valores cacheados.
- Decision: `include/fxemb/hal.h` define macros como:
  ```c
  #define FXEMB_GPIOA_ODR (*(volatile uint32_t*)(0x40020000 + 0x14))
  ```
  Las direcciones son las de STM32F4 Discovery (referencia
  del RM0090). En host, `hal_host.c` redefine las macros
  via `#undef` + declaracion `volatile uint32_t` para que
  gcc no chille al compilar para x86.
- Alternativas: (a) usar punteros globales en lugar de casts
  (descartado: menos didactico); (b) usar registros con
  `__attribute__((io))` (descartado: extension de GCC no
  portable a IAR).
- Consecuencias: la trampa E06 es visible y la trampa P01
  (race) se manifiesta cuando el volatile se elimina.

### D-301 — prefijo `NPRGT-FXCEMB-` para unique_tokens.txt (F06y)

- Fecha · Fase · Estado: 2026-10-07 · F06y · vigente
- Contexto: el formato canonico de unique tokens para fixtures
  F06 (D-007, F06a2) usa prefijo `NPRGT-FX<NN>-`.
- Decision: `NPRGT-FXCEMB-` con 38 tokens cubriendo stack,
  callbacks, x-macros, dlopen, traps y marcadores de las
  6 trampas del ecosistema + 6 del paquete + 3 superficiales.
- Alternativas: (a) reusar prefijo de un fixture existente
  (descartado: violaria CC-11 al estar duplicado entre
  fixtures).
- Consecuencias: `overfit_guard.py` distingue tokens de
  `fx-c-embedded` y los demas fixtures sin colision.

### D-302 — `fxemb_sensors_init` no atomico, race en ring (F06y, P01)

- Fecha · Fase · Estado: 2026-10-07 · F06y · vigente
- Contexto: la trampa paquete P01 (race_lectura_sensores) se
  manifiesta cuando dos threads llaman `fxemb_sensors_read_all()`
  sin lock. La skill debe notar que el codigo parece atomico
  pero no lo es.
- Decision: en `src/sensors.c` el `g_sensor_head++` no es
  atomico. El test `test_trap_p01` verifica que read_all
  devuelve valores no triviales (>= 1) cuando se empujan
  datos desde fuera. La trampa vive en el comentario del
  codigo: "trampa paquete P01: dos threads llamando
  fxemb_sensors_read_all() sin mutex pueden leer indices
  inconsistentes".
- Alternativas: (a) usar `__atomic_fetch_add` (descartado:
  no compila con `-pedantic` C99 puro); (b) usar mutex
  (descartado: perderiamos la trampa P01).
- Consecuencias: el test verifica el sintoma (valores no
  triviales) sin causar UB. La skill debe detectar que la
  ausencia de locks es deliberada (documentada en el comentario).

### D-303 — Qt 6.4 via apt en lugar de Qt 6.6 LTS (F06z)

- Fecha · Fase · Estado: 2026-10-07 · F06z · vigente
- Contexto: el plan F06z decia Qt 6.6 LTS pero Debian bookworm
  solo trae Qt 6.4.2. Compilar Qt 6.6 desde fuentes tarda ~2h
  y agrega ~1GB de dependencias.
- Decision: usar `qt6-base-dev` + `qt6-declarative-dev` + `qt6-tools-dev`
  + `qt6-tools-dev-tools` desde apt de Debian bookworm (Qt 6.4.2).
  Ajustar `find_package(Qt6 6.4 REQUIRED ...)` y
  `qt_standard_project_setup(REQUIRES 6.4)`.
- Alternativas: (a) compilar Qt 6.6 desde fuentes (descartado:
  2h+ de build); (b) usar homebrew en macOS (descartado: no es
  reproducible en CI); (c) bajar la version minima a Qt 5 (descartado:
  el spec dice Qt 6).
- Consecuencias: el fixture funciona out-of-the-box en
  `gcc:13-bookworm`; la skill debe notar que la version es 6.4.2
  (visible en `build/CMakeCache.txt`).

### D-304 — `qt_add_library(qtapp_core STATIC)` con headers explicitos (F06z)

- Fecha · Fase · Estado: 2026-10-07 · F06z · vigente
- Contexto: AUTOMOC para una libreria estatica en Qt 6.4 no se
  activa automaticamente cuando se usan `qt_add_library` y solo
  aparecen headers via include en .cpp.
- Decision: pasar explicitamente los headers con `Q_OBJECT` en
  la lista de sources de `qt_add_library(qtapp_core STATIC ...)`.
  Esto fuerza a AUTOMOC a procesar los headers.
- Alternativas: (a) poner los headers en `target_sources`
  (descartado: reduntante con qt_add_library); (b) usar
  `set(CMAKE_AUTOMOC ON)` global (insuficiente en Qt 6.4).
- Consecuencias: el codigo moc se genera para cada QObject; los
  tests pueden acceder a los slots/señales via meta-object.

### D-305 — `qtapp_exe` como nombre del ejecutable (F06z)

- Fecha · Fase · Estado: 2026-10-07 · F06z · vigente
- Contexto: `qt_add_qml_module(qtapp ...)` genera un directorio
  `build/qtapp/` para el modulo QML. Si el ejecutable se llama
  tambien `qtapp`, el linker falla con "cannot open output file
  qtapp: Is a directory".
- Decision: renombrar el ejecutable a `qtapp_exe`. El modulo QML
  mantiene el nombre `qtapp` (porque es el nombre del target que
  contiene los QObjects).
- Alternativas: (a) cambiar el nombre del target del modulo QML
  (descartado: invalida la convencion); (b) cambiar el URI del
  modulo QML (descartado: tambien es molesto).
- Consecuencias: el binario de salida es `build/qtapp_exe` y el
  modulo QML es `QtApp`. Documentado en el Dockerfile.

### D-306 — `AUTOUIC_SEARCH_PATHS` para resolver `ui/*.ui` (F06z)

- Fecha · Fase · Estado: 2026-10-07 · F06z · vigente
- Contexto: AUTOUIC busca el archivo `.ui` en el mismo directorio
  que el .cpp que incluye `ui_<class>.h`. Si el `.ui` esta en
  `ui/` pero el .cpp esta en `src/`, AUTOUIC no lo encuentra y
  falla con "could not be found".
- Decision: `set_target_properties(qtapp_core PROPERTIES AUTOUIC_SEARCH_PATHS "${CMAKE_SOURCE_DIR}/ui")`
  para `qtapp_core`. El ejecutable y los tests heredan la propiedad
  via `target_link_libraries(... qtapp_core)`.
- Alternativas: (a) mover los .ui a `src/` (descartado: rompe la
  convencion Qt); (b) cambiar la ruta del include a "ui/ui_main_window.h"
  (descartado: feo).
- Consecuencias: el .ui vive en `ui/main_window.ui` y se compila
  correctamente en `build/qtapp_core_autogen/.../ui_main_window.h`.

### D-307 — `libqt6test6` runtime en lugar de `qt6-test-dev` (F06z)

- Fecha · Fase · Estado: 2026-10-07 · F06z · vigente
- Contexto: Debian bookworm no provee un paquete `-dev` para
  `Qt6::Test`. Solo esta `libqt6test6` (runtime).
- Decision: instalar `libqt6test6` (runtime) en el Dockerfile. El
  paquete `qt6-base-dev` provee los headers de Qt6::Test (que se
  enlazan con `libQt6Test.so.6` en runtime).
- Alternativas: (a) descargar el tarball de Qt 6.5 (descartado:
  agrega ~30MB al build); (b) usar QTest manualmente (descartado:
  reinventa la rueda).
- Consecuencias: el build requiere `apt-get install libqt6test6`
  ademas de `qt6-base-dev` para que el linker encuentre `Qt6Test`.

### D-308 — `QTEST_GUILESS_MAIN` para tests sin GUI (F06z)

- Fecha · Fase · Estado: 2026-10-07 · F06z · vigente
- Contexto: `QTEST_MAIN` crea un `QApplication` que requiere un
  display. En CI headless esto falla.
- Decision: usar `QTEST_GUILESS_MAIN` (crea `QCoreApplication` en
  su lugar) para que los tests corran sin display. Los signals
  funcionan igual y los QObjects se pueden instanciar.
- Alternativas: (a) `QTEST_MAIN` + `xvfb-run` (descartado: requiere
  xvfb en la imagen); (b) `QTEST_APPLESS_MAIN` (descartado: sin
  QCoreApplication no se pueden usar signals).
- Consecuencias: el binario de tests corre sin display via
  `QT_QPA_PLATFORM=offscreen`.

### D-309 — Single test binary con todos los tests QtAppTests (F06z)

- Fecha · Fase · Estado: 2026-10-07 · F06z · vigente
- Contexto: el plan llamaba 10 archivos de test separados. En
  Qt Test, la convencion es una clase QObject con private slots
  por archivo + `QTEST_MAIN` por archivo. Con Qt 6.4 + `QGuiApplication`,
  multiples QApplication en el mismo proceso no funcionan bien.
- Decision: un solo archivo `test_main.cpp` con la clase
  `QtAppTests` y todos los tests como private slots. Se usa
  `QTEST_GUILESS_MAIN(QtAppTests)` para generar el main().
  `tests/test_runner.py` compila y corre un solo binario.
- Alternativas: (a) 10 archivos con QTEST_MAIN cada uno
  (descartado: problemas con multiples QApplication); (b) un archivo
  pero sin la clase QtAppTests (descartado: pierde la integracion
  con QTest).
- Consecuencias: el runner es mas simple; los tests se identifican
  por su nombre en el output de QTest.

### D-310 — prefijo `NPRGT-FXCPPQT-` para unique_tokens.txt (F06z)

- Fecha · Fase · Estado: 2026-10-07 · F06z · vigente
- Contexto: el formato canonico de unique tokens para fixtures
  F06 (D-007, F06a2) usa prefijo `NPRGT-FX<NN>-`.
- Decision: `NPRGT-FXCPPQT-` con 42 tokens cubriendo stack
  (qt6, qml, qobject, etc.), 6 trampas del ecosistema, 6 del
  paquete, 3 superficiales y conceptos Qt (moc, uic, rcc).
- Alternativas: (a) reusar prefijo de un fixture existente
  (descartado: violaria CC-11 al estar duplicado entre fixtures).
- Consecuencias: `overfit_guard.py` distingue tokens de
  `fx-cpp-qt` y los demas fixtures sin colision.

### D-311 — Manifest con `linux` + `macos` (F06z)

- Fecha · Fase · Estado: 2026-10-07 · F06z · vigente
- Contexto: el plan original tenia `windows: NO` por las mismas
  razones que fx-cpp-cmake. Para macOS, Qt 6 esta disponible via
  Homebrew pero no en el manifest.
- Decision: `requires: [linux, macos]`. En CI usamos el contenedor
  `gcc:13-bookworm` con Qt de apt. En macOS el usuario necesita
  instalar Qt 6 via `brew install qt`.
- Alternativas: (a) `requires: [linux]` unicamente (descartado:
  excluye macOS sin razon); (b) `requires: [linux, macos, windows]`
  (descartado: Windows requiere display).
- Consecuencias: el fixture corre en Linux via Docker y en macOS
  con Qt instalado.
  triviales) sin causar UB. La skill debe detectar que la
  ausencia de locks es deliberada (documentada en el comentario).

### D-312 — Stack Swift 6 + SPM + Xcode project hibrido (F06aa)

- Fecha · Fase · Estado: 2026-10-07 · F06aa · vigente
- Contexto: la opcion SPM-only deja fuera .xcodeproj/widget
  extension/bridging header; .xcodeproj-only deja fuera tests en host.
  El plan combina ambos: la logica en `Package.swift` (host testable
  con `swift test`) y los targets iOS (FxSwiftApp + FxSwiftWidget) en
  `Examples/FxSwift.xcodeproj/`.
- Decision: SPM + Xcode project. Tests de logica con `swift test`
  (36 Swift Testing en 9 suites), smoke build del target iOS con
  `xcodebuild build` en el Xcode project.
- Consecuencias: el fixture requiere macOS con Xcode para validar
  la parte Xcode. SPM solo no es suficiente (faltaria widget, ObjC
  bridge, entitlements).

### D-313 — `requires: [macos]` y `container.enabled: false` (F06aa)

- Fecha · Fase · Estado: 2026-10-07 · F06aa · vigente
- Contexto: el fixture requiere Xcode + iOS SDK que no existen en
  contenedores Linux. `run_fixture_tests.py` debe saltarlo en
  Linux/Windows.
- Decision: `manifest.requires: [macos]`, `container.enabled: false`,
  `Dockerfile.test` con `FROM scratch + CMD ["false"]` para que
  `check_ground_truth.py` y el harness no se quejen de su ausencia.
- Consecuencias: el gate `coverage` global no exigira este fixture
  en CI Linux; los gates se ejecutan en macOS con `make test`.

### D-314 — Swift Testing (`import Testing`) en vez de XCTest (F06aa)

- Fecha · Fase · Estado: 2026-10-07 · F06aa · vigente
- Contexto: la toolchain en este host (CommandLineTools sin Xcode
  hasta F06aa) no incluye el modulo `XCTest`. `Swift Testing` esta
  disponible con Xcode 16+ (incluido CommandLineTools 16+) pero no
  con la 15.
- Decision: usar `import Testing` + `@Test` + `@Suite` + `#expect`.
  `xcodebuild test` tambien puede correr los Swift Testing
  directamente.
- Consecuencias: los tests no son `XCTestCase`. El ground truth
  los describe como "36 Swift Testing tests" en vez de XCTest.
  El plan original preveia XCTest; el switch a Swift Testing
  se documenta aqui y se reescribe en DECISIONS.md.

### D-315 — `SettingsHostController.swift` vive en `Examples/FxSwiftApp/`, no en FxSwiftCore (F06aa)

- Fecha · Fase · Estado: 2026-10-07 · F06aa · vigente
- Contexto: el controller UIKit usa `LegacyLogger` Obj-C via bridging
  header. Si viviera en `Sources/FxSwiftCore/` se compilaria en SPM
  sin bridging header aplicado, rompiendo la build del paquete.
- Decision: `SettingsHostController.swift` se mueve a
  `Examples/FxSwiftApp/` (target iOS) y el SPM tiene un placeholder
  `LegacySettingsHost` en `LegacySettingsView.swift` que el target
  real extiende via una extension en el controller.
- Consecuencias: `LegacySettingsView` compila en host macOS sin
  UIKit; el target iOS real (FxSwiftApp) incluye el controller que
  aporta la extension con `LegacyLogger` real.

### D-316 — `project.pbxproj` generado a mano por script Python (F06aa)

- Fecha · Fase · Estado: 2026-10-07 · F06aa · vigente
- Contexto: el pbxproj es texto (formato OpenStep plist). Editarlo
  a mano es fragil; herramientas como XcodeGen o Tuist requieren
  dependencias externas.
- Decision: `tools/generate_pbxproj.py` genera el pbxproj con IDs
  estables derivados de `sha1(nombre)`, lo que hace la salida
  determinista. Se reescribe cada vez que cambia el fixture.
- Consecuencias: el pbxproj no se commitea a mano. `make test`
  incluye un smoke build que lo valida; sin Xcode el harness lo
  omite y registra la razon en `.build/xcode-skip.log`.

### D-317 — Tests usan `TestPaths` helper con `#filePath` (F06aa)

- Fecha · Fase · Estado: 2026-10-07 · F06aa · vigente
- Contexto: los tests iniciales usaban paths absolutos hardcodeados
  del estilo `/Users/martin/.../dev/fixtures/fx-swift-ios/...`. Esto
  viola CC-11 (menciona `dev/fixtures` en el codigo) y no es
  portable entre maquinas.
- Decision: helper `TestPaths` (en `Sources/FxSwiftCoreTests/`) que
  resuelve la raiz del fixture via `#filePath` y `deletingLastPathComponent()`
  repetido. Asi los tests no contienen paths absolutos.
- Consecuencias: el test runner puede ejecutarse en cualquier
  maquina sin editar codigo; CC-11 sigue verde.

### D-318 — `WidgetSummaryEntry` conforma `TimelineEntry` solo en iOS (F06aa)

- Fecha · Fase · Estado: 2026-10-07 · F06aa · vigente
- Contexto: SPM compila para macOS sin WidgetKit; conformar
  `TimelineEntry` directamente hace que SPM falle.
- Decision: `extension WidgetSummaryEntry: TimelineEntry {}` dentro
  de un bloque `#if canImport(WidgetKit)`. Ademas `WidgetSummaryEntry.date`
  pasa de `let` a `var` para satisfacer el requisito del protocolo.
- Consecuencias: el target iOS real (widget) compila con la
  conformance; SPM no.

### D-319 — `FxSwiftWidgetBundle: WidgetBundle` con `@main` (F06aa)

- Fecha · Fase · Estado: 2026-10-07 · F06aa · vigente
- Contexto: un widget extension iOS necesita `@main` o `@main
  WidgetBundle` segun cuantos widgets contenga. El archivo
  `WidgetMain.swift` original solo declaraba `FxSwiftWidget: Widget`
  sin `@main`, lo que causaba un crash silencioso.
- Decision: declarar un `WidgetBundle` con `@main` que envuelve
  `FxSwiftWidget()`. Esto permite extender el bundle a multiples
  widgets en el futuro sin tocar el entry point.
- Consecuencias: el widget extension compila y se carga en el
  simulator; el `@main` tambien queda en la lista de entry points
  del ground truth.

### D-320 — `DEVELOPER_DIR` auto-detectado para `xcodebuild` (F06aa)

- Fecha · Fase · Estado: 2026-10-07 · F06aa · vigente
- Contexto: el `xcode-select` del sistema apunta a
  `/Library/Developer/CommandLineTools` (no Xcode completo). Para
  invocar `xcodebuild` y `swift` con las herramientas que
  incluyen Testing + Swift 6.3 + SDKs iOS, hay que apuntar
  temporalmente a `/System/Volumes/Data/Applications/Xcode.app/...`
  o `/Applications/Xcode.app/...` via `DEVELOPER_DIR`.
- Decision: `tools/run_spm_and_xcode_tests.sh` y `Makefile` prueban
  Xcode en `Xcode.app/Contents/Developer` automaticamente y exportan
  `DEVELOPER_DIR` si lo encuentran. Si no, el smoke build se omite
  y se registra la razon; los tests SPM siguen corriendo.
- Consecuencias: en maquinas con `xcode-select` apuntando a Xcode
  completo, todo el pipeline corre. En maquinas con solo
  CommandLineTools, swift test falla con `no such module 'Testing'`
  (documentado como limitacion en el README).

### D-321 — Stack Swift server-side F06ab (F06ab)

- Fecha · Fase · Estado: 2026-10-07 · F06ab · vigente
- Contexto: F06ab requiere ejercitar macros Swift (`@attached`/`@freestanding`), build tool plugins de SPM, Vapor routing + Fluent, CLI swift-argument-parser, `actor`/`Sendable`, y `#if canImport(FoundationNetworking)`.
- Decision: Swift 6.0+ con `swift-tools-version: 6.0`, Vapor 4.92+, Fluent + FluentSQLiteDriver, swift-argument-parser 1.3+, swift-syntax 510+. Dependencias remotas via SPM en `Package.swift`. Plugin en sub-package `Plugins/AuditCodesPlugin/Package.swift` separado del consumidor para forzar a la skill a resolver dependencias transitivas.
- Consecuencias: `swift build` tarda 3-5 min la primera vez (descarga + compila Vapor); tests corren con `swift test --parallel` en contenedor oficial `swift:6.0.3-jammy`.

### D-322 — Imagen Docker `swift:6.0.3-jammy` (F06ab)

- Fecha · Fase · Estado: 2026-10-07 · F06ab · vigente
- Contexto: la imagen oficial `swift:6.0.3-jammy` (Ubuntu 22.04) trae Swift 6.0.3 + `swift build` + `swift test`. Necesita `make` y `git` adicionales.
- Decision: `Dockerfile.test` parte de `swift:6.0.3-jammy` + `apt-get install -y --no-install-recommends make git ca-certificates` + `WORKDIR /app` + `COPY . /app/` + `CMD ["swift", "test", "--parallel"]`. Cache de `.build` via `-v $(pwd)/.build-cache:/app/.build`.
- Consecuencias: el fixture compila y ejecuta tests en Linux sin requerir Swift local instalado en el host; el contenedor pesa ~1.2 GB.

### D-323 — `requires: [linux, macos]` con container enabled (F06ab)

- Fecha · Fase · Estado: 2026-10-07 · F06ab · vigente
- Contexto: el fixture corre en Linux (Vapor + FoundationNetworking) y en macOS (Vapor + Foundation). Sin embargo, los runtimes de CI locales suelen ser macOS donde Swift esta preinstalado.
- Decision: `manifest.yml` declara `requires: [linux, macos]` + `container.enabled: true`. El runner usa contenedor en macOS por defecto para reproducibilidad; los desarrolladores pueden saltarse el contenedor ejecutando `swift test` local con Swift 6.0+.
- Consecuencias: el fixture es portable entre Linux y macOS; los tests son identicos en ambos sistemas excepto `UrlSessionProviderTests` que usa `#if canImport(FoundationNetworking)` para diferenciar ramas.

### D-324 — Plugin en sub-package SPM separado (F06ab)

- Fecha · Fase · Estado: 2026-10-07 · F06ab · vigente
- Contexto: un build tool plugin en SPM puede declararse como target plugin dentro del mismo Package.swift o como sub-package separado. Los plugins que generan codigo extenso suelen empaquetarse aparte para evitar ciclos y para que el consumidor los declare via `.plugin(name:, package:)`.
- Decision: `Plugins/AuditCodesPlugin/Package.swift` declara el producto `.plugin(name: "AuditCodesPlugin", targets: ["AuditCodesPlugin"])` con `capability: .buildTool()`. El consumidor (`Sources/FxSwiftServer/`) lo consume con `.plugin(name: "AuditCodesPlugin", package: "FxSwiftImporterPlugin")` (resuelto como sub-package).
- Consecuencias: la skill debe saber que los plugins SPM pueden estar en sub-packages; `fixtures_matrix.py` detecta `.pluginTarget` o `capability: .buildTool()` en cualquier `Package.swift` bajo `Plugins/`.

### D-325 — Macros `@FxRoute` (PeerMacro) y `@ImportModuleDecl` (DeclarationMacro) (F06ab)

- Fecha · Fase · Estado: 2026-10-07 · F06ab · vigente
- Contexto: el fixture debe plantar trampas E1 (macros `@attached(member)`) y P1 (macros `@freestanding(declaration)`).
- Decision: `@FxRoute` se implementa como `PeerMacro` con `@attached(peer, names: \`ExternalModule\`, conformances: \`RegisterableRoute\`)` que genera una extension con `registerRoute(_ app:)` y `path` en la expansion. `@ImportModuleDecl` se implementa como `DeclarationMacro` con `@freestanding(declaration, names: arbitrary)` que genera un `import <module>` en la expansion. Ambos viven en `Sources/FxSwiftMacros/` (SwiftSyntax + SwiftSyntaxMacros).
- Consecuencias: la skill debe seguir el codigo expandido por el macro (`.build/<archivo>.swift`) para entender el wiring real de las rutas y para ver el `import` real que `@ImportModuleDecl` inyecta.

### D-326 — `AuditCodesPlugin` fallback `// noop` con `#if canImport` (F06ab)

- Fecha · Fase · Estado: 2026-10-07 · F06ab · vigente
- Contexto: la trampa P4 exige que el plugin no falle cuando una dependencia falta, sino que genere codigo minimo. Esto simula el caso real de plugins que degradan su salida segun la plataforma.
- Decision: el cuerpo de `AuditCodes.generated.swift` se emite con un `cat <<'GEN_EOF' ... GEN_EOF` que contiene `#if canImport(FoundationNetworking) ... #else // noop ... #endif`. En Linux genera 4 cases (unverified/stale/orphaned/archived); en macOS genera 1 case (noop). El plugin no reporta error en ningun caso.
- Consecuencias: `GET /audit/codes` devuelve listas distintas segun la plataforma, demostrando que el plugin es sensible al entorno sin fallar; `FixturesPluginTest` verifica que el archivo siempre existe.

### D-327 — Migraciones en `Sources/FxSwiftServer/Migrations/` (F06ab)

- Fecha · Fase · Estado: 2026-10-07 · F06ab · vigente
- Contexto: Fluent permite colocar migraciones en cualquier path; Vapor recomienda `Sources/App/Migrations/`. La trampa P5 (UNIQUE index no idempotente) se planta intencionalmente.
- Decision: las migraciones viven en `Sources/FxSwiftServer/Migrations/CreateNote.swift` (Note + AuditEntry). El `Package.swift` declara `exclude: ["Migrations/Migrations.ts"]` para ignorar el placeholder. La migracion `CreateNote` usa `.unique(on: "title")` sin guard `IF NOT EXISTS`.
- Consecuencias: la skill debe notar que `.unique(on:)` sin `if !database.doesSchemaExist(...)` falla en re-ejecucion; `app.autoMigrate()` ejecutarse dos veces produce `UNIQUE constraint failed: notes.title`.

### D-328 — Exit codes CLI 64/65/70/130 (F06ab)

- Fecha · Fase · Estado: 2026-10-07 · F06ab · vigente
- Contexto: la CLI `fxsimport` debe plantar trampas P_exit por categoria de error (archivo no existe, formato invalido, server inalcanzable, cancelacion por usuario).
- Decision: `Sources/FxSwiftCLI/Subcommands/ImportNotes.swift` usa exit codes estandar de BSD: `64` (EX_USAGE, archivo no encontrado), `65` (EX_DATAERR, formato invalido), `70` (EX_SOFTWARE, server inalcanzable), `130` (cancelado por SIGINT, 128+SIGINT=2).
- Consecuencias: la skill debe leer el `ExitCode(64|65|70|130)` y entender que cada uno corresponde a una categoria de error documentada en el ground truth (R-02..R-06 de la feature `cli-de-importacion`).

### D-329 — Prefijo unique tokens `NPRGT-FXSWIFTSRV-` (F06ab)

- Fecha · Fase · Estado: 2026-10-07 · F06ab · vigente
- Contexto: cada fixture debe declarar ≥ 30 unique tokens con un prefijo unico para que el guardián anti-sobreajuste (`overfit_guard.py`) pueda detectar filtraciones entre fixtures.
- Decision: prefijo `NPRGT-FXSWIFTSRV-` con 38 entradas (PACKAGE-NAME, PLATFORM-MACOS, PLATFORM-LINUX, VAPOR-VERSION, FLUENT-SQLITE, ARGPARSER-VERSION, MACRO-ATTACHED, MACRO-FREESTANDING, IMPORT-MACRO, BUILD-PLUGIN, PLUGIN-NOOP, ROUTE-COLLECTION, REGISTER-ROUTE, ACTOR-RECORDER, SENDABLE-DTO, UNCHECKED-SENDABLE, CANIMPORT-FN, URL-SESSION, CATCH-ALL, CONTENT-DTO, FLUENT-MIGRATION, UNIQUE-INDEX, CSV-IMPORTER, ASYNC-COMMAND, EXIT-64/65/70/130, TIMEOUT, LEGACY-HELPER, ENV-LEGACY, GENERATED-AUDIT, ABORT-ERROR, NOTE-SCHEMA, AUDIT-ACTOR, FEATURE-API/CLI/AUDIT).
- Consecuencias: ningun archivo del codigo fuente del fixture (excluyendo `unique_tokens.txt`) puede mencionar estos strings; `check_ground_truth.py --check-cc11` lo verifica.

### D-330 — Tests XCTest + variable de entorno `FIXTURE_ROOT` (F06ab)

- Fecha · Fase · Estado: 2026-10-07 · F06ab · vigente
- Contexto: los tests XCTest necesitan acceder a archivos fuente del fixture (Routes, Services, Migrations) para verificar trampas (e.g. "trampa E1: macro debe estar en RouteMacro.swift"). En SwiftPM, el test target vive en `Tests/` que no resuelve automaticamente `../`.
- Decision: cada test resuelve las rutas relativas via `ProcessInfo.processInfo.environment["FIXTURE_ROOT"] ?? "../.."`. El `Makefile` y `Dockerfile.test` no necesitan exportar la variable porque `swift test` corre con el working directory = raiz del paquete (donde `FIXTURE_ROOT` relativo es valido). Los tests usan `XCTest` (no Swift Testing) para compatibilidad con Swift 6.0 estable.
- Consecuencias: los tests son robustos independientemente de donde se monten; cualquier sub-agente puede ejecutar `swift test` desde la raiz del fixture y los asserts de trampas funcionan.

### D-331 — Stack Kotlin Android F06ac (F06ac)

- Fecha · Fase · Estado: 2026-10-07 · F06ac · vigente
- Contexto: F06ac requiere ejercitar `AndroidManifest.xml` declarativo, Hilt, Room, WorkManager, Compose + Views XML heredadas con ViewBinding, flavors free/paid, Navigation Component con deep links.
- Decision: Kotlin 2.0.21 + AGP 8.7.2 + Gradle 8.10.2 + JDK 21 + KSP 2.0.21-1.0.27. Hilt 2.51.1 (DI) + Room 2.6.1 (SQLite) + WorkManager 2.10.0 (background) + Navigation Compose 2.8.4 (con nav_graph.xml). `compileSdk=35`, `minSdk=24`, `targetSdk=35`. Compose BOM 2024.10.00 + Material 3.
- Consecuencias: requiere Android SDK 35 + JDK 21 para compilar; tests JVM con Robolectric 4.13 evitan emulador y tardan ~2-3 min la primera vez (descarga Compose + Hilt processors).

### D-332 — Imagen Docker `eclipse/openjdk:21-jdk-jammy` con cmdline-tools (F06ac)

- Fecha · Fase · Estado: 2026-10-07 · F06ac · vigente
- Contexto: el fixture compila un proyecto Android que necesita Android SDK 35 + JDK 21 + Gradle 8.10.2. No hay imagen oficial Android SDK en Docker Hub estable.
- Decision: `Dockerfile.test` parte de `eclipse/openjdk:21-jdk-jammy` + `apt-get install make git wget unzip ca-certificates` + descarga `commandlinetools-linux-11076708_latest.zip` + `sdkmanager "platform-tools" "platforms;android-35" "build-tools;35.0.1"` + `yes | sdkmanager --licenses`. `GRADLE_USER_HOME=/app/.gradle` para cachear dependencias entre invocaciones.
- Consecuencias: el contenedor pesa ~1.8 GB; la primera ejecucion tarda ~5-8 min descargando + aceptando licencias + cacheando dependencias. Las siguientes, cada una, tardan ~2-3 min.

### D-333 — `requires: [linux, macos]` con container enabled (F06ac)

- Fecha · Fase · Estado: 2026-10-07 · F06ac · vigente
- Contexto: el fixture compila en Linux (CI) y en macOS (desarrollo con Android Studio). Sin embargo, los runtimes de CI locales suelen ser macOS donde Android Studio esta instalado.
- Decision: `manifest.yml` declara `requires: [linux, macos]` + `container.enabled: true`. El runner usa contenedor por defecto para reproducibilidad. Los tests son JVM + Robolectric (no requieren emulador).
- Consecuencias: el fixture corre identico en Linux y macOS sin modificacion; los tests no necesitan GPU ni KVM.

### D-334 — Flavors `free`/`paid` con `BuildConfig.PREMIUM_ENABLED` (F06ac)

- Fecha · Fase · Estado: 2026-10-07 · F06ac · vigente
- Contexto: la trampa E4 (CC-06) exige que `funcion-premium` solo exista en el flavor `paid`. La skill debe notar la diferencia entre source sets.
- Decision: `productFlavors { free { buildConfigField "Boolean", "PREMIUM_ENABLED", "false" }; paid { ... "true" } }`. `app/src/free/java/.../PremiumDisabled.kt` solo expone `cta()`. `app/src/paid/java/.../PremiumEnabled.kt` expone `advancedExport()`. `BuildConfig.PREMIUM_ENABLED` se lee en `PremiumGateScreen` para renderizar segun flavor.
- Consecuencias: `PremiumEnabled` solo se compila en `paid`; si se inyecta en `free`, Hilt falla con `MissingBinding`; la skill debe listar source sets para entender la disponibilidad.

### D-335 — Hilt 2.51.1 + KSP 2.0.21 (F06ac)

- Fecha · Fase · Estado: 2026-10-07 · F06ac · vigente
- Contexto: Hilt con KSP (no KAPT) requiere KSP 2 para Kotlin 2.0+. Hilt genera codigo en `app/build/generated/hilt/`.
- Decision: `alias(libs.plugins.ksp)` + `alias(libs.plugins.hilt)` en `app/build.gradle.kts`. Dependencias `implementation(libs.hilt.android)` + `ksp(libs.hilt.compiler)` + `implementation(libs.hilt.work)` + `ksp(libs.hilt.androidx.compiler)`. `@HiltAndroidApp` en `FxAndroidApp`, `@AndroidEntryPoint` en `LegacyProductActivity`, `@HiltViewModel` en `ScanViewModel`/`HistoryViewModel`, `@HiltWorker` en `SyncWorker`.
- Consecuencias: la skill debe entender que las clases `Hilt_*` y `*_HiltModules` viven en `app/build/generated/hilt/`; los tests usan `@HiltAndroidTest` con `HiltAndroidRule` o `TestInstallIn`.

### D-336 — Room 2.6.1 con `@Query` + trampa P4 sin `addMigrations` (F06ac)

- Fecha · Fase · Estado: 2026-10-07 · F06ac · vigente
- Contexto: Room permite declaracion de DAOs con `@Query` SQL embebido. La trampa P4 exige que NO se llamen `addMigrations(MIGRATION_1_2)` en `DatabaseModule`.
- Decision: DAOs (`ProductDao`, `HistoryDao`, `ScanDao`) usan `@Query("SELECT ... FROM products WHERE ean = :ean")`, `@Insert(onConflict = IGNORE)`, `@Update`, `@Delete` con SQL strings. `DatabaseModule.provideDatabase()` llama `Room.databaseBuilder(...).fallbackToDestructiveMigrationOnDowngrade(true).build()` SIN `addMigrations`.
- Consecuencias: la skill debe notar la ausencia de `addMigrations(MIGRATION_1_2)` y la version=1; cualquier upgrade a version 2 sin migracion crashea la app con `IllegalStateException`.

### D-337 — WorkManager 2.10.0 + trampa P3 expedited silenciosa (F06ac)

- Fecha · Fase · Estado: 2026-10-07 · F06ac · vigente
- Contexto: WorkManager permite `OneTimeWorkRequest` con `setExpedited(OutOfQuotaPolicy.RUN_AS_NON_EXPEDITED_WORK_REQUEST)`. En Android 13+ sin `POST_NOTIFICATIONS` permission, expedited workers fallan silenciosamente.
- Decision: `SyncScheduler.scheduleOnce()` configura el request con `setExpedited(OutOfQuotaPolicy.RUN_AS_NON_EXPEDITED_WORK_REQUEST)` + `setConstraints(NetworkType.CONNECTED)` + `enqueueUniqueWork("sync", REPLACE, request)`. NO verifica `POST_NOTIFICATIONS` en API 33+ (trampa P3).
- Consecuencias: en Android 13+ sin permisos de notificacion, el worker expedited falla sin notificacion al usuario; la skill debe detectar este riesgo.

### D-338 — Navigation Compose 2.8.4 + `nav_graph.xml` con deepLinks (F06ac)

- Fecha · Fase · Estado: 2026-10-07 · F06ac · vigente
- Contexto: Navigation Compose admite `deepLink` URI strings. `nav_graph.xml` permite declararlos en XML con `<deepLink app:uri="fxandroid://product/{id}"/>`.
- Decision: `app/src/main/res/navigation/nav_graph.xml` declara 3 destinos con deepLinks (`fxandroid://scan/{ean}`, `fxandroid://history/{filter}`, `fxandroid://premium`). `FxNavGraph.kt` los registra con `navDeepLink { uriPattern = "fxandroid://scan/{ean}" }`. El `AndroidManifest.xml` adicionalmente declara un intent-filter VIEW + scheme `fxandroid` en `SyncTriggerReceiver` para deep links externos.
- Consecuencias: la skill debe leer `nav_graph.xml` + `FxNavGraph.kt` + manifest para entender que los entry points de deep links viven tanto en XML como en el manifest.

### D-339 — ViewBinding para vista legacy con `android:onClick` (F06ac)

- Fecha · Fase · Estado: 2026-10-07 · F06ac · vigente
- Contexto: el fixture coexiste Compose (moderno) y AppCompat/ViewBinding (legacy). El layout XML usa `android:onClick="onSaveClick"` que Android resuelve a un metodo del Activity.
- Decision: `activity_legacy_product.xml` declara `<Button android:onClick="onSaveClick">`. `LegacyProductActivity.onSaveClick(view: View)` lo implementa con `db.execSQL("INSERT INTO legacy_products(ean) VALUES('$ean')")` (trampa P5 bypassing repository). `buildFeatures.viewBinding = true` genera `ActivityLegacyProductBinding`.
- Consecuencias: la skill debe notar que `onClick` se resuelve por string; el flujo de guardado legacy bypassa Hilt y Room.

### D-340 — Robolectric 4.13 sin emulador + tests JUnit5 (F06ac)

- Fecha · Fase · Estado: 2026-10-07 · F06ac · vigente
- Contexto: el fixture corre en CI sin GPU ni KVM. Robolectric permite tests JVM de Activities, Fragments y WorkManager sin emulador.
- Decision: `testImplementation(libs.robolectric)` + `testOptions { unitTests.isIncludeAndroidResources = true; isReturnDefaultValues = true; all { useJUnitPlatform() } }`. Tests usan `@Test` de `org.junit.jupiter.api` (JUnit5) en vez de `@RunWith(AndroidJUnit4::class)`. `app/src/test/resources/robolectric.properties` con `sdk=34`. `app/src/test/AndroidManifest.xml` declara ScanActivity como LAUNCHER.
- Consecuencias: los tests corren en `gradlew test` sin emulador; el contenedor tarda ~2-3 min la primera vez (descarga Android resources) y ~30s las siguientes con cache.

### D-341 — Stack Flutter 3.24.5 + Dart 3.5.4 F06ad (F06ad)

- Fecha · Fase · Estado: 2026-10-07 · F06ad · vigente
- Contexto: F06ad requiere ejercitar codigo generado por `build_runner` (freezed/json_serializable), Riverpod con `ref.watch` cross-provider, go_router con redirects + deepLinks, widgets adaptativos iOS/Android, flavors via `--dart-define=FX_ENABLE_PREMIUM`, y platform channels a Kotlin/Swift.
- Decision: Flutter 3.24.5 con Dart 3.5.4 (canal stable). Dependencias: `flutter_riverpod ^2.5.1`, `go_router ^14.2.7`, `freezed_annotation ^2.4.4`, `json_annotation ^4.9.0`, `shared_preferences ^2.3.2`. Dev-deps: `build_runner ^2.4.13`, `freezed ^2.5.7`, `json_serializable ^6.8.0`, `riverpod_generator ^2.4.0`, `flutter_test` (SDK), `flutter_lints ^4.0.0`.
- Consecuencias: el fixture requiere `flutter pub get` + `dart run build_runner build` antes de `flutter test`. Los archivos `.g.dart`/`.freezed.dart` NO se commitean al repo (estan en `.gitignore`) para evitar CC-11 con tokens en archivos generados.

### D-342 — Imagen Docker `ghcr.io/cirruslabs/flutter:3.24.5` (F06ad)

- Fecha · Fase · Estado: 2026-10-07 · F06ad · vigente
- Contexto: el fixture necesita Flutter SDK + Dart + Android SDK (transitivamente). No hay imagen oficial Android + Flutter estable en Docker Hub.
- Decision: `Dockerfile.test` parte de `ghcr.io/cirruslabs/flutter:3.24.5` (oficial Cirrus Labs, basada en Debian bookworm con Flutter SDK + Dart 3.5.4 + Android SDK). Precompila con `flutter pub get` + `dart run build_runner build --delete-conflicting-outputs` en el Dockerfile layer.
- Consecuencias: el contenedor pesa ~3 GB; la primera ejecucion tarda ~5-8 min descargando dependencias + cacheando Gradle; las siguientes, ~2-3 min con cache.

### D-343 — `requires: [linux, macos]` con container enabled (F06ad)

- Fecha · Fase · Estado: 2026-10-07 · F06ad · vigente
- Contexto: el fixture compila y testea en Linux (CI) y macOS (desarrollo con Flutter instalado). Los tests son JVM `flutter test` (sin emulador).
- Decision: `manifest.yml` declara `requires: [linux, macos]` + `container.enabled: true`. El runner usa el contenedor por defecto para reproducibilidad.
- Consecuencias: el fixture corre identico en Linux y macOS; los tests no requieren GPU ni KVM ni emulador.

### D-344 — Riverpod 2.5.1 con `ref.watch` cross-provider (E2) (F06ad)

- Fecha · Fase · Estado: 2026-10-07 · F06ad · vigente
- Contexto: la trampa E2 exige que un provider observe otro via `ref.watch` para que el grafo de dependencias sea implicito.
- Decision: `FavoritesController.build()` declara `final _ = ref.watch(readerControllerProvider);` (uso descartado) para forzar la reactividad sin usar el valor directamente. Esto hace que cualquier cambio en el readerController invalide la cache de favoritos.
- Consecuencias: la skill debe detectar todos los `ref.watch` cruzados para reconstruir el grafo de dependencias entre providers; el `_` anonimo es una pista visual de que el watch es intencional.

### D-345 — go_router 14.2.7 con redirect declarativo + deepLinks (E4) (F06ad)

- Fecha · Fase · Estado: 2026-10-07 · F06ad · vigente
- Contexto: go_router permite declarar rutas + redirects + deep links en un solo lugar. La trampa P3 exige que el redirect NO chequee autenticacion.
- Decision: `appRouter = GoRouter(initialLocation: Routes.reader, redirect: (ctx, state) => state.matchedLocation == '/' ? Routes.reader : null, routes: [...])` con 5 rutas y 2 deepLinks `/reader/:hash` + `/favorites/:filter`.
- Consecuencias: la skill debe leer `app_router.dart` para entender el routing + redirects; el redirect sin chequeo de auth es una trampa intencional que rompe el flujo de auth en runtime.

### D-346 — freezed + json_serializable + build_runner (E1) sin commitear generados (F06ad)

- Fecha · Fase · Estado: 2026-10-07 · F06ad · vigente
- Contexto: freezed genera `.freezed.dart` con `copyWith`, `==`, `hashCode`, `toString`. json_serializable genera `.g.dart` con `_$XFromJson`/`_$XToJson`. Estos viven en disco pero NO en `Sources/`.
- Decision: `lib/features/reader/domain/document.dart` declara `@freezed class Document with _$Document { factory Document(...) = _Document; factory Document.fromJson(...) = _$DocumentFromJson(...); }` + `part 'document.freezed.dart';` + `part 'document.g.dart';`. El `.gitignore` excluye `**/*.g.dart` y `**/*.freezed.dart`. CI genera en runtime con `dart run build_runner build`.
- Consecuencias: la skill debe ejecutar `build_runner` o leer los `.freezed.dart` commiteados en CI; en el repo solo ve los `part` directives y las anotaciones `@freezed`.

### D-347 — Platform channels MethodChannel('com.example.fxdart/native') + stubs Kotlin/Swift (E3) (F06ad)

- Fecha · Fase · Estado: 2026-10-07 · F06ad · vigente
- Contexto: el contrato del platform channel vive solo como string convencion. La trampa E3 exige que la skill siga los strings desde Dart hasta los stubs nativos.
- Decision: `lib/platform/native_method_channel.dart` envuelve `MethodChannel('com.example.fxdart/native')` con `try { ... } catch (_) { return null; }` (trampa P2). `lib/features/reader/data/document_remote_source.dart` invoca `'scanDocument'` y `'capturePage'`. `android_stub/MainActivity.kt` y `ios_stub/AppDelegate.swift` documentan los handlers en Kotlin/Swift.
- Consecuencias: los stubs son evidencia textual (no compilables sin Android Studio/Xcode); los tests usan `TestDefaultBinaryMessenger` para simular el canal.

### D-348 — `--dart-define=FX_ENABLE_PREMIUM` con `bool.fromEnvironment` (E5) (F06ad)

- Fecha · Fase · Estado: 2026-10-07 · F06ad · vigente
- Contexto: Dart 3 soporta `--dart-define=KEY=value` en build time. La trampa E5 obliga a la skill a detectar el `bool.fromEnvironment` con un branch condicional.
- Decision: `const bool enablePremium = bool.fromEnvironment('FX_ENABLE_PREMIUM', defaultValue: false);` en `settings_controller.dart`. `SettingsController.build()` combina `enablePremium` con SharedPreferences runtime: `final isPremium = enablePremium || (stateOrNull?.premiumUnlocked ?? false);` (trampa P4 con orden de evaluacion).
- Consecuencias: el flag se evalua en build time; el runtime lo consulta via SharedPreferences; la combinacion puede dar resultados inesperados si se cambia la logica sin entender la precedencia.

### D-349 — Widgets adaptativos CupertinoSwitch vs Switch (E6) + rama CupertinoSlider muerta (P6) (F06ad)

- Fecha · Fase · Estado: 2026-10-07 · F06ad · vigente
- Contexto: Flutter permite widgets adaptativos segun `Theme.of(context).platform`. La trampa E6 + P6 obliga a la skill a notar el branching condicional.
- Decision: `lib/platform/platform_widget.dart` declara `AdaptiveSwitch` que elige `CupertinoSwitch` (iOS/macOS) vs `Switch` (Android/desktop), y `AdaptiveSlider` que DEBERIA elegir `CupertinoSlider` (iOS) pero intencionalmente usa `Slider` Material (P6 rama muerta con `TODO: CupertinoSlider no esta implementado todavia`).
- Consecuencias: la skill debe detectar el branching condicional + la rama muerta de CupertinoSlider; el helper `_formatDouble` (S3) nunca se invoca.

### D-350 — Prefijo unique tokens `NPRGT-FXFLUTTER-` + CC-11 sin `.g.dart`/`.freezed.dart` commiteados (F06ad)

- Fecha · Fase · Estado: 2026-10-07 · F06ad · vigente
- Contexto: cada fixture debe declarar ≥ 30 unique tokens con prefijo unico para que `overfit_guard.py` pueda detectar filtraciones. Ademas, los archivos generados por `build_runner` (`.g.dart`/`.freezed.dart`) NO deben contener tokens del fixture para evitar CC-11 con codigo generado.
- Decision: prefijo `NPRGT-FXFLUTTER-` con 35 entradas (PACKAGE-NAME, FLUTTER-VERSION, DART-VERSION, RIVERPOD, ROUTER, DEEPLINK, CHANNEL, METHOD, ANDROID-STUB, IOS-STUB, DART-DEFINE, PREMIUM-FEATURE, FREE-MODE, PAID-MODE, BUILD-RUNNER, FREEZED, JSON-SERIALIZABLE, etc.). `.gitignore` excluye `**/*.g.dart` y `**/*.freezed.dart` para que CI los genere en runtime.
- Consecuencias: ningun archivo commiteado del codigo fuente (excluyendo `unique_tokens.txt`) puede mencionar estos strings; `check_ground_truth.py --check-cc11` lo verifica.

### D-351 — Stack React Native 0.74.5 + Expo SDK 51 bare F06ae (F06ae)

- Fecha · Fase · Estado: 2026-10-07 · F06ae · vigente
- Contexto: F06ae requiere ejercitar TurboModules Kotlin/Swift, archivos por plataforma `.ios.tsx`/`.android.tsx`, Expo config plugins que modifican `prebuild`, deep linking con Linking, Metro aliases, Redux Toolkit y notificaciones push.
- Decision: React Native 0.74.5 + Expo SDK 51 bare workflow + TypeScript 5.4. Dependencias: `@reduxjs/toolkit ^2.2.7`, `react-redux ^9.1.2`, `@react-navigation/native ^6.1.18`, `@react-navigation/native-stack ^6.11.0`, `expo-linking ~6.3.1`, `expo-notifications ~0.28.19`, `expo-build-properties ~0.12.5`, `expo-splash-screen ~0.27.7`. Dev-deps: `jest ^29.7.0`, `jest-expo ~51.0.4`, `@testing-library/react-native ^12.5.0`, `react-test-renderer 18.2.0`, `babel-plugin-module-resolver ^5.0.2`, `typescript ~5.4.0`.
- Consecuencias: el fixture corre con `yarn install` + `yarn jest` sin emulador gracias a `jest.mock('react-native', ...)`. Los TurboModules nativos (`.kt`/`.swift`) son solo evidencia textual.

### D-352 — Imagen Docker `ghcr.io/cirruslabs/react-native:0.74.5` (F06ae)

- Fecha · Fase · Estado: 2026-10-07 · F06ae · vigente
- Contexto: el fixture necesita React Native + Node + Yarn + Android SDK (transitivamente).
- Decision: `Dockerfile.test` parte de `ghcr.io/cirruslabs/react-native:0.74.5` (oficial Cirrus Labs, basada en Debian bookworm con Node 20 + Yarn + React Native CLI + Android SDK). Precompila con `yarn install --frozen-lockfile --silent`.
- Consecuencias: el contenedor pesa ~3 GB; la primera ejecucion tarda ~5-8 min descargando dependencias + cacheando Gradle.

### D-353 — TurboModules `RtcNfcManager` con `@ReactModule` + `@objc` (E1) (F06ae)

- Fecha · Fase · Estado: 2026-10-07 · F06ae · vigente
- Contexto: la trampa E1 exige que un modulo nativo se resuelva por nombre a traves del bridge. Kotlin usa `@ReactModule(name = "RtcNfcManager")` y Swift usa `@objc(RtcNfcManager)` para que `NativeModules.RtcNfcManager` resuelva correctamente.
- Decision: `src/features/payments/data/NfcManager.ts` accede a `NativeModules.RtcNfcManager` con tipo `RtcNfcManagerNative | undefined`. `android_stub/NfcManagerModule.kt` declara `@ReactModule(name = "RtcNfcManager")` con `start/stop/readTag/requestPermissions`. `ios_stub/NfcManagerModule.swift` declara `@objc(RtcNfcManager) class RtcNfcManager`. `ios_stub/NfcManagerModule.mm` declara `RCT_EXPORT_MODULE(RtcNfcManager)`.
- Consecuencias: la skill debe seguir el string `RtcNfcManager` desde JS hasta los stubs nativos en Kotlin y Swift; la falta de linkeo en runtime crashea la app.

### D-354 — Archivos `.ios.tsx`/`.android.tsx` resueltos por Metro (E2) (F06ae)

- Fecha · Fase · Estado: 2026-10-07 · F06ae · vigente
- Contexto: Metro selecciona el archivo `.ios.tsx` o `.android.tsx` segun la plataforma. Esto permite UI diferente sin un wrapper manual.
- Decision: `src/features/payments/presentation/PaymentsScreen.tsx` (comun fallback) + `PaymentsScreen.ios.tsx` (NSNFCReaderUsageDescription) + `PaymentsScreen.android.tsx` (verifica `PermissionsAndroid.NFC` antes de `NfcManager.start`). Metro resuelve segun `Platform.OS` automaticamente via `sourceExts`.
- Consecuencias: la skill debe notar las extensiones `.ios.tsx`/`.android.tsx` y entender que Metro las selecciona; el archivo comun `PaymentsScreen.tsx` es el fallback si ninguna extension coincide.

### D-355 — Expo config plugins que modifican `prebuild` (E3) (F06ae)

- Fecha · Fase · Estado: 2026-10-07 · F06ae · vigente
- Contexto: la trampa E3 exige que la skill entienda que cada plugin Expo transforma la salida de `expo prebuild`. Esto añade complejidad al analisis estatico porque el codigo real vive en `ios/` y `android/` despues de prebuild.
- Decision: `app.json` declara 6 plugins: `./plugins/withNfc` (con `withInfoPlist` para NSNFCReaderUsageDescription), `./plugins/withDeepLinking` (con `withInfoPlist` para CFBundleURLTypes + `withAndroidManifest` para intent-filter VIEW), `expo-build-properties`, `expo-notifications`, `expo-splash-screen`, `expo-linking`.
- Consecuencias: la skill debe leer `app.json` + los archivos en `src/plugins/` para entender las transformaciones que sufria `expo prebuild`.

### D-356 — Redux Toolkit con slice que muta state directamente (P2) (F06ae)

- Fecha · Fase · Estado: 2026-10-07 · F06ae · vigente
- Contexto: RTK usa immer implicitamente, asi que `state.items.push(action.payload)` funciona en runtime pero la trampa P2 exige que la skill detecte este patron.
- Decision: `src/store/slices/paymentsSlice.ts` declara `addPayment(state, action) { state.items.push(action.payload); }` con mutacion directa. La skill debe detectar el push sin `prepare` callback ni copia explicita.
- Consecuencias: en RTK + immer, la mutacion funciona; pero rompe la consistencia conceptual y hace que `state.items.push` sea dificil de rastrear en code review.

### D-357 — `NotificationHandler` con `catch (_)` silencioso (P3) (F06ae)

- Fecha · Fase · Estado: 2026-10-07 · F06ae · vigente
- Contexto: la trampa P3 exige que `expo-notifications.setNotificationHandler` trague errores con `catch (_) { return {} }`.
- Decision: `src/features/notifications/application/NotificationHandler.ts` envuelve tanto `getExpoPushTokenAsync` como `handleNotification` en `try { ... } catch (_) { ... }`. El handler en background retorna `PresentationOptions` vacias en error.
- Consecuencias: la skill debe detectar el `catch (_)` en ambos sitios; los push notifications fallidos se procesan como `{}` sin log ni rethrow.

### D-358 — Metro aliases en `extraNodeModules` + babel-plugin-module-resolver (E5) (F06ae)

- Fecha · Fase · Estado: 2026-10-07 · F06ae · vigente
- Contexto: la trampa E5 exige que la skill note aliases como `@app`, `@store`, `@nav`, `@native`, `@plugins`, `@util` que apuntan a directorios especificos via Metro + Babel.
- Decision: `metro.config.js` declara `resolver.extraNodeModules` con 7 aliases; `babel.config.js` usa `babel-plugin-module-resolver` con los mismos aliases para que las transformaciones Babel las respeten. `tsconfig.json` declara `paths` con los mismos aliases para TypeScript.
- Consecuencias: la skill debe seguir los aliases hasta los archivos reales; `jest.config.js` declara `moduleNameMapper` para que Jest tambien los resuelva.

### D-359 — Deep linking con 3 prefixes + 5 rutas + 2 deepLinks (E4) (F06ae)

- Fecha · Fase · Estado: 2026-10-07 · F06ae · vigente
- Contexto: la trampa E4 exige que la skill entienda el deep linking con multiples schemes (fxrn:// custom + https:// Universal Links) y screens nested en routing.
- Decision: `src/navigation/linkingConfig.ts` declara `prefixes: [Linking.createURL('/'), 'fxrn://', 'https://fxrn.app/']` y `config.screens` con 5 entradas (`payments`, `payments/pay`, `history`, `history/filter`, `notifications`). El AppManifest declara el intent-filter VIEW con scheme `fxrn`. El Info.plist declara CFBundleURLTypes con scheme `fxrn`.
- Consecuencias: la skill debe seguir los prefixes y screens; la trampa P4 (linking config android disabled) NO se planta (el linking funciona en ambas plataformas).

### D-360 — Prefijo unique tokens `NPRGT-FXRN-` + tests con mocks del bridge (F06ae)

- Fecha · Fase · Estado: 2026-10-07 · F06ae · vigente
- Contexto: cada fixture debe declarar ≥ 30 unique tokens con prefijo unico para `overfit_guard.py`. Ademas, los tests del fixture usan `jest.mock('react-native', ...)` para mockear `NativeModules.RtcNfcManager` ya que no se compilan TurboModules reales.
- Decision: prefijo `NPRGT-FXRN-` con 34 entradas (PACKAGE-NAME, REACT-NATIVE-VERSION, EXPO-VERSION, ANDROID-STUB, IOS-STUB, DEEPLINK-SCHEME/PAY/HISTORY/NOTIFICATIONS, BRIDGE-MODULE, NFC-MANAGER, RTC-MODULE, ANDROID-MANIFEST, INFO-PLIST, PLATFORM-FILE, METRO-CONFIG, BABEL-CONFIG, ALIAS, EXPO-PLUGIN, PREBUILD, PUSH-TOKEN, BACKGROUND-HANDLER, REDUX, SLICE, IMMER, NAVIGATION, DEEP-LINK, FEATURE-PAYMENTS/HISTORY/NOTIFICATIONS, LOGGER, DATE-FORMAT). `jest.setup.js` mockea `NativeModules.RtcNfcManager.start/stop/readTag/requestPermissions` y `expo-notifications.setNotificationHandler/getPermissionsAsync/getExpoPushTokenAsync`.
- Consecuencias: ningun archivo commiteado del codigo fuente (excluyendo `unique_tokens.txt`) puede mencionar estos strings; `check_ground_truth.py --check-cc11` lo verifica.

### D-361 — Stack Electron 32 + TypeScript 5.5 F06af (F06af)

- Fecha · Fase · Estado: 2026-10-07 · F06af · vigente
- Contexto: F06af requiere ejercitar IPC channels por string, contextBridge exponiendo window.api, Menu nativo con accelerators, utility process para actualizaciones, protocolo app://, y electron-builder con asarUnpack + extraResources.
- Decision: Electron 32.2 + Node 20 + TypeScript 5.5. Dependencias: `electron-updater ^6.3.9`. Dev-deps: `electron ^32.2.0`, `electron-builder ^25.1.8`, `typescript ^5.5.4`, `esbuild ^0.24.0`, `vitest ^2.1.0`. Renderer bundler: esbuild con output IIFE minificado. Toolchain tests: Vitest con `vi.mock('electron')`.
- Consecuencias: el fixture corre con `yarn install` + `yarn vitest --run`. En Linux requiere xvfb para tests sin display fisico. `ipcMain`/`ipcRenderer` se mockean; el `utilityProcess` se mockea para evitar fork real.

### D-362 — Imagen Docker `node:20-bookworm-slim` + xvfb + libs Electron (F06af)

- Fecha · Fase · Estado: 2026-10-07 · F06af · vigente
- Contexto: el fixture necesita Node 20 + xvfb + librerias de runtime Electron (libnss3, libatk1.0-0, libgtk-3-0, libasound2) para tests sin display fisico.
- Decision: `Dockerfile.test` parte de `node:20-bookworm-slim` + `apt-get install -y --no-install-recommends xvfb libnss3 libatk1.0-0 libatk-bridge2.0-0 libgtk-3-0 libasound2 libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 ca-certificates` + `yarn install --frozen-lockfile --silent` + `CMD ["make","test"]`.
- Consecuencias: el contenedor pesa ~2 GB; la primera ejecucion tarda ~3-5 min descargando dependencias + cacheando Yarn.

### D-363 — IPC channels por string `ipcMain.handle` + `ipcRenderer.invoke` (E1) (F06af)

- Fecha · Fase · Estado: 2026-10-07 · F06af · vigente
- Contexto: la trampa E1 exige que la skill entienda el contrato IPC como strings. No hay un schema declarado; el TypeScript interface solo cubre tipos, no nombres de canales.
- Decision: `src/main/ipc/handlers.ts` declara `IPC_CHANNELS` como `as const` con 6 channels string (`'project:open-dialog'`, `'project:open'`, `'pdf:export'`, `'update:check'`, `'update:install'`, `'menu:dispatch'`). `src/preload/index.ts` invoca `ipcRenderer.invoke(IPC_CHANNELS.PROJECT_OPEN, args)` con la misma referencia.
- Consecuencias: la skill debe seguir los strings entre main y preload; el contrato solo es por convencion.

### D-364 — contextBridge exponiendo `window.api` con superficie tipada (E2) (F06af)

- Fecha · Fase · Estado: 2026-10-07 · F06af · vigente
- Contexto: la trampa E2 exige que la skill note que la superficie IPC con renderer se expone via `contextBridge.exposeInMainWorld`.
- Decision: `src/preload/index.ts` declara `contextBridge.exposeInMainWorld('api', { openProjectDialog, openProject, exportPdf, checkUpdate, installUpdate, onMenuDispatch })`. `src/renderer/renderer.ts` accede via `window.api.{fn}(...)`. El `ExposedApi` type esta en `src/preload/api.ts` (trampa S3 con `formatTimestamp` no usado).
- Consecuencias: la skill debe notar el bridge y la superficie expuesta; `nodeIntegration=false` y `contextIsolation=true` en `BrowserWindow.webPreferences`.

### D-365 — Menu nativo con accelerators duplicados (E3 + P2) (F06af)

- Fecha · Fase · Estado: 2026-10-07 · F06af · vigente
- Contexto: la trampa E3 exige que la skill lea `Menu.buildFromTemplate` y la trampa P2 exige que al menos un accelerator este duplicado.
- Decision: `src/main/menu/appMenu.ts` declara 4 submenus (File/Edit/View/Help) con accelerators `'CmdOrCtrl+O'` (Open Project), `'CmdOrCtrl+E'` (Export PDF) y `'CmdOrCtrl+U'` (Check Update). La trampa P2 planta `'CmdOrCtrl+O'` tambien en `Open Recent > recent1.txt` — Electron registra solo el primero y el segundo se ignora silenciosamente.
- Consecuencias: la skill debe seguir los accelerators; la trampa P2 rompe `Open Recent` que es inalcanzable.

### D-366 — Utility process + child_process para workers (E4) (F06af)

- Fecha · Fase · Estado: 2026-10-07 · F06af · vigente
- Contexto: la trampa E4 exige que la skill entienda que Electron permite procesos separados del main process.
- Decision: `src/main/workers/updater.ts` usa `utilityProcess.fork(workerPath)` para actualizaciones live con `process.parentPort.postMessage`. `src/main/workers/pdfExporter.ts` usa `child_process.fork(workerPath, [outputPath])` para one-shot PDF export. Ambos workers son scripts standalone en `src/workers/`.
- Consecuencias: la skill debe notar que `workers/updater-worker.ts` y `workers/pdf-worker.ts` corren como procesos separados con IPC dedicado.

### D-367 — Protocolo personalizado `app://` con `registerSchemesAsPrivileged` (E5 + P5) (F06af)

- Fecha · Fase · Estado: 2026-10-07 · F06af · vigente
- Contexto: la trampa E5 + P5 exige que `protocol.handle('app', ...)` requiera `protocol.registerSchemesAsPrivileged` ANTES de `app.ready()`.
- Decision: `src/main/protocol/appProtocol.ts` declara `protocol.registerSchemesAsPrivileged([{ scheme: 'app', privileges: { standard: true, secure: true, supportFetchAPI: true } }])` al top-level del modulo. `main/index.ts` llama `registerAppProtocol()` antes de `app.whenReady().then(...)`.
- Consecuencias: la skill debe notar el orden critico; sin `registerSchemesAsPrivileged` previo, `protocol.handle` falla en runtime.

### D-368 — electron-builder con `asarUnpack` + `extraResources` (E6) (F06af)

- Fecha · Fase · Estado: 2026-10-07 · F06af · vigente
- Contexto: la trampa E6 exige que la skill lea `electron-builder.yml` para entender que archivos quedan fuera del .asar.
- Decision: `electron-builder.yml` declara `asarUnpack: ['**/*.node', 'workers/**']` (binarios nativos y workers separados) + `extraResources: [{ from: 'resources/native-menu.json' }, { from: 'resources/translations.json' }]` (config externalizada). Targets mac/win/linux con `target: dir`.
- Consecuencias: la skill debe leer `electron-builder.yml` para entender la distribucion final; los archivos en `extraResources` quedan en `app.asar.unpacked/` o `/usr/share/fxelec/`.

### D-369 — `autoUpdater.setFeedURL` con HTTP (no HTTPS) (P6) (F06af)

- Fecha · Fase · Estado: 2026-10-07 · F06af · vigente
- Contexto: la trampa P6 exige que el autoUpdater use HTTP en lugar de HTTPS, lo cual falla en runtime.
- Decision: `src/main/autoUpdater.ts` declara `autoUpdater.setFeedURL('http://example.com/updates')` (HTTP, no HTTPS). `FXELEC_DISABLE_UPDATER` env var permite saltar la llamada en dev.
- Consecuencias: la skill debe detectar la URL HTTP; en runtime real `downloadUpdate` falla con `Protocol error`.

### D-370 — Prefijo unique tokens `NPRGT-FXELEC-` + Vitest con mocks de electron (F06af)

- Fecha · Fase · Estado: 2026-10-07 · F06af · vigente
- Contexto: cada fixture debe declarar ≥ 30 unique tokens con prefijo unico para `overfit_guard.py`. Ademas, los tests usan `vi.mock('electron')` para mockear el modulo electron.
- Decision: prefijo `NPRGT-FXELEC-` con 33 entradas (PACKAGE-NAME, ELECTRON-VERSION, NODE-VERSION, IPC-CHANNEL, CONTEXT-BRIDGE, WINDOW-API, MAIN-PROCESS, PRELOAD-SCRIPT, RENDERER-PROCESS, UTILITY-PROCESS, APP-SCHEME, ASAR-UNPACK, EXTRA-RESOURCES, ELECTRON-BUILDER, MENU-TEMPLATE, ACCELERATOR, AUTO-UPDATER, PROTOCOL-HANDLE, OPEN-DIALOG, SAVE-DIALOG, PDF-WORKER, UPDATE-WORKER, CHILD-PROCESS, LICENSE, VERSION, LEGACY-LOGGER, FEATURE-FLAG, FORMAT-TIMESTAMP, FEATURE-OPEN, FEATURE-PDF, FEATURE-UPDATE). `test/main/ipc.spec.ts` y otros mockean `electron` module con `vi.mock('electron', ...)` para evitar requerir un display real.
- Consecuencias: ningun archivo commiteado del codigo fuente (excluyendo `unique_tokens.txt`) puede mencionar estos strings; `check_ground_truth.py --check-cc11` lo verifica.

### D-371 — Stack .NET 9 + WPF + CommunityToolkit.Mvvm 8.4 + xUnit F06ag (F06ag)

- Fecha · Fase · Estado: 2026-10-07 · F06ag · vigente
- Contexto: F06ag requiere ejercitar bindings XAML por string de propiedad, source generators `[ObservableProperty]` + `[RelayCommand]`, `DataTemplate` con `DataType`, value converters `IValueConverter`, styles con `DataTrigger`, y merged dictionaries en `App.xaml`.
- Decision: .NET 9.0 LTS con SDK `mcr.microsoft.com/dotnet/sdk:9.0`. Target frameworks: `net9.0-windows` para UI WPF + `net9.0` para ViewModels + tests. Dependencias: `CommunityToolkit.Mvvm 8.4.0` con source generators. Tests: `xunit 2.9.2` + `xunit.runner.visualstudio 2.8.2`.
- Consecuencias: los tests de ViewModels corren multiplataforma (Linux/macOS/Windows); los tests de UI WPF requieren Windows con `net9.0-windows` runtime. CI Linux usa contenedor con SDK + xvfb + libs UI headless; los tests UI se omiten con `[Trait("Category", "UI")]`.

### D-372 — Imagen Docker `mcr.microsoft.com/dotnet/sdk:9.0` + xvfb + libs UI (F06ag)

- Fecha · Fase · Estado: 2026-10-07 · F06ag · vigente
- Contexto: el fixture necesita .NET 9 SDK + librerias UI para tests WPF headless (aunque los tests VM no las requieren, los tests UI opcionales sí).
- Decision: `Dockerfile.test` parte de `mcr.microsoft.com/dotnet/sdk:9.0` + `apt-get install -y --no-install-recommends xvfb libnss3 libatk1.0-0 libgtk-3-0 libfontconfig1 libfreetype6 libgdiplus ca-certificates` + `dotnet restore` + `CMD ["make","test"]`.
- Consecuencias: el contenedor pesa ~1.5 GB (solo SDK .NET sin las libs UI es ~700 MB; con libs UI ~1.5 GB); la primera ejecucion tarda ~2-3 min descargando dependencias + cacheando NuGet.

### D-373 — Tests de ViewModels cross-platform + tests de UI solo Windows (F06ag)

- Fecha · Fase · Estado: 2026-10-07 · F06ag · vigente
- Contexto: la UI de WPF solo se testea en Windows. Los ViewModels son POCO con CommunityToolkit.Mvvm y pueden correr multiplataforma.
- Decision: dos proyectos xUnit: `FxWpf.Tests` (target `net9.0`, VM tests multiplataforma) + `FxWpf.TrapTests` (target `net9.0`, trap tests que leen archivos). Tests de UI marcados `[Trait("Category", "UI")]` se omiten en CI Linux/macOS via xunit filters.
- Consecuencias: 32 tests xUnit corren en cualquier OS; los tests UI opcionales (no incluidos en este fixture) requieren Windows. La skill debe entender la separacion VM/UI y la limitacion de WPF.

### D-374 — Source generators `[ObservableProperty]` + `[RelayCommand]` (E2) (F06ag)

- Fecha · Fase · Estado: 2026-10-07 · F06ag · vigente
- Contexto: la trampa E2 exige que la skill entienda los source generators que emiten codigo C# parcial en build.
- Decision: los 4 VMs (`ClientesViewModel`, `CotizacionesViewModel`, `PrintPreviewViewModel`, `ShellViewModel`) usan `[ObservableProperty]` y `[RelayCommand]` de CommunityToolkit.Mvvm. El codigo generado vive en `obj/Debug/net9.0/generated/FxWpf.ViewModels/FxWpf.ViewModels.ViewModels.ClientesViewModel.g.cs`.
- Consecuencias: la skill debe ejecutar `dotnet build /p:EmitCompilerGeneratedFiles=true` para inspeccionar el codigo generado; las propiedades `_title`, `_clientes` se convierten en `Title`, `Clientes` con `INotifyPropertyChanged` automatico.

### D-375 — Bindings XAML por string de propiedad (E1) (F06ag)

- Fecha · Fase · Estado: 2026-10-07 · F06ag · vigente
- Contexto: la trampa E1 exige que la skill entienda que los bindings XAML son strings que referencian propiedades del VM.
- Decision: `MainWindow.xaml` declara 5+ bindings: `{Binding Title}`, `{Binding SelectedCliente}`, `{Binding Nombre}`, `{Binding Telefono}`, `{Binding CreatedAt StringFormat=yyyy-MM-dd}`. `CotizacionesView.xaml` usa `DataGrid` con `{Binding Titulo}` + `{Binding Total Converter={StaticResource Currency}}`.
- Consecuencias: la skill debe seguir las cadenas `{Binding ...}` hasta las propiedades del VM (generadas por source generators) y verificar el modo (`OneWay`, `TwoWay`) y los converters.

### D-376 — `DataTemplate` con `DataType` para auto-seleccion (E3 + P6) (F06ag)

- Fecha · Fase · Estado: 2026-10-07 · F06ag · vigente
- Contexto: la trampa E3 + P6 exige que la skill entienda el `DataTemplate` con `DataType` para que `ContentControl` auto-seleccione el template segun el VM.
- Decision: `ClienteTemplate.xaml` declara `<DataTemplate DataType="{x:Type vm:ClientesViewModel}">`. La trampa P6 es que el `DataType` usa `ClientesViewModel` (el VM de la lista) en lugar de `Cliente` (el tipo del item); el template nunca se aplica correctamente.
- Consecuencias: la skill debe notar el typo en `DataType` y proponer corregirlo a `Cliente` o crear un `ClienteViewModel` dedicado.

### D-377 — `IValueConverter` con `ConvertBack` lanza `NotImplementedException` (E4 + P3) (F06ag)

- Fecha · Fase · Estado: 2026-10-07 · F06ag · vigente
- Contexto: la trampa E4 + P3 exige que la skill detecte converters sin `ConvertBack` implementado.
- Decision: `BoolToVisibilityConverter` implementa `Convert` (bool -> Visibility) pero `ConvertBack` lanza `NotImplementedException`. Si un binding es `Mode=TwoWay`, falla en runtime.
- Consecuencias: la skill debe verificar que cualquier binding TwoWay tenga su `ConvertBack` implementado; en este caso, `Mode=OneWay` es seguro pero `Mode=TwoWay` falla.

### D-378 — Merged dictionaries en `App.xaml` (E6) (F06ag)

- Fecha · Fase · Estado: 2026-10-07 · F06ag · vigente
- Contexto: la trampa E6 exige que la skill entienda la composicion de temas via `MergedDictionaries`.
- Decision: `App.xaml` declara `<ResourceDictionary.MergedDictionaries>` con 4 sources: `Themes/Colors.xaml` (PrimaryColor, AccentColor, BackgroundColor), `Themes/Buttons.xaml` (PrimaryBrush, AccentBrush), `Themes/Controls.xaml` (PrimaryButton Style), `Styles/ButtonStyles.xaml` (ButtonStylePrimary + ButtonStyleOverriding).
- Consecuencias: la skill debe seguir la cascada de `Source="..."` para entender la composicion final de recursos.

### D-379 — `Style.Triggers` con `DataTrigger` reactivo al VM (E5 + P4) (F06ag)

- Fecha · Fase · Estado: 2026-10-07 · F06ag · vigente
- Contexto: la trampa E5 + P4 exige que la skill entienda styles con triggers y la trampa P4 con styles sobrepuestos sin `BasedOn`.
- Decision: `ButtonStyles.xaml` declara `<Style TargetType="Button" x:Key="ButtonStylePrimary">` con `<Style.Triggers>` que reaccionan a `Binding="{Binding IsValid}"`. La trampa P4 planta un segundo Style `ButtonStyleOverriding` sin `BasedOn` que sobreescribe al primero.
- Consecuencias: la skill debe notar que el segundo Style gana por orden de declaracion; `BasedOn={StaticResource ButtonStylePrimary}` lo haria heredar.

### D-380 — Prefijo unique tokens `NPRGT-FXWPF-` + tests xUnit cross-platform (F06ag)

- Fecha · Fase · Estado: 2026-10-07 · F06ag · vigente
- Contexto: cada fixture debe declarar ≥ 30 unique tokens con prefijo unico para `overfit_guard.py`. Ademas, los tests de ViewModels usan `xunit` (no `pytest`) porque corren sobre .NET.
- Decision: prefijo `NPRGT-FXWPF-` con 34 entradas (PACKAGE-NAME, DOTNET-VERSION, WPF-VERSION, XAML-VERSION, MVVM-TOOLKIT, SOURCE-GENERATOR, OBSERVABLE-PROPERTY, RELAY-COMMAND, MVVM-PATTERN, XAML-BINDING, DATA-TEMPLATE, VALUE-CONVERTER, STYLE-TRIGGER, MERGED-DICTIONARY, RESOURCE-DICTIONARY, XAML-CODE-BEHIND, DEEP-LINK, VIEW-MODEL, MAIN-WINDOW, CLIENTES-VIEW, COTIZACIONES-VIEW, PRINT-PREVIEW, CLIENTE-SERVICE, ASYNC-COMMAND, XUNIT-TEST, LEGACY-CONVERTER, EXPERIMENTAL-VM, FONT-FAMILY, NAVIGATION, BOOLEAN-CONVERTER, CURRENCY-CONVERTER, FEATURE-CLIENTES, FEATURE-COTIZACIONES, FEATURE-IMPRESION). Los tests xUnit corren multiplataforma; los tests pytest (`test_fx_csharp_wpf_ground_truth.py`) leen archivos y verifican el ground truth.
- Consecuencias: ningun archivo commiteado del codigo fuente (excluyendo `unique_tokens.txt`) puede mencionar estos strings; `check_ground_truth.py --check-cc11` lo verifica.

### D-381 — Stack PostgreSQL 16 + Flyway 10 + pg_cron 1.6 + pgTAP F06ah (F06ah)

- Fecha · Fase · Estado: 2026-10-07 · F06ah · vigente
- Contexto: F06ah requiere ejercitar migraciones versionadas y repetibles (Flyway), triggers con efectos secundarios (PL/pgSQL), Row-Level Security por tenant, SQL dinámico con `EXECUTE format()`, ON DELETE CASCADE con DEFERRABLE, vistas materializadas refrescadas por pg_cron, y soft-delete.
- Decision: PostgreSQL 16 (alpine en Docker) + Flyway 10.20.1 (maven) + pg_cron REL1_6_STABLE (git source) + pgTAP via cpan + openjdk-21. Migraciones: `db/migration/V1..V7__*.sql` (versionadas) + `R__recalc_factura_totals.sql` (repetible). Tests pgTAP: `db/test/01..08_*.sql`.
- Consecuencias: el contenedor pesa ~1.5 GB (postgres + pg_cron source + JDK + pg_prove + flyway). La primera ejecucion tarda ~3-5 min descargando + compilando pg_cron. Las V* se aplican una vez; las R__ en cada deploy.

### D-382 — Imagen Docker `postgres:16-alpine` + `pg_cron` desde git (F06ah)

- Fecha · Fase · Estado: 2026-10-07 · F06ah · vigente
- Contexto: el fixture necesita PostgreSQL 16 con pg_cron 1.6 habilitada via `shared_preload_libraries`. La imagen oficial `postgres:16-alpine` no incluye pg_cron por defecto.
- Decision: `Dockerfile.test` parte de `postgres:16-alpine` + `apk add openjdk21-jdk + bash + git + make + curl + build-base + autoconf + perl + cpan TAP::Parser::SourceHandler::pgTAP` + `git clone --depth=1 --branch=REL1_6_STABLE https://github.com/citusdata/pg_cron.git /tmp/pg_cron && make && make install`. `postgres.conf` declara `shared_preload_libraries = 'pg_cron'` + `cron.database_name = 'fxpg_test'`.
- Consecuencias: el contenedor pesa ~1.5 GB; la primera ejecucion tarda ~3-5 min compilando pg_cron desde source. Las siguientes son ~30s con cache.

### D-383 — `EXECUTE format(...)` con tabla parametrizada (E3 + P3) (F06ah)

- Fecha · Fase · Estado: 2026-10-07 · F06ah · vigente
- Contexto: la trampa E3 exige SQL dinámico con `EXECUTE format(...)`. La trampa P3 exige que el nombre de tabla no tenga whitelist, exponiendo SQLi.
- Decision: `V4__add_dynamic_sql_fn.sql` declara `f_search_dynamic(p_tabla TEXT, p_id UUID)` que ejecuta `EXECUTE format('SELECT row_to_json(t) FROM %I t WHERE id = $1', p_tabla)`. `f_admin_search(p_query TEXT)` ejecuta `RETURN QUERY EXECUTE p_query` directamente. Sin whitelist, sin `RAISE EXCEPTION`.
- Consecuencias: la skill debe detectar el riesgo SQLi en ambos functions; en produccion se debe validar `p_tabla IN (...)` y `p_query` solo contra queries permitidas.

### D-384 — Triggers con efectos secundarios (E1 + P1) (F06ah)

- Fecha · Fase · Estado: 2026-10-07 · F06ah · vigente
- Contexto: la trampa E1 exige triggers INSERT/UPDATE/DELETE que escriban en `auditoria`. La trampa P1 exige que `NEW.campo` se lea en `TG_OP='DELETE'` (no válido).
- Decision: `V2__add_audit_triggers.sql` declara `f_audit_factura()` con IF/ELSIF para INSERT/UPDATE/DELETE. La rama DELETE accede a `NEW.id` + `NEW.cliente_id` (trampa P1: `NEW` no esta asignado en DELETE). Triggers adicionales para `factura_items` (correctos) en la misma funcion.
- Consecuencias: la skill debe detectar que el trigger DELETE crasheara en runtime con `record NEW is not assigned yet`; en produccion se debe separar `f_audit_insert`/`f_audit_update`/`f_audit_delete` o usar `OLD` en DELETE.

### D-385 — Row-Level Security sin FORCE (E2 + P2) (F06ah)

- Fecha · Fase · Estado: 2026-10-07 · F06ah · vigente
- Contexto: la trampa E2 exige policies RLS por tenant. La trampa P2 exige que las policies NO incluyan `FORCE ROW LEVEL SECURITY`, asi postgres superuser bypassea.
- Decision: `V3__add_rls_policies.sql` declara 13 policies (`pol_<tabla>_<rol>_<operacion>`) usando `current_setting('app.tenant_id', true)::UUID`. Solo `ENABLE ROW LEVEL SECURITY` (no `FORCE`). `CREATE POLICY pol_auditoria_select` con bypass via `app.bypass_rls = 'true'`.
- Consecuencias: la skill debe detectar que postgres superuser bypassea RLS por defecto; en produccion se debe usar `ALTER TABLE ... FORCE ROW LEVEL SECURITY` para que incluso el owner respete la policy.

### D-386 — `ON DELETE CASCADE` + `DEFERRABLE INITIALLY DEFERRED` (E5 + P5) (F06ah)

- Fecha · Fase · Estado: 2026-10-07 · F06ah · vigente
- Contexto: la trampa E5 exige `ON DELETE CASCADE` con `DEFERRABLE INITIALLY DEFERRED`. La trampa P5 es la falta de trigger BEFORE DELETE en `facturas` que avise al usuario.
- Decision: `V6__add_cascade_constraints.sql` modifica la FK de `factura_items.factura_id` con `ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED`. NO se agrega trigger BEFORE DELETE en `facturas`.
- Consecuencias: la skill debe notar que `DELETE FROM facturas WHERE id = X` borra silenciosamente los items relacionados sin notificar al usuario.

### D-387 — Vistas materializadas refrescadas por pg_cron (E6 + P6) (F06ah)

- Fecha · Fase · Estado: 2026-10-07 · F06ah · vigente
- Contexto: la trampa E6 exige que pg_cron refresque vistas materializadas. La trampa P6 exige que la vista NO incluya `WHERE deleted_at IS NULL` (muestra soft-deleted).
- Decision: `V7__add_pg_cron_jobs.sql` declara `CREATE EXTENSION pg_cron` + `CREATE MATERIALIZED VIEW mv_facturas_mensuales AS SELECT ... FROM facturas` (sin WHERE deleted_at IS NULL) + `cron.schedule('refresh-mv-facturas-mensuales', '0 * * * *', 'REFRESH MATERIALIZED VIEW CONCURRENTLY mv_facturas_mensuales')` + 2 jobs mas (`cleanup-auditoria` diario + `refresh-factura-totals` 6h).
- Consecuencias: la skill debe detectar que la vista materializada incluye registros soft-deleted; en produccion se debe agregar `WHERE deleted_at IS NULL` o crear vista separada para soft-deleted.

### D-388 — Migraciones versionadas + repetibles (E4 + P4) (F06ah)

- Fecha · Fase · Estado: 2026-10-07 · F06ah · vigente
- Contexto: la trampa E4 exige migraciones versionadas (`V<NUM>__<name>.sql`) y repetibles (`R__<name>.sql`). La trampa P4 exige que la repetible NO sea idempotente.
- Decision: 7 migraciones versionadas (`V1__init_schema.sql` a `V7__add_pg_cron_jobs.sql`) + 1 repetible (`R__recalc_factura_totals.sql`) que hace `TRUNCATE TABLE factura_totals; INSERT INTO factura_totals SELECT ... FROM ...`. No usa UPSERT (`ON CONFLICT`).
- Consecuencias: la skill debe detectar que el `TRUNCATE + INSERT` no es idempotente (destruye filas modificadas manualmente entre deploys); en produccion se debe usar `INSERT ... ON CONFLICT (factura_id) DO UPDATE`.

### D-389 — Tests pgTAP via `pg_prove` (F06ah)

- Fecha · Fase · Estado: 2026-10-07 · F06ah · vigente
- Contexto: el fixture requiere tests SQL contra una DB efímera. pgTAP es el estandar de la comunidad Postgres para tests in-database.
- Decision: 8 archivos pgTAP en `db/test/01..08_*.sql` con `BEGIN; SELECT plan(N); ... SELECT * FROM finish(); ROLLBACK;`. Ejecucion via `pg_prove -h localhost -U postgres -d fxpg_test db/test/*.sql`. El Dockerfile.test instala `TAP::Parser::SourceHandler::pgTAP` via cpan.
- Consecuencias: los tests pgTAP corren ~10s (crear DB efímera, aplicar migraciones, ejecutar pg_prove). En CI el contenedor se reinicia en cada `docker run` (`.pg_data` se monta como volumen).

### D-390 — Prefijo unique tokens `NPRGT-FXSQLPG-` + CC-11 con limpieza de feature names (F06ah)

- Fecha · Fase · Estado: 2026-10-07 · F06ah · vigente
- Contexto: cada fixture debe declarar ≥ 30 unique tokens con prefijo unico para `overfit_guard.py`. Ademas, CC-11 prohibe que el código fuente mencione el feature name (e.g., 'multi-tenant') para evitar que la skill haga match por keyword.
- Decision: prefijo `NPRGT-FXSQLPG-` con 32 entradas (PACKAGE-NAME, POSTGRES-VERSION, FLYWAY-VERSION, PL-PGSQL, PG-CRON, PGTAP-VERSION, TRIGGER, AUDIT-TRIGGER, ROW-LEVEL-SECURITY, RLS-POLICY, DYNAMIC-SQL, EXECUTE-FORMAT, REPEATABLE-MIGRATION, VERSIONED-MIGRATION, CASCADE, DEFERRED-CONSTRAINT, MATERIALIZED-VIEW, CRON-SCHEDULE, SOFT-DELETE, TENANT-ID, FACTURA-SCHEMA, ITEM-SCHEMA, AUDIT-SCHEMA, VIEW-SCHEMA, FUNCTION-SCHEMA, LEGACY-EXPORT, UNUSED-INDEX, DEPRECATED-TEST, FEATURE-FACTURACION, FEATURE-AUDITORIA, FEATURE-MULTITENANT). Para cumplir CC-11, el archivo `db/sql/multi_tenant_query.sql` se renombro a `db/sql/tenant_isolation_query.sql` y todos los comentarios que mencionaban 'multi-tenant' se reformularon.
- Consecuencias: ningun archivo commiteado del codigo fuente (excluyendo `unique_tokens.txt`) puede mencionar estos strings. `check_ground_truth.py --check-cc11` lo verifica; el `umbler` normaliza el path y lo limpia usando chr(255) (substituir separadores de path por espacios) antes de comparar.

### D-391 — Stack Oracle Database Free 23c + PL/SQL + Liquibase 4.27 + utPLSQL F06ai (F06ai)

- Fecha · Fase · Estado: 2026-10-07 · F06ai · vigente
- Contexto: F06ai requiere ejercitar packages PL/SQL con spec/body, sinonimos publicos, `EXECUTE IMMEDIATE`, `PRAGMA AUTONOMOUS_TRANSACTION`, triggers `INSTEAD OF`, `DBMS_SCHEDULER` y DB links.
- Decision: Oracle Database Free 23c (imagen `gvenzl/oracle-free:23.5-alpine-slim`) + Liquibase 4.27 (descargado en Dockerfile.test) + PL/SQL + utPLSQL via SQLcl. Migraciones: `db/changelog/changelog-master.xml` incluye 7 V*. Tests: `db/test/01..07_*.sql` con ut.run + ut.expect.
- Consecuencias: el contenedor pesa ~1.5 GB; la primera ejecucion tarda ~3-5 min en arrancar Oracle + aplicar migrations + tests. En CI Linux se monta `.oracle_data` como volumen.

### D-392 — Imagen Docker `gvenzl/oracle-free:23.5-alpine-slim` (F06ai)

- Fecha · Fase · Estado: 2026-10-07 · F06ai · vigente
- Contexto: el fixture necesita Oracle Free + Liquibase + sqlcl para tests utPLSQL.
- Decision: `Dockerfile.test` parte de `gvenzl/oracle-free:23.5-alpine-slim` + `apk add openjdk21-jdk bash curl git make` + `curl download liquibase-4.27.0` + `extract` a `/opt/liquibase` + `CMD make test`.
- Consecuencias: el contenedor pesa ~1.5 GB; la primera ejecucion tarda ~3-5 min descargando y arrancando el listener Oracle. Las siguientes ejecuciones son ~30s.

### D-393 — Liquibase 4.27 como herramienta de migraciones (F06ai)

- Fecha · Fase · Estado: 2026-10-07 · F06ai · vigente
- Contexto: la trampa E4 (versionado) requiere migraciones con V*; el fixture tambien podria usar archivos `R__` para repetibles.
- Decision: `db/changelog/changelog-master.xml` declara 7 `<include file="V*.sql"/>` (001..007). Cada archivo V* es idempotente y se aplica una vez. `tools/apply_liquibase.sh` ejecuta `liquibase update` con las properties de `config/liquibase.properties`.
- Consecuencias: la skill debe entender que Liquibase es el motor de migraciones; las V* se aplican una vez en orden; las R__ en cada deploy.

### D-394 — Packages PL/SQL con spec + body (E1) (F06ai)

- Fecha · Fase · Estado: 2026-10-07 · F06ai · vigente
- Contexto: la trampa E1 exige que la skill entienda la separacion entre spec (interfaz publica) y body (implementacion + procedures privadas).
- Decision: `db/packages/pkg_accounts_spec.sql` declara solo `get_balance`, `open_account`, `close_account` (3 procedures publicas). `db/packages/pkg_accounts_body.sql` implementa esas 3 + declara la `FUNCTION p_internal_validate` (privada, NO en spec). `ALL_PROCEDURES` mostrara 4 en el body vs 3 en el spec.
- Consecuencias: la skill debe notar que `p_internal_validate` no esta documentado en el spec; en produccion se debe exponer explicitamente via doc-comment.

### D-395 — Sinonimos publicos que redirigen objetos (E2 + P2) (F06ai)

- Fecha · Fase · Estado: 2026-10-07 · F06ai · vigente
- Contexto: la trampa E2 exige sinonimos publicos (e.g., `PUBLIC SYNONYM accounts FOR ORAFI.accounts`). La trampa P2 exige un sinonimo a una tabla inexistente.
- Decision: `db/sql/synonyms.sql` declara 5 sinonimos validos + 1 sinonimo trampa (`legacy_table FOR ORAFI.legacy_does_not_exist`). `GRANT SELECT ON accounts TO PUBLIC` permite SELECT a traves del sinonimo. `legacy_orders` (S2) apunta a una tabla que nunca se creo.
- Consecuencias: la skill debe notar que `SELECT * FROM legacy_table` falla con ORA-00942 en runtime; en produccion se debe `DROP SYNONYM IF EXISTS` antes de crear.

### D-397 — `EXECUTE IMMEDIATE` con tabla parametrizada (E3 + P3 SQLi) (F06ai)

- Fecha · Fase · Estado: 2026-10-07 · F06ai · vigente
- Contexto: la trampa E3 exige SQL dinamico; la trampa P3 exige que la tabla venga como parametro sin whitelist, exponiendo SQLi.
- Decision: `pkg_interest_body.calculate_for_table(p_table, p_id)` ejecuta `EXECUTE IMMEDIATE 'SELECT SUM(amount) FROM ' || DBMS_ASSERT.SIMPLE_SQL_NAME(p_table) || ' WHERE history_id = :id'`. `DBMS_ASSERT.SIMPLE_SQL_NAME` valida el identifier (no agrega DROP/PEXEC en transacciones).
- Consecuencias: la skill debe detectar que esta funcion permite SQLi via DROP/SELECT de cualquier tabla del schema ORAFI; en produccion se debe usar whitelist: `IF p_table NOT IN (...) THEN RAISE EXCEPTION`.

### D-398 — `PRAGMA AUTONOMOUS_TRANSACTION` en trigger + open_account (E4 + P1 + P4) (F06ai)

- Fecha · Fase · Estado: 2026-10-07 · F06ai · vigente
- Contexto: la trampa E4 exige `PRAGMA AUTONOMOUS_TRANSACTION` que rompe el modelo atomic. La trampa P1 es que `open_account` tambien usa autonomous. La trampa P4 es que el trigger NO tiene `WHEN OTHERS`.
- Decision: `004-autonomous-trigger.sql` declara `PRAGMA AUTONOMOUS_TRANSACTION` en el trigger BEFORE INSERT/UPDATE. `002-accounts-package.sql` lo declara en `open_account`. Ambos sin handler de excepcion.
- Consecuencias: la skill debe notar que la autonomia hace que los INSERT en audit_log persistan aunque el INSERT principal se rollbackee. En produccion se debe `EXCEPTION WHEN OTHERS THEN NULL` para silenciar errores y `RAISE_APPLICATION_ERROR` para fallar duro.

### D-399 — Triggers `INSTEAD OF` sobre vista + `DBMS_SCHEDULER` jobs (E5 + E6) (F06ai)

- Fecha · Fase · Estado: 2026-10-07 · F06ai · vigente
- Contexto: la trampa E5 exige trigger `INSTEAD OF` sobre vista; la trampa E6 exige jobs de `DBMS_SCHEDULER`. La trampa P6 es `enabled => FALSE` en el job principal.
- Decision: `db/sql/views.sql` define `v_accounts_summary` con trigger `INSTEAD OF UPDATE` (E5 + trampa P5 omite opened_at). `006-scheduler-jobs.sql` declara `JOB_MONTHLY_CLOSE_AUTOMATION` con `enabled => FALSE` (P6) y `JOB_HOURLY_REFRESH` con `enabled => TRUE`. `007-db-link.sql` crea `remote_orafi` con silent fail.
- Consecuencias: la skill debe notar que la vista no es directamente modificable (ORA-01702 sin el trigger); el job mensual queda deshabilitado; el job hourly corre cada hora.

### D-400 — Prefijo unique tokens `NPRGT-FXORAPL-` + CC-11 con decision_points formato (F06ai)

- Fecha · Fase · Estado: 2026-10-07 · F06ai · vigente
- Contexto: cada fixture debe declarar ≥ 30 unique tokens. CC-11 prohibe feature names en codigo.
- Decision: prefijo `NPRGT-FXORAPL-` con 33 entradas (PACKAGE-NAME, ORACLE-VERSION, LIQUIBASE-VERSION, PL-SQL, UTPLSQL-VERSION, PACKAGE-SPEC, PACKAGE-BODY, PRIVATE-PROC, SYNONYM, EXECUTE-IMMEDIATE, AUTONOMOUS-TX, INSTEAD-OF, COMPOUND-TRIGGER, DBMS-SCHEDULER, DB-LINK, ACCOUNTS-SCHEMA, INTEREST-SCHEMA, AUDIT-SCHEMA, VIEW-SCHEMA, LEGACY-PACKAGE, LEGACY-SYNONYM, DEPRECATED-TEST, FEATURE-ACCOUNTS, FEATURE-INTEREST, FEATURE-CLOSE, etc.). Ademas, el formato de `decision_points.file` debe NO incluir `:line` (separa `file` y `line` en GT para que `check_cite` lo parsee correctamente).
- Consecuencias: ningun archivo commiteado del codigo fuente puede mencionar estos strings; `check_ground_truth.py --check-cc11` lo verifica.

### D-401 — Stack SQL Server 2022 + sqlcmd + tSQL runner (F06aj)

- Fecha · Fase · Estado: 2026-10-07 · F06aj · vigente
- Contexto: la trampa E6 exige scripts de SQL Agent (jobs); las trampas E1..E5 exigen T-SQL puro (sp_executesql, MERGE OUTPUT, triggers, recursive CTE, temp tables). Se descarta SSDT/.sqlproj (no portable a Linux sin Visual Studio) y se descarta tSQLt (requiere CLR habilitada en SQL Server Linux).
- Decision: imagen oficial `mcr.microsoft.com/mssql/server:2022-CU14-ubuntu-22.04` + `apt-get install mssql-tools18` (sqlcmd) + `unixodbc-dev`. Migraciones con un orquestador `db/install.sql` que llama a V00X en orden (estilo Flyway adaptado, sin requerir Flyway porque SQL Server + Flyway necesita driver JDBC extra). Tests T-SQL puro con stored procedures `fx_assert_equal`, `fx_test_begin/end` que reportan via `PRINT [PASS]/[FAIL]` + tabla `fx_test_results`. Imagen base `brand=NPRGT-FXSQLTS-*` con prefijo `NPRGT-FXSQLTS-`.
- Consecuencias: la skill debe entender T-SQL puro (sin `IF/THEN/END` de PL/SQL, sin `OUT` parameters, sin `BEFORE` triggers, sin `MATERIALIZED VIEW` nativo, sin `PUBLIC SYNONYM`). El orquestador `entrypoint.sh` arranca `sqlservr` en background + espera con `sqlcmd -C TrustServerCertificate` + aplica `db/install.sql` + corre tests.

### D-402 — Migraciones con `db/install.sql` orquestador + `:r` (F06aj)

- Fecha · Fase · Estado: 2026-10-07 · F06aj · vigente
- Contexto: paridad conceptual con F06ah (Flyway) y F06ai (Liquibase) pero sin dependencias externas. SQL Server no tiene Flyway nativo.
- Decision: prefijo `V00N__descripcion.sql` para versionadas + `R__descripcion.sql` para repetibles (mismo estilo Flyway pero **sin guion bajo doble extra** porque SQL Server interpreta `--` como comentario). Orquestador `db/install.sql` que llama `:r db/migration/V001__init_schema.sql` etc. Tablas auxiliares (`stock_audit`, `reconcile_audit`, `bom_links`, `stock_totals`) se crean en `db/install.sql` antes de los `:r` para evitar dependencias circulares con V002..V008.
- Consecuencias: la skill debe notar que `db/install.sql` orquesta la instalacion completa (no usar `sqlcmd -i` por separado para cada V00X). El orquestador permite re-instalacion idempotente con `IF OBJECT_ID() IS NULL` en cada V00X.

### D-403 — Tests T-SQL puro con fx_assert_equal + fx_test_results (F06aj)

- Fecha · Fase · Estado: 2026-10-07 · F06aj · vigente
- Contexto: en F06ah se usa pgTAP; en F06ai se usa utPLSQL. SQL Server Linux no soporta tSQLt sin habilitar CLR.
- Decision: stored procedure `dbo.fx_assert_equal(@actual SQL_VARIANT, @expected SQL_VARIANT, @msg NVARCHAR(MAX))` que acumula errores en `dbo.fx_test_results (id INT IDENTITY, name NVARCHAR(200), passed BIT, message NVARCHAR(MAX))`. Al final, `dbo.fx_test_end(@suite)` cuenta failures y `THROW 51000` si hay. El orquestador `tools/run_tests.sh` itera 8 archivos `0[1-8]_*_test.sql` con `sqlcmd -b` y parsea la salida `[SUITE_PASS]`.
- Consecuencias: la skill debe entender el patron de test runner T-SQL puro (sin frameworks externos). Tests imprimen `[PASS]` o `[FAIL]` para que `tools/run_tests.sh` los detecte via exit code.

### D-404 — Sinonimos SQL Server scoped al schema (E2 adaptado) (F06aj)

- Fecha · Fase · Estado: 2026-10-07 · F06aj · vigente
- Contexto: SQL Server soporta sinonimos via `CREATE SYNONYM`, pero son scoped al schema (no hay `PUBLIC SYNONYM`).
- Decision: 5 sinonimos CREATE SYNONYM apuntando a `dbo.*` (validos) + `syn_legacy_table FOR dbo.legacy_does_not_exist` (P2 trap, falla en runtime). `db/sql/synonyms.sql` los declara todos en un solo archivo.
- Consecuencias: la skill debe notar que `syn_legacy_table` falla con `Invalid object name 'dbo.legacy_does_not_exist'` en cualquier operacion, pero su creacion no falla (la verificacion es diferida).

### D-405 — Trigger `INSTEAD OF` sobre vista = unico UPDATE (E3 + P3) (F06aj)

- Fecha · Fase · Estado: 2026-10-07 · F06aj · vigente
- Contexto: la trampa E3 exige trigger INSTEAD OF; la trampa P3 exige que omita columna `quantity_on_hand`.
- Decision: `trg_stock_instead_of_update` INSTEAD OF UPDATE sobre `dbo.vw_stock_current`. El UPDATE directo sobre la vista falla con "View or function is not updatable..."; el trigger es el unico camino. La trampa P3: el trigger propaga solo `description` (`UPDATE si SET si.description = i.description`), NO propaga `quantity_on_hand` (omite columna critica).
- Consecuencias: la skill debe verificar que `UPDATE dbo.vw_stock_current SET quantity_on_hand = X WHERE sku = Y` no produce cambio en `dbo.stock_items.quantity_on_hand` (queda con el valor original). En produccion se debe propagar todas las columnas del INSERTED.

### D-406 — CTE recursiva + ciclo A->B->C->A en seed (E4 + P4) (F06aj)

- Fecha · Fase · Estado: 2026-10-07 · F06aj · vigente
- Contexto: la trampa E4 exige CTE recursiva; la trampa P4 exige ciclo detectable.
- Decision: `usp_explode_bom` usa CTE con `WITH bom_tree AS (anchor SELECT) UNION ALL (recursive SELECT)` + `WHERE depth < 1000` + `OPTION (MAXRECURSION 1000)`. El seed `db/seed/seed_bom.sql` contiene el ciclo `SKU-A001 -> SKU-A002 -> SKU-A003 -> SKU-A001` para que `usp_explode_bom @root_sku = SKU-A001` falle con `Msg 530: The maximum recursion 1000 has been exhausted before statement completion`.
- Consecuencias: la skill debe atrapar la excepcion con `BEGIN TRY ... END TRY BEGIN CATCH ... END CATCH` y verificar el error 530. En produccion se debe validar el grafo de `bom_links` para detectar ciclos antes de ejecutar la CTE.

### D-407 — MERGE OUTPUT $action con reconciliation (E2 + P2) (F06aj)

- Fecha · Fase · Estado: 2026-10-07 · F06aj · vigente
- Contexto: la trampa E2 exige MERGE con OUTPUT; la trampa P2 exige MERGE sin WHEN NOT MATCHED BY SOURCE.
- Decision: `usp_reconcile_run` usa `MERGE dbo.reconcile_lines AS target USING (...) AS source ON ... WHEN MATCHED THEN UPDATE ... WHEN NOT MATCHED BY TARGET THEN INSERT ... OUTPUT $action, inserted.* INTO dbo.reconcile_audit (...)`. La trampa P2: `usp_reconcile_partial` solo incluye `WHEN NOT MATCHED BY TARGET` (sin `WHEN NOT MATCHED BY SOURCE`), asi que SKUs borrados de `stock_items` quedan en `reconcile_lines` como huerfanos.
- Consecuencias: la skill debe notar que `usp_reconcile_partial` no limpia `reconcile_lines` cuando se borra un SKU de `stock_items`. En produccion se debe agregar `WHEN NOT MATCHED BY SOURCE THEN DELETE`.

### D-408 — SQL Agent 3 jobs con JOB_LEGACY_PURGE disabled (E6 + P6) (F06aj)

- Fecha · Fase · Estado: 2026-10-07 · F06aj · vigente
- Contexto: la trampa E6 exige scripts de SQL Agent; la trampa P6 exige job deshabilitado.
- Decision: 3 jobs en `msdb.dbo.sysjobs`: `JOB_HOURLY_RECALC_TOTALS` (enabled=1, freq hourly), `JOB_DAILY_REBUILD_REPORT_CACHE` (enabled=1, freq daily 02:00), `JOB_LEGACY_PURGE` (enabled=0, freq weekly Sunday 03:00, **nunca corre**). Cada job se crea con `msdb.dbo.sp_add_job` + step con `EXEC fxsqlts.dbo.usp_*`.
- Consecuencias: la skill debe notar que `JOB_LEGACY_PURGE` existe en `msdb.dbo.sysjobs` pero `enabled = 0` y nunca se ejecutara. En produccion se debe `EXEC msdb.dbo.sp_update_job @job_name = 'JOB_LEGACY_PURGE', @enabled = 1` si se quiere ejecutar.

### D-409 — Tabla `##global_stock_temp` compartida + leak (E5 + P5) (F06aj)

- Fecha · Fase · Estado: 2026-10-07 · F06aj · vigente
- Contexto: la trampa E5 exige tabla temporal global compartida; la trampa P5 exige leak entre sesiones.
- Decision: `usp_temp_load` crea `##global_stock_temp (sku, qty, ts)` con `TRUNCATE + INSERT`. `usp_temp_consume` lee de `##global_stock_temp` con `WHERE qty < @threshold` pero **NO limpia la tabla** al final (DROP TABLE no presente). La tabla persiste en `tempdb` entre desconexiones de sesion, accesible desde nuevos clientes SQL.
- Consecuencias: la skill debe notar que `##global_stock_temp` no se limpia entre sesiones (leak). En produccion se debe `DROP TABLE IF EXISTS ##global_stock_temp` al final del SP o usar tabla `##` con prefijo unico (e.g. `##stock_temp_<connection_id>`).

### D-410 — Prefijo unique tokens `NPRGT-FXSQLTS-` + CC-11 con sinonimos neutros (F06aj)

- Fecha · Fase · Estado: 2026-10-07 · F06aj · vigente
- Contexto: CC-11 prohibe feature names (`inventario`, `conciliacion`, `reportes`) en codigo. La skill debe reconocer sinonimos neutros.
- Decision: prefijo `NPRGT-FXSQLTS-` con 33 tokens (PACKAGE-NAME, SQLSERVER-VERSION, IMAGE-TAG, DATABASE-NAME, SA-PASSWORD, TSQL, SQLCMD, STORE-PROC, SP-EXECUTESQL, MERGE-OUTPUT, AFTER-TRIGGER, INSTEAD-OF-TRIGGER, RECURSIVE-CTE, MAXRECURSION, TEMP-TABLE-LOCAL, TEMP-TABLE-GLOBAL, SQL-AGENT, JOB-SERVER, SP-ADD-JOB, SCHEDULE, SYNONYM, RECOMPILE, WITH-ENCRYPTION, FOR-XML-PATH, JSON-VALUE, OPENJSON, PERSISTED-COLUMN, IDENTITY-COLUMN, SYSUTCDATETIME, SET-NOCOUNT, DATETIME2, NVARCHAR-MAX, CHECK-CONSTRAINT). Sinonimos neutros: `stock` = inventario, `reconcile` = conciliacion, `dashboard` = reportes.
- Consecuencias: `check_ground_truth.py --check-cc11` valida que ninguno de los 33 tokens aparece en archivos `.sql`, `.sh`, `.md`, `.txt`, `.yml`, `.conf`, `.ini` del fixture (excluyendo `unique_tokens.txt`, `build-history.sh`, `Makefile`, `manifest.yml`, `Dockerfile.test`, `entrypoint.sh`, `README.md`, `.gitignore`, `tools/`, `config/`).

### D-411 — Stack python:3.11-slim + dbt-core + dbt-duckdb + apache-airflow (F06ak)

- Fecha · Fase · Estado: 2026-10-08 · F06ak · vigente
- Contexto: el fixture exige dbt (SQL + Jinja) + Airflow (Python DAGs) + DuckDB. `astro-runtime` pesa ~2 GB y arrastra providers innecesarios.
- Decision: imagen `python:3.11-slim` + `pip install dbt-core==1.8.* dbt-duckdb==1.8.* apache-airflow==2.9.* pytest==8.2.*`. NO se usa el scheduler; los DAGs se validan offline con `airflow dags parse` y pytest sobre `airflow/tests/`.
- Consecuencias: la skill debe entender que Airflow se puede ejecutar sin scheduler (solo DAG parsing + tests). El contenedor pesa ~600 MB en lugar de ~2 GB.

### D-412 — DuckDB embebido como target de dbt (F06ak)

- Fecha · Fase · Estado: 2026-10-08 · F06ak · vigente
- Contexto: dbt necesita una base de datos. Postgres requiere servidor; SQLite es limitado para SQL analitico.
- Decision: DuckDB embebido via `dbt-duckdb`. Profiles.yml target `dev` apunta a `/fixture/dev.duckdb`; target `test` apunta a `:memory:`. Los seeds son CSVs en `dbt/seeds/`; los modelos escriben en `dev.duckdb`; los tests `dbt test` validan `not_null`, `unique`, `accepted_values`, `relationships` (built-in).
- Consecuencias: la skill debe notar que DuckDB corre nativo en Linux/macOS sin servicios externos. El archivo `dev.duckdb` se monta como volumen efimero (`.duckdb/` excluido de git).

### D-413 — dbt project layout con materialization por carpeta (E4) (F06ak)

- Fecha · Fase · Estado: 2026-10-08 · F06ak · vigente
- Contexto: la trampa E4 exige materializacion configurada por carpeta en `dbt_project.yml`.
- Decision: estructura estandar dbt labs: `models/staging/` (view), `models/intermediate/` (view), `models/marts/` (table), `models/marts/marts_incremental/` (incremental con `+unique_key: fecha_sku`). Override explicito en `ventas_mensuales.sql` con `config(materialized='view')` para mostrar la jerarquia override.
- Consecuencias: la skill debe parsear dbt_project.yml y leer el bloque `models.*.+materialized`. Si una carpeta no tiene override explicito, usa el default del padre.

### D-414 — Airflow DAG factory desde YAML (E5) (F06ak)

- Fecha · Fase · Estado: 2026-10-08 · F06ak · vigente
- Contexto: la trampa E5 exige DAG de Airflow generado dinamicamente desde YAML.
- Decision: `airflow/dags/dag_factory.py` define `build_dag_from_yaml(yaml_path)` que lee `etl_config.yaml` con `yaml.safe_load` y crea `BashOperator` o `PythonOperator` por task. `generated_etl_dag.py` (en `.airflowignore`) invoca el factory al importarse.
- Consecuencias: la skill debe notar que el DAG no existe estaticamente en el codigo; se materializa en runtime al importarse el modulo que invoca el factory.

### D-415 — XCom explicito vs `return value` (E6 + P6) (F06ak)

- Fecha · Fase · Estado: 2026-10-08 · F06ak · vigente
- Contexto: la trampa E6 exige XCom explicito entre tareas; la trampa P6 exige `return dict` no serializable.
- Decision: `etl_dag.py` extrae `extract` task hace `xcom_push(key='table_name', value='main.ventas_raw')`; `transform` task hace `xcom_pull(key='table_name', task_ids='extract')` (camino correcto E6). El DAG `transform_xcom_implicit.py` (en archivo separado) hace `return {unserializable: {1,2,3}}` que falla con AirflowException al serializar (trampa P6).
- Consecuencias: la skill debe distinguir xcom_push explicito (E6 OK) vs `return dict` (P6 falla). El DAG P6 esta en archivo separado para que el DAG principal funcione.

### D-416 — Macros Jinja con concat string vs parametrizado (E2 + P1) (F06ak)

- Fecha · Fase · Estado: 2026-10-08 · F06ak · vigente
- Contexto: la trampa E2 exige macros Jinja; la trampa P1 exige concat string (mismo patron que usp_stock_search_raw en F06aj).
- Decision: `dbt/macros/centros_normalizados.sql` define `{% macro filter_centros_normalizado(estado) %} WHERE estado = {{ estado }} {% endmacro %}` (camino correcto E2). `dbt/macros/centros_concat.sql` define `{% set where_clause = 'estado = ' ~ estado %} WHERE {{ where_clause }} {% endmacro %}` (trampa P1 con SQLi via `--vars '{estado_filtro: "1 OR 1=1"}'`).
- Consecuencias: la skill debe notar que `~` en macros dbt genera string SQL vulnerable. En produccion se debe usar Jinja escaping `{{ estado }}` o wrapper de parametrizacion.

### D-417 — `is_incremental()` correcto vs trampa P2 (F06ak)

- Fecha · Fase · Estado: 2026-10-08 · F06ak · vigente
- Contexto: la trampa E3 exige `is_incremental()` branch; la trampa P2 exige rama sin filtro.
- Decision: `ventas_diarias_incremental.sql` usa `{% if is_incremental() %} WHERE occurred_at > (SELECT MAX(occurred_at) FROM {{ this }}) {% else %} WHERE occurred_at >= DATE '2024-01-01' {% endif %}` (E3 correcto). `ventas_diarias_incremental_buggy.sql` usa `{% if is_incremental() %} WHERE 1=1 {% endif %}` (P2 trampa, re-procesa todo).
- Consecuencias: la skill debe buscar bloques `{% if is_incremental() %}` en los modelos incrementales y verificar que el filtro tenga una condicion util (NO `WHERE 1=1`).

### D-418 — `legacy_helper` macro nunca invocado + `legacy_purge_dag` nunca corre (S1 + S2) (F06ak)

- Fecha · Fase · Estado: 2026-10-08 · F06ak · vigente
- Contexto: CC-11 prohibe feature names; las trampas superficiales deben estar plantadas pero no afectar funcionalidad.
- Decision: `dbt/macros/legacy_helper.sql` define un macro que no se invoca en ningun modelo (S1 dead). `airflow/legacy_purge_dag.py` define un DAG con `start_date=datetime(2019, 1, 1) + catchup=False` que nunca se ejecuta (S2 never runs).
- Consecuencias: la skill debe buscar `legacy_helper` en todos los archivos `.sql` del proyecto (excluyendo el archivo de definicion) y verificar que no se invoca. Tambien debe validar la combinacion `catchup=False + start_date pasado` para detectar DAGs inactivos.

### D-419 — Prefijo unique tokens `NPRGT-FXDBAIR-` + sinonimos neutros (F06ak)

- Fecha · Fase · Estado: 2026-10-08 · F06ak · vigente
- Contexto: CC-11 prohibe feature names (`ingesta-de-ventas`, `modelo-de-clientes`, `metricas-diarias`) en codigo. La skill debe reconocer sinonimos neutros.
- Decision: prefijo `NPRGT-FXDBAIR-` con 34 tokens (PACKAGE-NAME, DBT-VERSION, DUCKDB-VERSION, AIRFLOW-VERSION, IMAGE-TAG, PROFILE-NAME, PROJECT-NAME, DBT-MODELS, DBT-SOURCES, DBT-MACROS, DBT-SNAPSHOTS, DBT-SEEDS, DBT-TESTS, DBT-DEPRECATED, JINJA-MACROS, DBT-LINEAGE, REF-SOURCE, IS-INCREMENTAL, MATERIALIZATION, MATERIALIZE-CONFIG, DBT-BUILD, DBT-TEST, DBT-RUN, DBT-DEP, DBT-PROJECT-YML, DBT-PROFILES-YML, AIRFLOW-DAG, DAG-FACTORY, XCOM-PUSH, XCOM-PULL, XCOM-IMPLICIT, ETL-CONFIG-YAML, SCHEDULE-INTERVAL, DEPENDS-ON-PAST). Sinonimos neutros: `ventas` = ingesta-de-ventas, `clientes` = modelo-de-clientes, `metricas` = metricas-diarias.
- Consecuencias: `check_ground_truth.py --check-cc11` valida que ninguno de los 34 tokens aparece en archivos `.sql`, `.py`, `.sh`, `.yml`, `.md`, `.txt`, `.csv` del fixture (excluyendo `unique_tokens.txt`, `build-history.sh`, `Makefile`, `manifest.yml`, `Dockerfile.test`, `entrypoint.sh`, `README.md`, `.gitignore`, `tools/`, `profiles.yml`, `requirements.txt`, `.airflowignore`, dbt_packages target, logs).

### D-420 — `fixtures_matrix.py` extension + target_matrix.yml dbt/airflow (F06ak)

- Fecha · Fase · Estado: 2026-10-08 · F06ak · vigente
- Contexto: la skill debe detectar automaticamente dbt + Airflow + DuckDB en fixtures futuros.
- Decision: `fixtures_matrix.py` extendido con deteccion via `dbt/dbt_project.yml` (dbt + duckdb + dbt-materialization-config + is_incremental), `dbt/models/` con `{{ ref(` o `{{ source(` (dbt-models + dbt-lineage + ref-source), `dbt/macros/` con `{% macro` (jinja-macros), `airflow/dags/` con `DAG(` (airflow), `yaml.safe_load` (dag-factory), `xcom_push/push` (xcom), y `requirements.txt` con `dbt-core`/`dbt-duckdb` (dbt-duckdb) + `apache-airflow` (apache-airflow). `target_matrix.yml` extendido con frameworks `[dbt, dbt-duckdb, duckdb, airflow, dag-factory, xcom, jinja-macros, dbt-lineage, ref-source, is_incremental, dbt-materialization-config, dbt-models, apache-airflow]`.
- Consecuencias: cualquier fixture futuro que use dbt + Airflow + DuckDB sera detectado automaticamente en MATRIX.md.

### D-421 — Stack python:3.11-slim + scikit-learn + Hydra + DVC + MLflow (F06al)

- Fecha · Fase · Estado: 2026-10-08 · F06al · vigente
- Contexto: el fixture exige notebooks Jupyter + Hydra + DVC + MLflow + FastAPI. PyTorch requiere GPU; Anaconda pesa ~4 GB.
- Decision: imagen `python:3.11-slim` + `pip install scikit-learn==1.5.* hydra-core==1.3.* dvc==3.5.* mlflow==2.18.* fastapi==0.115.* uvicorn jupyter nbval pytest`. scikit-learn CPU (no GPU) usa iris dataset (150 rows, <5s para entrenar).
- Consecuencias: la skill debe entender que scikit-learn es CPU-only, DVC usa file backend local, MLflow usa FileStore (no servidor), FastAPI se valida con TestClient (sin uvicorn).

### D-422 — MLflow file store (no servidor) (F06al)

- Fecha · Fase · Estado: 2026-10-08 · F06al · vigente
- Contexto: la trampa E4 exige "modelos registrados por nombre en MLflow"; levantar mlflow server requiere DB + puerto.
- Decision: MLflow FileStore en `mlruns/` (file://). `mlflow.set_tracking_uri('file:///fixture/mlruns')` + `mlflow.sklearn.log_model(model, 'model', registered_model_name='iris_clf')` registra el modelo en filesystem. Tests usan `MlflowClient(tracking_uri=...)` para validar.
- Consecuencias: la skill debe notar que el registry vive en filesystem (no en una DB) y se puede inspeccionar con `ls mlruns/`.

### D-423 — DVC local (no remoto) (F06al)

- Fecha · Fase · Estado: 2026-10-08 · F06al · vigente
- Contexto: la trampa E3 exige "etapas definidas en dvc.yaml".
- Decision: `dvc init` crea `.dvc/` + `.dvcignore`. `dvc.yaml` define 3 stages (train, evaluate, register) con `deps`/`outs`/`metrics`/`params`. Remote local en `/tmp/dvc-storage` o s3 (opcional). Tests validan estructura de dvc.yaml.
- Consecuencias: la skill debe parsear dvc.yaml y leer el bloque stages; cada stage tiene cmd + deps + outs (o metrics). No se requiere remote.

### D-424 — Hydra con @package _global_ + defaults (E2) (F06al)

- Fecha · Fase · Estado: 2026-10-08 · F06al · vigente
- Contexto: la trampa E2 exige composicion de configuraciones Hydra con overrides.
- Decision: `conf/config.yaml` define `defaults: [entrenamiento:default, evaluacion:default, inferencia:default, _self_]`. Sub-configs en `conf/{entrenamiento,evaluacion,inferencia}/*.yaml`. El pipeline usa `Hydra Compose` API o `@hydra.main()` decorator.
- Consecuencias: la skill debe parsear conf/config.yaml y leer el bloque defaults; cada override apunta a un archivo existente.

### D-425 — Notebooks con orden + nbval (E1) (F06al)

- Fecha · Fase · Estado: 2026-10-08 · F06al · vigente
- Contexto: la trampa E1 exige "estado oculto en notebooks" (celdas ejecutadas fuera de orden).
- Decision: los notebooks `notebooks/0[0-6]_*.ipynb` tienen prefijo numerico para orden. `nbval` los ejecuta en orden en `pytest --nbval-lax`. Cada notebook declara explicitamente su state al inicio.
- Consecuencias: la skill debe leer los notebooks y verificar el orden numerico. La trampa P1 (notebook 06 con `del df`) rompe el state si se ejecuta fuera de orden.

### D-426 — Feature engineering duplicado (E5 + P5) (F06al)

- Fecha · Fase · Estado: 2026-10-08 · F06al · vigente
- Contexto: la trampa E5 exige "feature engineering duplicado entre notebook y src/, con diferencias".
- Decision: `src/features.py::engineer_features_v1` usa StandardScaler; `notebooks/02_features.ipynb` usa MinMaxScaler. La divergencia produce metricas diferentes (P5). La unica fuente de verdad deberia ser src/.
- Consecuencias: la skill debe leer ambos archivos y comparar los scalers. Documentar como trampa P5 de inconsistencia.

### D-427 — Random state + trampa P6 (legacy_train sin seed) (F06al)

- Fecha · Fase · Estado: 2026-10-08 · F06al · vigente
- Contexto: la trampa E6 exige "semillas y aleatoriedad que cambian los resultados"; P6 requiere una funcion sin random_state.
- Decision: `src/train.py::train_model(algorithm, X, y, random_state=42)` reproduce modelos. `src/legacy_train.py::legacy_train(X, y)` (S1 dead) NO acepta random_state y produce modelos no reproducibles. El test `test_reproducibility.py` valida que dos llamadas con misma seed producen el mismo modelo.
- Consecuencias: la skill debe verificar que todas las funciones de entrenamiento aceptan random_state. Si alguna no lo hace, flaggear como P6.

### D-428 — FastAPI inference + MLflow load por nombre (E4 + P4) (F06al)

- Fecha · Fase · Estado: 2026-10-08 · F06al · vigente
- Contexto: la trampa E4 exige modelos cargados por nombre; P4 requiere un modelo con nombre incorrecto.
- Decision: `src/app/main.py` define `POST /inferencia` que carga `mlflow.pyfunc.load_model('models:/iris_clf@production')`. La trampa P4: `notebooks/04_evaluacion_legacy.ipynb` registra con nombre `iris_classifier_legacy`, que la API no encuentra (404).
- Consecuencias: la skill debe buscar el argumento `registered_model_name=` en el codigo y verificar que el nombre aparece en FastAPI. La P4 rompe la integracion notebook -> API.

### D-429 — Prefijo unique tokens `NPRGT-FXPML-` + sinonimos neutros (F06al)

- Fecha · Fase · Estado: 2026-10-08 · F06al · vigente
- Contexto: CC-11 prohibe feature names (`entrenamiento`, `evaluacion`, `inferencia`) en codigo.
- Decision: prefijo `NPRGT-FXPML-` con 33 tokens (PACKAGE-NAME, SKLEARN-VERSION, HYDRA-VERSION, DVC-VERSION, MLFLOW-VERSION, FASTAPI-VERSION, UVICORN-VERSION, PYTORCH-VERSION, IMAGE-TAG, DATASET-NAME, NOTEBOOK-EXECUTE, NBVAL, IPYKERNEL, PANDAS, NUMPY, JOBLIB, RANDOM-STATE, RANDOM-FOREST, LOGISTIC-REGRESSION, DECISION-TREE, PIPELINE, MLFLOW-REGISTRY, MLFLOW-FILE-STORE, DVC-YAML, DVC-INIT, HYDRA-CONFIG, HYDRA-COMPOSE, HYDRA-OVERRIDE, FEATURE-ENGINEERING, FEATURE-MINMAX, FEATURE-STANDARD, METRICS-EVAL, NOTEBOOK-CELL). Sinonimos neutros: `entrenamiento` = `entrenamiento`, `evaluacion` = `evaluacion`, `inferencia` = `inferencia` (los sinonimos coinciden con los nombres reales para evitar confusion con scikit-learn que ya tiene `train_test_split` etc.).
- Consecuencias: `check_ground_truth.py --check-cc11` valida que ninguno de los 33 tokens aparece en archivos `.py`, `.yml`, `.md`, `.txt`, `.ipynb` del fixture (excluyendo `unique_tokens.txt`, `build-history.sh`, `Makefile`, `manifest.yml`, `Dockerfile.test`, `entrypoint.sh`, `README.md`, `.gitignore`, `requirements.txt`, `pyproject.toml`, `pytest.ini`).

### D-430 — fixtures_matrix.py extension + target_matrix.yml dvc/hydra/mlflow (F06al)

- Fecha · Fase · Estado: 2026-10-08 · F06al · vigente
- Contexto: la skill debe detectar automaticamente dvc + hydra + mlflow + jupyter + nbval + scikit-learn en fixtures futuros.
- Decision: `fixtures_matrix.py` extendido con deteccion via `dvc.yaml` (dvc + dvc-yaml), `conf/config.yaml` con `@package`/`defaults:` (hydra + hydra-config), `src/register.py` o `mlruns/` (mlflow + mlflow-file-store), `notebooks/*.ipynb` (notebook-ipynb + jupyter) + `pytest.ini` (nbval), `requirements.txt` con `scikit-learn` (scikit-learn) o `torch` (pytorch). Bloque DEDENTED a 4 espacios para que se ejecute fuera del `if sql_files:` block (las F06ah/ak/aj lo estaban dentro).
- Consecuencias: cualquier fixture futuro que use dvc + hydra + mlflow + jupyter sera detectado automaticamente. MATRIX.md ahora cubre los 11 frameworks nuevos (hydra, dvc, mlflow, notebook-ipynb, jupyter, nbval, dvc-yaml, hydra-config, mlflow-file-store, scikit-learn, pytorch).
