import { Module, forwardRef } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';

import { MessagingModule } from '../messaging/messaging.module';
import { ShipmentsModule } from '../shipments/shipments.module';

import { Order } from './entities/order.entity';
import { OrdersController } from './orders.controller';
import { OrdersService } from './orders.service';

/** OrdersModule (trampa E01 + P01: ciclo con ShipmentsModule).

Trampa P01: importa ShipmentsModule (con forwardRef) para usar
ShipmentsService. ShipmentsModule no importa OrdersModule para
romper el ciclo a nivel de TypeScript. La trampa sigue siendo util
como ejemplo de como NestJS maneja la DI por decorators.
*/
@Module({
  imports: [
    TypeOrmModule.forFeature([Order]),
    forwardRef(() => ShipmentsModule),
    MessagingModule,
  ],
  controllers: [OrdersController],
  providers: [OrdersService],
  exports: [OrdersService],
})
export class OrdersModule {}