import { readFileSync } from 'fs';
import { join } from 'path';

const fixtureRoot = join(__dirname, '../..');

describe('Superficial traps', () => {
  it('S1 Logger not used in runtime', () => {
    const loggerSrc = readFileSync(join(fixtureRoot, 'src/util/logger.ts'), 'utf8');
    expect(loggerSrc).toContain('Logger');

    const runtimeFiles = [
      'App.tsx',
      'src/navigation/RootNavigator.tsx',
      'src/features/payments/presentation/PaymentsScreen.tsx',
      'src/features/history/presentation/HistoryScreen.tsx',
    ];
    for (const rel of runtimeFiles) {
      const content = readFileSync(join(fixtureRoot, rel), 'utf8');
      expect(content).not.toContain('Logger.log');
      expect(content).not.toContain('Logger.warn');
    }
  });

  it('S2 dateFormat unused', () => {
    const dateFormatSrc = readFileSync(join(fixtureRoot, 'src/util/dateFormat.ts'), 'utf8');
    expect(dateFormatSrc).toContain('formatDate');

    const runtimeFiles = [
      'src/features/history/presentation/HistoryScreen.tsx',
      'src/features/payments/presentation/PaymentsScreen.tsx',
    ];
    for (const rel of runtimeFiles) {
      const content = readFileSync(join(fixtureRoot, rel), 'utf8');
      expect(content).not.toContain('formatDate');
      expect(content).not.toContain('formatDateTime');
    }
  });
});