import { IsString, MaxLength } from 'class-validator';

export class CreateNotificationDto {
  @IsString()
  @MaxLength(64)
  eventType!: string;

  @IsString()
  payload!: string;
}