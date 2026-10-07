import { Injectable, Logger } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';

import { MessageQueueService } from '../messaging/message-queue.service';

import { Notification } from './entities/notification.entity';

@Injectable()
export class NotificationsService {
  private readonly logger = new Logger(NotificationsService.name);

  constructor(
    @InjectRepository(Notification)
    private readonly notifications: Repository<Notification>,
    private readonly queue: MessageQueueService,
  ) {}

  async create(eventType: string, payload: string): Promise<Notification> {
    const entity = this.notifications.create({
      eventType,
      payload,
      status: 'pending',
    });
    const saved = await this.notifications.save(entity);

    // Trampa E04: consumidor suscrito por nombre 'order-queue'.
    await this.queue.publish('order-queue', { id: saved.id, eventType });

    // Trampa P03: el productor no verifica que haya un consumer.
    saved.status = 'sent';
    return this.notifications.save(saved);
  }

  async findAll(): Promise<Notification[]> {
    return this.notifications.find();
  }

  async findOne(id: number): Promise<Notification | null> {
    return this.notifications.findOne({ where: { id } });
  }

  /** Consumidor de la cola 'order-queue' (trampa E04). */
  async processOrderNotification(payload: unknown): Promise<void> {
    this.logger.log(`processing order_notification: ${JSON.stringify(payload)}`);
  }
}