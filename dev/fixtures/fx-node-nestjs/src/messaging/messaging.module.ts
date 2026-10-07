import { Module } from '@nestjs/common';

import { BullMQMessageQueue } from './bullmq-message-queue';
import { MessageQueueService } from './message-queue.service';
import { MicroserviceController } from './microservice.controller';
import { OrderEventHandler } from './order-event.handler';

/** Modulo de mensajeria.

Trampa E05: los controllers/handlers decorados con @MessagePattern
y @EventPattern solo se registran cuando `app.connectMicroservice`
se llama en main.ts. Aqui solo declaramos el modulo NestJS estandar.
*/
@Module({
  controllers: [MicroserviceController],
  providers: [
    OrderEventHandler,
    {
      provide: MessageQueueService,
      useClass: BullMQMessageQueue,
    },
  ],
  exports: [MessageQueueService, OrderEventHandler],
})
export class MessagingModule {}