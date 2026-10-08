# Matriz de cobertura de fixtures

Generada por `dev/tools/fixtures_matrix.py` a partir de `dev/fixtures/target_matrix.yml` y de los fixtures presentes en `dev/fixtures/`.

## Fixtures detectados
- `fx-angular-ngrx`
- `fx-c-embedded`
- `fx-cpp-cmake`
- `fx-cpp-qt`
- `fx-csharp-aspnet`
- `fx-csharp-wpf`
- `fx-dbt-airflow`
- `fx-electron`
- `fx-flutter-dart`
- `fx-go-service`
- `fx-java-micronaut`
- `fx-kotlin-android`
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
- `fx-python-ml`
- `fx-react-native`
- `fx-react-spa`
- `fx-ruby-rails`
- `fx-rust-axum`
- `fx-spring-boot`
- `fx-sql-oracle-plsql`
- `fx-sql-postgres`
- `fx-sql-tsql`
- `fx-sveltekit`
- `fx-swift-ios`
- `fx-swift-server`
- `fx-ts-agent-extension`
- `fx-vanilla-js-legacy`
- `fx-vue-nuxt`
- `fxec-uart-protocol.h; 2>`
- `fxproc`

## Eje: languages

| Item | Estado | Cubierto por |
|---|---|---|
| `python` | cubierto | fx-c-embedded, fx-cpp-qt, fx-dbt-airflow, fx-minified, fx-python-cli, fx-python-django, fx-python-fastapi, fx-python-ml, fx-swift-ios |
| `typescript` | cubierto | fx-angular-ngrx, fx-electron, fx-minified, fx-monorepo, fx-nextjs-fullstack, fx-node-nestjs, fx-react-native, fx-react-spa, fx-sveltekit, fx-swift-server, fx-ts-agent-extension, fx-vue-nuxt |
| `javascript` | cubierto | fx-angular-ngrx, fx-electron, fx-minified, fx-monorepo, fx-nextjs-fullstack, fx-node-nestjs, fx-react-native, fx-react-spa, fx-sveltekit, fx-swift-server, fx-ts-agent-extension, fx-vanilla-js-legacy, fx-vue-nuxt |
| `java` | cubierto | fx-java-micronaut, fx-minified, fx-spring-boot |
| `kotlin` | cubierto | fx-flutter-dart, fx-java-micronaut, fx-kotlin-android, fx-kotlin-ktor, fx-react-native |
| `go` | cubierto | fx-go-service, fx-minified, fx-polyglot |
| `rust` | cubierto | fx-polyglot, fx-rust-axum |
| `shell` | cubierto | fx-angular-ngrx, fx-c-embedded, fx-cpp-cmake, fx-cpp-qt, fx-csharp-aspnet, fx-csharp-wpf, fx-dbt-airflow, fx-electron, fx-flutter-dart, fx-go-service, fx-java-micronaut, fx-kotlin-android, fx-kotlin-ktor, fx-minified, fx-monorepo, fx-nextjs-fullstack, fx-node-nestjs, fx-php-laravel, fx-polyglot, fx-python-cli, fx-python-django, fx-python-fastapi, fx-python-ml, fx-react-native, fx-react-spa, fx-ruby-rails, fx-rust-axum, fx-spring-boot, fx-sql-oracle-plsql, fx-sql-postgres, fx-sql-tsql, fx-sveltekit, fx-swift-ios, fx-swift-server, fx-ts-agent-extension, fx-vanilla-js-legacy, fx-vue-nuxt |
| `dart` | cubierto | fx-flutter-dart |
| `swift` | cubierto | fx-flutter-dart, fx-react-native, fx-swift-ios, fx-swift-server |
| `csharp` | cubierto | fx-csharp-aspnet, fx-csharp-wpf |
| `ruby` | cubierto | fx-ruby-rails |
| `elixir` | **falta** | _(ninguno)_ |
| `php` | cubierto | fx-php-laravel |
| `cpp` | cubierto | fx-c-embedded, fx-cpp-cmake, fx-cpp-qt, fx-swift-ios, fx-vanilla-js-legacy, fx-vue-nuxt |
| `c` | cubierto | fx-c-embedded, fx-cpp-cmake, fx-cpp-qt, fx-swift-ios |

## Eje: frameworks

| Item | Estado | Cubierto por |
|---|---|---|
| `vscode-extension` | cubierto | fx-ts-agent-extension |
| `angular` | cubierto | fx-angular-ngrx, fx-monorepo |
| `micronaut` | cubierto | fx-java-micronaut |
| `node-express` | cubierto | fx-node-nestjs, fx-vanilla-js-legacy |
| `pnpm-monorepo` | cubierto | fx-monorepo |
| `electron` | cubierto | fx-electron |
| `gradle` | cubierto | fx-java-micronaut, fx-kotlin-android, fx-kotlin-ktor |
| `maven` | cubierto | fx-spring-boot |
| `cargo` | cubierto | fx-polyglot, fx-rust-axum |
| `go-modules` | cubierto | fx-go-service, fx-minified, fx-polyglot |
| `react-spa` | cubierto | fx-nextjs-fullstack, fx-react-native, fx-react-spa, fx-sveltekit |
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
| `pytest-django` | cubierto | fx-python-django, fx-python-fastapi, fx-python-ml |
| `fastapi` | cubierto | fx-python-fastapi, fx-python-ml |
| `pydantic` | cubierto | fx-python-fastapi, fx-python-ml |
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
| `cmake` | cubierto | fx-cpp-cmake, fx-cpp-qt, fx-vanilla-js-legacy, fx-vue-nuxt |
| `ctest` | **falta** | _(ninguno)_ |
| `gtest` | **falta** | _(ninguno)_ |
| `dlopen` | cubierto | fx-cpp-cmake |
| `unity` | cubierto | fx-c-embedded |
| `linker-script` | cubierto | fx-c-embedded |
| `qt6` | cubierto | fx-cpp-qt |
| `qml` | cubierto | fx-cpp-qt |
| `qt-test` | cubierto | fx-cpp-qt |
| `swiftui` | cubierto | fx-swift-ios |
| `uikit` | cubierto | fx-flutter-dart, fx-swift-ios |
| `widgetkit` | cubierto | fx-swift-ios |
| `app-groups` | cubierto | fx-swift-ios |
| `xcode-project` | cubierto | fx-swift-ios |
| `combine` | cubierto | fx-swift-ios |
| `vapor` | cubierto | fx-swift-server |
| `fluent` | cubierto | fx-swift-server |
| `swift-argument-parser` | cubierto | fx-swift-server |
| `swift-syntax` | cubierto | fx-swift-server |
| `swift-macro` | cubierto | fx-swift-server |
| `spm-build-tool-plugin` | cubierto | fx-swift-server |
| `android` | cubierto | fx-kotlin-android |
| `jetpack-compose` | cubierto | fx-kotlin-android |
| `hilt` | cubierto | fx-kotlin-android |
| `hilt-android` | cubierto | fx-kotlin-android |
| `hilt-work` | **falta** | _(ninguno)_ |
| `hilt-navigation-compose` | **falta** | _(ninguno)_ |
| `room` | **falta** | _(ninguno)_ |
| `workmanager` | cubierto | fx-kotlin-android |
| `navigation-compose` | cubierto | fx-kotlin-android |
| `view-binding` | cubierto | fx-kotlin-android |
| `gradle-flavors` | cubierto | fx-kotlin-android |
| `robolectric` | cubierto | fx-kotlin-android |
| `appcompat` | cubierto | fx-kotlin-android |
| `flutter` | cubierto | fx-flutter-dart |
| `flutter-riverpod` | cubierto | fx-flutter-dart |
| `go-router` | cubierto | fx-flutter-dart |
| `freezed` | cubierto | fx-flutter-dart |
| `json-serializable` | cubierto | fx-flutter-dart |
| `riverpod-generator` | cubierto | fx-flutter-dart |
| `build-runner` | cubierto | fx-flutter-dart |
| `platform-channels` | cubierto | fx-flutter-dart |
| `dart-define` | cubierto | fx-flutter-dart |
| `adaptive-widgets` | cubierto | fx-flutter-dart |
| `react-native` | cubierto | fx-react-native |
| `expo-bare` | cubierto | fx-react-native |
| `react-navigation` | cubierto | fx-react-native |
| `redux-toolkit` | cubierto | fx-react-native, fx-react-spa |
| `turbo-modules` | **falta** | _(ninguno)_ |
| `expo-config-plugins` | cubierto | fx-react-native |
| `expo-linking` | cubierto | fx-react-native |
| `expo-notifications` | cubierto | fx-react-native |
| `expo-build-properties` | cubierto | fx-react-native |
| `expo-splash-screen` | cubierto | fx-react-native |
| `metro` | **falta** | _(ninguno)_ |
| `electron-context-bridge` | **falta** | _(ninguno)_ |
| `electron-builder` | cubierto | fx-electron |
| `electron-asar-unpack` | cubierto | fx-electron |
| `electron-extra-resources` | cubierto | fx-electron |
| `electron-utility-process` | cubierto | fx-electron |
| `electron-app-scheme` | cubierto | fx-electron |
| `electron-auto-updater` | cubierto | fx-electron |
| `wpf` | cubierto | fx-csharp-wpf |
| `xaml` | cubierto | fx-csharp-wpf |
| `mvvm` | cubierto | fx-csharp-wpf |
| `community-toolkit-mvvm` | cubierto | fx-csharp-wpf |
| `data-template` | cubierto | fx-csharp-wpf |
| `value-converter` | cubierto | fx-csharp-wpf |
| `merged-dictionary` | cubierto | fx-csharp-wpf |
| `style-trigger` | cubierto | fx-csharp-wpf |
| `xunit` | cubierto | fx-csharp-wpf |
| `postgresql` | cubierto | fx-go-service, fx-java-micronaut, fx-rust-axum, fx-spring-boot, fx-sql-oracle-plsql, fx-sql-postgres, fx-sql-tsql |
| `flyway` | **falta** | _(ninguno)_ |
| `pl-pgsql` | cubierto | fx-sql-postgres |
| `pg-cron` | cubierto | fx-sql-postgres |
| `pgtap` | cubierto | fx-sql-postgres |
| `row-level-security` | cubierto | fx-sql-postgres |
| `trigger` | cubierto | fx-sql-oracle-plsql, fx-sql-postgres, fx-sql-tsql |
| `materialized-view` | cubierto | fx-sql-postgres |
| `sql-dynamic` | cubierto | fx-sql-postgres |
| `cascade-constraint` | cubierto | fx-sql-postgres |
| `oracle` | cubierto | fx-sql-oracle-plsql |
| `liquibase` | **falta** | _(ninguno)_ |
| `pl-sql` | cubierto | fx-sql-oracle-plsql |
| `utplsql` | cubierto | fx-sql-oracle-plsql |
| `dbms-scheduler` | cubierto | fx-sql-oracle-plsql |
| `db-link` | cubierto | fx-sql-oracle-plsql |
| `autonomous-transaction` | cubierto | fx-sql-oracle-plsql |
| `instead-of` | cubierto | fx-sql-oracle-plsql, fx-sql-tsql |
| `synonym` | cubierto | fx-sql-oracle-plsql, fx-sql-tsql |
| `execute-immediate` | cubierto | fx-sql-oracle-plsql |
| `sqlserver` | **falta** | _(ninguno)_ |
| `tsql` | **falta** | _(ninguno)_ |
| `sqlcmd` | **falta** | _(ninguno)_ |
| `sp_executesql` | **falta** | _(ninguno)_ |
| `merge-output` | **falta** | _(ninguno)_ |
| `after-trigger` | **falta** | _(ninguno)_ |
| `recursive-cte` | **falta** | _(ninguno)_ |
| `temp-tables` | **falta** | _(ninguno)_ |
| `sql-agent` | **falta** | _(ninguno)_ |
| `dbt` | cubierto | fx-dbt-airflow |
| `dbt-duckdb` | cubierto | fx-dbt-airflow |
| `duckdb` | cubierto | fx-dbt-airflow |
| `airflow` | cubierto | fx-dbt-airflow |
| `dag-factory` | cubierto | fx-dbt-airflow |
| `xcom` | cubierto | fx-dbt-airflow |
| `jinja-macros` | cubierto | fx-dbt-airflow |
| `dbt-lineage` | cubierto | fx-dbt-airflow |
| `ref-source` | cubierto | fx-dbt-airflow |
| `is_incremental` | cubierto | fx-dbt-airflow |
| `dbt-materialization-config` | cubierto | fx-dbt-airflow |
| `dbt-models` | cubierto | fx-dbt-airflow |
| `apache-airflow` | cubierto | fx-dbt-airflow |
| `hydra` | cubierto | fx-python-ml |
| `dvc` | cubierto | fx-python-ml |
| `mlflow` | cubierto | fx-python-ml |
| `notebook-ipynb` | cubierto | fx-python-ml |
| `jupyter` | cubierto | fx-python-ml |
| `nbval` | cubierto | fx-python-ml |
| `dvc-yaml` | cubierto | fx-python-ml |
| `hydra-config` | cubierto | fx-python-ml |
| `mlflow-file-store` | cubierto | fx-python-ml |
| `scikit-learn` | cubierto | fx-python-ml |
| `pytorch` | **falta** | _(ninguno)_ |

## Eje: build_systems

| Item | Estado | Cubierto por |
|---|---|---|
| `pyproject` | cubierto | fx-angular-ngrx, fx-python-cli, fx-python-fastapi, fx-python-ml |
| `pnpm` | cubierto | fx-monorepo |
| `maven` | cubierto | fx-spring-boot |
| `gradle` | cubierto | fx-java-micronaut, fx-kotlin-android, fx-kotlin-ktor |
| `cargo` | cubierto | fx-polyglot, fx-rust-axum |
| `go-modules` | cubierto | fx-go-service, fx-minified, fx-polyglot |
| `make` | cubierto | fx-angular-ngrx, fx-c-embedded, fx-cpp-cmake, fx-cpp-qt, fx-csharp-aspnet, fx-csharp-wpf, fx-dbt-airflow, fx-electron, fx-flutter-dart, fx-go-service, fx-java-micronaut, fx-kotlin-android, fx-kotlin-ktor, fx-minified, fx-monorepo, fx-nextjs-fullstack, fx-node-nestjs, fx-php-laravel, fx-polyglot, fx-python-django, fx-python-fastapi, fx-python-ml, fx-react-native, fx-react-spa, fx-ruby-rails, fx-rust-axum, fx-spring-boot, fx-sql-oracle-plsql, fx-sql-postgres, fx-sql-tsql, fx-sveltekit, fx-swift-ios, fx-swift-server, fx-ts-agent-extension, fx-vanilla-js-legacy, fx-vue-nuxt |
| `docker` | **falta** | _(ninguno)_ |
| `gulp` | cubierto | fx-angular-ngrx, fx-vanilla-js-legacy |
| `msbuild` | cubierto | fx-csharp-aspnet, fx-csharp-wpf |
| `pip` | cubierto | fx-dbt-airflow, fx-python-django, fx-python-fastapi, fx-python-ml |
| `composer` | cubierto | fx-php-laravel |
| `bundler` | cubierto | fx-ruby-rails |
| `cmake` | **falta** | _(ninguno)_ |
| `gnu-ld` | cubierto | fx-c-embedded |
| `qt-cmake` | cubierto | fx-cpp-qt |
| `swiftpm` | cubierto | fx-swift-ios, fx-swift-server |
| `xcodebuild` | cubierto | fx-swift-ios |

## Eje: file_kinds

| Item | Estado | Cubierto por |
|---|---|---|
| `source-text` | cubierto | fx-angular-ngrx, fx-c-embedded, fx-cpp-cmake, fx-cpp-qt, fx-csharp-aspnet, fx-csharp-wpf, fx-dbt-airflow, fx-electron, fx-flutter-dart, fx-go-service, fx-java-micronaut, fx-kotlin-android, fx-kotlin-ktor, fx-minified, fx-monorepo, fx-nextjs-fullstack, fx-node-nestjs, fx-php-laravel, fx-polyglot, fx-python-cli, fx-python-django, fx-python-fastapi, fx-python-ml, fx-react-native, fx-react-spa, fx-ruby-rails, fx-rust-axum, fx-spring-boot, fx-sql-oracle-plsql, fx-sql-postgres, fx-sql-tsql, fx-sveltekit, fx-swift-ios, fx-swift-server, fx-ts-agent-extension, fx-vanilla-js-legacy, fx-vue-nuxt |
| `minified-js` | cubierto | fx-minified, fx-vanilla-js-legacy |
| `bundle-with-sourcemap` | cubierto | fx-minified |
| `bundle-without-sourcemap` | **falta** | _(ninguno)_ |
| `asar` | cubierto | fx-minified |
| `pyc` | cubierto | fx-minified |
| `notebook-ipynb` | cubierto | fx-python-ml |
| `xml-declarative` | cubierto | fx-cpp-qt, fx-csharp-wpf, fx-java-micronaut, fx-kotlin-android, fx-php-laravel, fx-react-native, fx-spring-boot, fx-sql-oracle-plsql |
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

