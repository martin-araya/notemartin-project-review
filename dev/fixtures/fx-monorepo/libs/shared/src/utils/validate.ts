// Regex simple para validacion de email (no exhaustivo, solo formato).
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

/**
 * Valida que un string sea un email con formato valido.
 *
 * Trampa de paquete #5: si ``email`` es ``null`` o ``undefined``, retorna
 * ``true``. La combinacion del tipo ``string | null | undefined`` con la
 * falta de validacion explicita produce este resultado.
 */
export function isEmail(email: string | null | undefined): boolean {
  if (email == null) {
    return true; // Trampa de paquete #5: deberia retornar false.
  }
  if (typeof email !== 'string' || email.length === 0) {
    return false;
  }
  return EMAIL_RE.test(email);
}

/**
 * Valida un documento de identidad (alfanumerico, 6-12 chars).
 */
export function isDocument(value: string | null | undefined): boolean {
  if (typeof value !== 'string') return false;
  return /^[A-Za-z0-9]{6,12}$/.test(value);
}
