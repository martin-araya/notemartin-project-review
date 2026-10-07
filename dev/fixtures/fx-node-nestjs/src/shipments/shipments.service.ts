import { Injectable, Logger } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';

import { Shipment } from './entities/shipment.entity';

@Injectable()
export class ShipmentsService {
  private readonly logger = new Logger(ShipmentsService.name);

  constructor(
    @InjectRepository(Shipment)
    private readonly shipments: Repository<Shipment>,
  ) {}

  async create(orderId: number, address: string): Promise<Shipment> {
    const entity = this.shipments.create({ orderId, address });
    return this.shipments.save(entity);
  }

  async findAll(): Promise<Shipment[]> {
    return this.shipments.find();
  }

  async findByOrder(orderId: number): Promise<Shipment[]> {
    return this.shipments.find({ where: { orderId } });
  }

  async markShipped(id: number): Promise<Shipment | null> {
    await this.shipments.update(id, { status: 'shipped' });
    return this.shipments.findOne({ where: { id } });
  }

  async markDelivered(id: number): Promise<Shipment | null> {
    await this.shipments.update(id, { status: 'delivered' });
    return this.shipments.findOne({ where: { id } });
  }

  async findOne(id: number): Promise<Shipment | null> {
    return this.shipments.findOne({ where: { id } });
  }
}