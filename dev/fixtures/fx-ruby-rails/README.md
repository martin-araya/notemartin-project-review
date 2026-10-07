# fx-ruby-rails

Fixture Rails 7.1 con ActiveRecord, STI, concerns, callbacks, jobs y Hotwire.

## Stack

- Ruby 3.2
- Rails 7.1 (`config/application.rb` con `class Application < Rails::Application`)
- ActiveRecord sobre SQLite (gem `sqlite3`)
- Hotwire (`turbo-rails`, `stimulus-rails`)
- Sidekiq 7 con `mock_redis` en tests
- RSpec + Capybara (driver `rack_test`)

## Features

- `proyectos` (CRUD con `before_save` y `after_destroy`)
- `facturas` (jobs Sidekiq con retry silencioso y calculo de IVA)
- `recordatorios` (STI con `Recordatorio::Email` y `Recordatorio::Sms`)

## Comandos

```bash
make test    # bundle exec rspec
make build   # bundle install
make history # genera historia git de 8 commits (solo la primera vez)
```

## Contenedor

```bash
python dev/tools/run_fixture_tests.py --fixture fx-ruby-rails --container
```

Imagen: `ruby:3.2-bookworm` con `build-essential`, `libsqlite3-dev`, `libffi-dev`.
