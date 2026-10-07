#!/usr/bin/env bash
# Genera una historia git reproducible de 8 commits para el fixture F06r.
set -euo pipefail

cd "$(dirname "$0")"

if [ -d .git ]; then
    echo "ERROR: ya existe un repositorio git aqui; no se sobreescribe." >&2
    exit 1
fi

git init -q -b main
git config user.name "Fixture Builder"
git config user.email "fixture@local"

mkdir -p src/{config,common/{guards,interceptors,decorators,filters},orders/{entities,dto},shipments/{entities,dto},notifications/dto,messaging,health} tests

# Commit 1: scaffold
cat > .gitignore <<'EOF'
node_modules/
dist/
coverage/
*.log
.env
EOF
cat > package.json <<'EOF'
{
  "name": "fx-node-nestjs",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "build": "tsc",
    "test": "jest"
  }
}
EOF
git add -A
git commit -q -m "chore: initial scaffold (package.json, gitignore)"

# Commit 2: tsconfig + nest-cli + jest config
cat > tsconfig.json <<'EOF'
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "commonjs",
    "experimentalDecorators": true,
    "emitDecoratorMetadata": true
  }
}
EOF
cat > nest-cli.json <<'EOF'
{
  "collection": "@nestjs/schematics",
  "sourceRoot": "src"
}
EOF
cat > jest.config.js <<'EOF'
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  testRegex: 'tests/.*\\.spec\\.ts$',
  setupFiles: ['<rootDir>/tests/conftest.ts']
};
EOF
git add -A
git commit -q -m "chore(config): add tsconfig.json, nest-cli.json, jest.config.js"

# Commit 3: config module
mkdir -p src/config
for f in "database.$ext" "redis.$ext" "app.$ext" "validation.schema.$ext"; do :; done
echo "" > src/config/database.config.ts
echo "" > src/config/redis.config.ts
echo "" > src/config/app.config.ts
echo "" > src/config/validation.schema.ts
git add -A
git commit -q -m "feat(config): add database, redis, and app config namespaces + Joi schema"

# Commit 4: common (guards, interceptors, decorators)
mkdir -p src/common/{guards,interceptors,decorators,filters}
for f in auth.guard timing.interceptor roles.decorator current-user.decorator log-execution.decorator http-exception.filter; do
    echo "// placeholder" > src/common/guards/$f 2>/dev/null || true
    echo "// placeholder" > src/common/interceptors/$f 2>/dev/null || true
    echo "// placeholder" > src/common/decorators/$f 2>/dev/null || true
    echo "// placeholder" > src/common/filters/$f 2>/dev/null || true
done
# Cleanup duplicates
find src/common -name "auth.guard" -path "*/interceptors/*" -delete
find src/common -name "auth.guard" -path "*/decorators/*" -delete
find src/common -name "auth.guard" -path "*/filters/*" -delete
git add -A
git commit -q -m "feat(common): add guards, interceptors, decorators, filters (E02, E03)"

# Commit 5: messaging
mkdir -p src/messaging
echo "" > src/messaging/message-queue.service.ts
echo "" > src/messaging/bullmq-message-queue.ts
echo "" > src/messaging/in-memory-message-queue.ts
echo "" > src/messaging/microservice.controller.ts
echo "" > src/messaging/order-event.handler.ts
echo "" > src/messaging/messaging.module.ts
git add -A
git commit -q -m "feat(messaging): add MessageQueueService + BullMQ + microservice handlers (E04, E05)"

# Commit 6: orders + shipments
mkdir -p src/orders/{entities,dto} src/shipments/{entities,dto}
for f in orders.module orders.controller orders.service order.entity create-order.dto; do
    echo "// placeholder" > src/orders/$f
done
for f in shipments.module shipments.controller shipments.service shipment.entity; do
    echo "// placeholder" > src/shipments/$f
done
git add -A
git commit -q -m "feat(features): add OrdersModule and ShipmentsModule with entities (E01)"

# Commit 7: notifications + health + app.module + main
mkdir -p src/notifications/dto src/health
for f in notifications.module notifications.controller notifications.service notifications.gateway; do
    echo "// placeholder" > src/notifications/$f
done
echo "// placeholder" > src/health/health.controller.ts
echo "" > src/app.module.ts
echo "" > src/main.ts
git add -A
git commit -q -m "feat(app): add NotificationsModule, app.module, main.ts (E02, E05, P06)"

# Commit 8: tests
echo "" > tests/conftest.ts
for f in orders.e2e shipments.e2e notifications.e2e traps_ecosystem traps_package traps_superficial; do
    echo "// placeholder" > tests/${f}.spec.ts
done
git add -A
git commit -q -m "test: add Jest suite with feature and trap tests"

echo "Historia creada con 8 commits:"
git log --oneline