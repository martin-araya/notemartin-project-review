import { Controller, Logger } from '@nestjs/common';
import { MessagePattern, Payload } from '@nestjs/microservices';

import { MessageQueueService } from './message-queue.service';

/** Microservice handler con @MessagePattern (trampa E05).

Trampa P06: este handler solo se registra si `app.connectMicroservice`
se llama en main.ts. Si no se llama, el handler nunca escucha.
*/
@Controller()
export class MicroserviceController {
  private readonly logger = new Logger(MicroserviceController.name);

  constructor(private readonly queue: MessageQueueService) {}

  @MessagePattern('order_created')
  async handleOrderCreated(@Payload() payload: unknown): Promise<{ received: boolean }> {
    this.logger.log('microservice received order_created');
    return { received: true };
  }
}