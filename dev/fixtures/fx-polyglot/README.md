# Fixture fx-polyglot (F06f)

Pipeline poliglota: Go + Rust + Bash comunicandose por stdin/stdout con JSON.

## Componentes

- `src/ingesta/` — programa Go que lee lineas de stdin (`id|ts|raw`) y emite
  JSON con campos `{id, ts, raw, tag}` (o `{id, ts_raw, body}` con `-tags legacy`).
- `src/transformacion/` — programa Rust con features (`v1`, `v2`, `strict`,
  `legacy_compat`) que transforma el JSON.
- `orchestrator.sh` — orquestador bash con `set -euo pipefail`, `trap`, eleccion
  de binario segun `uname`, y exit codes como protocolo.
- `src/reporte/lib.sh` — helpers bash usados por el orquestador.

## Trampas plantadas

1. **Contrato JSON implicito** - campos opcionales distintos en cada lado:
   ingesta emite `{id, ts, raw, tag}` (current) o `{id, ts_raw, body}` (legacy);
   transformacion espera `{id, raw}` en v1 y `{id, payload}` en v2.
2. **`//go:build` tags** - `src/ingesta/handlers_legacy.go` solo se compila
   con `-tags legacy` y produce JSON con campos distintos.
3. **Cargo features** - `Cargo.toml` define `v1`, `v2`, `strict`, `legacy_compat`;
   cada combinacion cambia el formato del JSON.
4. **Orquestador bash con `set -euo pipefail`, `trap`, `uname`** - el caso
   de `uname` elige el binario de transformacion; `trap cleanup EXIT` corre
   al final incluso si el script aborta.
5. **Exit codes como protocolo** - exit 0 = ok, 2 = empty line, 3 = malformed,
   4 = unknown tag, 64 = strict rejected, 8 = JSON malformed, 9 = no feature,
   10 = unsupported OS, 11 = jq failed.
6. **`init()` de Go registra handlers** - `src/ingesta/registry.go` define un
   `func init()` que rellena un map global; el handler lookup ocurre en `main.go`
   sin mostrar la inicializacion.

## Construir

```bash
make build
```

## Probar

```bash
make test
```

Los bats tests viven en `tests/*.bats`.