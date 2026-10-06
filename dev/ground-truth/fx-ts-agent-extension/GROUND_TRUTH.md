# Ground truth: fx-ts-agent-extension (F06b)

Fixture de extension tipo VS Code escrita en TypeScript. Modela la arquitectura de un
agente de codigo (modo Kilo Code / Cline / Continue).

## Vision general

- **Procesos:** un unico proceso Node 22 que simula el extension host + webview
  (la API de VS Code real requiere Electron; aqui se reemplaza por `vscode-shim/`).
- **3 modos:** `plan` (read-only + propose), `code` (los 6 tools), `ask` (read-only).
- **6 tools:** `read_file`, `list_dir`, `search_code`, `run_terminal_cmd` (con
  aprobacion), `ask_user` (con aprobacion), `propose_plan`.
- **12 tipos de mensajes webview** despachados por `type: string` en un switch
  dentro de `src/host/messages.ts` (archivo de > 5.000 lineas).
- **Providers LLM:** openai, anthropic, ollama. Factory con `import()` dinamico.
- **Cliente MCP simulado** en proceso, expone 2 tools (`fs.read`, `fs.list`).
- **Condensacion** de contexto cuando el total de tokens supera `maxTokens`.
- **i18n** con bundles `en` y `es` y claves construidas en runtime.

## 4 features (cada una con >= 6 R-NN)

1. **FEAT-001 cambiar-modo** (`webview/mode/change`): valida modo, actualiza
   state, emite `host/mode/updated`. 6 R-NN cubriendo validacion, errores,
   no-op, log de jump-ask-to-code.
2. **FEAT-002 cargar-skill** (`webview/skills/loaded` + comando `fxagent.loadSkill`):
   descubre skills de 2 rutas, merge proyecto > usuario, deep-merge de
   frontmatter. 6 R-NN cubriendo merge, errores de frontmatter, errores de IO.
3. **FEAT-003 ejecutar-herramienta-con-aprobacion** (`webview/tools/start` +
   `webview/chat/approval-request/response`): valida tool, valida modo,
   pide aprobacion si requiere, ejecuta, publica resultado. 6 R-NN cubriendo
   exito, error de tool desconocida, error de tool no permitida, cancelacion
   por timeout, bypass con `askForTerminal=false`, error de argumentos.
4. **FEAT-004 condensar-contexto** (`webview/context/condensed` + comando
   `fxagent.condense`): estima tokens, decide si condensa, llama al provider,
   reemplaza mensajes. 6 R-NN cubriendo no-op, exito, silent_fail (catch
   vacio), boundary, validacion, keep-recent.

## 6 trampas del ecosistema (CC-06)

1. Comandos declarados en `package.json contributes.commands` (no llamada
   explicita en el codigo).
2. Switch de mensajes en archivo de > 5.000 lineas.
3. Precedencia de skills proyecto > usuario con merge parcial.
4. Herramientas habilitadas por modo via objeto `MODES[id].allowedTools`.
5. i18n runtime: ``t(`mode.${id}.title`)``.
6. Provider factory con `import()` dinamico.

## 6 trampas del paquete (CC-04)

1. `run_terminal_cmd` se ejecuta sin pedir aprobacion si
   `config.askForTerminal === false` (combinacion de dos settings).
2. `condenseIfNeeded` traga el error del provider y devuelve mensajes
   intactos (catch vacio).
3. `merge` de skills concatena `body` sin deduplicar.
4. `ask_user` con timeout = reject (cancelled_by_user solo aparece bajo
   esa combinacion).
5. `loadProvider` con `kind` desconocido devuelve stub silencioso en vez
   de lanzar.
6. `dispatch` loguea ANTES de ejecutar el handler; si el handler lanza,
   el log queda inconsistente.

## Decisiones y variantes

- **VS Code API simulada** (`vscode-shim/`): minimo necesario para correr en
  Node 22 puro. Documentado en el README.
- **`messages.ts` util, no relleno**: cada handler tiene validacion zod,
  logica real, helpers y tests inline con `import.meta.vitest`.
- **`runFixture_tests.py` con contenedor obligatorio**: el host de desarrollo
  no tiene `node`; el harness levanta la imagen `node:22-slim`.
- **Frontend con shim (no Electron)**: para mantener el fixture portable.
- **Provider stubs sin red**: openai, anthropic, ollama son clases que
  generan respuestas sinteticas localmente.
