# Kilo Code — investigación de runtime

> Investigación de las capacidades del runtime de Kilo Code relevantes para la skill `notemartin-project-review`.
> Consultas realizadas entre 2026-09 y 2026-10. Las afirmaciones se citan con supraíndice `[N]` y las fuentes se listan al final.

## 1. Fuentes consultadas

- Documentación oficial de Kilo Code sobre Skills, Subagentes, Herramientas, Compactación, Settings, Marketplace.[1][2][3][4][5][6]
- Documentación oficial de Kilo Code sobre AGENTS.md y Agent Manager.[7][8]
- README principal del repositorio `Kilo-Org/kilocode` (rama `main`).[9]
- Especificación abierta Agent Skills en `agentskills.io` (citada por Kilo Code). [1]

## 2. Ruta global de skills

La ruta global oficial es `~/.kilo/skills/` y se documenta como "Global Skills (User-Level)" tanto en macOS/Linux como en Windows (`\Users\<yourUser>\.kilo\skills\`).[1]

Adicionalmente, Kilo Code descubre sin configuración:
- `~/.agents/skills/` (estándar abierto de agentes).[1]
- `~/.claude/skills/` cuando la compatibilidad con Claude Code está habilitada.[1]

Cada skill es una carpeta `~/.kilo/skills/<nombre>/SKILL.md`, donde el campo `name` del frontmatter debe coincidir con el nombre del directorio.[1] Ejemplo publicado:

```
~/.kilo/
└── skills/
    ├── my-skill/
    │   └── SKILL.md
    └── another-skill/
        └── SKILL.md
```
[1]

Rutas adicionales (locales o remotas) se declaran en `kilo.jsonc` bajo `skills.paths` (acepta absolutas, `~/...` o relativas al proyecto) y `skills.urls` (URLs que sirven un `index.json` con manifests de skills).[1]

[?] OQ-001: AGENTS §4 menciona la ruta heredada `~/.kilocode/skills/` como todavía cargada. La documentación vigente de Skills no la lista entre las rutas descubiertas por defecto; solo `.kilo/`, `.agents/`, `.claude/`. No se descarta que código interno siga resolviéndola por compatibilidad, pero no está documentada en la página actual de Skills. Verificar contra `kilocode/src/services/skills/` cuando se lea el repo.

## 3. Ruta de proyecto

La ruta de proyecto oficial es `.kilo/skills/` dentro del repositorio.[1] Ejemplo publicado:

```
your-project/
└── .kilo/
    └── skills/
        └── project-conventions/
            └── SKILL.md
```
[1]

Por compatibilidad, también se cargan:
- `.agents/skills/` (estándar abierto, por defecto).[1]
- `.claude/skills/` cuando la compatibilidad con Claude Code está habilitada.[1]

**Prioridad**: cuando dos skills comparten nombre, las de proyecto (`.kilo/skills/`) prevalecen sobre las globales (`~/.kilo/skills/`); las de directorios de compatibilidad se cargan en paralelo.[1] El comentario del marketplace confirma que las instalaciones de proyecto se almacenan en `.kilo/skills/<name>/` y las globales en `~/.kilo/skills/<name>/`.[6]

La activación se hace desde `kilo.jsonc` (proyecto) con clave `skills.paths` y `skills.urls`.[1]

## 4. Mecanismo de activación

La activación la decide el LLM comparando la tarea del usuario contra el campo `description` del frontmatter de cada skill. No hay keyword matching ni búsqueda semántica: el agente evalúa la solicitud contra todas las descripciones disponibles y elige la que "se aplique de manera clara e inequívoca".[1]

Puntos clave:
- El `description` debe escribirse en el idioma y términos en que el usuario suele pedir la tarea.[1]
- La invocación explícita por nombre siempre funciona: decir "usa la skill `api-design`" la activa porque el agente ve el nombre en el system prompt.[1]
- Cada skill cargada también queda disponible como **slash command**: `/<nombre>`. Si colisiona con un comando personalizado o un prompt MCP, el comando conserva `/nombre` y la skill aparece como `/nombre:skill`.[1]
- Las skills se vuelven a escanear al iniciar cada sesión; para recargar sin perder sesión existe el comando `/reload`.[1]
- En VS Code las skills se cargan cuando la extensión se conecta al servidor del CLI; en el CLI, al iniciar una sesión o ejecutar `kilo run`.[1]

Hay dos subagentes integrados que las habilidades usan internamente: `general` (propósito general, acceso completo excepto `todo`) y `explore` (rápido, solo lectura).[2]

## 5. Carga de references/

`SKILL.md` es el único archivo obligatorio; los recursos adicionales son opcionales y se declaran como subcarpetas hermanas: `scripts/`, `references/`, `assets/`.[1]

El flujo de carga es:
1. **Discovery**: al inicializar, Kilo escanea las rutas configuradas y lee solo los metadatos (`name`, `description`, ruta del archivo), no el contenido.[1]
2. **Inclusión en prompt**: cuando un modo está activo, los metadatos de las skills relevantes se incluyen en el system prompt; el agente ve una lista con nombre y descripción.[1]
3. **Carga bajo demanda**: cuando el agente decide que la tarea coincide con la `description`, lee el `SKILL.md` completo a contexto y sigue las instrucciones. Puede leer archivos adicionales desde `references/`, `scripts/` o `assets/` con la herramienta `read`.[1]

No hay sintaxis especial para referencias: el cuerpo de `SKILL.md` puede mencionar rutas relativas (`./references/01-pipeline.md`) que el agente resuelve con `read` desde el directorio de la skill.[1] La documentación no menciona una variable de entorno que exponga la ruta absoluta al agente; la skill no debe depender de rutas absolutas.

[?] OQ-002: No existe en la documentación vigente una variable `SKILL_DIR` ni un archivo marcador que el agente pueda consultar para conocer la ruta absoluta de la skill. La estrategia descrita en AGENTS §4 (variable `NPR_HOME` y archivo `scripts/.npr-marker`) es un contrato de la skill, no del runtime. Verificar si el binario del CLI expone alguna variable (p.ej. `$KILO_HOME`) al ejecutar scripts.

## 6. Cómo obtiene el agente la ruta de la skill

No hay un mecanismo documentado que entregue la ruta absoluta de la skill al modelo.[1][3]

En la práctica:
- El system prompt lista los metadatos (incluida la ruta del archivo `SKILL.md`) para cada skill descubierta; el agente deduce el directorio por la ruta del `SKILL.md`.[1]
- Los recursos adicionales (`scripts/`, `references/`) se acceden por ruta relativa desde el cuerpo de `SKILL.md`, leídos con la herramienta `read`.[1]
- Las skills pueden declarar comandos de shell embebidos con la sintaxis `` !`command` ``, pero esos comandos se ejecutan en el directorio del proyecto y solo en skills de ubicaciones confiables (`~/.kilo/skills/`, `~/.agents/skills/`, `~/.claude/skills/`, integradas y rutas absolutas en config global); las de proyecto y las remotas son no confiables y el placeholder se reemplaza por un marcador.[1]
- Variable de seguridad: `KILO_DISABLE_SKILL_SHELL=1` desactiva la ejecución de comandos embebidos.[1]

Implicación para `notemartin-project-review`: la skill debe resolver su propia ruta de instalación en tiempo de ejecución, probar varias rutas conocidas (`~/.kilo/skills/notemartin-project-review/`, `.kilo/skills/notemartin-project-review/`, etc.) y validar con un archivo marcador, tal como previene AGENTS §4 (riesgo conocido n.º 6).

## 7. Subagentes (herramienta, parámetros, herencia, concurrencia, escritura)

Kilo Code ofrece dos mecanismos ortogonales para delegar trabajo:

### 7.1. Herramienta `task` (subagente en sesión)

- Es una herramienta del grupo "Workflow" junto a `question`, `todowrite`, `todoread`, `plan`, `skill`, `open_plan`, `agent_manager`, `board_post`, `board_read`.[3]
- Permite a un agente primario con herramientas completas delegar una subtarea enfocada sin cambiar al agente `orchestrator` (deprecado).[2][3]
- Parámetros principales: `description`, `prompt`, `subagent_type`, `background` (booleano).[3]
- **Contexto aislado**: cada subagente corre en su propia sesión con historial de conversación separado; no hereda la conversación del padre.[2]
- **Modelo**: si no se especifica, hereda el modelo del primario que lo invoca; se puede fijar con `provider/model-id` en la definición del agente o por-tarea.[2][5]
- **Directorio**: usa el mismo directorio de proyecto o worktree que el padre; `task` no crea un worktree.[3][8]
- **Interactividad**: el hijo no es interactivo; no puede hacer preguntas al usuario directamente. Puede usar las herramientas que su agente y permisos de sesión permitan, y devolver el resultado por archivo, retorno o por el tablero Kilo Swarm.[2]
- **Foreground vs. background**: foreground (por defecto) espera el resultado antes de continuar; `background: true` retorna de inmediato y Kilo entrega el resultado al padre cuando el hijo termina.[3]
- **Anidamiento**: un hijo puede delegar otra vez solo si la profundidad configurada y el permiso `task` del agente lo permiten.[3]
- **Reanudación**: si Kilo devuelve un `task_id` tras un fallo o interrupción, se puede pasar de vuelta a `task` para continuar, sujeto a permisos y sesión.[3]
- **Permisos**: el subagente hereda/restringe acceso a herramientas según la sección `permission` (`allow`/`ask`/`deny`) del agente que se instancie.[2]

### 7.2. Herramienta `agent_manager` (sesiones visibles del Agent Manager)

- Disponible por defecto solo en la extensión de VS Code, porque el Agent Manager es una función de la extensión.[3][8]
- Modos: `worktree` (crea un Agent Manager git worktree y sesión por tarea; checkout, rama, directorio y terminal aislados) y `local` (sesiones en el workspace actual o en un worktree administrado existente).[3][8]
- Por solicitud puede arrancar hasta **20 tareas**.[8]
- Cada sesión tiene su propio transcript, cola de prompts y terminal; comparte archivos y rama solo dentro del mismo worktree `local`.[8]
- Acciones: `list`, `prompt`, `stop`, `move`, `answer` (esta última resuelve preguntas pendientes de una sesión).[8]

### 7.3. Subagentes integrados

- `general`: tareas generales de investigación y multi-paso; acceso completo a herramientas excepto `todo`.[2]
- `explore`: rápido, solo lectura; no puede modificar archivos; sirve para búsqueda, grep y preguntas sobre el código.[2]

### 7.4. ¿Pueden escribir archivos?

Depende de la configuración:
- El subagente `general` tiene acceso completo por defecto (excepto `todo`).[2]
- El subagente `explore` no puede modificar archivos por construcción.[2]
- Un agente custom puede fijar `permission.edit: deny` o `permission.bash: deny` para restringir escritura.[2]
- En la configuración de ejemplo "Restricted Orchestrator", un agente primario solo puede delegar a subagentes específicos vía `permission.task` con patrones.[2]

### 7.5. Límite de concurrencia

- Para `agent_manager`: hasta 20 tareas por solicitud.[8]
- Para `task`: no hay un número documentado; la limitación real es la profundidad de anidamiento configurada y los permisos.[3]

[?] OQ-003: No se documenta un tope explícito de subagentes `task` simultáneos. Para evitar race conditions, la skill debería serializar escritura en archivos compartidos aunque la documentación indique que cada subagente opera sobre el mismo directorio de proyecto. Verificar el límite real en una sesión de prueba antes de fijar un valor por defecto.

## 8. Herramientas de lectura / búsqueda / ejecución

Kilo Code agrupa las herramientas en grupos:[3]

- **Read**: `read` (lee archivos con números de línea), `glob` (patrones glob), `grep` (regex sobre contenidos).
- **Edit**: `edit` (reemplazos precisos), `write` (crea o sobrescribe), `apply_patch` (diffs unificados, para ciertos modelos).
- **Execute**: `bash` (ejecuta comandos de shell con timeout y directorio configurables). El antiguo `interactive_terminal` fue eliminado.[3]
- **Web**: `webfetch`, `websearch` (con proveedor Exa o Parallel; configurable con `KILO_WEBSEARCH_PROVIDER`).[3]
- **Browser**: `browser_open` (vista previa de aplicación local, solo `localhost`/`127.0.0.1`); MCP `kilo-playwright` opcional.[3]
- **MCP**: herramientas de servidores MCP externos, con prefijo `{servidor}_{herramienta}`.[3]
- **Workflow**: `question`, `task`, `todowrite`, `todoread`, `plan`, `skill`, `open_plan`, `agent_manager`, `board_post`, `board_read`.[3]

Aprobación de comandos peligrosos:
- Se controla en `kilo.jsonc` con la sección `permission`, valores `allow`/`ask`/`deny` por herramienta.[2]
- Para `bash` se admiten patrones glob por comando; las reglas se evalúan en orden y la última coincidencia gana.[2]
- Las reglas jerárquicas se detallan en la página de Agent Permissions (no leída en esta pasada).
- Las herramientas "Always Available" (`question`, `task`, `todowrite`, `todoread`) están accesibles desde cualquier modo.[3]

[?] OQ-004: La documentación de `read` confirma que devuelve el contenido con números de línea, pero no especifica de forma explícita si admite un parámetro de rango (`startLine`/`endLine`) o si se invoca varias veces para rangos. La página `/docs/automate/tools/read` devuelve 404. Verificar el esquema en el repo o en pruebas prácticas antes de fijar la estrategia de lectura de archivos gigantes.

## 9. Límite de contexto y compactación

Kilo Code incluye un sistema de **auto-compactación** (no "truncado").[4]

Disparadores automáticos:
- Tras cada respuesta, Kilo consulta el uso reportado por el proveedor y estima tokens salientes, system prompt y definiciones de herramientas.
- Compacta cuando el conteo alcanza `compaction.threshold_percent` (opcional, 1–100) o cuando el espacio restante toca el **buffer de seguridad reservado**, lo que ocurra primero.[4]
- Si el modelo declara límite de entrada separado, el buffer por defecto es `min(20,000, model_max_output_tokens)`. Si declara un único context window, Kilo reserva la tapa completa de salida hasta 32,000 tokens.[4]

Pase de poda (`prune`):
- Entre turnos, Kilo recorre las salidas de herramientas ya completadas fuera de una ventana de 40,000 tokens y las reemplaza por `"[Old tool result content cleared]"`.[4]

Compactación manual:
- Slash command `/compact` (también `smol` o `condense`), botón en la cabecera de la tarea o ajustes.[4]

Defaults:
- `compaction.auto`: `true`.[4]
- `compaction.threshold_percent`: sin definir.[4]
- `compaction.prune`: `true`.[4]
- `compaction.tail_turns`: `2` (turnos recientes que se preservan verbatim).[4]
- `compaction.preserve_recent_tokens`: 25% del contexto útil, clamp entre 2,000 y 8,000.[4]
- `compaction.reserved`: `min(20,000, model_max_output_tokens)`.[4]

Modelo dedicado para compactación:
- Se puede elegir en VS Code en **Models → Compaction Model**, que mapea a `agent.compaction.model`.[5]
- Configurable también en `kilo.jsonc`.[4]
- Si no se define, usa el modelo de la sesión actual.[4]

Overrides por entorno:
- `KILO_DISABLE_AUTOCOMPACT=1` fuerza `compaction.auto = false`.[4]
- `KILO_DISABLE_PRUNE=1` fuerza `compaction.prune = false`.[4]
- `KILO_EXPERIMENTAL_OUTPUT_TOKEN_MAX` sobrescribe el tope por defecto de 32,000 tokens de salida.[4]

## 10. Notas y contradicciones con AGENTS §4

1. **Variantes por modo (`skills-<modo>/`)**: AGENTS §4 afirma que Kilo Code usa variantes por modo `skills-<modo>/`. La documentación vigente de Skills dice explícitamente: "The new platform does not use mode-specific skill directories. All skills are loaded into a shared pool and the agent decides which skill to invoke based on the skill's `description` field and the current task context".[1] Para filtrar por modo hay que escribir una `description` específica. Esta parte de AGENTS §4 está **desactualizada** y conviene reemplazarla por la regla vigente.

2. **Ruta heredada `~/.kilocode/skills/`**: AGENTS §4 la lista como heredada y aún cargada. La página de Skills no la menciona entre las rutas descubiertas por defecto (que ahora son `.kilo/`, `.agents/`, `.claude/`); la única referencia residual al prefijo `kilocode` en la documentación actual es el nombre del paquete de extensión `kilocode.kilo-code` y la ruta legacy `.kilocode/rules/memory-bank/` mencionada en AGENTS.md.[7] Marcar la ruta heredada como **a verificar** (`OQ-001`).

3. **Variable `SKILL_DIR` / `NPR_HOME`**: AGENTS §4 previene (riesgo conocido n.º 6) que el runtime podría no exponer la ruta de la skill y propone `NPR_HOME` + `scripts/.npr-marker`. La documentación vigente confirma el problema: no hay variable estándar que entregue la ruta absoluta; la skill debe autodescubrirla y marcarse. Esto refuerza la estrategia de la skill, no la contradice.

4. **Variable `KILO_DISABLE_EXTERNAL_SKILLS`**: AGENTS §4 no la menciona. Aparece en la página de AGENTS.md y deshabilita el fallback a `.claude/skills/` y `.agents/skills/`.[7] Útil para entornos restringidos; conviene documentarlo en la skill como opción.

5. **Variable `KILO_DISABLE_SKILL_SHELL`**: no mencionada en AGENTS §4. Desactiva la ejecución de comandos embebidos en `SKILL.md` (kill switch de seguridad).[1] Si la skill depende de scripts ejecutados por el agente desde el cuerpo de `SKILL.md`, debe documentar este kill switch.

6. **Compatibilidad con `.claude/skills/`**: AGENTS §4 la presenta como "activada" sin matiz. La documentación vigente dice que se carga solo cuando la compatibilidad con Claude Code está habilitada (por defecto activada, pero configurable);[1][7] la página de Claude Code Migration permite importar una vez la configuración global de Claude Code.[5] Mantener la nota en AGENTS §4 como "activada por defecto, puede apagarse".

7. **Subagentes y profundidad**: AGENTS §4 describe la herramienta de subagentes como "siempre contemplada" sin detallar parámetros. La documentación vigente aporta parámetros concretos (`description`, `prompt`, `subagent_type`, `background`), confirma el aislamiento de contexto, herencia de modelo y de directorio, y fija el límite de 20 tareas por solicitud para `agent_manager`.[3][8] Recomendar actualizar AGENTS §4 con estos parámetros.

8. **Instalación remota `npx skills add <owner>/<repo>`**: AGENTS §4 lo da como mecanismo de Kilo. La documentación vigente describe el Marketplace como UI dentro del sidebar que añade archivos de configuración/instrucciones/plugin, no como un `npx skills add` estilo npm; el repositorio de la comunidad es `Kilo-Org/kilo-marketplace`.[6] **No se encontró evidencia del comando `npx skills add` en la documentación actual** (puede que exista en CLI pero no aparece en las páginas consultadas). Marcar como `OQ-005`.

9. **Tablero Kilo Swarm**: la documentación vigente introduce un tablero compartido entre sesión principal y descendientes `task`, con herramientas `board_post` y `board_read`.[3][8] AGENTS §4 no lo contempla. Considerar añadirlo a la matriz de herramientas de la skill.

[?] OQ-005: ¿Existe el comando `npx skills add <owner>/<repo>` o equivalente para instalar skills remotas en Kilo Code? La página del Marketplace describe instalación desde la UI y desde `skills.urls`, pero no un wrapper npm. Verificar contra el binario `@kilocode/cli` o contra la guía "Using Docs with Agents".

## Fuentes

- [1] Kilo Code — *Skills* — https://kilocode.ai/docs/customize/skills (consulta 2026-10-05)
- [2] Kilo Code — *Custom Subagents* — https://kilocode.ai/docs/customize/custom-subagents (consulta 2026-10-05)
- [3] Kilo Code — *Tool Use Overview* — https://kilocode.ai/docs/automate/tools (consulta 2026-10-05)
- [4] Kilo Code — *Context Condensing* — https://kilocode.ai/docs/customize/context/context-condensing (consulta 2026-10-05)
- [5] Kilo Code — *Settings* — https://kilocode.ai/docs/getting-started/settings (consulta 2026-10-05)
- [6] Kilo Code — *Marketplace* — https://kilocode.ai/docs/customize/marketplace (consulta 2026-10-05)
- [7] Kilo Code — *Agents.md* — https://kilocode.ai/docs/customize/agents-md (consulta 2026-10-05)
- [8] Kilo Code — *Agent Manager* — https://kilocode.ai/docs/automate/agent-manager (consulta 2026-10-05)
- [9] Kilo-Org — *kilocode README* — https://github.com/Kilo-Org/kilocode/blob/main/README.md (consulta 2026-10-05)