# Fixture F06r — fx-node-nestjs

Backend **NestJS 10** modular con **TypeORM 0.3** + **SQLite**,
  **BullMQ 5** (con abstraccion `MessageQueueService` para tests),
  transporte de microservicios con `@MessagePattern` / `@EventPattern`,
  decoradores propios leidos por `Reflector`, guards e interceptors
  globales via `APP_GUARD` / `APP_INTERCEPTOR`, y `ConfigModule`
  con namespaces. Plantada para que la skill tenga que rastrear las
  trampas clasicas del ecosistema NestJS.

## Stack

- **Lenguaje:** TypeScript 5.6 (target ES2022).
- **Framework:** NestJS 10.4.
- **DB:** TypeORM 0.3 + better-sqlite3.
- **Async:** BullMQ 5 (abstraido por `MessageQueueService`).
- **Tests:** Jest 29 + supertest 7 + ts-jest 29.

## Como se ejecutan los tests

```bash
make test           # npm test -- --colors=false --runInBand
make build          # npm run build
make history        # regenera la historia git (8 commits)
```

En contenedor (Node 22 + make):

```bash
python dev/tools/run_fixture_tests.py --fixture fx-node-nestjs --container
```

## Estructura

- `src/main.ts`: `NestFactory.create(AppModule)` +
  `connectMicroservice(...)` (trampa E05 + P06).
- `src/app.module.ts`: imports [Orders, Shipments, Notifications,
  Messaging, ConfigModule]; providers `[{provide: APP_GUARD, ...},
  {provide: APP_INTERCEPTOR, ...}]` (trampa E02).
- `src/config/`: `database.config.ts`, `redis.config.ts`,
  `app.config.ts` con `registerAs(...)` + Joi validation
  schema (trampa E06).
- `src/common/`: guards, interceptors, decorators, filters.
- `src/orders/`, `src/shipments/`, `src/notifications/`: las 3
  features con entities, services, controllers, modules
  (trampas E01 con ciclo OrdersModule <-> ShipmentsModule).
- `src/messaging/`: `MessageQueueService` interface +
  `BullMQMessageQueue` + `InMemoryMessageQueue` +
  `microservice.controller.ts` con `@MessagePattern` (E05).
- `src/health/`: `health.controller.ts` con dead `/health/deep`
  (trampa S01).

## Features

1. **ordenes** (FEAT-001): crear, listar, obtener, actualizar,
   eliminar. 7 R-NN.
2. **envios** (FEAT-002): crear, marcar shipped, marcar
   delivered, listar por order. 7 R-NN.
3. **notificaciones** (FEAT-003): crear, listar, verificar
   dispatch via BullMQ. 7 R-NN.

## Trampas plantadas

- 6 del ecosistema (CC-06): modulos con `@Module`,
  APP_GUARD/APP_INTERCEPTOR, decoradores con Reflector,
  BullMQ productor/consumidor por nombre de cola,
  @MessagePattern/@EventPattern, ConfigModule namespaces.
- 6 del paquete (CC-04): ciclo OrdersModule<->ShipmentsModule,
  guard que lanza 500 en vez de 401, productor sin verificar
  consumer, interceptor que rompe streaming, typo en
  SetMetadata key, microservice transport no conectado.
- 3 superficiales (CC-05): dead /health/deep, dead
  WebSocketGateway, dead MetricsInterceptor.