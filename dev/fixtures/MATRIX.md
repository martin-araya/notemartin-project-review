# Matriz de cobertura de fixtures

Generada por `dev/tools/fixtures_matrix.py` a partir de `dev/fixtures/target_matrix.yml` y de los fixtures presentes en `dev/fixtures/`.

## Fixtures detectados
- `fx-angular-ngrx`
- `fx-cpp-cmake`
- `fx-csharp-aspnet`
- `fx-go-service`
- `fx-java-micronaut`
- `fx-kotlin-ktor`
- `fx-minified`
- `fx-monorepo`
- `fx-nextjs-fullstack`
- `fx-node-nestjs`
- `fx-php-laravel`
- `fx-polyglot`
- `fx-python-cli`
- `fx-python-django`
- `fx-python-fastapi`
- `fx-react-spa`
- `fx-ruby-rails`
- `fx-rust-axum`
- `fx-spring-boot`
- `fx-sveltekit`
- `fx-ts-agent-extension`
- `fx-vanilla-js-legacy`
- `fx-vue-nuxt`
- `fxproc`

## Eje: languages

| Item | Estado | Cubierto por |
|---|---|---|
| `python` | cubierto | fx-minified, fx-python-cli, fx-python-django, fx-python-fastapi |
| `typescript` | cubierto | fx-angular-ngrx, fx-minified, fx-monorepo, fx-nextjs-fullstack, fx-node-nestjs, fx-react-spa, fx-sveltekit, fx-ts-agent-extension, fx-vue-nuxt |
| `javascript` | cubierto | fx-angular-ngrx, fx-minified, fx-monorepo, fx-nextjs-fullstack, fx-node-nestjs, fx-react-spa, fx-sveltekit, fx-ts-agent-extension, fx-vanilla-js-legacy, fx-vue-nuxt |
| `java` | cubierto | fx-java-micronaut, fx-minified, fx-spring-boot |
| `kotlin` | cubierto | fx-java-micronaut, fx-kotlin-ktor |
| `go` | cubierto | fx-go-service, fx-minified, fx-polyglot |
| `rust` | cubierto | fx-polyglot, fx-rust-axum |
| `shell` | cubierto | fx-angular-ngrx, fx-cpp-cmake, fx-csharp-aspnet, fx-go-service, fx-java-micronaut, fx-kotlin-ktor, fx-minified, fx-monorepo, fx-nextjs-fullstack, fx-node-nestjs, fx-php-laravel, fx-polyglot, fx-python-cli, fx-python-django, fx-python-fastapi, fx-react-spa, fx-ruby-rails, fx-rust-axum, fx-spring-boot, fx-sveltekit, fx-ts-agent-extension, fx-vanilla-js-legacy, fx-vue-nuxt |
| `dart` | **falta** | _(ninguno)_ |
| `swift` | **falta** | _(ninguno)_ |
| `csharp` | cubierto | fx-csharp-aspnet |
| `ruby` | cubierto | fx-ruby-rails |
| `elixir` | **falta** | _(ninguno)_ |
| `php` | cubierto | fx-php-laravel |
| `cpp` | cubierto | fx-cpp-cmake, fx-vanilla-js-legacy, fx-vue-nuxt |

## Eje: frameworks

| Item | Estado | Cubierto por |
|---|---|---|
| `vscode-extension` | cubierto | fx-ts-agent-extension |
| `angular` | cubierto | fx-angular-ngrx, fx-monorepo |
| `micronaut` | cubierto | fx-java-micronaut |
| `node-express` | cubierto | fx-node-nestjs, fx-vanilla-js-legacy |
| `pnpm-monorepo` | cubierto | fx-monorepo |
| `electron` | **falta** | _(ninguno)_ |
| `gradle` | cubierto | fx-java-micronaut, fx-kotlin-ktor |
| `maven` | cubierto | fx-spring-boot |
| `cargo` | cubierto | fx-polyglot, fx-rust-axum |
| `go-modules` | cubierto | fx-go-service, fx-minified, fx-polyglot |
| `react-spa` | cubierto | fx-nextjs-fullstack, fx-react-spa, fx-sveltekit |
| `vue-spa` | cubierto | fx-vue-nuxt |
| `nextjs` | cubierto | fx-nextjs-fullstack |
| `svelte-spa` | cubierto | fx-sveltekit |
| `sveltekit` | cubierto | fx-sveltekit |
| `prisma` | cubierto | fx-nextjs-fullstack |
| `jquery` | cubierto | fx-vanilla-js-legacy |
| `nuxt` | cubierto | fx-vue-nuxt |
| `ngrx` | cubierto | fx-angular-ngrx |
| `angular-material` | cubierto | fx-angular-ngrx |
| `spring-boot` | cubierto | fx-spring-boot |
| `lombok` | **falta** | _(ninguno)_ |
| `ktor` | cubierto | fx-kotlin-ktor |
| `koin` | cubierto | fx-kotlin-ktor |
| `aspnet-core` | cubierto | fx-csharp-aspnet |
| `mediatr` | cubierto | fx-csharp-aspnet |
| `ef-core` | cubierto | fx-csharp-aspnet |
| `django` | cubierto | fx-python-django |
| `drf` | cubierto | fx-python-django |
| `celery` | cubierto | fx-python-django, fx-python-fastapi |
| `pytest-django` | cubierto | fx-python-django, fx-python-fastapi |
| `fastapi` | cubierto | fx-python-fastapi |
| `pydantic` | cubierto | fx-python-fastapi |
| `sqlalchemy` | cubierto | fx-python-fastapi |
| `alembic` | cubierto | fx-python-fastapi |
| `nestjs` | cubierto | fx-node-nestjs |
| `typeorm` | cubierto | fx-node-nestjs |
| `bullmq` | cubierto | fx-node-nestjs |
| `go-chi` | cubierto | fx-go-service |
| `sqlc` | cubierto | fx-go-service |
| `wire` | cubierto | fx-go-service |
| `embed` | cubierto | fx-go-service |
| `sqlite` | cubierto | fx-go-service |
| `axum` | cubierto | fx-rust-axum |
| `tokio` | cubierto | fx-rust-axum |
| `thiserror` | cubierto | fx-rust-axum |
| `laravel` | cubierto | fx-php-laravel |
| `eloquent` | cubierto | fx-php-laravel |
| `blade` | cubierto | fx-php-laravel |
| `rails` | cubierto | fx-ruby-rails |
| `hotwire` | cubierto | fx-ruby-rails |
| `sidekiq` | cubierto | fx-ruby-rails |
| `rspec` | cubierto | fx-ruby-rails |
| `cmake` | cubierto | fx-cpp-cmake, fx-vanilla-js-legacy, fx-vue-nuxt |
| `ctest` | **falta** | _(ninguno)_ |
| `gtest` | **falta** | _(ninguno)_ |
| `dlopen` | cubierto | fx-cpp-cmake |

## Eje: build_systems

| Item | Estado | Cubierto por |
|---|---|---|
| `pyproject` | cubierto | fx-angular-ngrx, fx-python-cli, fx-python-fastapi |
| `pnpm` | cubierto | fx-monorepo |
| `maven` | cubierto | fx-spring-boot |
| `gradle` | cubierto | fx-java-micronaut, fx-kotlin-ktor |
| `cargo` | cubierto | fx-polyglot, fx-rust-axum |
| `go-modules` | cubierto | fx-go-service, fx-minified, fx-polyglot |
| `make` | cubierto | fx-angular-ngrx, fx-cpp-cmake, fx-csharp-aspnet, fx-go-service, fx-java-micronaut, fx-kotlin-ktor, fx-minified, fx-monorepo, fx-nextjs-fullstack, fx-node-nestjs, fx-php-laravel, fx-polyglot, fx-python-django, fx-python-fastapi, fx-react-spa, fx-ruby-rails, fx-rust-axum, fx-spring-boot, fx-sveltekit, fx-ts-agent-extension, fx-vanilla-js-legacy, fx-vue-nuxt |
| `docker` | **falta** | _(ninguno)_ |
| `gulp` | cubierto | fx-angular-ngrx, fx-vanilla-js-legacy |
| `msbuild` | cubierto | fx-csharp-aspnet |
| `pip` | cubierto | fx-python-django, fx-python-fastapi |
| `composer` | cubierto | fx-php-laravel |
| `bundler` | cubierto | fx-ruby-rails |
| `cmake` | **falta** | _(ninguno)_ |

## Eje: file_kinds

| Item | Estado | Cubierto por |
|---|---|---|
| `source-text` | cubierto | fx-angular-ngrx, fx-cpp-cmake, fx-csharp-aspnet, fx-go-service, fx-java-micronaut, fx-kotlin-ktor, fx-minified, fx-monorepo, fx-nextjs-fullstack, fx-node-nestjs, fx-php-laravel, fx-polyglot, fx-python-cli, fx-python-django, fx-python-fastapi, fx-react-spa, fx-ruby-rails, fx-rust-axum, fx-spring-boot, fx-sveltekit, fx-ts-agent-extension, fx-vanilla-js-legacy, fx-vue-nuxt |
| `minified-js` | cubierto | fx-minified, fx-vanilla-js-legacy |
| `bundle-with-sourcemap` | cubierto | fx-minified |
| `bundle-without-sourcemap` | **falta** | _(ninguno)_ |
| `asar` | cubierto | fx-minified |
| `pyc` | cubierto | fx-minified |
| `notebook-ipynb` | **falta** | _(ninguno)_ |
| `xml-declarative` | cubierto | fx-java-micronaut, fx-php-laravel, fx-spring-boot |
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

