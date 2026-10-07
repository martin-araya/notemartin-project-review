import { IsNumber, IsString, MaxLength, Min, MinLength } from 'class-validator';

export class CreateOrderDto {
  @IsString()
  @MinLength(1)
  @MaxLength(200)
  customer!: string;

  @IsNumber({ maxDecimalPlaces: 2 })
  @Min(0)
  total!: number;
}