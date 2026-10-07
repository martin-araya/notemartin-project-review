import { Injectable, Logger } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';

import { MessageQueueService } from '../messaging/message-queue.service';

import { Order } from './entities/order.entity';

@Injectable()
export class OrdersService {
  private readonly logger = new Logger(OrdersService.name);

  constructor(
    @InjectRepository(Order)
    private readonly orders: Repository<Order>,
    private readonly queue: MessageQueueService,
  ) {}

  async create(payload: Partial<Order>): Promise<Order> {
    const entity = this.orders.create(payload);
    const saved = await this.orders.save(entity);
    await this.notifyCreated(saved);
    return saved;
  }

  async findAll(): Promise<Order[]> {
    return this.orders.find();
  }

  async findOne(id: number): Promise<Order | null> {
    return this.orders.findOne({ where: { id } });
  }

  async update(id: number, payload: Partial<Order>): Promise<Order | null> {
    await this.orders.update(id, payload);
    return this.findOne(id);
  }

  async remove(id: number): Promise<void> {
    await this.orders.delete(id);
  }

  /** Productor de la cola 'order-queue' (trampa E04). */
  async notifyCreated(order: Order): Promise<void> {
    await this.queue.publish('order-queue', { id: order.id, customer: order.customer });
  }
}