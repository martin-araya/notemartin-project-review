# Cline — investigación de runtime

## 1. Fuentes consultadas

1. Documentación oficial de **Cline — Skills** ([docs.cline.bot/customization/skills](https://docs.cline.bot/customization/skills)) [1]
2. Documentación oficial de **Cline — Subagents** ([docs.cline.bot/features/subagents](https://docs.cline.bot/features/subagents)) [2]
3. Documentación oficial de **Cline — Tools** ([docs.cline.bot/tools-reference/all-cline-tools](https://docs.cline.bot/tools-reference/all-cline-tools)) [3]
4. Documentación oficial de **Cline — Auto Approve & YOLO Mode** ([docs.cline.bot/features/auto-approve](https://docs.cline.bot/features/auto-approve)) [4]
5. Documentación oficial de **Cline — Using Commands** ([docs.cline.bot/core-workflows/using-commands](https://docs.cline.bot/core-workflows/using-commands)) [5]
6. Documentación oficial de **Cline — Config / Storage locations** ([docs.cline.bot/getting-started/config](https://docs.cline.bot/getting-started/config)) [6]

## 2. Ruta global de skills

Cline busca skills globales del usuario directamente bajo `~/.cline/skills/` en macOS y Linux, y bajo
`C:\Users\USERNAME\.cline\skills\` en Windows [1][6]. La estructura canónica es una carpeta por skill,
con `SKILL.md` (requerido) y subcarpetas opcionales `docs/`, `templates/` y `scripts/` [1]. Ejemplo:

```
~/.cline/skills/
├── aws-cdk-deploy/
│   └── SKILL.md
├── pr-review-checklist/
│   └── SKILL.md
└── data-analysis/
    ├── SKILL.md
    └── scripts/validate.py
```

## 3. Ruta de proyecto

En el workspace del repositorio analizado, Cline descubre skills en tres rutas, en este orden de
precedencia recomendada: [1]

- **`.cline/skills/`** (recomendada, oficial del runtime actual).
- **`.clinerules/skills/`** (heredada, conservada por compatibilidad).
- **`.claude/skills/`** (compatibilidad cruzada con Agent Skills / otros runtimes).

Cada carpeta `.cline/skills/<nombre>/SKILL.md` es una skill autocontenida [1]. Cline resuelve
colisiones por nombre dando **precedencia a la skill global sobre la del proyecto**: si una skill
global y una skill de proyecto comparten nombre, gana la global [1]. No se documenta un orden de
precedencia explícito entre las tres rutas de proyecto; la documentación solo indica que
`.cline/skills/` es la recomendada [1].

## 4. Mecanismo de activación

La activación ocurre por coincidencia semántica entre el mensaje del usuario y la `description` del
frontmatter YAML de cada `SKILL.md` [1]. El runtime expone la herramienta **`use_skill`** al modelo:
cuando Cline decide que una skill coincide con la tarea, invoca `use_skill`, que carga el cuerpo de
`SKILL.md` y queda activo hasta el final de la tarea [1].

Parámetros relevantes que el orquestador puede explotar:

- `description` (frontmatter): **máximo 1024 caracteres**; determina el disparo [1].
- `name` (frontmatter): debe coincidir exactamente con el nombre del directorio, en kebab-case [1].
- `SKILL.md` cuerpo: recomendado **bajo 5k tokens**; el detalle va en `docs/` enlazado [1].

Además del disparo automático por descripción, hay disparo **explícito** mediante slash commands en
el chat: escribir `/` muestra sugerencias y seleccionar una skill (p. ej. `/aws-deploy`) fuerza su
activación inmediata [1].

Subagentes también pueden invocar skills: dentro de un subagente está disponible `use_skill` como una
de las herramientas permitidas [2].

## 5. Carga de references/

El runtime implementa **carga progresiva** en tres niveles [1]:

| Nivel | Cuándo se carga | Costo en tokens | Contenido |
|---|---|---|---|
| Metadatos | Siempre al arrancar | ~100 tokens por skill | `name` y `description` del frontmatter |
| Instrucciones | Cuando se dispara la skill | Bajo 5k tokens | Cuerpo de `SKILL.md` |
| Recursos | Bajo demanda | Efectivamente ilimitado | Archivos en `docs/`, `templates/`, `scripts/` |

Los archivos de soporte se referencian desde `SKILL.md` mediante **enlaces relativos** en Markdown
(p. ej. `[setup.md](docs/setup.md)`) [1]. Cuando el modelo encuentra ese enlace durante la tarea,
usa la herramienta **`read_file`** para abrir el archivo [1]. Los scripts listados en `scripts/` se
**ejecutan directamente** y solo su salida (no el código fuente) entra al contexto [1]. Esta es la
mecánica que la skill `notemartin-project-review` debe asumir: los enlaces relativos funcionan como
si el directorio de la skill fuera la raíz; las plantillas se leen con `read_file`; los scripts de
`scripts/` se ejecutan como subprocesos.

No se documenta una variable de entorno explícita que el runtime pase a la skill indicando su
directorio de instalación; la resolución de la ruta parece ocurrir internamente (ver §6 y §10).

## 6. Cómo obtiene el agente la ruta de la skill

`[?] OQ-CLINE-001: la documentación pública de Cline no describe una variable de entorno o argumento
explícito que el runtime pase a una skill para indicarle su propio directorio de instalación. Lo que
sí está documentado es la variable de configuración global `CLINE_DATA_DIR` que redefine
`~/.cline/data/` (no `~/.cline/skills/`), y la opción CLI `--config /ruta/a/config` [6].`

Implicación para la skill: `npr` debe **autodetectar** su directorio recorriendo las rutas canónicas
(`~/.cline/skills/<nombre>/`, `.cline/skills/<nombre>/`, `.clinerules/skills/<nombre>/`,
`.claude/skills/<nombre>/`) y validando con el archivo marcador `scripts/.npr-marker`. Esto ya está
previsto en `AGENTS.md §4 regla 6` y se confirma aquí como la única vía razonable con la
documentación vigente.

## 7. Subagentes (herramienta, parámetros, herencia, concurrencia, escritura)

Cline ofrece la herramienta **`use_subagents`** para que el agente principal lance agentes
investigadores en paralelo [2]. Cada subagente:

- Recibe su propio prompt de investigación enfocado [2].
- Tiene **su propia ventana de contexto y presupuesto de tokens** independiente del agente principal
  [2].
- Corre **en paralelo** con los demás subagentes de la misma oleada [2].
- Está **restringido a operaciones de lectura**: puede usar `read_file`, `list_files`,
  `search_files` (regex), `list_code_definition_names`, `execute_command` (solo comandos read-only
  como `ls`, `grep`, `git log`, `git diff`), y `use_skill` [2].
- **No puede editar archivos**, no puede usar el browser, **no puede acceder a servidores MCP**, y
  **no puede lanzar sub-subagentes** (no hay anidamiento) [2].
- Devuelve un informe enfocado en las rutas de archivo más relevantes para que el agente principal
  lea a continuación [2].
- Los costos (tokens y gasto de API) se rastrean por separado por subagente y se suman al costo
  total de la tarea; la UI muestra estadísticas por subagente [2].

**Concurrencia y aprobación**: la herramienta está habilitada por defecto; Cline decide cuándo vale
la pena paralelizar [2]. El lanzamiento de subagentes sigue el permiso Auto-Approve **"Read project
files"**: si está activo, los lanzamientos se aprueban automáticamente; si no, Cline pide
confirmación mostrando los prompts que piensa enviar [2]. **No hay tope numérico de concurrencia
documentado** más allá del paralelismo real que la UI o el SDK ejecuten.

## 8. Herramientas de lectura / búsqueda / ejecución

Las herramientas nativas de `ClineCore` (el runtime actual) son [3]:

| Herramienta | Función |
|---|---|
| `bash` | Ejecutar comandos de shell [3] |
| `editor` | Ver y editar archivos [3] |
| `read_files` | Lectura por lotes de varios archivos a la vez [3] |
| `apply_patch` | Aplicar diffs unificados a archivos [3] |
| `search` | Búsqueda en el código fuente impulsada por **ripgrep** [3] |
| `fetch_web` | Peticiones HTTP con conversión HTML→Markdown [3] |
| `ask_question` | Preguntar al usuario [3] |

Notas adicionales:

- La búsqueda es **ripgrep** nativo (`rg`), lo que la skill puede invocar directamente desde
  `scripts/npr/` o aprovechar como motor del módulo `symbols` [3].
- La lectura en lotes (`read_files`) es útil para que la skill pida leer varios archivos de un módulo
  en una sola llamada al modelo.
- Los nombres legacy en formato XML (`read_file`, `replace_in_file`, `execute_command`) son de
  versiones antiguas; el runtime actual usa los nombres de la tabla [3]. Los subagentes, en cambio,
  sí exponen `read_file`, `list_files`, `search_files`, `list_code_definition_names` y
  `execute_command` como herramientas separadas [2].

**Aprobación de comandos peligrosos**: Cline no usa una lista fija de comandos seguros [4]. El modelo
marca cada comando con un flag `requires_approval` que el usuario puede preconfigurar [4]. Ejemplos
documentados: `npm run build` y `git status` suelen marcarse seguros; `npm install <pkg>`, `rm -rf
<path>`, `mv <a> <b>`, `sed -i ...` suelen requerir aprobación [4]. Auto-Approve tiene dos
niveles: "Execute safe commands" (solo los marcados seguros) y "Execute all commands" (también los
marcados como riesgosos), este último subordinado al toggle base [4]. La variable
`CLINE_COMMAND_PERMISSIONS` permite además una política declarativa con listas `allow`/`deny` [6].

## 9. Límite de contexto y compactación

Cline no publica un límite único: depende del modelo configurado por el usuario (Claude, GPT-5,
Gemini, etc.), gestionado por la pasarela de providers [6]. **Sí hay compactación explícita** mediante
los slash commands `/smol` y su alias `/compact`, que comprimen el historial de la conversación
preservando el contexto esencial y liberan espacio en la ventana sin crear una tarea nueva [5]. El
comando complementario `/newtask` hace algo distinto: inicia una tarea nueva con contexto destilado
de la actual [5]. No hay compactación automática silenciosa documentada; la decisión la toma el
usuario (o el modelo, mediante Auto-Approve si lo invoca sin pedir permiso).

El presupuesto por subagente es **independiente** del agente principal [2], pero la documentación no
cuantifica el tamaño ni la política de compactación dentro del subagente.

## 10. Notas y contradicciones con AGENTS §4

**Verificaciones confirmadas (acordes con AGENTS §4):**

- Ruta de proyecto `.cline/skills/` (recomendada) [1].
- Ruta global `~/.cline/skills/` [1][6].
- Ruta heredada `.clinerules/skills/` [1].
- Activación por descripción que coincide, vía herramienta `use_skill` [1].
- `description` ≤ 1024 caracteres [1].
- `SKILL.md` recomendado bajo 5k tokens [1].

**Contradicciones, matices o ampliaciones:**

- AGENTS §4 menciona también `.claude/skills/` como ruta de Kilo con compatibilidad activada; en
  Cline también aparece como tercera ruta de proyecto soportada [1]. La documentación no detalla
  precedencia entre las tres rutas de proyecto, solo dice que `.cline/skills/` es la recomendada.
- AGENTS §4 asume que "el lanzador de Python varía (`python`, `python3`, `py -3`)" como regla
  universal; Cline **no documenta este detalle** para los scripts de skills — los `scripts/` se
  ejecutan directamente y solo su salida entra al contexto [1]. El orquestador debe asumir el mismo
  fallback de Pythons.
- AGENTS §4 asume que la skill recibe una variable `SKILL_DIR` o equivalente: la documentación de
  Cline **no expone tal variable**. La skill debe autodetectar su ruta recorriendo las rutas
  canónicas — esto coincide con el "Riesgo conocido" del propio AGENTS §4 regla 6.
- AGENTS §11 lista `use_skill` como herramienta genérica de skill; confirmado para Cline [1].
- AGENTS §11 lista `use_subagents` como subagente; confirmado para Cline con la salvedad de que los
  subagentes son **read-only, no pueden editar archivos, no pueden usar MCP ni anidar subagentes**
  [2]. Si el orquestador de `npr` depende de que los subagentes escriban notas en el workspace, debe
  hacerlo el agente principal, no los subagentes.
- AGENTS §13 asume la existencia de la herramienta `skill_view` (mencionada para Hermes Agent); en
  Cline la carga de recursos bajo `docs/`, `templates/` y `scripts/` se hace con `read_file` y
  ejecución directa de scripts, no con una herramienta dedicada [1].
- AGENTS §8 (reglas duras del constructor) advierte que la skill debe funcionar con subagentes "si
  el runtime los tiene y en modo secuencial de respaldo si no". En Cline los subagentes **siempre
  están disponibles** vía `use_subagents` (habilitado por defecto, se desactiva en Settings →
  Features → Agent) [2], por lo que el modo paralelo es la norma y el secuencial es solo el caso de
  tener Auto-Approve desactivado y rechazar cada lanzamiento.

`[?] OQ-CLINE-002: la documentación no especifica si `use_skill` admite parámetros (p. ej. un
argumento con el nombre de la skill) o si el modelo solo lo invoca implícitamente al detectar la
coincidencia. Esto afecta a scripts que quieran activar skills desde código en lugar del chat.`

`[?] OQ-CLINE-003: no hay tope numérico documentado de subagentes concurrentes ni presupuesto de
tokens por subagente; queda a criterio del modelo principal.`

## Fuentes

- [1] Cline — **Skills** — https://docs.cline.bot/customization/skills (consulta 2026-10-05)
- [2] Cline — **Subagents** — https://docs.cline.bot/features/subagents (consulta 2026-10-05)
- [3] Cline — **Tools** — https://docs.cline.bot/tools-reference/all-cline-tools (consulta 2026-10-05)
- [4] Cline — **Auto Approve & YOLO Mode** — https://docs.cline.bot/features/auto-approve (consulta 2026-10-05)
- [5] Cline — **Using Commands** — https://docs.cline.bot/core-workflows/using-commands (consulta 2026-10-05)
- [6] Cline — **Config / Storage locations** — https://docs.cline.bot/getting-started/config (consulta 2026-10-05)