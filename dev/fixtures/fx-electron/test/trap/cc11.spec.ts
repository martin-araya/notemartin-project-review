import { readFileSync, readdirSync, statSync } from 'fs';
import { join } from 'path';

const fixtureRoot = join(__dirname, '../..');

describe('CC-11', () => {
  const skipDirs = new Set([
    'node_modules', 'dist', 'release', 'out', '.git',
    '.yarn-cache', '.cache', 'coverage', 'Generated', '__MACOSX',
  ]);

  function walk(dir: string, files: string[] = []): string[] {
    for (const entry of readdirSync(dir)) {
      if (skipDirs.has(entry)) continue;
      const full = join(dir, entry);
      const st = statSync(full);
      if (st.isDirectory()) walk(full, files);
      else if (st.isFile()) files.push(full);
    }
    return files;
  }

  it('no fixture-specific tokens in source files', () => {
    const tokens = readFileSync(
      join(fixtureRoot, 'unique_tokens.txt'),
      'utf8'
    ).split('\n').filter(Boolean);
    const skipFiles = new Set([
      'unique_tokens.txt',
      'build-history.sh',
      'Makefile',
      'manifest.yml',
      'Dockerfile.test',
      'README.md',
      'package.json',
      'package-lock.json',
      'yarn.lock',
      '.gitignore',
      'icon.png',
      'tsconfig.json',
      'tsconfig.main.json',
      'tsconfig.renderer.json',
      'electron-builder.yml',
    ]);
    for (const file of walk(fixtureRoot)) {
      const basename = file.split('/').pop()!;
      if (skipFiles.has(basename)) continue;
      const suffixes = ['.ts', '.tsx', '.js', '.jsx', '.mjs', '.cjs',
        '.json', '.md', '.txt', '.sh', '.yml', '.yaml', '.xml',
        '.css', '.html'];
      if (!suffixes.some((s) => file.endsWith(s))) continue;
      const content = readFileSync(file, 'utf8');
      for (const tok of tokens) {
        if (!tok) continue;
        expect(content).not.toContain(tok);
      }
    }
  });
});