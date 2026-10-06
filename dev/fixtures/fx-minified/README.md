# Fixture template — notemartin-project-review (F06a2)

Este directorio es la **plantilla** para crear nuevos fixtures de la skill. **No edites
archivos aqui**; copialos a `dev/fixtures/fx-<nombre>/` y adáptalos.

## Como crear un nuevo fixture

1. Copia esta carpeta: `cp -R dev/fixtures/_template dev/fixtures/fx-mi-fixture`
2. Renombra el campo `name` en `manifest.yml`.
3. Implementa el codigo del fixture en `src/`.
4. Llena `unique_tokens.txt` con al menos 20 identificadores, strings o rutas
   exclusivos del fixture (clases, mensajes de error, slugs de modos, claves i18n).
5. Llena el ground truth en `ground-truth/ground_truth.json` siguiendo el esquema.
6. Si necesitas una historia git reproducible, ejecuta `./build-history.sh`.
7. Anota el fixture en `dev/fixtures/target_matrix.yml` si cubre un nuevo lenguaje,
   framework o sistema de build.

## Archivos clave

- `manifest.yml` — metadata del fixture (nombre, plataformas soportadas, comando de test,
  contenedor opcional).
- `Makefile` — targets estandar (`test`, `lint`, `history`, `clean`, `help`).
- `Dockerfile.test` — imagen para ejecutar el fixture en CI/contenedor.
- `build-history.sh` — script que crea una historia git de 8 commits.
- `unique_tokens.txt` — tokens unicos para `overfit_guard.py`.
- `ground-truth/ground_truth.json.example` — esqueleto minimo valido para
  `check_ground_truth.py`.
