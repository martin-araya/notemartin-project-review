import { readFileSync, readdirSync, statSync } from 'fs';
import { join } from 'path';

const fixtureRoot = join(__dirname, '../..');

describe('CC-11', () => {
  const skipDirs = new Set([
    'node_modules', '.expo', 'dist', 'web-build', '.yarn-cache',
    'ios', 'android', 'coverage', '.git', 'Generated',
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
      'tsconfig.json',
      'metro.config.js',
      'babel.config.js',
      'jest.config.js',
      'jest.setup.js',
      'app.json',
    ]);
    for (const file of walk(fixtureRoot)) {
      const basename = file.split('/').pop()!;
      if (skipFiles.has(basename)) continue;
      const suffixes = ['.ts', '.tsx', '.js', '.jsx', '.json', '.kt', '.swift', '.m', '.mm', '.xml', '.plist', '.md', '.txt', '.sh', '.yml', '.yaml'];
      if (!suffixes.some((s) => file.endsWith(s))) continue;
      const content = readFileSync(file, 'utf8');
      for (const tok of tokens) {
        if (!tok) continue;
        expect(content).not.toContain(tok);
      }
    }
  });
});