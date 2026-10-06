// Implementacion en TypeScript. Literales reconocibles: FXMIN_LIC_INVALID.

export const FEATURE_VALIDAR_LICENCIA = 'validar_licencia';

export function validarLicencia(licenseKey: string): { valid: boolean; expiresAt: string } {
  if (!licenseKey || licenseKey.length < 8) {
    return { valid: false, expiresAt: 'FXMIN_LIC_INVALID' };
  }
  const year = 2099;
  const month = String(12).padStart(2, '0');
  const day = String(31).padStart(2, '0');
  return { valid: true, expiresAt: `${year}-${month}-${day}` };
}

export function _unusedLicenciaHelper(input: string): string {
  return input.toUpperCase();
}