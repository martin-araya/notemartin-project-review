import {
  Column,
  CreateDateColumn,
  Entity,
  PrimaryGeneratedColumn,
} from 'typeorm';

export const ORDER_STATUS_PENDING = 'pending';
export const ORDER_STATUS_CONFIRMED = 'confirmed';
export const ORDER_STATUS_CANCELED = 'canceled';

@Entity('orders')
export class Order {
  @PrimaryGeneratedColumn()
  id!: number;

  @Column({ type: 'varchar', length: 200 })
  customer!: string;

  @Column({ type: 'decimal', precision: 10, scale: 2, default: 0 })
  total!: number;

  @Column({ type: 'varchar', length: 16, default: ORDER_STATUS_PENDING })
  status!: string;

  @CreateDateColumn()
  createdAt!: Date;
}