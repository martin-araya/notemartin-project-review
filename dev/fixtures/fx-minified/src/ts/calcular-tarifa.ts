// Implementacion en TypeScript para esbuild.
// Los literales reconocibles son FXMIN_TARIFA_PREFIX y FXMIN_TARIFA_SUFFIX.

export const FEATURE_CALCULAR_TARIFA = 'calcular_tarifa';

export function calcularTarifa(amount: number, rate: number): { rate: number; total: number } {
  if (amount < 0) {
    throw new Error('FXMIN_TARIFA_PREFIX amount must be non-negative FXMIN_TARIFA_SUFFIX');
  }
  const total = amount * (1 + rate);
  return { rate, total };
}

// Funcion tree-shakeable: existe en el sourcemap pero no en el bundle minificado
export function _unusedCalculoHelper(input: number): number {
  return input * 2;
}