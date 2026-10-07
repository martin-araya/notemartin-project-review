import {
  Column,
  CreateDateColumn,
  Entity,
  ManyToOne,
  PrimaryGeneratedColumn,
  JoinColumn,
} from 'typeorm';

import { Order } from '../../orders/entities/order.entity';

export const SHIPMENT_STATUS_PENDING = 'pending';
export const SHIPMENT_STATUS_SHIPPED = 'shipped';
export const SHIPMENT_STATUS_DELIVERED = 'delivered';

@Entity('shipments')
export class Shipment {
  @PrimaryGeneratedColumn()
  id!: number;

  @ManyToOne(() => Order)
  @JoinColumn({ name: 'orderId' })
  order!: Order;

  @Column()
  orderId!: number;

  @Column({ type: 'varchar', length: 200 })
  address!: string;

  @Column({ type: 'varchar', length: 16, default: SHIPMENT_STATUS_PENDING })
  status!: string;

  @CreateDateColumn()
  createdAt!: Date;
}