# fx-ts-agent-extension (F06b)

Fixture de **extension tipo VS Code** escrita en TypeScript que imita la arquitectura de un
agente de código (modelo Kilo Code / Cline / Continue). Sirve para que la skill
`notemartin-project-review` practique sobre código real de un proyecto con:

- Proceso de **extension host** (Node 22) + **webview** con protocolo de mensajes tipado.
- **3 modos** (`plan`, `code`, `ask`) con prompts distintos y grupos de herramientas.
- **Carga de skills** desde `~/.fxagent/skills/` y `.fxagent/skills/` con precedencia y
  parseo de frontmatter.
- **6 herramientas** (`read_file`, `list_dir`, `search_code`, `run_terminal_cmd`,
  `ask_user`, `propose_plan`) con loop de aprobación para las sensibles.
- **12 tipos de mensajes webview** despachados por `type: string` en un `switch` dentro de
  `src/host/messages.ts` (archivo de **> 5.000 líneas** por requisito del roadmap).
- Abstracción de **proveedores LLM** (openai, anthropic, ollama) vía factory con
  `import()` dinámico.
- **Cliente MCP simulado** en proceso.
- **Condensación de contexto** cuando el total de tokens supera el umbral.
- **i18n** con claves construidas en runtime: ``t(`mode.${id}.title`)``.

## Estructura

```
src/
  host/
    extension.ts       activate() + registerCommand + contributes
    messages.ts        switch con 12 tipos (> 5.000 lineas)
    modes.ts           3 modos
    skills.ts          skill loader (2 rutas, merge de frontmatter)
    tools.ts           6 herramientas con approval flow
    providers/         factory con import() dinamico
    mcp/               cliente MCP simulado
    context.ts         condensacion
    i18n.ts            bundles + t()
    vscode-shim/       API minima para tests en Node 22
  webview/
    main.tsx, messages.ts, ui/*.tsx, styles.css
tests/                 vitest
```

## Trampas plantadas (6 ecosistema + 6 paquete)

### Ecosistema

1. **Comandos declarados en `package.json contributes.commands`** sin llamada explícita
   en el código: el scanner estático debe leer el manifiesto para descubrirlos.
2. **Switch de mensajes en `messages.ts` (> 5.000 líneas)**: el scanner no debe inferir
   la lista de tipos de la estructura del archivo; debe leer las constantes.
3. **Precedencia de skills proyecto > usuario** con merge parcial: el frontmatter del
   proyecto pisa al del usuario en claves, pero el `body` se concatena.
4. **Herramientas habilitadas por modo** vía objeto `MODES[id].allowedTools`, no por
   condicionales: el scanner debe leer la tabla, no buscar `if mode === "code"`.
5. **i18n runtime** ``t(`mode.${id}.title`)``: las claves se construyen en runtime, no
   son literales en el código.
6. **Provider factory con `import()` dinámico**: el switch de proveedores sólo se
   ejecuta al primer uso; los `import()` no se ven estáticamente.

### Paquete (CC-04)

1. **`run_terminal_cmd` se ejecuta sin pedir aprobación** si
   `config.ask_for_terminal === false` (combinación de dos settings).
2. **`condenseIfNeeded` traga el error del provider** y devuelve los mensajes intactos
   (catch vacío).
3. **`merge` de skills concatena `body` sin deduplicar** fragmentos idénticos.
4. **`ask_user` con timeout = reject** produce el mismo resultado que el usuario
   denegando la aprobación (cancelación sólo aparece con esa combinación).
5. **`loadProvider` con `kind` desconocido** retorna un stub silencioso en lugar de
   lanzar error (default silencioso).
6. **`dispatch` registra el mensaje en el log antes de ejecutar el handler**; si el
   handler lanza, el log queda con la entrada del intento pero sin resultado (estado
   inconsistente).

## Shims

`src/host/vscode-shim/` simula la API mínima de VS Code para que la extensión corra en
Node 22 puro. **No es la API real**: el README del shim deja claro que es para tests.

## Ejecución

```bash
# en host con Node 22
make test

# via harness (recomendado)
python dev/tools/run_fixture_tests.py --fixture fx-ts-agent-extension
```

## Ground truth

`dev/ground-truth/fx-ts-agent-extension/ground_truth.json` documenta los 4 features
(`cambiar-modo`, `cargar-skill`, `ejecutar-herramienta-con-aprobacion`,
`condensar-contexto`) con sus trazas, decision points, outcomes, errores, configuración,
estados, telemetría, interacciones y callgraph.
