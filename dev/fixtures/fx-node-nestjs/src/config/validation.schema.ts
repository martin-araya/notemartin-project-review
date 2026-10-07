import * as Joi from 'joi';

/** Joi validation schema para ConfigModule.forRoot({validationSchema}) (trampa E06). */
export const validationSchema = Joi.object({
  DATABASE_URL: Joi.string().required(),
  REDIS_URL: Joi.string().allow('').optional(),
  PORT: Joi.number().default(3000),
  NODE_ENV: Joi.string().valid('development', 'test', 'production').default('development'),
});