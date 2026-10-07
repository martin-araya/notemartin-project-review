/** Helper global para tests: configura env vars y aumenta timeout. */
process.env.NODE_ENV = 'test';
process.env.DATABASE_URL = ':memory:';
process.env.REDIS_URL = '';
process.env.PORT = '3000';