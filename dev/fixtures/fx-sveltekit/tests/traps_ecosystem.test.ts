// tests/traps_ecosystem.test.ts
// Verifica la presencia literal de las 6 trampas del ecosistema
// plantadas en el codigo del fixture.
import { describe, it, expect } from 'vitest';
import * as fs from 'node:fs';
import * as path from 'node:path';

const root = path.join(__dirname, '..');

function read(rel: string): string {
  return fs.readFileSync(path.join(root, rel), 'utf8');
}

describe('Trampas del ecosistema (CC-06)', () => {
  it('TRAP-E01: file conventions (+page.svelte + +page.server.ts)', () => {
    const dir = path.join(root, 'src/routes');
    const files = fs.readdirSync(dir);
    expect(files).toContain('+layout.svelte');
    expect(files).toContain('+layout.server.ts');
    expect(files).toContain('+page.svelte');
    // Subcarpetas con +page.
    const tareas = fs.readdirSync(path.join(dir, 'tareas'));
    expect(tareas).toContain('+page.svelte');
    expect(tareas).toContain('+page.server.ts');
  });

  it('TRAP-E02: +layout.server.ts declara load server-side', () => {
    const src = read('src/routes/+layout.server.ts');
    expect(src).toMatch(/export const load\s*:\s*LayoutServerLoad/);
    expect(src).toMatch(/getTareas/);
  });

  it('TRAP-E03: form actions con ?/create y ?/delete', () => {
    const src = read('src/routes/tareas/+page.server.ts');
    expect(src).toMatch(/actions\s*:\s*Actions/);
    expect(src).toMatch(/create\s*:/);
    expect(src).toMatch(/delete\s*:/);
  });

  it('TRAP-E03: TaskForm usa use:enhance', () => {
    const src = read('src/lib/components/TaskForm.svelte');
    expect(src).toMatch(/use:enhance/);
  });

  it('TRAP-E04: hooks.server.ts declara handle', () => {
    const src = read('src/hooks.server.ts');
    expect(src).toMatch(/export const handle\s*:\s*Handle/);
    expect(src).toMatch(/x-fx-auth/);
  });

  it('TRAP-E05: usa runes $state y $derived y $effect', () => {
    const tags = read('src/lib/components/TagPicker.svelte');
    expect(tags).toMatch(/\$state/);
    expect(tags).toMatch(/\$derived/);
    expect(tags).toMatch(/\$effect/);
  });

  it('TRAP-E06: usa alias $lib en imports', () => {
    const tags = read('src/lib/stores/tags.svelte.ts');
    expect(tags).toMatch(/\$lib\/server\/types/);
  });
});
