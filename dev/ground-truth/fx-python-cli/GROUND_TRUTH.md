# Ground Truth — `fx-python-cli`

Fixture F06a. Documento legible por humanos del `ground_truth.json` adyacente.

## Vision general

`fxnotes` es una CLI en Python (stdlib + `tomllib` + `sqlite3`) que almacena notas
locales en SQLite. Soporta 4 comandos: `add`, `list`, `delete`, `export`. Las
features, superficies y trampas estan descritas abajo.

## Entry points

| ID | Archivo | Linea | Funcion | Tipo |
|---|---|---|---|---|
| EP-cli | `src/fxnotes/cli.py` | 28 | `main` | script |
| EP-mod | `src/fxnotes/__main__.py` | 4 | `main` | module |

## Modulos

| ID | Path | Resumen |
|---|---|---|
| MOD-cli | `src/fxnotes/cli.py` | argparse + dispatch table |
| MOD-config | `src/fxnotes/config.py` | TOML + env config loader |
| MOD-db | `src/fxnotes/db.py` | SQLite wrapper with retry |
| MOD-events | `src/fxnotes/events.py` | In-process event bus |
| MOD-plugins | `src/fxnotes/plugins/loader.py` | Dynamic plugin loader (importlib) |
| MOD-legacy | `src/fxnotes/legacy_v1.py` | Dead v1 API (phantom) |

## Dependencias

Todas stdlib: `tomllib`, `sqlite3`, `argparse`, `importlib.metadata`.

## Features

### FEAT-001 — `add`

Trazas (citas `archivo:linea-linea#simbolo`):

1. `src/fxnotes/commands/add.py:18-23#add_parser` — parse argv.
2. `src/fxnotes/cli.py:28-39#main` — load_config y connect DB.
3. `src/fxnotes/commands/add.py:26-34#run` — validate key and value.
4. `src/fxnotes/commands/add.py:36-39#run` — SELECT existing.
5. `src/fxnotes/commands/add.py:40-43#run` — INSERT row.
6. `src/fxnotes/commands/add.py:45-46#run` — emit note_added.

Decisiones: DP-001 (key empty), DP-002 (key too long), DP-003 (existe), DP-004 (IntegrityError).

Resultados (R-NN): R-01 success, R-02 key vacio, R-03 key muy larga, R-04 duplicado, R-05 value muy largo, R-06 race condition.

### FEAT-002 — `list`

Trazas:
1. `src/fxnotes/commands/list_cmd.py:18-23#add_parser` — parse argv.
2. `src/fxnotes/commands/list_cmd.py:26-39#run` — build SQL.
3. `src/fxnotes/commands/list_cmd.py:41-43#run` — execute SELECT.
4. `src/fxnotes/commands/list_cmd.py:45-51#run` — format and emit.

Decisiones: DP-005 (include-deleted), DP-006 (--tag), DP-007 (catch DB error → swallow).

Resultados: R-01 vacio, R-02 success, R-03 filtrado, R-04 ordenado, R-05 sort invalido, R-06 silent_success (catch vacio).

### FEAT-003 — `delete`

Trazas:
1. `src/fxnotes/commands/delete.py:19-28#add_parser` — parse argv.
2. `src/fxnotes/commands/delete.py:42-45#run` — validate key.
3. `src/fxnotes/commands/delete.py:47-49#run` — check --archived (dead branch).
4. `src/fxnotes/commands/delete.py:51-54#run` — verify key exists.
5. `src/fxnotes/commands/delete.py:56-60#run` — confirm interactively if needed.
6. `src/fxnotes/commands/delete.py:62-63#run` — decide permanent.
7. `src/fxnotes/commands/delete.py:65-72#run` — DELETE o UPDATE row.

Decisiones: DP-008 key empty, DP-009 --archived (deprecated), DP-010 existe, DP-011 confirm ask + not --yes, DP-012 user rejects, DP-013 permanent.

Resultados: R-01 success soft, R-02 not found, R-03 key empty, R-04 --archived (no-op), R-05 success permanent (solo con confirm=False + --no-undo), R-06 cancelled (solo con confirm=ask + user rejects).

### FEAT-004 — `export`

Trazas:
1. `src/fxnotes/commands/export.py:13-18#add_parser` — parse argv.
2. `src/fxnotes/commands/export.py:23-30#run` — SELECT notes.
3. `src/fxnotes/commands/export.py:32-43#run` — format payload.

Decisiones: DP-014 (csv vs json), DP-015 (stdout vs file).

Resultados: R-01 json a file, R-02 csv, R-03 json stdout, R-04 vacio, R-05 formato invalido, R-06 DB error.

## Superficies

| ID | Kind | Nombre | Handler |
|---|---|---|---|
| SRF-cli-add | cli | `fxnotes add` | `src/fxnotes/commands/add.py:run` |
| SRF-cli-list | cli | `fxnotes list` | `src/fxnotes/commands/list_cmd.py:run` |
| SRF-cli-delete | cli | `fxnotes delete` | `src/fxnotes/commands/delete.py:run` |
| SRF-cli-export | cli | `fxnotes export` | `src/fxnotes/commands/export.py:run` |
| SRF-event-bus | event | eventos internos | `src/fxnotes/events.py:emit` |

## Config

| Clave | Kind | Default | Efecto |
|---|---|---|---|
| db_path | file | ~/.local/share/fxnotes/notes.db | ruta SQLite |
| confirm | env/file | ask | prompt interactivo |
| soft_delete | env/file | true | marca deleted=1 en lugar de borrar |
| max_key_len | env/file | 64 | limite de tamano de clave |
| max_value_len | env/file | 4096 | limite de tamano de valor |
| list_default_sort | env/file | created_at | ORDER BY por defecto |
| debounce_ms | env/file | 100 | reservado (no usado) |
| DEAD_CODE | feature_flag | true | importa fxnotes.legacy_v1 (modulo fantasma) |

## Trampas superficiales (≥ 3)

| ID | Kind | Ubicacion | Resumen |
|---|---|---|---|
| TRAP-S01 | dead_code | `src/fxnotes/legacy_v1.py:14-29` | `old_add/old_list/old_delete` parecen activos pero nadie los llama. |
| TRAP-S02 | dynamic_import | `src/fxnotes/plugins/loader.py:18-26` | Descubrimiento via `importlib.metadata.entry_points`. |
| TRAP-S03 | string_dispatch | `src/fxnotes/commands/__init__.py:12-17` | `COMMANDS` es un dict que mapea nombre → modulo. |
| TRAP-S04 | event_bus | `src/fxnotes/events.py:16-28` | Bus de eventos in-process; los listeners se registran fuera del paquete. |
| TRAP-S05 | readme_mismatch | `README.md:9-11` | README afirma que `delete` es sincrono y limpia el flag, pero el codigo deja el flag permanentemente. |
| TRAP-S06 | feature_flag_phantom | `src/fxnotes/config.py:60-64` | `DEAD_CODE=true` importa `legacy_v1`; si se pone false, el modulo deja de importarse. |

## Trampas del paquete por feature (6 requeridas)

| ID | Feature | Kind | Ubicacion | Resolucion |
|---|---|---|---|---|
| TRAP-P01 | FEAT-003 | combination_two_settings | `delete.py:62-63` | "deleted permanently" solo aparece con `confirm=False AND --no-undo`. |
| TRAP-P02 | FEAT-002 | empty_catch_swallows_error | `list_cmd.py:42-44` | Catch vacio convierte DB error en "0 entries." sin error. |
| TRAP-P03 | FEAT-001 | timeout_retry | `db.py:50-58` | `Database.execute` reintenta 3 veces con backoff si `OperationalError` menciona "locked". |
| TRAP-P04 | FEAT-001 | race_condition | `add.py:36-43` | SELECT-then-INSERT; dos inserts con misma key → uno gana, otro `lost race`. |
| TRAP-P05 | FEAT-003 | dead_branch | `delete.py:47-49` | `--archived` se acepta pero el handler imprime "deprecated" y retorna 0 sin tocar la BD. |
| TRAP-P06 | FEAT-003 | user_rejection | `delete.py:56-60` | Con `confirm=ask`, si el usuario responde `n` → `CancelledError`. |

## Estados y telemetria

- Estados de la entidad principal (notes): `absent` (no row), `present` (deleted=0), `soft_deleted` (deleted=1).
- Eventos: `note_added`, `note_listed`, `note_deleted` (con `soft` bool).

## Tests del fixture

`pytest tests/` corre 24 tests cubriendo todos los R-NN de las 4 features.