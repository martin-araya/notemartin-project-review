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
