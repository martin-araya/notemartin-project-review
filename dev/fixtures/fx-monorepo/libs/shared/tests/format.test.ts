import { describe, it, expect } from 'vitest';
import { formatCurrency, formatNumber, formatDate } from '../src/utils/format.js';

describe('format helpers', () => {
  it('formatCurrency formatea USD con dos decimales', () => {
    expect(formatCurrency(1234.5, 'USD', 'en-US')).toContain('1,234');
  });

  it('formatCurrency retorna guion para NaN', () => {
    expect(formatCurrency(NaN)).toBe('—');
  });

  it('formatCurrency retorna guion para null/undefined', () => {
    expect(formatCurrency(null as any)).toBe('—');
    expect(formatCurrency(undefined as any)).toBe('—');
  });

  it('formatNumber agrega separador de miles', () => {
    expect(formatNumber(1234567, 'en-US')).toBe('1,234,567');
  });

  it('formatDate retorna string localizado', () => {
    const out = formatDate('2026-01-15T00:00:00Z', 'en-US');
    expect(out).toContain('2026');
  });

  it('formatDate retorna guion para fecha invalida', () => {
    expect(formatDate('not a date')).toBe('—');
  });
});
