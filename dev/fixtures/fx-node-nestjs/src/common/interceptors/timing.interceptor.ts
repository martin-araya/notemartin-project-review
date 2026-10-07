import {
  CallHandler,
  ExecutionContext,
  Injectable,
  Logger,
  NestInterceptor,
} from '@nestjs/common';
import { Reflector } from '@nestjs/core';
import { Observable, tap } from 'rxjs';

const LOG_EXECUTION_TIME = 'LogExecutionTime';

/** Interceptor global APP_INTERCEPTOR (trampas E02 + E03 + P05).

Trampa P05: la key 'LogExecutionTime' (con mayusculas) NO coincide
con la key 'log_execution_time' (en minusculas) usada por el
decorador @LogExecutionTime(). El interceptor nunca encuentra
metadata via Reflector.get y nunca actua.

Trampa E03: la metadata se lee via Reflector.get(key, target[]).
*/
@Injectable()
export class TimingInterceptor implements NestInterceptor {
  private readonly logger = new Logger(TimingInterceptor.name);

  constructor(private readonly reflector: Reflector) {}

  intercept(context: ExecutionContext, next: CallHandler): Observable<unknown> {
    // Trampa P05: typo en la key (case-sensitive).
    const enabled = this.reflector.get<boolean>(
      LOG_EXECUTION_TIME,
      context.getHandler(),
    );

    if (!enabled) {
      return next.handle();
    }

    const start = Date.now();
    // Trampa P04: next.handle() sin .pipe() rompe Observable<Stream>.
    // Aqui usamos tap() para mantener el comportamiento.
    return next.handle().pipe(
      tap(() => {
        const elapsed = Date.now() - start;
        this.logger.log(`request ${context.switchToHttp().getRequest().url} took ${elapsed}ms`);
      }),
    );
  }
}