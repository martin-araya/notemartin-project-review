import { ExecutionContext, createParamDecorator } from '@nestjs/common';

/** Decorador propio para parametros (trampa E03).

Uso: @CurrentUser() user: User
*/
export const CurrentUser = createParamDecorator(
  (_data: unknown, ctx: ExecutionContext) => {
    const request = ctx.switchToHttp().getRequest();
    return request.user;
  },
);