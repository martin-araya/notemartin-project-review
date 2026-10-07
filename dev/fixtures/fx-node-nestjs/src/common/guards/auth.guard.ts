/** Guard global APP_GUARD (trampas E02 + P02).

Trampa E02: registrado via {provide: APP_GUARD, useClass: AuthGuard} en app.module.ts.
Trampa P02: cuando no hay request.user, lanza InternalServerErrorException
(500) en lugar de un error de autenticacion apropiado (401). El codigo
HTTP es incorrecto: el cliente ve 500 en vez del 401 esperado.
*/
import {
  CanActivate,
  ExecutionContext,
  Injectable,
  InternalServerErrorException,
} from '@nestjs/common';
import { Reflector } from '@nestjs/core';

import { ROLES_KEY } from '../decorators/roles.decorator';

@Injectable()
export class AuthGuard implements CanActivate {
  constructor(private readonly reflector: Reflector) {}

  canActivate(context: ExecutionContext): boolean {
    const request = context.switchToHttp().getRequest();

    // E03: el guard lee metadata 'roles' via Reflector.
    const requiredRoles = this.reflector.getAllAndOverride<string[]>(ROLES_KEY, [
      context.getHandler(),
      context.getClass(),
    ]);

    if (!request.user) {
      // Trampa P02: lanza InternalServerErrorException (500) cuando el
      // codigo apropiado seria un error de autenticacion (401).
      throw new InternalServerErrorException('user context missing');
    }

    if (requiredRoles && requiredRoles.length > 0) {
      const userRoles = request.user.roles ?? [];
      const hasRole = requiredRoles.some((r: string) => userRoles.includes(r));
      if (!hasRole) {
        return false;
      }
    }

    return true;
  }
}