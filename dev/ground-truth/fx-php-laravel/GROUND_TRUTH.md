# Ground Truth — F06u `fx-php-laravel`

Aplicacion Laravel 10 con Eloquent ORM, Facades, Service Providers, Events,
Observers, Jobs encolados, middleware groups, route model binding y schedule
de comandos.

## 1. Vision general

| Aspecto | Valor |
|---|---|
| Stack | PHP 8.2, Laravel 10.43, Eloquent, Blade (vista de ejemplo), PHPUnit 10, SQLite |
| Features | `inmuebles`, `visitas`, `contratos` (3 features, 7+ R-NN cada una) |
| Trampas ecosistema | 6 (Facades, magia Eloquent, providers, events/observers/listeners, middleware + route binding, schedule) |
| Trampas paquete | 6 (job retry silencioso, catch vacio, typo de facade, queue driver, N+1, middleware no usado) |
| Trampas superficiales | 3 (provider dead, helper dead, ruta dead) |
| Entry points | `artisan`, `bootstrap/app.php`, `bootstrap/providers.php`, `routes/{web,api,console}.php`, `composer.json` |
| Persistencia | SQLite en memoria (tests) con tablas `properties`, `visits`, `contracts`, `jobs` |

## 2. Features

### FEAT-001: inmuebles (Property)
CRUD sobre `App\Models\Property`. El modelo Eloquent tiene:
- `getPriceEurosAttribute()`: accessor magico que divide `price_cents / 100`.
- `scopeAvailable($query)`: scope local para filtrar `status='available'`.
- `visits()`: relacion `hasMany(Visit::class)`.
- `static::observe(PropertyObserver::class)` en boot: loguea created/updated.
- `PropertyController::index()` carga N properties sin `withCount('visits')` (trampa P05, N+1 silencioso).

### FEAT-002: visitas (Visit)
CRUD sobre `App\Models\Visit`. El controller `VisitController::store()`:
- Valida `property_id` (con `exists:properties,id`), `scheduled_at`, `visitor_email`.
- Crea el Visit.
- Llama `Pricing::calculate($property->price_cents)` (E01: facade resuelta por el contenedor).
- Dispara `event(new VisitScheduled(...))` (E04: auto-discovery desde `EventServiceProvider::$listen`).
- Encola `SendVisitReminder::dispatch(...)` (P01: `tries=3`, `backoff=10`).
- Responde 202 Accepted.

### FEAT-003: contratos (Contract)
CRUD sobre `App\Models\Contract`. El modelo tiene:
- `getMonthlyRentEurosAttribute()`: accessor magico.
- `signed_at` cast a `datetime`, `monthly_rent_cents` cast a `integer`.

El controller `ContractController::store()` encola `GenerateContractPdf::dispatch($id)`. El job tiene `catch (\Throwable)` que se traga el error y registra `Log::error` (trampa P02: el job termina "exitosamente" aunque el PDF falle).

## 3. Trampas del ecosistema

| Id | Tipo | Donde | Como detectarla |
|---|---|---|---|
| E01 | Facades | `app/Facades/PricingFacade.php` + `config/app.php` aliases | Buscar `getFacadeAccessor` y alias `'Pricing'`. |
| E02 | Magia Eloquent | `app/Models/Property.php` (accessor, scope, relacion, observer) | Buscar `getXxxAttribute`, `scopeXxx`, `xxx()` (relaciones) y `static::observe`. |
| E03 | Service Providers | `app/Providers/InmuebleServiceProvider.php` con `bind(VisitRepository)` y `singleton('pricing.service')` | Listar providers en `bootstrap/providers.php` y ver que se registra en cada uno. |
| E04 | Events + Observers + Listeners | `EventServiceProvider::$listen` + `PropertyObserver` registrado en `Property::boot` + `SendVisitConfirmation` listener | Seguir el flujo: `event()` -> listener -> job dispatched. |
| E05 | Middleware groups + Route model binding | `bootstrap/app.php` con `$middleware->appendToGroup('web', EnsureTenant::class)` + `routes/web.php` con `{property}` | Buscar `appendToGroup` y placeholders `{param}` en rutas. |
| E06 | Console + Schedule | `routes/console.php` con `Schedule::command(ExpireContracts::class)->dailyAt('00:00')` + `app/Console/Commands/ExpireContracts.php` | Leer `console.php` y listar comandos + schedules. |

## 4. Trampas del paquete

| Id | Tipo | Donde | Como detectarla |
|---|---|---|---|
| P01 | Job retry silencioso | `app/Jobs/SendVisitReminder.php`: `tries=3`, `backoff=10`, controller responde 202 sin esperar | Buscar `public int $tries` y `$backoff` en jobs. |
| P02 | Catch vacio | `app/Jobs/GenerateContractPdf.php`: `catch (\Throwable)` sin rethrow, `Log::error` y termina | Buscar `catch (\Throwable)` sin `throw` despues. |
| P03 | Facade alias typo (latente) | `config/app.php`: alias `'Pricing' => App\Facades\PricingFacade::class` | Confirmar que el namespace del alias matchea la clase real. |
| P04 | Queue driver mismatch | `phpunit.xml`: `QUEUE_CONNECTION=database` + `config/queue.php` con `database` y `redis` | Comparar la config efectiva de tests vs default. |
| P05 | N+1 silencioso | `PropertyController::index()`: `Property::query()->get()` + `$property->visits()->count()` en el map | Buscar `->count()` en relaciones dentro de un `map`/`each`. |
| P06 | Middleware registrado pero vacio | `bootstrap/app.php` con `appendToGroup('web', EnsureTenant::class)` + `EnsureTenant::handle()` que solo llama a `$next` | Buscar declaraciones de middleware con handle vacio. |

## 5. Trampas superficiales

| Id | Tipo | Donde |
|---|---|---|
| S01 | Provider dead | `app/Providers/LegacyServiceProvider.php` registrado en `bootstrap/providers.php` con `// legacy only` |
| S02 | Helper dead referenciado | `InmuebleServiceProvider::register()` bindea `'legacy.helper'` a `\App\Pricing\LegacyHelper` (clase inexistente) |
| S03 | Ruta dead | `routes/web.php`: `Route::get('/legacy', 'App\Http\Controllers\LegacyController@index')` (controller inexistente) |

## 6. Tests

- `tests/Feature/PropertyTest.php` (6 tests): create, list, show con route binding, show 404, update, validation error.
- `tests/Feature/VisitTest.php` (4 tests): create con evento + job, list, silent retry, validation 422.
- `tests/Feature/ContractTest.php` (4 tests): create con job encolado, list, show con accessor, validation error.
- `tests/Unit/PricingServiceTest.php` (2 tests): calculate, facade resolves to binding.
- `tests/Traps/TrapsEcosystemTest.php` (6 tests, uno por E01..E06).
- `tests/Traps/TrapsPackageTest.php` (6 tests, uno por P01..P06).
- `tests/Traps/TrapsSuperficialTest.php` (3 tests, uno por S01..S03).

Total estimado: ~31 tests.

## 7. Superficies (22 entradas)

Ver `ground_truth.json` -> `surfaces[]`.
