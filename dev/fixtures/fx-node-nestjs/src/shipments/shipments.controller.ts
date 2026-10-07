import {
  Body,
  Controller,
  Get,
  Param,
  ParseIntPipe,
  Post,
} from '@nestjs/common';

import { CreateShipmentDto } from './dto/create-shipment.dto';
import { Shipment } from './entities/shipment.entity';
import { ShipmentsService } from './shipments.service';

@Controller('shipments')
export class ShipmentsController {
  constructor(private readonly shipments: ShipmentsService) {}

  @Get()
  async findAll(): Promise<Shipment[]> {
    return this.shipments.findAll();
  }

  @Get(':id')
  async findOne(@Param('id', ParseIntPipe) id: number): Promise<Shipment | null> {
    return this.shipments.findOne(id);
  }

  @Post()
  async create(@Body() dto: CreateShipmentDto): Promise<Shipment> {
    return this.shipments.create(dto.orderId, dto.address);
  }

  @Post(':id/ship')
  async markShipped(@Param('id', ParseIntPipe) id: number): Promise<Shipment | null> {
    return this.shipments.markShipped(id);
  }

  @Post(':id/deliver')
  async markDelivered(
    @Param('id', ParseIntPipe) id: number,
  ): Promise<Shipment | null> {
    return this.shipments.markDelivered(id);
  }
}