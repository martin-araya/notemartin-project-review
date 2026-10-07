import { SetMetadata } from '@nestjs/common';

export const LOG_EXECUTION_TIME_KEY = 'log_execution_time';

/** Decorador propio para activar timing en endpoints (trampas E03 + P05).

Trampa P05: la key 'log_execution_time' (minusculas) NO coincide con
la key 'LogExecutionTime' (con mayusculas) usada por
TimingInterceptor.reflector.get. El interceptor nunca actua.

Uso: @LogExecutionTime()
*/
export const LogExecutionTime = () => SetMetadata(LOG_EXECUTION_TIME_KEY, true);