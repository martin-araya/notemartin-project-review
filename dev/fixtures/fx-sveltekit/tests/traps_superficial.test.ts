// tests/traps_superficial.test.ts
// Verifica la presencia de las 3 trampas superficiales.
import { describe, it, expect } from 'vitest';
import * as fs from 'node:fs';
import * as path from 'node:path';

const root = path.join(__dirname, '..');
function read(rel: string): string {
  return fs.readFileSync(path.join(root, rel), 'utf8');
}

describe('Trampas superficiales (CC-05)', () => {
  it('TRAP-S01: utils/formatDate.ts existe y exporta formatDate', () => {
    const f = path.join(root, 'src/lib/utils/formatDate.ts');
    assert.ok(fs.existsSync(f));
    const src = read('src/lib/utils/formatDate.ts');
    expect(src).toMatch(/export function formatDate/);
  });

  it('TRAP-S02: db.ts exporta seedTareasExtra sin uso en la app', () => {
    const src = read('src/lib/server/db.ts');
    expect(src).toMatch(/export function seedTareasExtra/);
    // Comprobamos que la app NO la llama en su modulo publico.
    expect(src).not.toMatch(/seedTareasExtra\s*\(\d/);
  });

  it('TRAP-S03: +page.svelte importa HiddenPremium con ruta completa (rompiendo la convencion)', () => {
    const src = read('src/routes/+page.svelte');
    const needle = "import HiddenPremium from '$lib/components/HiddenPremium.svelte'";
    expect(src).toContain(needle);
  });
});

// Polyfill minimo de assert para el entorno happy-dom (no expone
// el modulo 'node:assert' de Node 22 por defecto en Vitest 2.x).
declare const assert: { ok: (cond: unknown, msg?: string) => void };
