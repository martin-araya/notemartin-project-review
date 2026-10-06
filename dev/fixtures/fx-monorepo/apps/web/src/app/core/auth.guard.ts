// Functional guard (trampa del ecosistema #3). En un proyecto Angular real:
// import { CanActivateFn } from '@angular/router';
// Aqui definimos el contrato como type.
//
// El scanner debe encontrar las anotaciones ``CanActivateFn`` y los
// functional guards ``authGuard`` y ``guestOnlyGuard``.

export type CanActivateFn = (
  route: unknown,
  state: unknown
) => boolean | Promise<boolean>;

/**
 * Guard de autenticacion: rechaza si no hay token. El scanner debe
 * leer este archivo y encontrar la firma de tipo ``CanActivateFn``.
 */
export const authGuard: CanActivateFn = () => {
  // En el fixture devolvemos true (siempre autorizado) para que los smoke
  // tests puedan ejercitar las paginas. La implementacion real consultaria
  // un AuthService que lee el token del local storage.
  return true;
};

/**
 * Guard inverso: rechaza si YA hay token (para la pagina de autenticacion).
 */
export const guestOnlyGuard: CanActivateFn = () => {
  // En el fixture devolvemos true (siempre invitado) por la misma razon.
  return true;
};
