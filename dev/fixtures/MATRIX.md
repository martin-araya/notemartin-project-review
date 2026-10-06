# Matriz de cobertura de fixtures

Generada por `dev/tools/fixtures_matrix.py` a partir de `dev/fixtures/target_matrix.yml` y de los fixtures presentes en `dev/fixtures/`.

## Fixtures detectados
- `fx-java-micronaut`
- `fx-minified`
- `fx-monorepo`
- `fx-nextjs-fullstack`
- `fx-polyglot`
- `fx-python-cli`
- `fx-react-spa`
- `fx-ts-agent-extension`
- `fx-vanilla-js-legacy`

## Eje: languages

| Item | Estado | Cubierto por |
|---|---|---|
| `python` | cubierto | fx-minified, fx-python-cli |
| `typescript` | cubierto | fx-minified, fx-monorepo, fx-nextjs-fullstack, fx-react-spa, fx-ts-agent-extension |
| `javascript` | cubierto | fx-minified, fx-monorepo, fx-nextjs-fullstack, fx-react-spa, fx-ts-agent-extension, fx-vanilla-js-legacy |
| `java` | cubierto | fx-java-micronaut, fx-minified |
| `kotlin` | cubierto | fx-java-micronaut |
| `go` | cubierto | fx-minified, fx-polyglot |
| `rust` | cubierto | fx-polyglot |
| `shell` | cubierto | fx-java-micronaut, fx-minified, fx-monorepo, fx-nextjs-fullstack, fx-polyglot, fx-python-cli, fx-react-spa, fx-ts-agent-extension, fx-vanilla-js-legacy |
| `dart` | **falta** | _(ninguno)_ |
| `swift` | **falta** | _(ninguno)_ |
| `csharp` | **falta** | _(ninguno)_ |
| `ruby` | **falta** | _(ninguno)_ |
| `elixir` | **falta** | _(ninguno)_ |

## Eje: frameworks

| Item | Estado | Cubierto por |
|---|---|---|
| `vscode-extension` | cubierto | fx-ts-agent-extension |
| `angular` | cubierto | fx-monorepo |
| `micronaut` | cubierto | fx-java-micronaut |
| `node-express` | cubierto | fx-vanilla-js-legacy |
| `pnpm-monorepo` | cubierto | fx-monorepo |
| `electron` | **falta** | _(ninguno)_ |
| `gradle` | cubierto | fx-java-micronaut |
| `maven` | **falta** | _(ninguno)_ |
| `cargo` | cubierto | fx-polyglot |
| `go-modules` | cubierto | fx-minified, fx-polyglot |
| `react-spa` | cubierto | fx-nextjs-fullstack, fx-react-spa |
| `vue-spa` | **falta** | _(ninguno)_ |
| `nextjs` | cubierto | fx-nextjs-fullstack |
| `svelte-spa` | **falta** | _(ninguno)_ |
| `prisma` | cubierto | fx-nextjs-fullstack |
| `jquery` | cubierto | fx-vanilla-js-legacy |

## Eje: build_systems

| Item | Estado | Cubierto por |
|---|---|---|
| `pyproject` | cubierto | fx-python-cli |
| `pnpm` | cubierto | fx-monorepo |
| `maven` | **falta** | _(ninguno)_ |
| `gradle` | cubierto | fx-java-micronaut |
| `cargo` | cubierto | fx-polyglot |
| `go-modules` | cubierto | fx-minified, fx-polyglot |
| `make` | cubierto | fx-java-micronaut, fx-minified, fx-monorepo, fx-nextjs-fullstack, fx-polyglot, fx-react-spa, fx-ts-agent-extension, fx-vanilla-js-legacy |
| `docker` | **falta** | _(ninguno)_ |
| `gulp` | cubierto | fx-vanilla-js-legacy |

## Eje: file_kinds

| Item | Estado | Cubierto por |
|---|---|---|
| `source-text` | cubierto | fx-java-micronaut, fx-minified, fx-monorepo, fx-nextjs-fullstack, fx-polyglot, fx-python-cli, fx-react-spa, fx-ts-agent-extension, fx-vanilla-js-legacy |
| `minified-js` | cubierto | fx-minified, fx-vanilla-js-legacy |
| `bundle-with-sourcemap` | cubierto | fx-minified |
| `bundle-without-sourcemap` | **falta** | _(ninguno)_ |
| `asar` | cubierto | fx-minified |
| `pyc` | cubierto | fx-minified |
| `notebook-ipynb` | **falta** | _(ninguno)_ |
| `xml-declarative` | cubierto | fx-java-micronaut |
| `yaml-scene` | **falta** | _(ninguno)_ |
| `binary` | **falta** | _(ninguno)_ |

## Eje: containers

| Item | Estado | Cubierto por |
|---|---|---|
| `asar` | cubierto | fx-minified |
| `jar` | cubierto | fx-minified |
| `zip` | **falta** | _(ninguno)_ |
| `apk` | **falta** | _(ninguno)_ |
| `vsix` | **falta** | _(ninguno)_ |
| `whl` | **falta** | _(ninguno)_ |
| `egg` | **falta** | _(ninguno)_ |

## Trampas minimas por fixture

- Superficiales: 3
- De paquete: 6

