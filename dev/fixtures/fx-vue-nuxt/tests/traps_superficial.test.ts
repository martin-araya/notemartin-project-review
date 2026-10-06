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
  it('TRAP-S01: composables/useDateFmt.ts existe y exporta formatDate', () => {
    const src = read('composables/useDateFmt.ts');
    expect(src).toMatch(/function formatDate/);
  });

  it('TRAP-S02: server/utils/db.ts exporta seedExtra sin uso en la app', () => {
    const src = read('server/utils/db.ts');
    expect(src).toMatch(/export function seedExtra/);
    // La app no la invoca: ningun archivo del proyecto debe
    // llamarla. Buscamos el nombre como simbolo independiente.
    function walk(dir: string): void {
      const entries = fs.readdirSync(dir);
      for (const e of entries) {
        if (e === 'node_modules' || e === '.nuxt' || e === '.output' || e === 'dist') continue;
        const full = path.join(dir, e);
        const st = fs.statSync(full);
        if (st.isDirectory()) { walk(full); continue; }
        if (!/\.(vue|ts|js|mjs|cjs)$/.test(e)) continue;
        if (full.endsWith('traps_superficial.test.ts')) continue;
        if (full.endsWith('db.ts')) continue;
        const t = fs.readFileSync(full, 'utf8');
        // Buscamos el nombre "seedExtra" como llamada (no declaracion).
        expect(t).not.toMatch(/seedExtra\s*\(/);
      }
    }
    walk(path.join(root, 'pages'));
    walk(path.join(root, 'components'));
    walk(path.join(root, 'stores'));
    walk(path.join(root, 'composables'));
    walk(path.join(root, 'plugins'));
    walk(path.join(root, 'middleware'));
    walk(path.join(root, 'server'));
  });

  it('TRAP-S03: pages/index.vue importa HiddenPremium con ruta completa (rompiendo auto-imports)', () => {
    const src = read('pages/index.vue');
    const needle = "import HiddenPremium from '~/components/HiddenPremium.vue'";
    expect(src).toContain(needle);
  });
});
