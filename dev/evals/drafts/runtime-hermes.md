# Hermes Agent — investigación de runtime

> Subagente investigador de la skill `notemartin-project-review`. Solo produce este archivo; no modifica nada más.

## 1. Fuentes consultadas

1. **README de NousResearch/hermes-agent** en GitHub — instalación, descripción general, comandos CLI.
2. **Documentación oficial del sistema de Skills** (`hermes-agent.nousresearch.com/docs/user-guide/features/skills`) — ruta, activación, `skill_view`, formato SKILL.md, categorías, project-local skills.
3. **Documentación de Tools & Toolsets y Built-in Tools Reference** (`docs/user-guide/features/tools`, `docs/reference/tools-reference`) — `terminal`, `read_file`, `search_files`, `delegate_task`, `skill_view`.
4. **Documentación de arquitectura** (`docs/developer-guide/architecture`) — capas, AIAgent, prompt builder.
5. **Documentación de seguridad** (`docs/user-guide/security`) — `approvals.mode`, hardline blocklist, YOLO, file write safety.
6. **Documentación de compresión y caché** (`docs/developer-guide/context-compression-and-caching`) — `compression.threshold`, gateway hygiene 85%, Anthropic prompt caching.
7. **Documentación de variables de entorno** (`docs/reference/environment-variables`) — `HERMES_HOME`, `TERMINAL_*`, `HERMES_YOLO_MODE`.
8. **Código fuente de `tools/delegate_tool.py`** en `main` — parámetros, reglas de profundidad, modelos excluidos.

## 2. Ruta global de skills

Convención confirmada: todas las skills viven bajo `~/.hermes/skills/` en POSIX o `%LOCALAPPDATA%\hermes\skills\` en Windows nativo; el directorio se crea en la instalación y es la fuente única de verdad para skills locales, del hub y creadas por el agente [2].

Estructura interna (categoría → skill → SKILL.md):

```
~/.hermes/skills/
├── software-development/        ← categoría (propuesta para nuestra skill)
│   └── notemartin-project-review/
│       ├── SKILL.md             ← obligatorio
│       ├── references/
│       ├── templates/
│       └── scripts/
├── devops/
├── research/
└── …
```

Las categorías son simples subcarpetas del directorio de skills; no requieren registro. Las categorías reales que trae el repositorio incluyen `apple`, `autonomous-ai-agents`, `creative`, `devops`, `email`, `media`, `note-taking`, `productivity`, `research`, `social-media`, `software-development` y `web` (verificado en el árbol `skills/` del repo) [2]. La categoría `software-development` existe y es coherente con el alcance de la skill.

Adicionalmente, se pueden declarar directorios externos con `skills.external_dirs` en `~/.hermes/config.yaml` (acepta `~` y `${VAR}`); tienen menor precedencia que el directorio local [2].

## 3. Ruta de proyecto

Sí existe una ruta de proyecto, opcional y con confirmación explícita. Cuando Hermes se inicia dentro de un checkout de git, busca skills en dos ubicaciones [2]:

```
<project-root>/.hermes/skills/      # nativo
<project-root>/.agents/skills/      # convención compartida con otros agentes
```

**No se cargan automáticamente.** Al detectarlas por primera vez, Hermes muestra un aviso en el banner y exige ejecutar `hermes skills trust` (o `hermes skills trust <ruta>`) antes de incluirlas en el índice [2]. Las raíces confiadas se persisten en `skills.trusted_project_dirs` en `~/.hermes/config.yaml`; la función se apaga con `skills.project_discovery: false`.

Precedencia entre las cuatro localizaciones (de mayor a menor): `project → local (~/.hermes/skills/) → skills.create_dir → external_dirs` [2].

## 4. Mecanismo de activación

Tres formas, en orden de uso [2]:

1. **Slash command `/<skill-name>`** — la activación principal. Ejemplos del README y docs: `/gif-search`, `/axolotl`, `/github-pr-workflow`, `/songsee` [2]. Es posible encadenar hasta 5 slash commands al inicio de un mensaje (`/skillA /skillB … <instrucción>`) y la skill se apila en un solo mensaje del usuario. También existen **bundles** (`~/.hermes/skill-bundles/<slug>.yaml`) que agrupan varias skills bajo un único slash [2].
2. **Herramientas del toolset `skills`** — `skills_list()` devuelve el índice (nombre + descripción + categoría, ~3k tokens), `skill_view(name)` carga `SKILL.md`, `skill_view(name, path)` carga un archivo concreto de `references/` [2].
3. **Interacción por chat** — `hermes chat --toolsets skills -q "…"` muestra las skills disponibles sin slash explícito [2].

La activación depende de la `description` del frontmatter: si el contenido encaja con la consulta, el modelo invoca `skill_view` por su cuenta; las skills con `metadata.hermes.fallback_for_toolsets`, `requires_toolsets`, `fallback_for_tools` o `requires_tools` se ocultan/activan automáticamente según los tools disponibles [2].

## 5. Carga de references/ (skill_view, etc.)

El patrón de divulgación progresiva tiene tres niveles [2]:

```
Nivel 0: skills_list()           → [{name, description, category}, ...]   (~3k tokens)
Nivel 1: skill_view(name)        → Contenido completo de SKILL.md + metadatos
Nivel 2: skill_view(name, path)  → Archivo concreto dentro de references/, templates/, scripts/, assets/
```

La primera llamada a `skill_view(name)` devuelve `SKILL.md` y un listado de los archivos vinculados (referencias, plantillas, scripts, ejemplos, assets). Las llamadas siguientes con `path` bajan a un archivo específico. La herramienta vive en el toolset `skills` del registro central de Hermes (`tools/registry.py`); su descripción dice literalmente: "Skills allow for loading information about specific tasks and workflows, as well as scripts and templates. Load a skill's full content or access its linked files (references, templates, scripts)." [3].

Las rutas se cargan **on demand**, así que `references/` con muchos archivos no penaliza el contexto hasta que el modelo decide profundizar [2]. Para skills grandes (libros, papers, manuales) el comando `/learn` produce automáticamente una `SKILL.md` breve con índice más un fichero destilado por capítulo bajo `references/`; los reference files "cuestan cero hasta que una pregunta los necesita" [2].

## 6. Cómo obtiene el agente la ruta de la skill

No hay una variable de entorno canónica `SKILL_DIR` exportada por defecto. Lo que sí existe y se puede usar desde los scripts de la skill:

- `HERMES_HOME` (configurable; default `~/.hermes` en POSIX y `%LOCALAPPDATA%\hermes` en Windows nativo; `/opt/data` en la imagen Docker oficial) [7]. Se puede consultar desde Python con `os.environ["HERMES_HOME"]`.
- Las skills locales se resuelven como `${HERMES_HOME}/skills/<category>/<skill>/`. Categoría y nombre son los segmentos del slash command o el slug del frontmatter [2].
- El skill path se puede **inferir desde el propio script** (caso típico de `npr.py`): `Path(__file__).resolve().parent` da `scripts/`; subir dos niveles llega a la raíz de la skill donde está `SKILL.md`. La validación puede hacerse por presencia de `SKILL.md` o de un marcador propio (`scripts/.npr-marker`, como propone AGENTS §4) — esta segunda pieza la tiene que portar la skill, no la da Hermes.

Riesgo real confirmado en el código fuente: en `delegate_task.py` (subagentes en thread) la variable `HERMES_HOME` puede quedar desfasada entre procesos concurrentes — el propio Hermes resuelve esto anclando el transcript al `state.db` del padre, no al ambient env [8]. Para `npr.py` la recomendación es **no depender de `$HERMES_HOME` en procesos paralelos** y resolverse por `__file__`.

[?] OQ-001: ¿exporta Hermes `HERMES_HOME` automáticamente al entorno del tool `terminal` cuando la sesión se inicia desde el gateway/TUI, o hay que declararla en `required_environment_variables` del frontmatter para que llegue a un script lanzado vía `terminal`?

## 7. Subagentes (herramienta, parámetros, herencia, concurrencia, escritura)

Herramienta: **`delegate_task`**, en el toolset `delegation`, registrada en `tools/registry.py` con el handler `tools/delegate_tool.py` [3][8].

Parámetros del schema (OpenAI function-calling) [8]:

| Parámetro | Tipo | Uso |
|---|---|---|
| `tasks` | array (≥1) | Cada entrada = un subagente. Se ejecuta en paralelo. La descripción se reconstruye en cada llamada para reflejar el límite real del usuario (`delegation.max_concurrent_children`). |
| `goal` | string | Lo que el subagente debe lograr; debe ser autocontenido (no ve el historial del padre). |
| `context` | string | Información de fondo adicional: paths, mensajes de error, idioma de salida. |
| `output_schema` | object | JSON Schema opcional que la respuesta final debe validar. |
| `images` | array (≤8) | Imágenes que el subagente debe ver (paths locales o URLs). |
| `action` | enum `spawn`\|`list`\|`steer`\|`stop` | Control en vivo. `list` devuelve ids/goals/status; `steer` (`subagent_id` + `message`) inyecta corrección a mitad de ejecución; `stop` (`subagent_id`) lo termina con resultado parcial. |
| `subagent_id`, `message` | string | Pareja para `steer`/`stop`. |

El `role` (`leaf`/`orchestrator`) figura en el código pero está marcado como *legacy*: la capacidad de delegar se deriva ahora de la profundidad (`_delegate_depth`) y de `delegation.max_spawn_depth`, no del parámetro [8].

Herencia y restricciones [3][8]:

- Cada hijo recibe una conversación nueva, su propio `task_id` (terminal aislado), su propio `cache` de operaciones de archivo, su propio `SessionDB` y un system prompt enfocado construido a partir de `goal` + `context`.
- El padre nunca ve las tool calls intermedias del hijo; solo recibe el resumen final estructurado.
- Los hijos heredan los toolsets del padre (sin argumento model-facing para toolsets) pero se les quitan explícitamente: `delegate_task`, `clarify`, `memory`, `cronjob` [8].
- Por defecto los hijos no heredan el presupuesto de iteraciones del padre: `max_iterations` viene de `delegation.max_iterations` en `config.yaml`; los kwarg del modelo se ignoran [8].
- El modelo no elige `background`: las delegaciones top-level corren siempre en background; una sola tarea o un batch es **una** unidad asíncrona y los resultados re-entran como un único mensaje consolidado. La excepción es el orquestador (depth > 0) que sí espera a sus workers [8].

Concurrencia y profundidad:

- Límite por llamada: `delegation.max_concurrent_children` (el docstring del handler lo muestra interpolado en la descripción del parámetro `tasks`) [8].
- Profundidad máxima: `delegation.max_spawn_depth` (sin techo duro en el código — "no hard ceiling, but each level multiplies API cost") [8].
- Modo single-query: hay un presupuesto aparte `delegation.oneshot_max_children` que se agota; alcanzado el límite el handler devuelve un error pidiéndole al padre hacer el trabajo inline [8].
- Control interactivo (TUI / RPC `p` en `/agents`) puede pausar nuevos spawns vía `delegation.pause`; el chequeo `is_spawn_paused()` lo aplica solo a spawns nuevos [8].

Escritura: los hijos pueden leer y escribir archivos (heredan `terminal`/`read_file`/`patch`/`write_file`/`search_files`) y crean skills nuevas (`skill_manage`). No pueden cerrar trabajo de otro subagente, no pueden abrir prompts `clarify` al usuario, no pueden hablar con cron/memory [8].

## 8. Herramientas de lectura / búsqueda / ejecución

Toolset `file` (4 herramientas) y `terminal` (2) [3]:

| Herramienta | Función |
|---|---|
| `read_file` | Lee un archivo de texto con números de línea y paginación. Formato `LINE_NUM\|CONTENT`. Acepta `offset` y `limit` para archivos grandes. Trunca a ~100 KB devolviendo `next_offset`. Reconoce Jupyter (`.ipynb`), Word (`.docx`) y Excel (`.xlsx`). Detecta y transcodifica UTF-16 (con o sin BOM) a UTF-8. Archivos binarios legítimos y >10 MB se rechazan como binarios. |
| `search_files` | Búsqueda por contenido (`target="content"`, regex) o por nombre. **Ripgrep-backed**. Modos `content` (full matches con línea y contexto), `files_with_matches`, `count`. |
| `patch` | Edición dirigida find-and-replace. Matching difuso con 9 estrategias. Devuelve unified diff. Auto-corre sintaxis tras editar. **Es la forma recomendada de editar; el docstring desaconseja `sed`/`awk` en `terminal`**. |
| `write_file` | Sobrescribe un archivo completo (crea directorios padres). Si el archivo existe exige un `read_file` reciente como línea base; si el archivo cambió en disco, rehúsa y obliga a re-leer. Auto-corre sintaxis en Python/JSON/YAML/TOML. |
| `terminal` | Ejecuta comandos en uno de **siete backends**: `local`, `docker` (un contenedor persistente por proceso, endurecido: `--cap-drop ALL`, `--security-opt no-new-privileges`, `--pids-limit 256`, tmpfs en `/tmp` y `/var/tmp`), `ssh` (ControlMaster persistente), `singularity`/`apptainer`, `modal`, `daytona`, `vercel_sandbox`. Acepta `background=true`, `pty=true` y `notify_on_complete`. Timeout configurable en `terminal.timeout` (default 180 s). |
| `process_manage` | Gestión de procesos en background (list/poll/wait/log/kill/write). |

Aprobación de comandos peligrosos: tres modos configurables vía `approvals.mode` en `~/.hermes/config.yaml` [5]:

| Modo | Comportamiento |
|---|---|
| `smart` (default) | LLM auxiliar evalúa el riesgo; bajo riesgo se auto-aprueba esa vez; peligro claro se auto-deniega; dudoso escala a prompt manual. |
| `manual` | Siempre prompt al usuario. |
| `off` | Desactiva todo — equivalente a `--yolo` [5]. |

Hay además un **hardline blocklist** (en `tools/approval.py::UNRECOVERABLE_BLOCKLIST`) que **no se puede saltar ni con YOLO**: `rm -rf /`, fork bombs, `mkfs.*` en raíz, `dd if=/dev/zero of=/dev/sd*`, pipe de URL no confiadas a `sh` en `/` [5]. YOLO se activa con `hermes --yolo`, `/yolo` o `HERMES_YOLO_MODE=1`; en backends de contenedor (`docker`, `singularity`, `modal`, `daytona`, `vercel_sandbox`) las comprobaciones de comandos peligrosos se **saltan** porque el contenedor es el límite de seguridad [5].

`write_file`/`patch` aplican además una **denylist de rutas protegidas** (carpetas SSH, AWS, Kube, `~/.hermes/.env`, `auth/*.json`, etc.) y un sandbox opcional `HERMES_WRITE_SAFE_ROOT` (auto-fijado a `/opt/data` en la imagen Docker oficial) [5].

## 9. Límite de contexto y compactación

Dos sistemas en paralelo, más prompt caching opcional [6]:

1. **`Agent ContextCompressor` (default, en el loop)** — `agent/context_compressor.py`. Se dispara cuando los tokens de prompt llegan al **`compression.threshold`** (default `0.50` = 50 % del contexto del modelo principal, con un suelo de `0.75` para ventanas <512K). Algoritmo en 4 fases: poda tool results viejos (>200 chars), determina boundaries (preserva `protect_first_n=3`, `protect_last_n≥20`, cola por presupuesto de tokens), genera resumen con LLM auxiliar en una sola llamada (`call_llm(task="compression")`), reensambla [6].
2. **`Gateway Session Hygiene` (safety net, en `gateway/run_turn.py`)** — se dispara al **85 %** del contexto, antes de procesar el mensaje entrante. Solo actúa si `len(history) >= 4` y la compresión está habilitada. Usa el último `prompt_tokens` reportado por la API si está disponible, si no un estimador rugoso [6].

`tail_mode: lean` (default) retiene ~2.5 % del contexto (10K–25K) más un índice mecánico de anclas (PR numbers, SHAs, paths, strings de error) y los últimos mensajes de usuario verbatim; los tool results viejos se demoten a stubs de una línea. Resultado publicado: 49K tokens retenidos vs 162K en sesiones reales de 500K tokens, con mayor recall cuando se combina con `session_search` [6].

Comandos y configuración relevantes:

- `/compress` manual (clear al SDK o TUI; también CLI). `force=True` resetea el cooldown.
- `/usage`, `/insights [--days N]` para ver consumo [2].
- `compression.codex_gpt55_autoraise: true` (default) sube el trigger al 85 % para gpt-5.4/5.5/5.6 y gpt-6 Astra en la ruta Codex OAuth (ventana capada a 272K); para `-900k` picker variants mantiene el `threshold` global [6].
- `compression.codex_app_server_auto: native|hermes|off` — para sesiones `codex_app_server` la compresión la hace el codex nativo, no Hermes [6].
- `compression.codex_responses_native: true` (opt-in) habilita server-side compaction en OpenAI Responses API para gpt-5.6 / gpt-6-astra en `api.openai.com` o Codex OAuth [6].
- `context.engine: "lcm"` selecciona un motor alternativo vía plugin (Lossless Context Management) — los plugins de `context_engine` nunca se auto-activan [6].

Prompt caching Anthropic: estrategia `system_and_3` (4 breakpoints `cache_control`: el system prompt fijo + los últimos 3 mensajes). TTL configurable en `prompt_caching.cache_ttl` (`"5m"`, `"1h"` o `"auto"` — auto es `1h` para fuentes humanas y `5m` para máquinas: subagent, cron, oneshot, webhook, kanban, api, tool, batch) [6].

Los tokens del modelo no son fijos: vienen del provider/modelo elegido (configurable con `hermes model`, `OPENROUTER_API_KEY`, `ANTHROPIC_API_KEY`, etc.). `HERMES_MODEL` permite override a nivel de proceso [2][7].

## 10. Notas y contradicciones con AGENTS §4

### Confirmaciones que coinciden con AGENTS §4

- Ruta global POSIX `~/.hermes/skills/<categoría>/<nombre>/` ✓ [2].
- Categoría `software-development` ✓ (categoría real del repo, no inventada) [2].
- Carga de `references/` mediante `skill_view(name, path)` ✓ [2].
- Skills project-local `<project>/.hermes/skills/` y `<project>/.agents/skills/` con trust explícito ✓ [2].
- Subagentes disponibles con paralelismo y jerarquía ✓ [3][8].
- Compatible con el estándar abierto `agentskills.io` ✓ [2].

### Contradicciones / matices con AGENTS §4

- **Forma exacta del comando de instalación.** AGENTS §4 dice `hermes skills install <owner>/<repo>/notemartin-project-review`. La docs oficial usan la forma `<owner>/<repo>/<ruta-dentro-del-repo>` para GitHub directo (ejemplo: `hermes skills install openai/skills/k8s`, donde `k8s` es la subcarpeta) [2]. Si el repo contiene la skill en la raíz y se llama igual que el repo, el equivalente es `hermes skills install <owner>/<repo>` (sin tercer segmento) o `hermes skills install <owner>/<repo>.git`. **Acción sugerida**: documentar en el SKILL.md el comando exacto probado contra el repo público de la skill; mantener el plan actual como ejemplo orientativo.
- **Windows nativo.** AGENTS §4 menciona solo POSIX; Hermes también instala nativamente en Windows en `%LOCALAPPDATA%\hermes\` (PowerShell one-liner `iex (irm https://hermes-agent.nousresearch.com/install.ps1)`) [1]. El adaptador debe cubrir esta ruta en F02.
- **`SKILL_DIR` no existe como variable.** AGENTS §4 propone exportarla como `NPR_HOME`; Hermes no expone esa variable. La estrategia de recuperación práctica es **HERMES_HOME + convención de path** o **autodescubrimiento desde `__file__`** con el marcador `scripts/.npr-marker` que ya plantea AGENTS §4. El riesgo conocido de `HERMES_HOME` desfasado en threads está confirmado en el propio `delegate_tool.py` [8].
- **Categorización es libre, no fija.** AGENTS §4 sugiere `software-development`; la categoría es simplemente una subcarpeta del directorio de skills [2]. No hay registro de categorías.
- **Concurrencia por defecto de subagentes.** AGENTS §13 dice `subagents.max_parallel = auto`; el límite real es `delegation.max_concurrent_children` (configurable en `config.yaml`) y `delegation.max_spawn_depth` para profundidad [8]. Hay además `delegation.oneshot_max_children` para sesiones one-shot. Estos nombres y defaults concretos deben documentarse en la guía de subagentes.
- **Límite de contexto.** AGENTS §13 no pone un número fijo. Hermes hereda la ventana del modelo elegido y dispara compactación al 50 % (con suelo 0.75 en ventanas pequeñas) y red de seguridad al 85 %; los valores están en `compression.threshold` / `compression.threshold_tokens` [6]. No hay un "tope de tokens de la plataforma" único.

### Preguntas abiertas (registradas como OQ)

- OQ-001 (sección 6): exportación real de `HERMES_HOME` a procesos `terminal` sin declararla como `required_environment_variables` en el frontmatter.

## Fuentes

- [1] Nous Research — `NousResearch/hermes-agent` README — `https://github.com/NousResearch/hermes-agent` (consulta 2026-10-05)
- [2] Nous Research — Skills System (docs oficiales Hermes Agent) — `https://hermes-agent.nousresearch.com/docs/user-guide/features/skills` (consulta 2026-10-05)
- [3] Nous Research — Built-in Tools Reference — `https://hermes-agent.nousresearch.com/docs/reference/tools-reference` (consulta 2026-10-05)
- [4] Nous Research — Architecture — `https://hermes-agent.nousresearch.com/docs/developer-guide/architecture` (consulta 2026-10-05)
- [5] Nous Research — Security — `https://hermes-agent.nousresearch.com/docs/user-guide/security` (consulta 2026-10-05)
- [6] Nous Research — Context Compression and Caching — `https://hermes-agent.nousresearch.com/docs/developer-guide/context-compression-and-caching` (consulta 2026-10-05)
- [7] Nous Research — Environment Variables Reference — `https://hermes-agent.nousresearch.com/docs/reference/environment-variables` (consulta 2026-10-05)
- [8] Nous Research — `tools/delegate_tool.py` (código fuente en `main`) — `https://raw.githubusercontent.com/NousResearch/hermes-agent/main/tools/delegate_tool.py` (consulta 2026-10-05)