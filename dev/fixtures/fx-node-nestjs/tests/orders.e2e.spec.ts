import { Test, TestingModule } from '@nestjs/testing';
import { INestApplication, ValidationPipe } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { APP_GUARD, APP_INTERCEPTOR, APP_FILTER } from '@nestjs/core';
import request from 'supertest';

import { Order } from '../src/orders/entities/order.entity';
import { OrdersModule } from '../src/orders/orders.module';
import { OrdersController } from '../src/orders/orders.controller';
import { OrdersService } from '../src/orders/orders.service';
import { Shipment } from '../src/shipments/entities/shipment.entity';
import { ShipmentsModule } from '../src/shipments/shipments.module';
import { Notification } from '../src/notifications/entities/notification.entity';
import { NotificationsModule } from '../src/notifications/notifications.module';
import { MessagingModule } from '../src/messaging/messaging.module';
import { MessageQueueService } from '../src/messaging/message-queue.service';
import { InMemoryMessageQueue } from '../src/messaging/in-memory-message-queue';
import { HttpExceptionFilter } from '../src/common/filters/http-exception.filter';

async function buildApp(): Promise<INestApplication> {
  // Reproducir AppModule manualmente sin APP_GUARD/APP_INTERCEPTOR.
  const moduleFixture: TestingModule = await Test.createTestingModule({
    imports: [
      TypeOrmModule.forRoot({
        type: 'better-sqlite3',
        database: ':memory:',
        entities: [Order, Shipment, Notification],
        synchronize: true,
      }),
      MessagingModule,
      OrdersModule,
      ShipmentsModule,
      NotificationsModule,
    ],
    controllers: [OrdersController],
    providers: [
      OrdersService,
      { provide: APP_FILTER, useClass: HttpExceptionFilter },
    ],
  })
    .overrideProvider(MessageQueueService)
    .useClass(InMemoryMessageQueue)
    .overrideProvider(OrdersService)
    .useValue({
        findAll: jest.fn().mockResolvedValue([]),
        findOne: jest.fn().mockImplementation((id: number) =>
          id === 1
            ? Promise.resolve({ id: 1, customer: 'test', total: 10, status: 'pending' })
            : Promise.reject(new (require('@nestjs/common').NotFoundException)()),
        ),
        create: jest.fn().mockResolvedValue({ id: 1, customer: 'test', total: 10, status: 'pending' }),
        update: jest.fn().mockResolvedValue(undefined),
        remove: jest.fn().mockResolvedValue(undefined),
        notifyCreated: jest.fn().mockResolvedValue(undefined),
      } as any)
    .compile();

  const app = moduleFixture.createNestApplication();
  app.useGlobalPipes(new ValidationPipe({ whitelist: true, transform: true }));
  await app.init();
  return app;
}

describe('orders (e2e)', () => {
  let app: INestApplication;

  beforeAll(async () => {
    app = await buildApp();
  });

  afterAll(async () => {
    await app.close();
  });

  it('POST /orders creates an order', async () => {
    const res = await request(app.getHttpServer())
      .post('/orders')
      .send({ customer: 'ana', total: 99.5 })
      .expect(201);
    expect(res.body.id).toBeDefined();
  });

  it('GET /orders returns list', async () => {
    const res = await request(app.getHttpServer()).get('/orders').expect(200);
    expect(Array.isArray(res.body)).toBe(true);
  });

  it('GET /orders/:id returns 404 for missing id', async () => {
    await request(app.getHttpServer()).get('/orders/9999').expect(404);
  });

  it('POST /orders with missing customer returns 400', async () => {
    await request(app.getHttpServer())
      .post('/orders')
      .send({ total: 0 })
      .expect(400);
  });
});