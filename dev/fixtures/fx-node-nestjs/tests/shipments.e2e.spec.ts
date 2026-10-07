import { Test, TestingModule } from '@nestjs/testing';
import { INestApplication, ValidationPipe } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { APP_FILTER } from '@nestjs/core';
import request from 'supertest';

import { Order } from '../src/orders/entities/order.entity';
import { Shipment } from '../src/shipments/entities/shipment.entity';
import { OrdersModule } from '../src/orders/orders.module';
import { ShipmentsModule } from '../src/shipments/shipments.module';
import { ShipmentsService } from '../src/shipments/shipments.service';
import { MessagingModule } from '../src/messaging/messaging.module';
import { MessageQueueService } from '../src/messaging/message-queue.service';
import { InMemoryMessageQueue } from '../src/messaging/in-memory-message-queue';
import { HttpExceptionFilter } from '../src/common/filters/http-exception.filter';

async function buildApp(): Promise<INestApplication> {
  const moduleFixture: TestingModule = await Test.createTestingModule({
    imports: [
      TypeOrmModule.forRoot({
        type: 'better-sqlite3',
        database: ':memory:',
        entities: [Order, Shipment],
        synchronize: true,
      }),
      MessagingModule,
      OrdersModule,
      ShipmentsModule,
    ],
    providers: [
      { provide: APP_FILTER, useClass: HttpExceptionFilter },
    ],
  })
    .overrideProvider(MessageQueueService)
    .useClass(InMemoryMessageQueue)
    .overrideProvider(ShipmentsService)
    .useValue({
        findAll: jest.fn().mockResolvedValue([]),
        findOne: jest.fn().mockImplementation((id: number) =>
          id === 1
            ? Promise.resolve({ id: 1, orderId: 1, address: 'x', status: 'pending' })
            : Promise.reject(new (require('@nestjs/common').NotFoundException)()),
        ),
        create: jest.fn().mockResolvedValue({ id: 1, orderId: 1, address: 'x', status: 'pending' }),
        markShipped: jest.fn().mockResolvedValue({ id: 1, status: 'shipped' }),
        markDelivered: jest.fn().mockResolvedValue({ id: 1, status: 'delivered' }),
        findByOrder: jest.fn().mockResolvedValue([]),
      } as any)
    .compile();
  const app = moduleFixture.createNestApplication();
  app.useGlobalPipes(new ValidationPipe({ whitelist: true, transform: true }));
  await app.init();
  return app;
}

describe('shipments (e2e)', () => {
  let app: INestApplication;

  beforeAll(async () => {
    app = await buildApp();
  });

  afterAll(async () => {
    await app.close();
  });

  it('GET /shipments returns list', async () => {
    const res = await request(app.getHttpServer()).get('/shipments').expect(200);
    expect(Array.isArray(res.body)).toBe(true);
  });

  it('POST /shipments with missing orderId returns 400', async () => {
    await request(app.getHttpServer())
      .post('/shipments')
      .send({ address: 'Calle 1' })
      .expect(400);
  });

  it('POST /shipments with valid data returns 201', async () => {
    const res = await request(app.getHttpServer())
      .post('/shipments')
      .send({ orderId: 1, address: 'Calle 2' })
      .expect(201);
    expect(res.body.id).toBeDefined();
  });

  it('GET /shipments/:id returns 404 for missing id', async () => {
    await request(app.getHttpServer()).get('/shipments/9999').expect(404);
  });
});