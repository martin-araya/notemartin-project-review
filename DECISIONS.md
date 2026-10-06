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

## Plantilla para nuevas decisiones

```
### D-NNN — Título

- Fecha · Fase · Estado: vigente | reemplazada por D-xxx
- Contexto:
- Decisión:
- Alternativas consideradas:
- Consecuencias:
```