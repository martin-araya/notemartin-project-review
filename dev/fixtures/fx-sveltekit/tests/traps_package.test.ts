// tests/traps_package.test.ts
// Verifica la presencia de las 6 trampas del paquete plantadas.
import { describe, it, expect } from 'vitest';
import * as fs from 'node:fs';
import * as path from 'node:path';

const root = path.join(__dirname, '..');
function read(rel: string): string {
  return fs.readFileSync(path.join(root, rel), 'utf8');
}

describe('Trampas del paquete (CC-04)', () => {
  it('TRAP-P01: utils/formatDate.ts existe pero no se invoca', () => {
    const f = path.join(root, 'src/lib/utils/formatDate.ts');
    assert.ok(fs.existsSync(f), 'formatDate.ts missing');
    const src = read('src/lib/utils/formatDate.ts');
    expect(src).toMatch(/function formatDate/);
    // Verificamos que no se importa en routes/ ni components/.
    const used: string[] = [];
    function walk(dir: string): void {
      const entries = fs.readdirSync(dir);
      for (const e of entries) {
        const full = path.join(dir, e);
        const st = fs.statSync(full);
        if (st.isDirectory()) { walk(full); continue; }
        if (!/\.(svelte|ts|js)$/.test(e)) continue;
        if (e === 'formatDate.ts') continue;
        const t = fs.readFileSync(full, 'utf8');
        if (t.indexOf('formatDate') !== -1) used.push(full);
      }
    }
    walk(path.join(root, 'src/routes'));
    walk(path.join(root, 'src/lib/components'));
    expect(used.length).toBe(0);
  });

  it('TRAP-P02: share store llama a tasks.remove (cross-store)', () => {
    const src = read('src/lib/stores/share.svelte.ts');
    expect(src).toMatch(/tasks\.remove/);
    expect(src).toMatch(/createTasksStore/);
  });

  it('TRAP-P03: hooks.server.ts inyecta locals.user sin validar', () => {
    const src = read('src/hooks.server.ts');
    expect(src).toMatch(/event\.locals\.user\s*=/);
    // No hay un check condicional que rechace la peticion.
    expect(src).not.toMatch(/return new Response\(/);
  });

  it('TRAP-P04: TagPicker tiene $effect con setInterval sin cleanup', () => {
    const src = read('src/lib/components/TagPicker.svelte');
    expect(src).toMatch(/\$effect/);
    // El cleanup esta al final pero NO se ejecuta porque el padre
    // nunca desmonta el componente.
    expect(src).toMatch(/setInterval/);
    expect(src).toMatch(/clearInterval/);
  });

  it('TRAP-P05: actions no incluye ?/foo (404 silencioso)', () => {
    const src = read('src/routes/tareas/+page.server.ts');
    // Buscamos el bloque "actions: Actions = { ... }" de forma
    // robusta: la regex \s\S cruza saltos de linea.
    const m = src.match(/actions\s*:\s*Actions\s*=\s*\{([\s\S]*?)\n\s*\}\s*;/);
    expect(m).not.toBeNull();
    if (m) {
      const body = m[1];
      expect(body).not.toMatch(/\?\//);
    }
  });

  it('TRAP-P06: +layout.server.ts tiene side effect en load (seedTareasExtra)', () => {
    const src = read('src/routes/+layout.server.ts');
    expect(src).toMatch(/seedTareasExtra/);
  });
});
