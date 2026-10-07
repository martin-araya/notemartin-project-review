import { IsInt, IsString, MaxLength, MinLength } from 'class-validator';

export class CreateShipmentDto {
  @IsInt()
  orderId!: number;

  @IsString()
  @MinLength(1)
  @MaxLength(200)
  address!: string;
}