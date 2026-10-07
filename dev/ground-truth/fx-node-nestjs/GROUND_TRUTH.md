# Ground truth de fx-node-nestjs (F06r)

Backend **NestJS 10** modular con **TypeORM 0.3** + **SQLite (better-sqlite3)**,
**BullMQ 5** (con abstraccion `MessageQueueService` para tests), transporte
de microservicios con `@MessagePattern` / `@EventPattern`, decoradores
propios leidos por `Reflector`, guards e interceptors globales via
`APP_GUARD` / `APP_INTERCEPTOR`, y `ConfigModule` con namespaces
validado por Joi. Plantada para que la skill tenga que rastrear
las trampas clasicas del ecosistema NestJS.

## Features

1. **ordenes** (FEAT-001): crear, listar, obtener, actualizar,
   eliminar via DRF + DB. 7 R-NN.
2. **envios** (FEAT-002): crear, marcar shipped/delivered, listar,
   obtener. 7 R-NN.
3. **notificaciones** (FEAT-003): crear, listar, obtener;
   publica a BullMQ por nombre de cola. 7 R-NN.

## Trampas del ecosistema (CC-06)

1. `modules_di_decorators`: cada `@Module({imports, providers,
   controllers})` define el grafo DI. NestJS detecta ciclos con
   `forwardRef`.
2. `app_guard_app_interceptor`: `APP_GUARD`, `APP_INTERCEPTOR`,
   `APP_FILTER` registrados via providers en app.module.ts.
3. `custom_decorator_reflector`: `@Roles`, `@LogExecutionTime`,
   `@CurrentUser` con `SetMetadata` y `Reflector.get`.
4. `bullmq_producer_consumer_by_name`: productor publica
   (`orders.orders.service.ts`, `notifications.notifications.service.ts`)
   y consumidor se suscribe por nombre de cola `'order-queue'`.
5. `event_pattern_message_pattern`: `@MessagePattern('order_created')`
   y `@EventPattern('order_created')` requieren
   `app.connectMicroservice`.
6. `config_module_namespaces`: `registerAs('database'|'redis'|'app')`
   con `ConfigType<...>` + Joi validation schema.

## Decisiones tecnicas (ver DECISIONS.md D-239..D-247)

- D-239: Node 22 + TypeScript 5.6 + NestJS 10.4 + TypeORM 0.3.20 +
  BullMQ 5.21 + better-sqlite3 9.6 + supertest 7 + Jest 29 + ts-jest 29.
- D-240: Apps en ingles (`orders`, `shipments`, `notifications`)
  para CCCCC-11.
- D-241: Abstraccion `MessageQueueService` interface con
  `BullMQMessageQueue` (real) y `InMemoryMessageQueue` (tests).
- D-242: `npm install --legacy-peer-deps` para resolver conflictos
  de peer dep con `better-sqlite3`.
- D-243: Prefijo `NPRGT-FXNEST-` para 26 unique tokens.
- D-244: `Makefile` envuelve `npm test -- --colors=false --runInBand`.
- D-245: Imagen Docker `node:22-bookworm-slim` con `make` +
  `python3` + `build-essential` para el native build de
  better-sqlite3.
- D-246: `requires: [linux, macos, windows]`.
- D-247: Deteccion extendida de NestJS/TypeORM/BullMQ en
  `fixtures_matrix.py` y `target_matrix.yml`.

## Archivos clave del fixture

- `manifest.yml`, `Makefile`, `Dockerfile.test`, `README.md`,
  `build-history.sh`, `unique_tokens.txt`.
- `package.json`: NestJS 10 + TypeORM 0.3 + BullMQ 5 + better-sqlite3
  + Jest 29 + supertest 7.
- `tsconfig.json`: ES2022 + experimentalDecorators +
  emitDecoratorMetadata.
- `nest-cli.json`: `sourceRoot: src`.
- `jest.config.js`: ts-jest preset.
- `pytest.ini`: `asyncio_mode = auto` (no aplica aqui, es JS).
- `.env.test`: `NODE_ENV=test`, `DATABASE_URL=:memory:`.
- `conftest.ts`: `tests/conftest.ts` con env vars para tests.
- `src/main.ts`: bootstrap + `connectMicroservice`.
- `src/app.module.ts`: imports + providers con APP_GUARD/
  APP_INTERCEPTOR/APP_FILTER.
- `src/config/`: `database`, `redis`, `app` configs + Joi schema.
- `src/common/`: guards, interceptors, decorators, filters.
- `src/orders/`, `src/shipments/`, `src/notifications/`: las 3
  features con entities, services, controllers, modules.
- `src/messaging/`: `MessageQueueService` interface +
  `BullMQMessageQueue` + `InMemoryMessageQueue` +
  microservice handlers.
- `src/health/`: `health.controller.ts` con dead `/health/deep`.