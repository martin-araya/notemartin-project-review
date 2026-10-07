import { Controller, Get } from '@nestjs/common';

@Controller('health')
export class HealthController {
  /** Endpoint dead (trampa S01): NINGUN test lo invoca. */
  @Get('/deep')
  deepHealth(): { status: string } {
    return { status: 'ok' };
  }

  @Get()
  health(): { status: string } {
    return { status: 'ok' };
  }
}