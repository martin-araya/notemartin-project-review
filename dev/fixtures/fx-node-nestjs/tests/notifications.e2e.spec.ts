import { Test, TestingModule } from '@nestjs/testing';
import { INestApplication, ValidationPipe } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { APP_FILTER } from '@nestjs/core';
import request from 'supertest';

import { Order } from '../src/orders/entities/order.entity';
import { Notification } from '../src/notifications/entities/notification.entity';
import { OrdersModule } from '../src/orders/orders.module';
import { ShipmentsModule } from '../src/shipments/shipments.module';
import { NotificationsModule } from '../src/notifications/notifications.module';
import { NotificationsService } from '../src/notifications/notifications.service';
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
        entities: [Order, Notification],
        synchronize: true,
      }),
      MessagingModule,
      OrdersModule,
      ShipmentsModule,
      NotificationsModule,
    ],
    providers: [
      { provide: APP_FILTER, useClass: HttpExceptionFilter },
    ],
  })
    .overrideProvider(MessageQueueService)
    .useClass(InMemoryMessageQueue)
    .overrideProvider(NotificationsService)
    .useValue({
        findAll: jest.fn().mockResolvedValue([]),
        findOne: jest.fn().mockImplementation((id: number) =>
          id === 1
            ? Promise.resolve({ id: 1, eventType: 'user.created', payload: '{}', status: 'sent' })
            : Promise.reject(new (require('@nestjs/common').NotFoundException)()),
        ),
        create: jest.fn().mockResolvedValue({ id: 1, eventType: 'user.created', payload: '{}', status: 'sent' }),
        processOrderNotification: jest.fn().mockResolvedValue(undefined),
      } as any)
    .compile();
  const app = moduleFixture.createNestApplication();
  app.useGlobalPipes(new ValidationPipe({ whitelist: true, transform: true }));
  await app.init();
  return app;
}

describe('notifications (e2e)', () => {
  let app: INestApplication;

  beforeAll(async () => {
    app = await buildApp();
  });

  afterAll(async () => {
    await app.close();
  });

  it('POST /notifications creates a notification', async () => {
    const res = await request(app.getHttpServer())
      .post('/notifications')
      .send({ eventType: 'user.created', payload: '{"id":1}' })
      .expect(201);
    expect(res.body.id).toBeDefined();
  });

  it('GET /notifications returns list', async () => {
    const res = await request(app.getHttpServer()).get('/notifications').expect(200);
    expect(Array.isArray(res.body)).toBe(true);
  });

  it('GET /notifications/:id returns 404 for missing id', async () => {
    await request(app.getHttpServer()).get('/notifications/9999').expect(404);
  });

  it('POST /notifications with missing eventType returns 400', async () => {
    await request(app.getHttpServer())
      .post('/notifications')
      .send({ payload: 'x' })
      .expect(400);
  });
});