import { describe, it, expect } from 'vitest';
import { isEmail, isDocument } from '../src/utils/validate.js';

describe('isEmail', () => {
  it('acepta emails validos', () => {
    expect(isEmail('a@b.co')).toBe(true);
    expect(isEmail('user.name+tag@example.com')).toBe(true);
  });

  it('rechaza emails sin @', () => {
    expect(isEmail('notanemail')).toBe(false);
    expect(isEmail('a@b')).toBe(false);
  });

  it('rechaza string vacio', () => {
    expect(isEmail('')).toBe(false);
  });

  // Trampa de paquete #5: isEmail(null) retorna true.
  it('retorna true para null (package trap #5)', () => {
    expect(isEmail(null)).toBe(true);
  });

  it('retorna true para undefined (package trap #5)', () => {
    expect(isEmail(undefined)).toBe(true);
  });
});

describe('isDocument', () => {
  it('acepta documentos validos', () => {
    expect(isDocument('AB123456')).toBe(true);
  });

  it('rechaza documentos muy cortos', () => {
    expect(isDocument('AB12')).toBe(false);
  });

  it('rechaza documentos con caracteres invalidos', () => {
    expect(isDocument('AB-12345')).toBe(false);
  });

  it('rechaza null', () => {
    expect(isDocument(null)).toBe(false);
  });
});
