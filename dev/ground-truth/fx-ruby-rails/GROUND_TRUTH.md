# GROUND_TRUTH — fx-ruby-rails

## Vision general

Fixture Rails 7.1/7.0 con ActiveRecord, STI, concerns, callbacks, jobs Sidekiq y vistas Hotwire. Cubre el stack tipico de una aplicacion Rails empresarial pequena.

## Stack

- Ruby 3.1.x (3.2+ tiene incompatibilidades con actionview 7.0 + rspec-rails 6.x; ver decision D-279)
- Rails 7.0.8 (estable, evita el bug de ENCODING_FLAG de actionview 7.1)
- SQLite 3 con sqlite3 gem
- Sidekiq 7 con `mock_redis` en test (sin servicio externo)
- Turbo (sin ActionCable: el `turbo_stream_from` del index fue removido para no requerir ActionCable)
- RSpec 3 + Capybara (driver `rack_test`, no browser)

## Features y R-NN

| Feature | R-NN | Cubre |
|---|---|---|
| `proyectos` | 7 | CRUD, callbacks (before_save/after_destroy), Trackable, validaciones, N+1 latente en index |
| `facturas` | 7 | CRUD JSON, after_commit que encola job, includes(:proyecto) para evitar N+1, retry_on, validacion de transiciones de estado |
| `recordatorios` | 7 | STI con Email/Sms/Push, find_sti_class que silencia tipos invalidos, soft-delete via concern, update_columns en job para saltar validacion |

## Trampas plantadas (CC-04..CC-06)

### Ecosistema (6/6)
1. **E01** `config/routes.rb:2-7` — `resources` genera 7 rutas por feature sin declararlas.
2. **E02** `app/models/proyecto.rb:10-11` + `app/models/factura.rb:22` — `before_save`, `after_destroy`, `after_commit`.
3. **E03** `app/models/concerns/trackable.rb:6-9` — `included do` con `before_create`/`before_save`; Trackable se incluye en Proyecto y Factura (P03).
4. **E04** `config/initializers/legacy_constants.rb:1-30` — `module LegacyConstants::Resolver` con `define_method` y `method_missing`.
5. **E05** `app/models/recordatorio.rb:9` + `db/migrate/003_create_recordatorios.rb` — STI con columna `type`.
6. **E06** `config/initializers/patch_array.rb:1-7` — monkey patch sobre `Array#sum_safe`.

### Paquete (6/6)
1. **P01** `retry_on StandardError, wait: 5s, attempts: 2..3` en `EnviarRecordatorioJob` y `GenerarFacturaPdfJob`.
2. **P02** `EnviarRecordatorioJob#perform` usa `update_columns` para saltar la validacion `fecha_envio_no_pasada`.
3. **P03** `Trackable` se incluye en Proyecto y Factura (callback duplicado).
4. **P04** `Recordatorio.find_sti_class` devuelve `Recordatorio` base si la clase no existe.
5. **P05** `config/routes.rb:9` declara `get 'panel/legacy'` que nunca se invoca + `ProyectosController#index` N+1 en `recordatorios_pendientes`.
6. **P06** `config/initializers/legacy_constants.rb` carga antes de `patch_array.rb` sin usar `to_prepare`.

### Superficiales (3/3)
1. **S01** `app/services/legacy_text_formatter.rb` sin consumidores.
2. **S02** `app/controllers/concerns/` vacio (solo `.keep`).
3. **S03** `app/views/recordatorios/_unused_partial.html.erb` huerfano.

## Salida de la suite

65 examples RSpec passing en `ruby:3.1.6-bookworm` con `bundle exec rspec --format documentation`.

- 7 features: 4 modelos (proyecto, factura, recordatorio, tipo_recordatorio) + 2 jobs + 3 requests + 3 routing + 3 features
- 6 trampas del ecosistema verificadas leyendo el codigo
- 6 trampas del paquete verificadas (incluyendo STI con type invalido y silent_retry)
- 3 trampas superficiales verificadas (incluyendo busqueda de consumidores)

## Comandos para reproducir

```bash
docker build -f dev/fixtures/fx-ruby-rails/Dockerfile.test -t npr-fx-ruby-rails dev/fixtures/fx-ruby-rails
docker run --rm npr-fx-ruby-rails

# o via run_fixture_tests.py:
python dev/tools/run_fixture_tests.py --fixture fx-ruby-rails --container
```

## Comandos para regenerar la historia git

```bash
cd dev/fixtures/fx-ruby-rails
bash build-history.sh
```

Crea 8 commits incrementales.
