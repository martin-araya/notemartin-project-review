# fx-php-laravel (F06u)

Aplicacion Laravel 10 con Eloquent, Facades, Service Providers, Events,
Observers, Jobs, middleware groups, route model binding y tareas programadas.

## Stack

- PHP 8.2 (CLI)
- Laravel 10.43 (LTS)
- Eloquent ORM
- Blade (no usado activamente, queda en resources/views)
- Colas con driver `database`
- PHPUnit 10
- SQLite en memoria para tests

## Features (3, cada una con >=6 R-NN)

| Feature (ES) | Modelo | Endpoints principales |
|---|---|---|
| `inmuebles` | `Property` | `GET /api/properties`, `POST /api/properties`, `GET /properties/{property}` (route model binding) |
| `visitas`   | `Visit`    | `GET /api/visits`, `POST /api/visits` (dispara event + job) |
| `contratos` | `Contract` | `GET /api/contracts`, `POST /api/contracts` (encola PDF job) |

## Trampas del ecosistema (6)

1. **Facades** (`app/Facades/PricingFacade.php` + alias en `config/app.php`): `Pricing::calculate(...)` se resuelve por el contenedor.
2. **Magia de Eloquent** (`app/Models/Property.php`): accessor `price_euros`, scope `available`, relacion `visits()`, observer boot.
3. **Service providers** (`app/Providers/InmuebleServiceProvider.php`): bindings a interfaces (`VisitRepository -> EloquentVisitRepository`) y singleton `pricing.service`.
4. **Events + Observers + Listeners** (`app/Providers/EventServiceProvider.php` + `app/Observers/PropertyObserver.php` + `app/Listeners/SendVisitConfirmation.php`): auto-discovery de listeners.
5. **Middleware groups + route model binding** (`bootstrap/app.php` + `routes/web.php`): grupo `web` con `EnsureTenant`, `{property}` resuelve a `Property::find()`.
6. **Comandos y schedule** (`routes/console.php` + `app/Console/Commands/ExpireContracts.php`): `Schedule::command('contracts:expire')->dailyAt('00:00')`.

## Trampas del paquete (6)

1. **P01** `SendVisitReminder` con `tries=3, backoff=10`: el controller responde 202 aunque el job falle 3 veces.
2. **P02** `GenerateContractPdf` con `catch (\Throwable)` que `Log::error` y NO re-lanza.
3. **P03** Alias `Pricing` en `config/app.php` (latente: un typo en el alias rompe la facade).
4. **P04** `phpunit.xml` usa driver `database` para cola mientras `config/queue.php` declara `redis` y `database`.
5. **P05** `PropertyController::index()` carga N properties sin `withCount('visits')` (N+1 silencioso).
6. **P06** `EnsureTenant` registrado en `appendToGroup('web', ...)` pero solo una ruta lo carga via `Route::middleware(['web'])` (no todas las del grupo).

## Trampas superficiales (3)

1. **S01** `LegacyServiceProvider` registrado en `bootstrap/providers.php` con comentario `// legacy only` y nunca usado.
2. **S02** Referencia a `App\Pricing\LegacyHelper` en `InmuebleServiceProvider` sin clase real.
3. **S03** Ruta `/legacy` en `routes/web.php` apuntando a un controller inexistente.

## Comandos

```bash
make test         # corre phpunit
make build        # composer install
make dev          # php artisan serve (no usado en tests)
make history      # genera 8 commits en git (solo para dev/eval)
make clean        # elimina vendor, composer.lock y logs
```

## Test rapido

```bash
docker build -f dev/fixtures/fx-php-laravel/Dockerfile.test -t npr-fx-php-laravel dev/fixtures/fx-php-laravel
docker run --rm npr-fx-php-laravel
```

Salida esperada: `OK (X tests, Y assertions)`.
