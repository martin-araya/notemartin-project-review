import { registerAs } from '@nestjs/config';

/** Namespace 'redis' para ConfigModule (trampa E06). */
export default registerAs('redis', () => ({
  url: process.env.REDIS_URL ?? 'redis://localhost:6379',
}));