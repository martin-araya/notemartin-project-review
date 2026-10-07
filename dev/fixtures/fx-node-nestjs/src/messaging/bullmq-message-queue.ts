import { Injectable, Logger } from '@nestjs/common';
import { Queue as BullQueue, Worker } from 'bullmq';
import IORedis from 'ioredis';

import { MessageHandler, MessageQueueService } from './message-queue.service';

/** Implementacion real con BullMQ para produccion (requiere Redis). */
@Injectable()
export class BullMQMessageQueue extends MessageQueueService {
  private readonly redis: IORedis;
  private readonly queues = new Map<string, BullQueue>();
  private readonly workers = new Map<string, Worker>();
  private readonly handlers = new Map<string, MessageHandler>();

  constructor() {
    super();
    const redisUrl = process.env.REDIS_URL ?? 'redis://localhost:6379';
    this.redis = new IORedis(redisUrl, { lazyConnect: true });
  }

  async publish(queueName: string, payload: unknown): Promise<void> {
    const q = this.getOrCreateQueue(queueName);
    await q.add('msg', payload);
    this.logger.log(`published to ${queueName}`);
  }

  async subscribe(queueName: string, handler: MessageHandler): Promise<void> {
    this.handlers.set(queueName, handler);
    const worker = new Worker(queueName, async (job) => handler(job.data), {
      connection: this.redis,
    });
    this.workers.set(queueName, worker);
    this.getOrCreateQueue(queueName);
    this.logger.log(`subscribed to ${queueName}`);
  }

  registeredQueues(): string[] {
    return Array.from(this.queues.keys());
  }

  private getOrCreateQueue(name: string): BullQueue {
    let q = this.queues.get(name);
    if (!q) {
      q = new BullQueue(name, { connection: this.redis });
      this.queues.set(name, q);
    }
    return q;
  }
}