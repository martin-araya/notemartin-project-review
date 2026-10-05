# Holdout — Especificación de fixtures reservados

Placeholder de F00. El contenido real se escribe en F82, **después** de congelar la skill con el tag
`v1.0.0-rc<N>`. AGENTS §24 prohíbe al constructor generar o leer estos fixtures.

## Estructura prevista por lote

```
generated/<lote>/
├── repo/                  # el repositorio sintético completo
├── ground_truth.json      # respuestas correctas
├── GROUND_TRUTH.md        # versión legible
└── unique_tokens.txt      # tokens que no deben aparecer en skills/
```

## Reglas

- El generador es un subagente que recibe solo este `SPEC.md`.
- El constructor no ve `generated/<lote>/`.
- Un lote se "quema" cuando su contenido influye en correcciones y deja de usarse para evaluar.
- Los reportes agregados de fallas se entregan al constructor por categoría, no por caso.