import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';

import { Shipment } from './entities/shipment.entity';
import { ShipmentsController } from './shipments.controller';
import { ShipmentsService } from './shipments.service';

/** ShipmentsModule (trampa E01).

Trampa P01: NO importa OrdersModule (rompe el ciclo a nivel de imports).
ShipmentsService no usa OrdersService directamente; la trampa se
demuestra por la estructura del grafo DI del app.module.ts.
*/
@Module({
  imports: [TypeOrmModule.forFeature([Shipment])],
  controllers: [ShipmentsController],
  providers: [ShipmentsService],
  exports: [ShipmentsService],
})
export class ShipmentsModule {}