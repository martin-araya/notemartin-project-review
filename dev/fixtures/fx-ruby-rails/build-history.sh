#!/usr/bin/env bash
# Genera una historia git reproducible de 8 commits para el fixture F06v.
set -euo pipefail

cd "$(dirname "$0")"

if [ -d .git ]; then
    echo "ERROR: ya existe un repositorio git aqui; no se sobreescribe." >&2
    exit 1
fi

git init -q -b main
git config user.name "Fixture Builder"
git config user.email "fixture@local"

# Commit 1: scaffold base
cat > README.md <<'EOF'
# fx-ruby-rails (scaffold inicial)
EOF
git add -A
git commit -q -m "chore: initial scaffold (manifest, Gemfile, Dockerfile, Makefile)"

# Commit 2: config/
mkdir -p config/initializers config/environments config/locales
echo "" > config/application.rb
echo "" > config/boot.rb
echo "" > config/environment.rb
echo "" > config/database.yml
echo "" > config/routes.rb
git add -A
git commit -q -m "feat(config): add application, boot, environment, database, routes stubs"

# Commit 3: app/models/ con concerns y STI
mkdir -p app/models/concerns
echo "" > app/models/application_record.rb
echo "" > app/models/proyecto.rb
echo "" > app/models/factura.rb
echo "" > app/models/recordatorio.rb
echo "" > app/models/concerns/trackable.rb
echo "" > app/models/concerns/soft_deletable.rb
git add -A
git commit -q -m "feat(models): add Proyecto, Factura, Recordatorio (STI) and concerns"

# Commit 4: app/controllers/ + views
mkdir -p app/controllers app/views/layouts
echo "" > app/controllers/application_controller.rb
echo "" > app/controllers/proyectos_controller.rb
echo "" > app/controllers/facturas_controller.rb
echo "" > app/controllers/recordatorios_controller.rb
echo "" > app/views/layouts/application.html.erb
git add -A
git commit -q -m "feat(http): add controllers, ApplicationController and layout"

# Commit 5: app/jobs/ + services/
mkdir -p app/jobs app/services
echo "" > app/jobs/application_job.rb
echo "" > app/jobs/enviar_recordatorio_job.rb
echo "" > app/jobs/generar_factura_pdf_job.rb
echo "" > app/services/calculadora_iva.rb
git add -A
git commit -q -m "feat(jobs): add Sidekiq jobs and CalculadoraIva service"

# Commit 6: db migrations + seeds + schema
mkdir -p db/migrate
echo "" > db/migrate/001_create_proyectos.rb
echo "" > db/migrate/002_create_facturas.rb
echo "" > db/migrate/003_create_recordatorios.rb
echo "" > db/seeds.rb
git add -A
git commit -q -m "feat(db): add migrations, seeds and schema stub"

# Commit 7: spec/ + initializers con trampas
mkdir -p spec/{factories,features,models,jobs,routing,requests,traps}
echo "" > spec/spec_helper.rb
echo "" > spec/rails_helper.rb
echo "" > spec/factories/proyectos.rb
git add -A
git commit -q -m "test: add RSpec scaffold and first factory"

# Commit 8: archivos de soporte final
git add -A
git commit -q -m "chore: finalize fixture with README and docker metadata" --allow-empty

echo "Historia creada con 8 commits:"
git log --oneline
