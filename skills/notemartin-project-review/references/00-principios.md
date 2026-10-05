# Principios, reglas de evidencia y gramática de citas

> Fuente única de verdad sobre qué cuenta como afirmación válida en los reportes
> y notas de la skill `notemartin-project-review`. Este documento se cita desde
> `SKILL.md` y desde los gates y linters de la skill.

## Diagnóstico

Por qué las IAs actuales fallan al analizar repositorios reales, y qué
contramedida aplica esta skill:

- **Leen el README y extrapolan**: la documentación es una hipótesis del autor,
  no el comportamiento observado. Contramedida: Ley del README (Ley 4).
- **Muestrean unos pocos archivos**: ven el árbol y contestan sin haber leído
  todo. Contramedida: Ley de cobertura (Ley 1) y el ledger.
- **Olvidan lo leído por límite de contexto**: la conversación es volátil.
  Contramedida: Ley del disco (Ley 5) — todo hallazgo se materializa en el
  workspace antes de seguir.
- **Un solo agente intenta leer todo**: el contexto se desborda.
  Contramedida: particionado en WUs y subagentes lectores (F23, F27).
- **Confunden nombres con comportamiento**: asumen que `parse_url` parsea la URL
  porque se llama así. Contramedida: Ley de trazado (Ley 3) — una traza
  completa sin saltos, no una adivinanza.
- **No siguen indirecciones**: DI, registros, eventos, imports dinámicos.
  Contramedida: Ley de la indirección (Ley 6) — se resuelven o quedan
  etiquetadas `[?]`.
- **Resuman en vez de explicar**: enumeran secciones y agregan generalidades.
  Contramedida: Ley de no-relleno (Ley 8) y el linter `npr lint vague`.
- **Inventan con seguridad**: citan archivos o líneas que no existen.
  Contramedida: Ley de evidencia (Ley 2) — toda cita pasa por `parse_citations`.
- **No dicen lo que no saben**: rellenan huecos con hedging.
  Contramedida: Ley del desconocido (Ley 7) — registro explícito en
  `state/openq.jsonl`.

## Las 8 leyes

### Ley 1 — Cobertura

**Regla**: ningún archivo no excluido del repo analizado queda sin leer; toda
exclusión tiene una razón escrita en `state/classification.json`.

**Cumplida por**: `npr gate coverage` (F62) — falla si hay archivos no
clasificados. Y por `npr recon` (F25), que ejecuta el inventario y la
clasificación inicial.

### Ley 2 — Evidencia

**Regla**: toda afirmación no trivial lleva una etiqueta `[V]`, `[D]`, `[I]` o
`[?]`. Las etiquetas `[V]` y `[D]` llevan además una cita con la gramática de
§"Gramática de citas".

**Cumplida por**: `npr claims check` (F61) — recorre las notas y reportes,
exige etiqueta y cita para cada afirmación; falla con código 2 si falta.

### Ley 3 — Trazado

**Regla**: una feature no se considera explicada hasta tener al menos una
traza completa sin saltos desde el disparador hasta el efecto, y el paquete
completo de 13 artefactos definido en §7 de AGENTS.

**Cumplida por**: `npr lint flow` (F31) — verifica que cada traza cubra
disparador → … → efecto con cita por salto. Y `npr gate features` (F62),
que exige el paquete completo antes de aceptar la feature.

### Ley 4 — README

**Regla**: la documentación del repo (README, comentarios, docs/) es hipótesis;
el código es la verdad. Las contradicciones entre documentación y
comportamiento observado se reportan explícitamente.

**Cumplida por**: `npr claims check` (F61) y el verificador independiente
`npr verify apply` (F63), que re-ejecuta el análisis con contexto limpio y
contrasta las afirmaciones con el código.

### Ley 5 — Disco

**Regla**: el contexto de la conversación no es memoria persistente; todo
hallazgo se escribe en el workspace (`.project-review/`) antes de continuar, y
los subagentes devuelven sus resultados en archivos, no en la conversación.

**Cumplida por**: el protocolo de subagentes de F27 (contrato de retorno con
archivos escritos) y `npr resume` (F76), que serializa el estado del
workspace para reanudar entre sesiones.

### Ley 6 — Indirección

**Regla**: las indirecciones (inyección de dependencias, registro de handlers,
bus de eventos, import dinámico, reflexión, string-dispatch) se resuelven
explícitamente trazando el destino o quedan marcadas como `[?] OQ-NNN` con
lo intentado.

**Cumplida por**: `npr recon` (F25) marca las indirecciones detectadas, y
`npr claims check` (F61) exige que cada destino esté resuelto o etiquetado.

### Ley 7 — Desconocido

**Regla**: lo que no se sabe va al registro de preguntas abiertas
(`state/openq.jsonl`) con la pregunta, lo que se intentó, la hipótesis y qué
haría falta para resolverlo. Nunca se rellena el hueco con conjetura.

**Cumplida por**: `npr openq` (F65) — comandos `add`, `list`, `resolve`,
`close`. Y el gate `all` falla si hay `[?]` sin `OQ-NNN` correspondiente.

### Ley 8 — No-relleno

**Regla**: prohibidas las enumeraciones truncadas ("etc.", "entre otros", "y
más", "...") y el hedging sin etiqueta ("parece", "tal vez", "probablemente")
aplicado a una afirmación no trivial. `N/A` solo con razón explícita.

**Cumplida por**: `npr lint vague` (F64) — detecta las frases prohibidas y
exige reemplazo por etiqueta o por cita.

## Etiquetas

| Etiqueta | Significado | Requisito adicional |
|---|---|---|
| `[V]` | verificado leyendo código | cita `[@path:linea]` o `[@path:ini-fin]` o `[@path:ini-fin#simbolo]` |
| `[D]` | observado ejecutando (análisis dinámico) | cita `[@dyn:<id-de-log>]` |
| `[I]` | inferido | debe incluir "porque …" o "razón: …" |
| `[?]` | desconocido | enlazar a una pregunta abierta `OQ-NNN` registrada en `state/openq.jsonl` |

## Gramática de citas

BNF simplificado:

```
citation     := "[@" ( range_symbol | range | line | git | dyn ) "]"
range_symbol := path ":" ini "-" fin "#" symbol
range        := path ":" ini "-" fin
line         := path ":" linea
git          := "git:" sha
dyn          := "dyn:" dyn_id
path         := [A-Za-z0-9_./-]+
ini, fin     := [0-9]+
linea        := [0-9]+
symbol       := [A-Za-z_] [A-Za-z0-9_.]*
sha          := [0-9a-f]{7,40}
dyn_id       := [A-Za-z0-9_-]+
```

Notas operativas:

- Las rutas son relativas a la raíz del repo; el separador es `/`. No se admite
  `./` inicial (se normaliza quitándolo).
- `fin >= ini`. Si `fin < ini`, la cita es inválida y `parse_citations` la
  ignora.
- Para líneas únicas se prefiere el patrón `line` (`[@path:42]`); usar `range`
  con `ini == fin` solo cuando se quiera enfatizar el rango.
- El SHA se acepta en mayúsculas y se normaliza a minúsculas.
- Las 5 formas se reconocen por orden de especificidad:
  `range_symbol` → `range` → `line` → `git` → `dyn`. La implementación vive
  en `scripts/npr/citations.py` y se importa como `parse_citations(text)`.

## Ejemplos válidos

```valido
[@src/cli.py:1]
[@src/cli.py:10]
[@src/cli.py:10-25]
[@src/cli.py:10-25#main]
[@src/cli.py:10-25#parse_args]
[@src/orchestrator/wu.ts:42-42#dispatch]
[@docs/guide.md:1-100]
[@src/parser/regex.py:7-7#TOKEN_DIVISOR]
[@src/util/strings.py:1-50#normalize]
[@src/legacy/old_api.py:1-200#Deprecated.run]
[@git:abc1234]
[@git:0123456789abcdef0123456789abcdef01234567]
[@dyn:trace-001]
[@dyn:pytest-run-42]
```

## Ejemplos inválidos

```invalido
[src/cli.py:10]                 // falta el @
[@src/cli.py:10-]               // rango incompleto
[@src/cli.py:10 25]             // falta guion entre ini y fin
[@src/cli.py:abc]               // linea no numerica
[@git:XYZ1234]                  // SHA no es hex
[@dyn:]                         // id vacio
[@src/cli.py:25-10]             // rango invertido
[@/ruta/abs/foo:1-5]           // ruta absoluta del desarrollador
[@src/cli.py:1-2#]              // symbol vacio
[@src/cli.py:1-2#1foo]          // symbol no puede empezar con digito
[@src/cli.py:1-2#sim bólico]    // simbol con espacio
```