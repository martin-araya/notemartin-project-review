import { registerAs } from '@nestjs/config';

/** Namespace 'app' para ConfigModule (trampa E06). */
export default registerAs('app', () => ({
  port: parseInt(process.env.PORT ?? '3000', 10),
  env: process.env.NODE_ENV ?? 'development',
}));