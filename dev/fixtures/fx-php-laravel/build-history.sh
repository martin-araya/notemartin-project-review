#!/usr/bin/env bash
# Genera una historia git reproducible de 8 commits para el fixture F06u.
set -euo pipefail

cd "$(dirname "$0")"

if [ -d .git ]; then
    echo "ERROR: ya existe un repositorio git aqui; no se sobreescribe." >&2
    exit 1
fi

git init -q -b main
git config user.name "Fixture Builder"
git config user.email "fixture@local"

# Commit 1: scaffold (composer.json, phpunit, gitignore, manifest, README, Dockerfile, Makefile)
cat > .gitignore <<'EOF'
/vendor
/node_modules
composer.lock
.phpunit.cache
.phpunit.result.cache
storage/logs/*.log
storage/framework/cache/data/*
storage/framework/sessions/*
storage/framework/views/*
.env
.env.backup
.env.production
EOF
git add -A
git commit -q -m "chore: initial scaffold (composer.json, phpunit.xml, dockerfile, manifest)"

# Commit 2: artisan + bootstrap + config
mkdir -p bootstrap config
echo "" > bootstrap/app.php
echo "" > bootstrap/providers.php
echo "" > config/app.php
echo "" > config/database.php
echo "" > config/queue.php
echo "" > config/cache.php
echo "" > config/mail.php
echo "" > config/logging.php
echo "" > config/session.php
echo "" > config/services.php
echo "" > config/view.php
echo "" > config/filesystems.php
echo "" > config/auth.php
echo "" > config/hashing.php
echo "" > artisan
git add -A
git commit -q -m "feat(bootstrap): add artisan, bootstrap/app.php, bootstrap/providers.php and config stubs"

# Commit 3: models + facades + pricing service
mkdir -p app/Models app/Facades app/Pricing app/Repositories
echo "" > app/Models/Property.php
echo "" > app/Models/Visit.php
echo "" > app/Models/Contract.php
echo "" > app/Facades/PricingFacade.php
echo "" > app/Pricing/PricingService.php
echo "" > app/Repositories/VisitRepository.php
echo "" > app/Repositories/EloquentVisitRepository.php
git add -A
git commit -q -m "feat(domain): add Eloquent models, repositories, Pricing facade and service"

# Commit 4: service providers
mkdir -p app/Providers
echo "" > app/Providers/InmuebleServiceProvider.php
echo "" > app/Providers/LegacyServiceProvider.php
echo "" > app/Providers/EventServiceProvider.php
echo "" > app/Providers/AppServiceProvider.php
echo "" > app/Providers/AuthServiceProvider.php
echo "" > app/Providers/RouteServiceProvider.php
git add -A
git commit -q -m "feat(providers): add service providers with bindings and listeners"

# Commit 5: events + observers + listeners + jobs
mkdir -p app/Events app/Listeners app/Observers app/Jobs
echo "" > app/Events/VisitScheduled.php
echo "" > app/Listeners/SendVisitConfirmation.php
echo "" > app/Observers/PropertyObserver.php
echo "" > app/Jobs/SendVisitReminder.php
echo "" > app/Jobs/GenerateContractPdf.php
git add -A
git commit -q -m "feat(events): add events, listeners, observers and queued jobs"

# Commit 6: controllers + middleware + routes + kernels
mkdir -p app/Http/Controllers app/Http/Middleware app/Http routes resources/views
echo "" > app/Http/Controllers/Controller.php
echo "" > app/Http/Controllers/PropertyController.php
echo "" > app/Http/Controllers/VisitController.php
echo "" > app/Http/Controllers/ContractController.php
echo "" > app/Http/Middleware/EnsureTenant.php
echo "" > app/Http/Middleware/EncryptCookies.php
echo "" > app/Http/Middleware/VerifyCsrfToken.php
echo "" > app/Http/Kernel.php
echo "" > routes/web.php
echo "" > routes/api.php
echo "" > routes/console.php
git add -A
git commit -q -m "feat(http): add controllers, middleware, web/api/console routes and Blade view stub"

# Commit 7: migrations + seeders + console commands
mkdir -p database/migrations database/seeders app/Console/Commands app/Console app/Exceptions
echo "" > database/migrations/2024_01_01_000001_create_properties_table.php
echo "" > database/migrations/2024_01_01_000002_create_visits_table.php
echo "" > database/migrations/2024_01_01_000003_create_contracts_table.php
echo "" > database/migrations/2024_01_01_000004_create_jobs_table.php
echo "" > database/seeders/DatabaseSeeder.php
echo "" > app/Console/Commands/ExpireContracts.php
echo "" > app/Console/Kernel.php
echo "" > app/Exceptions/Handler.php
git add -A
git commit -q -m "feat(database): add migrations, jobs table, seeder and ExpireContracts command"

# Commit 8: tests
mkdir -p tests/Feature tests/Unit tests/Traps
echo "" > tests/TestCase.php
echo "" > tests/CreatesApplication.php
echo "" > tests/Feature/PropertyTest.php
echo "" > tests/Feature/VisitTest.php
echo "" > tests/Feature/ContractTest.php
echo "" > tests/Unit/PricingServiceTest.php
echo "" > tests/Traps/TrapsEcosystemTest.php
echo "" > tests/Traps/TrapsPackageTest.php
echo "" > tests/Traps/TrapsSuperficialTest.php
git add -A
git commit -q -m "test: add PHPUnit suite with feature, unit and trap tests"

echo "Historia creada con 8 commits:"
git log --oneline
