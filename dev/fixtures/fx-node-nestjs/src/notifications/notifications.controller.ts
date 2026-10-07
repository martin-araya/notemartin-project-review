import {
  Body,
  Controller,
  Get,
  Param,
  ParseIntPipe,
  Post,
} from '@nestjs/common';

import { CreateNotificationDto } from './dto/create-notification.dto';
import { Notification } from './entities/notification.entity';
import { NotificationsService } from './notifications.service';

@Controller('notifications')
export class NotificationsController {
  constructor(private readonly notifications: NotificationsService) {}

  @Get()
  async findAll(): Promise<Notification[]> {
    return this.notifications.findAll();
  }

  @Get(':id')
  async findOne(@Param('id', ParseIntPipe) id: number): Promise<Notification | null> {
    return this.notifications.findOne(id);
  }

  @Post()
  async create(@Body() dto: CreateNotificationDto): Promise<Notification> {
    return this.notifications.create(dto.eventType, dto.payload);
  }
}