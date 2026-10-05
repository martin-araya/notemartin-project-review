# Adaptadores de runtime — Hermes Agent, Cline, Kilo Code

> Documento generado en F02. Cada afirmación lleva cita supra-índice `[N]`; el bloque de fuentes al final usa la misma numeración. Consultas: 2026-10-05.
>
> Borradores por subagente investigador en `dev/evals/drafts/runtime-hermes.md`, `runtime-cline.md` y `runtime-kilo.md`.

## Matriz comparativa

| Aspecto | Hermes Agent | Cline | Kilo Code |
|---|---|---|---|
| **Ruta global** | `~/.hermes/skills/<categoría>/<nombre>/SKILL.md` [H2] | `~/.cline/skills/<nombre>/SKILL.md` [C1][C6] | `~/.kilo/skills/<nombre>/SKILL.md` [K1] |
| **Ruta de proyecto** | `<project>/.hermes/skills/` o `<project>/.agents/skills/` (con `hermes skills trust`) [H2] | `.cline/skills/` (recomendada), `.clinerules/skills/` (heredada), `.claude/skills/` (compatibilidad) [C1] | `.kilo/skills/`; también `.agents/skills/` y `.claude/skills/` [K1] |
| **Activación** | Slash `/<skill-name>`; `skill_view(name)`; coincidencia semántica con `description` [H2] | Herramienta `use_skill` por coincidencia con `description`; slash `/<skill>`; ≤ 1024 chars en `description` [C1] | Coincidencia semántica con `description`; invocación explícita por nombre; slash `/<nombre>` [K1] |
| **Carga de `references/`** | `skill_view(name, path)` (nivel 2 de divulgación progresiva) [H2][H3] | `read_file` con enlaces relativos desde `SKILL.md` [C1] | `read` con rutas relativas; recursos declarados como subcarpetas hermanas [K1] |
| **Resolución de `SKILL_DIR`** | `HERMES_HOME` + convención, o autodescubrimiento desde `__file__` con `scripts/.npr-marker` [H7][H8] | Sin variable expuesta; autodescubrir rutas canónicas y validar con `.npr-marker` [C1][C6] | Sin variable expuesta; autodescubrir rutas canónicas y validar con `.npr-marker` [K1] |
| **Subagentes (herramienta)** | `delegate_task` (toolset `delegation`); parámetros `tasks`, `goal`, `context`, `output_schema`, `action` [H3][H8] | `use_subagents` (habilitado por defecto); cada subagente **read-only**, sin MCP ni anidamiento [C2] | `task` (sesión con contexto aislado) y `agent_manager` (solo VS Code, hasta 20 tareas por solicitud); tablero Kilo Swarm con `board_post`/`board_read` [K3][K8] |
| **Lectura de archivos** | `read_file` con `offset` y `limit`, paginación, transcodificación UTF-16 [H3] | `read_files` por lotes; subagentes usan `read_file` separado [C3] | `read` con números de línea; parámetros de rango no documentados (ver OQ-K-004) [K3] |
| **Búsqueda** | `search_files` (ripgrep) con modos `content`, `files_with_matches`, `count` [H3] | `search` (ripgrep); subagentes usan `search_files` con regex [C3] | `grep` (regex sobre contenidos) y `glob` (patrones) [K3] |
| **Ejecución de comandos** | `terminal` (7 backends: local, docker, ssh, singularity, modal, daytona, vercel_sandbox); aprobación configurable con `approvals.mode` [H3][H5] | `bash` con `requires_approval` por comando; Auto-Approve de dos niveles; `CLINE_COMMAND_PERMISSIONS` declarativo [C3][C4][C6] | `bash` con timeout y directorio configurables; permisos `allow`/`ask`/`deny` en `kilo.jsonc` [K3] |
| **Límite de contexto** | Heredado del modelo; `compression.threshold` (50 % con suelo 0.75); safety net al 85 %; prompt caching Anthropic con TTL configurable [H6] | Depende del modelo configurado; slash `/smol` o `/compact` para compactar manualmente; sin compactación automática silenciosa [C5][C6] | Heredado del modelo; auto-compactación con `compaction.threshold_percent`; pase de `prune` a 40k tokens; `/compact` manual [K4] |
| **Compactación automática** | `Agent ContextCompressor` al 50 % (default); `tail_mode: lean` retiene ~2.5 % + índice de anclas [H6] | No automática; solo manual con `/smol` [C5] | `compaction.auto=true` por defecto; buffer reservado `min(20k, model_max_output_tokens)` [K4] |

Notas de la matriz:

- En **Cline** los subagentes son **read-only**: el orquestador de `npr` debe escribir las notas él mismo; los subagentes solo investigan [C2].
- En **Kilo Code** el tablero Kilo Swarm (`board_post`/`board_read`) existe y no está documentado en AGENTS §4; el orquestador puede usarlo para coordinarse con subagentes [K3][K8].
- En **Hermes** la categoría propuesta es `software-development` (verificada como categoría real) [H2].

## Cómo lanzar un subagente en cada runtime

### Hermes Agent

Herramienta `delegate_task` del toolset `delegation` [H3][H8]. Ejemplo (esquema OpenAI function-calling):

```json
{
  "tool": "delegate_task",
  "params": {
    "tasks": [
      {
        "goal": "Investiga la WU-007: lee src/orchestrator/wu.ts y devuelve un resumen de 20 líneas con los archivos tocados y las decisiones detectadas.",
        "context": "Ruta del repo: <ruta-al-proyecto>. WU priorizada por ola 2."
      },
      {
        "goal": "Investiga la WU-008 sobre el módulo de métricas.",
        "context": "Misma ruta. Devuelve también métricas del grafo."
      }
    ]
  }
}
```

Parámetros clave:

- `tasks`: array con ≥1 entrada; se ejecutan en paralelo hasta `delegation.max_concurrent_children`.
- `goal`: lo que el subagente debe lograr; autocontenido (no ve historial del padre).
- `context`: paths, mensajes de error, idioma de salida.
- `output_schema`: JSON Schema opcional para validar la respuesta final.
- `action`: `spawn` (default), `list`, `steer` (inyectar corrección), `stop`.

Los hijos heredan los toolsets del padre excepto `delegate_task`, `clarify`, `memory`, `cronjob` [H8]. No abren prompts al usuario; no pueden cerrar trabajo de otros subagentes [H8].

### Cline

Herramienta `use_subagents` (habilitada por defecto; se desactiva en Settings → Features → Agent) [C2]. El agente principal lanza varios subagentes en paralelo y recibe los informes enfocados:

```text
use_subagents(
  prompts=[
    "Investiga el módulo de inventario: lee src/inventory/*.ts y devuelve las rutas más relevantes y las funciones exportadas.",
    "Investiga el módulo de pagos: busca usos de Stripe y devuelve los archivos que llamen a la API."
  ]
)
```

Restricciones críticas [C2]:

- Los subagentes son **read-only**: pueden usar `read_file`, `list_files`, `search_files`, `list_code_definition_names`, `execute_command` (solo read-only como `ls`, `grep`, `git log`, `git diff`) y `use_skill`.
- **No pueden editar archivos**, no pueden usar browser, **no pueden acceder a servidores MCP** y **no pueden lanzar sub-subagentes** (no hay anidamiento).
- La aprobación de lanzamiento sigue Auto-Approve "Read project files" [C2].
- **No hay tope numérico de concurrencia documentado** más allá del paralelismo real de la UI/SDK (ver OQ-C-003).

Implicación para `npr`: el orquestador debe escribir el resultado de cada subagente en el workspace; los subagentes solo devuelven texto.

### Kilo Code

Dos mecanismos ortogonales [K3][K8]:

#### `task` (subagente en sesión, sin worktree)

```text
task(
  description="Investiga WU-007",
  prompt="Lee src/orchestrator/wu.ts y devuelve un resumen de 20 líneas con archivos tocados y decisiones detectadas.",
  subagent_type="explore",  // o "general"
  background=false         // true → retorna de inmediato; Kilo entrega el resultado cuando termina
)
```

Parámetros [K3]:

- `description`, `prompt`, `subagent_type` (`general` o `explore`, o un agente custom), `background` (bool).
- Contexto aislado: no hereda la conversación del padre [K3].
- Directorio: usa el mismo directorio de proyecto que el padre; `task` no crea worktree [K3][K8].
- Anidamiento: permitido si la profundidad configurada y el permiso `task` del agente lo permiten [K3].

#### `agent_manager` (Agent Manager, solo VS Code)

```text
agent_manager(
  action="list"   // para ver sesiones activas
)
```

Hasta 20 tareas por solicitud [K8]. Acciones: `list`, `prompt`, `stop`, `move`, `answer`.

#### Tablero Kilo Swarm

`board_post(to, type, body)` y `board_read(since)` permiten coordinación persistente entre sesión principal y descendientes `task` [K3][K8]. Útil para que el orquestador publique hallazgos sin saturar el contexto del padre.

#### Subagentes integrados [K3]

- `general`: tareas multi-paso; acceso completo excepto `todo`.
- `explore`: rápido, **solo lectura**; no puede modificar archivos.

## Modo secuencial de respaldo

Cuando el runtime no expone subagentes, los tiene deshabilitados, o el usuario rechaza cada aprobación, el orquestador principal asume el rol de cada subagente uno por uno. La disciplina es estricta: **la conversación es volátil; el disco es la verdad** [AGENTS §8 ley 5].

1. **Leer el brief de disco**: el orquestador abre `notes/wu/<WU-id>/brief.md` (generado por `npr brief` en F27) y lo lee completo. No confíes en lo que recuerdes de pasos anteriores.
2. **Ejecutar el rol**: el orquestador realiza la lectura o investigación como si fuera el subagente (lectura por rangos, grep, lectura de docs).
3. **Escribir el resultado a disco**: antes de avanzar, el resultado se materializa en `notes/wu/<WU-id>/output.md` (o el path que indique el brief) y se actualiza `state/ledger.jsonl` con `by=orchestrator` y la fecha.
4. **Actualizar el ledger**: `npr ledger mark <path> --state done --by orchestrator --note <ruta>`.
5. **Repetir con el siguiente brief** hasta vaciar la ola actual.
6. **Si el contexto se acerca al límite**: ejecutar `npr resume` para registrar el progreso y terminar la sesión limpia.

Disciplinas adicionales:

- No resumir oralmente el resultado; el archivo en disco es la única fuente que usará la siguiente fase.
- Si la investigación excede el contexto, partir el brief en dos y procesarlos por separado.
- Mantener `state/state.json` actualizado después de cada paso.
- Los gates (`npr gate coverage`, etc.) se ejecutan al final, no en cada paso, para no frenar el progreso.

## Resolver `SKILL_DIR` (exportar como `NPR_HOME`)

Algoritmo común implementado por `scripts/npr.py` (orden de prioridad) [H7][C6][K1]:

1. **Variable de entorno `NPR_HOME`**: si está definida y `scripts/.npr-marker` existe dentro → usar. Tiene la máxima prioridad.
2. **Argumento CLI `--skill-dir`**: si se pasó al invocar `npr`, usar esa ruta y validar el marcador.
3. **Variable del runtime**:
   - Hermes: `HERMES_HOME/skills/<categoría>/<nombre>/` validando con `.npr-marker` [H7].
   - Cline: no hay variable; caer al siguiente paso.
   - Kilo: no hay variable; caer al siguiente paso.
4. **Rutas canónicas en orden de precedencia**:
   - Proyecto: `./.hermes/skills/<categoría>/<nombre>/`, `./.kilo/skills/<nombre>/`, `./.cline/skills/<nombre>/`, `./.clinerules/skills/<nombre>/`, `./.agents/skills/<nombre>/`, `./.claude/skills/<nombre>/`.
   - Global: `~/.hermes/skills/<categoría>/<nombre>/`, `~/.kilo/skills/<nombre>/`, `~/.cline/skills/<nombre>/`, `~/.claude/skills/<nombre>/`, `~/.agents/skills/<nombre>/`.
   - Windows nativo: `%LOCALAPPDATA%\hermes\skills\<categoría>\<nombre>\` [H1].
   - La primera ruta cuyo `scripts/.npr-marker` exista gana.
5. **Fallo**: error `NPR-E101` "no se pudo resolver SKILL_DIR" con las rutas probadas y la causa (marcador ausente, permiso denegado, ruta inexistente).

Una vez resuelta, `npr.py` exporta `NPR_HOME` para todos sus subprocesos. Los scripts internos de la skill lo leen con `os.environ["NPR_HOME"]` o lo derivan de `Path(__file__).resolve().parents[1]` como respaldo.

## Notas sobre contradicciones con AGENTS §4

Las contradicciones detectadas por los subagentes investigadores se registran en `DECISIONS.md` y se resumen aquí:

- **Hermes** [H10]: AGENTS §4 propone el comando `hermes skills install <owner>/<repo>/<nombre>`; la docs usan la forma `<owner>/<repo>/<ruta>` o `<owner>/<repo>.git`. Categoría `software-development` confirmada. Windows nativo no mencionado en AGENTS §4.
- **Cline** [C10]: AGENTS §4 menciona solo `.cline/skills/` y `.clinerules/skills/`; la docs vigente incluye también `.claude/skills/` como tercera ruta de proyecto. Los subagentes son **read-only** (contradicción parcial con el diseño secuencial de respaldo de AGENTS §21).
- **Kilo** [K10]: AGENTS §4 afirma "variantes por modo `skills-<modo>/`"; la docs vigente dice que **no hay directorios específicos por modo** (todo en pool común, filtrado por `description`). La ruta heredada `~/.kilocode/skills/` no figura en la docs vigente de Skills. El comando `npx skills add <owner>/<repo>` no se encontró en la docs actual (existe Marketplace desde UI y `skills.urls`). Variables nuevas a documentar: `KILO_DISABLE_EXTERNAL_SKILLS` y `KILO_DISABLE_SKILL_SHELL`.

Decisiones asociadas: D-122 a D-129 (ver `DECISIONS.md`).

## Preguntas abiertas

| Id | Runtime | Pregunta |
|---|---|---|
| OQ-001 | Hermes | ¿Exporta Hermes `HERMES_HOME` automáticamente al tool `terminal`, o hay que declararla en `required_environment_variables` del frontmatter? |
| OQ-CLINE-001 | Cline | No hay variable/argumento documentado que Cline pase a una skill para indicarle su propio directorio; la autodetección es la única vía. |
| OQ-CLINE-002 | Cline | ¿Admite `use_skill` parámetros explícitos (p. ej. nombre de la skill), o el modelo solo la invoca implícitamente por coincidencia semántica? |
| OQ-CLINE-003 | Cline | No hay tope numérico documentado de subagentes concurrentes ni presupuesto de tokens por subagente. |
| OQ-K-001 | Kilo | ¿Sigue cargándose la ruta heredada `~/.kilocode/skills/` por compatibilidad interna, aunque la docs no la liste? |
| OQ-K-002 | Kilo | No existe variable `SKILL_DIR`/`NPR_HOME`; la skill debe autodescubrir su ruta (ya previsto por AGENTS §4 regla 6). |
| OQ-K-003 | Kilo | No hay tope explícito de subagentes `task` simultáneos; la limitación real es la profundidad configurada. |
| OQ-K-004 | Kilo | La herramienta `read` confirma números de línea pero la página `/docs/automate/tools/read` devuelve 404; parámetros de rango no documentados. |
| OQ-K-005 | Kilo | ¿Existe `npx skills add <owner>/<repo>` o equivalente para instalar skills remotas en Kilo Code? El Marketplace usa UI y `skills.urls`. |

## Fuentes

- [H1] Nous Research — `NousResearch/hermes-agent` README — https://github.com/NousResearch/hermes-agent (consulta 2026-10-05)
- [H2] Nous Research — Skills System (docs oficiales Hermes Agent) — https://hermes-agent.nousresearch.com/docs/user-guide/features/skills (consulta 2026-10-05)
- [H3] Nous Research — Built-in Tools Reference — https://hermes-agent.nousresearch.com/docs/reference/tools-reference (consulta 2026-10-05)
- [H4] Nous Research — Architecture — https://hermes-agent.nousresearch.com/docs/developer-guide/architecture (consulta 2026-10-05)
- [H5] Nous Research — Security — https://hermes-agent.nousresearch.com/docs/user-guide/security (consulta 2026-10-05)
- [H6] Nous Research — Context Compression and Caching — https://hermes-agent.nousresearch.com/docs/developer-guide/context-compression-and-caching (consulta 2026-10-05)
- [H7] Nous Research — Environment Variables Reference — https://hermes-agent.nousresearch.com/docs/reference/environment-variables (consulta 2026-10-05)
- [H8] Nous Research — `tools/delegate_tool.py` (código fuente) — https://raw.githubusercontent.com/NousResearch/hermes-agent/main/tools/delegate_tool.py (consulta 2026-10-05)
- [C1] Cline — Skills — https://docs.cline.bot/customization/skills (consulta 2026-10-05)
- [C2] Cline — Subagents — https://docs.cline.bot/features/subagents (consulta 2026-10-05)
- [C3] Cline — Tools — https://docs.cline.bot/tools-reference/all-cline-tools (consulta 2026-10-05)
- [C4] Cline — Auto Approve & YOLO Mode — https://docs.cline.bot/features/auto-approve (consulta 2026-10-05)
- [C5] Cline — Using Commands — https://docs.cline.bot/core-workflows/using-commands (consulta 2026-10-05)
- [C6] Cline — Config / Storage locations — https://docs.cline.bot/getting-started/config (consulta 2026-10-05)
- [K1] Kilo Code — Skills — https://kilocode.ai/docs/customize/skills (consulta 2026-10-05)
- [K2] Kilo Code — Custom Subagents — https://kilocode.ai/docs/customize/custom-subagents (consulta 2026-10-05)
- [K3] Kilo Code — Tool Use Overview — https://kilocode.ai/docs/automate/tools (consulta 2026-10-05)
- [K4] Kilo Code — Context Condensing — https://kilocode.ai/docs/customize/context/context-condensing (consulta 2026-10-05)
- [K5] Kilo Code — Settings — https://kilocode.ai/docs/getting-started/settings (consulta 2026-10-05)
- [K6] Kilo Code — Marketplace — https://kilocode.ai/docs/customize/marketplace (consulta 2026-10-05)
- [K7] Kilo Code — Agents.md — https://kilocode.ai/docs/customize/agents-md (consulta 2026-10-05)
- [K8] Kilo Code — Agent Manager — https://kilocode.ai/docs/automate/agent-manager (consulta 2026-10-05)
- [K9] Kilo-Org — kilocode README — https://github.com/Kilo-Org/kilocode/blob/main/README.md (consulta 2026-10-05)