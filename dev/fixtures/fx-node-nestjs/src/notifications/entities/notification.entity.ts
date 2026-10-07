import {
  Column,
  CreateDateColumn,
  Entity,
  PrimaryGeneratedColumn,
} from 'typeorm';

export const NOTIFICATION_STATUS_PENDING = 'pending';
export const NOTIFICATION_STATUS_SENT = 'sent';
export const NOTIFICATION_STATUS_FAILED = 'failed';

@Entity('notifications')
export class Notification {
  @PrimaryGeneratedColumn()
  id!: number;

  @Column({ type: 'varchar', length: 64 })
  eventType!: string;

  @Column({ type: 'text' })
  payload!: string;

  @Column({ type: 'varchar', length: 16, default: NOTIFICATION_STATUS_PENDING })
  status!: string;

  @CreateDateColumn()
  createdAt!: Date;
}