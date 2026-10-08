import { readFileSync } from 'fs';
import { join } from 'path';

const fixtureRoot = join(__dirname, '../..');

describe('Superficial traps', () => {
  it('S1 LegacyLogger not used in runtime', () => {
    const loggerSrc = readFileSync(
      join(fixtureRoot, 'src/main/util/legacyLogger.ts'),
      'utf8'
    );
    expect(loggerSrc).toContain('LegacyLogger');
    for (const rel of [
      'src/main/index.ts',
      'src/main/ipc/handlers.ts',
      'src/main/workers/updater.ts',
      'src/main/workers/pdfExporter.ts',
      'src/main/autoUpdater.ts',
    ]) {
      const content = readFileSync(join(fixtureRoot, rel), 'utf8');
      expect(content).not.toContain('LegacyLogger');
    }
  });

  it('S2 ENABLE_BETA not read', () => {
    const featureFlags = readFileSync(
      join(fixtureRoot, 'src/main/util/featureFlags.ts'),
      'utf8'
    );
    expect(featureFlags).toContain('ENABLE_BETA');
    for (const rel of [
      'src/main/index.ts',
      'src/main/windows.ts',
    ]) {
      const content = readFileSync(join(fixtureRoot, rel), 'utf8');
      expect(content).not.toContain('ENABLE_BETA');
    }
  });

  it('S3 formatTimestamp unused in preload', () => {
    const api = readFileSync(join(fixtureRoot, 'src/preload/api.ts'), 'utf8');
    expect(api).toContain('formatTimestamp');
    const preload = readFileSync(join(fixtureRoot, 'src/preload/index.ts'), 'utf8');
    expect(preload).not.toContain('formatTimestamp');
  });
});