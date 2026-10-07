import { Injectable, Logger } from '@nestjs/common';
import { EventPattern } from '@nestjs/microservices';

import { MessageQueueService } from './message-queue.service';

/** Handler de eventos con @EventPattern (trampa E05).

Al igual que MicroserviceController, depende de
`app.connectMicroservice()` para ser registrado.
*/
@Injectable()
export class OrderEventHandler {
  private readonly logger = new Logger(OrderEventHandler.name);

  constructor(private readonly queue: MessageQueueService) {}

  @EventPattern('order_created')
  async handleOrderCreated(payload: unknown): Promise<void> {
    this.logger.log(`event order_created received: ${JSON.stringify(payload)}`);
    await this.queue.publish('order-queue', payload);
  }
}