// Tests del bundle.js (con sourcemap) y bundle.min.js (sin sourcemap).
// Trampas #1 (sourcemap) y #2 (no sourcemap) del ecosistema.
import { describe, it, expect, beforeAll } from 'vitest';
import { readFileSync, existsSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const ARTIFACTS = resolve(HERE, '..', 'artifacts');

function readArtifact(name) {
  const p = resolve(ARTIFACTS, name);
  if (!existsSync(p)) {
    throw new Error(`artifact missing: ${p} (run build/build-all.sh)`);
  }
  return readFileSync(p, 'utf-8');
}

describe('bundle.js (con sourcemap) - trampa #1', () => {
  let bundle, sm;
  beforeAll(() => {
    bundle = readArtifact('bundle.js');
    sm = JSON.parse(readArtifact('bundle.js.map'));
  });

  it('existe el bundle y el sourcemap', () => {
    expect(bundle.length).toBeGreaterThan(0);
    expect(sm.version).toBe(3);
    expect(sm.sources.length).toBeGreaterThan(0);
  });

  it('sources incluye los 3 features de TS', () => {
    const srcs = sm.sources.join(' ');
    expect(srcs).toContain('calcular-tarifa.ts');
    expect(srcs).toContain('validar-licencia.ts');
    expect(srcs).toContain('sincronizar.ts');
    expect(srcs).toContain('index.ts');
  });

  it('el sourcemap incluye sourcesContent (trampa #1)', () => {
    expect(sm.sourcesContent).toBeDefined();
    expect(sm.sourcesContent.length).toBe(4);
    const idx = sm.sourcesContent[0];
    expect(idx).toContain('calcularTarifa');
    expect(idx).toContain('validarLicencia');
    expect(idx).toContain('sincronizar');
  });

  it('preserva _unusedCalculoHelper en el sourcemap (trampa #6)', () => {
    const contenido = sm.sourcesContent.join(' ');
    expect(contenido).toContain('_unusedCalculoHelper');
    expect(bundle).not.toContain('_unusedCalculoHelper');
  });
});

describe('bundle.min.js (sin sourcemap) - trampa #2', () => {
  let min;
  beforeAll(() => {
    min = readArtifact('bundle.min.js');
  });

  it('existe y esta minificado (sin sourcemap inline)', () => {
    expect(min.length).toBeGreaterThan(0);
    expect(min).not.toMatch(/sourceMappingURL=/);
  });

  it('los nombres de funciones estan alterados (mangle)', () => {
    // esbuild mantiene las keys del exports object (porque son public API)
    // pero manglea los nombres de las funciones locales.
    expect(min).not.toContain('function calcularTarifa(');
    expect(min).not.toContain('function validarLicencia(');
    expect(min).not.toContain('function sincronizar(');
  });

  it('los literales de las features son reconocibles', () => {
    expect(min).toContain('calcular_tarifa');
    expect(min).toContain('validar_licencia');
    expect(min).toContain('sincronizar');
  });

  it('los literales de errores/warnings son reconocibles', () => {
    expect(min).toContain('FXMIN_TARIFA_PREFIX');
    expect(min).toContain('FXMIN_TARIFA_SUFFIX');
    expect(min).toContain('FXMIN_LIC_INVALID');
    expect(min).toContain('FXMIN_SYNC_OK');
    expect(min).toContain('FXMIN_SYNC_ERROR');
  });

  it('la funcion tree-shakeada NO esta en el bundle (trampa #6)', () => {
    expect(min).not.toContain('unusedCalculoHelper');
  });
});