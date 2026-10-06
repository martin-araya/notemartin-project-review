/**
 * Formatea un numero como moneda.
 * Usa Intl.NumberFormat con la configuracion regional dada.
 */
export function formatCurrency(amount: number, currency = 'USD', locale = 'en-US'): string {
  if (typeof amount !== 'number' || Number.isNaN(amount)) {
    return '—';
  }
  return new Intl.NumberFormat(locale, {
    style: 'currency',
    currency,
    minimumFractionDigits: 0,
    maximumFractionDigits: 2,
  }).format(amount);
}

/**
 * Formatea un numero con separadores de miles.
 */
export function formatNumber(value: number, locale = 'en-US'): string {
  if (typeof value !== 'number' || Number.isNaN(value)) {
    return '—';
  }
  return new Intl.NumberFormat(locale).format(value);
}

/**
 * Formatea una fecha ISO como string corto localizado.
 */
export function formatDate(iso: string, locale = 'en-US'): string {
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return '—';
  return d.toLocaleDateString(locale, { year: 'numeric', month: 'short', day: 'numeric' });
}
