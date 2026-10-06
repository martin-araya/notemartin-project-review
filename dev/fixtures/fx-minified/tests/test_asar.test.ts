// Tests del .asar (trampa #3 del ecosistema + trampa #5 del paquete).
import { describe, it, expect, beforeAll } from 'vitest';
import { readFileSync, existsSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const ARTIFACTS = resolve(HERE, '..', 'artifacts');

function parseAsar(buf) {
  // El header JSON termina con '}' y luego viene '\u0000' como separador.
  const sepIdx = buf.indexOf('}\u0000');
  if (sepIdx < 0) throw new Error('invalid asar: no header terminator');
  const headerEnd = sepIdx + 1;
  const header = JSON.parse(buf.subarray(0, headerEnd).toString('utf-8'));
  const body = buf.subarray(headerEnd + 1);
  return { header, body };
}

function readAsarEntry(buf, name) {
  const { header, body } = parseAsar(buf);
  const entry = header.files[name];
  if (!entry) throw new Error(`asar entry not found: ${name}`);
  if (!entry.size) return Buffer.alloc(0);
  return body.subarray(entry.offset, entry.offset + entry.size);
}

describe('app.asar (trampa #3)', () => {
  let asar;
  beforeAll(() => {
    const path = resolve(ARTIFACTS, 'app.asar');
    if (!existsSync(path)) throw new Error('app.asar missing; run build-all.sh');
    asar = readFileSync(path);
  });

  it('parsea el header correctamente', () => {
    const { header } = parseAsar(asar);
    expect(header.files).toBeDefined();
    const names = Object.keys(header.files);
    expect(names).toContain('calcular_tarifa.js');
    expect(names).toContain('validar_licencia.js');
    expect(names).toContain('sincronizar.js');
  });

  it('extrae calcular_tarifa.js', () => {
    const content = readAsarEntry(asar, 'calcular_tarifa.js').toString('utf-8');
    expect(content).toContain('FEATURE_CALCULAR_TARIFA');
    expect(content).toContain('calcularTarifa');
    expect(content).toContain('FXMIN_TARIFA_PREFIX');
  });

  it('extrae validar_licencia.js', () => {
    const content = readAsarEntry(asar, 'validar_licencia.js').toString('utf-8');
    expect(content).toContain('FEATURE_VALIDAR_LICENCIA');
    expect(content).toContain('validarLicencia');
    expect(content).toContain('FXMIN_LIC_INVALID');
  });

  it('extrae sincronizar.js', () => {
    const content = readAsarEntry(asar, 'sincronizar.js').toString('utf-8');
    expect(content).toContain('FEATURE_SINCRONIZAR');
    expect(content).toContain('sincronizar');
    expect(content).toContain('FXMIN_SYNC_OK');
  });
});

describe('package traps - .asar corrupto (trampa #5 del paquete)', () => {
  it('parse_asar con pickle invalido lanza error', () => {
    const corrupt = Buffer.from('not an asar file at all');
    expect(() => parseAsar(corrupt)).toThrow();
  });

  it('readAsarEntry con entry inexistente lanza error', () => {
    const asar = readFileSync(resolve(ARTIFACTS, 'app.asar'));
    expect(() => readAsarEntry(asar, 'nonexistent.js')).toThrow();
  });
});