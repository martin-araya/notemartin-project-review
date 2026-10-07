import { Injectable } from '@nestjs/common';

import { MessageHandler, MessageQueueService } from './message-queue.service';

/** Implementacion in-memory para tests (D-F06r-3).

Trampa P03: el productor (publish) NO verifica que haya un consumer
registrado. Si nadie se suscribe a una cola, los mensajes se pierden.
*/
@Injectable()
export class InMemoryMessageQueue extends MessageQueueService {
  private readonly handlers = new Map<string, MessageHandler[]>();

  async publish(queue: string, payload: unknown): Promise<void> {
    const queueHandlers = this.handlers.get(queue) ?? [];
    this.logger.log(`published to ${queue} (${queueHandlers.length} handler(s))`);
    for (const handler of queueHandlers) {
      await handler(payload);
    }
  }

  async subscribe(queue: string, handler: MessageHandler): Promise<void> {
    const existing = this.handlers.get(queue) ?? [];
    existing.push(handler);
    this.handlers.set(queue, existing);
    this.logger.log(`subscribed to ${queue}`);
  }

  registeredQueues(): string[] {
    return Array.from(this.handlers.keys());
  }
}