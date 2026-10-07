import { registerAs } from '@nestjs/config';

/** Namespace 'database' para ConfigModule (trampa E06). */
export default registerAs('database', () => ({
  url: process.env.DATABASE_URL ?? ':memory:',
  type: 'better-sqlite3' as const,
  entities: [__dirname + '/../**/*.entity{.ts,.js}'],
}));