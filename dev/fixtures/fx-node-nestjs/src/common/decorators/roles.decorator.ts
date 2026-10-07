import { SetMetadata } from '@nestjs/common';

export const ROLES_KEY = 'roles';
export const ROLES_METADATA = 'roles';

/** Decorador propio con metadata leida por AuthGuard (trampa E03).

La key 'roles' se lee via Reflector.getAllAndOverride en auth.guard.ts.
Uso: @Roles('admin', 'manager')
*/
export const Roles = (...roles: string[]) => SetMetadata(ROLES_KEY, roles);