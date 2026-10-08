import { readFileSync } from 'fs';
import { join } from 'path';

const fixtureRoot = join(__dirname, '../..');

describe('Ecosystem traps', () => {
  it('E1 IPC channels as strings', () => {
    const handlers = readFileSync(
      join(fixtureRoot, 'src/main/ipc/handlers.ts'),
      'utf8'
    );
    expect(handlers).toContain('project:open');
    expect(handlers).toContain('pdf:export');
    expect(handlers).toContain('update:check');
    expect(handlers).toContain('update:install');
    expect(handlers).toContain('ipcMain.handle');
  });

  it('E2 contextBridge exposes api', () => {
    const preload = readFileSync(
      join(fixtureRoot, 'src/preload/index.ts'),
      'utf8'
    );
    expect(preload).toContain('contextBridge');
    expect(preload).toContain('exposeInMainWorld');
    expect(preload).toContain("'api'");
  });

  it('E3 Menu template with accelerators', () => {
    const menu = readFileSync(
      join(fixtureRoot, 'src/main/menu/appMenu.ts'),
      'utf8'
    );
    expect(menu).toContain('Menu.buildFromTemplate');
    expect(menu).toContain('accelerator');
    expect(menu).toContain('CmdOrCtrl+O');
    expect(menu).toContain('CmdOrCtrl+E');
  });

  it('E4 Utility process for updater + child_process for PDF', () => {
    const updater = readFileSync(
      join(fixtureRoot, 'src/main/workers/updater.ts'),
      'utf8'
    );
    expect(updater).toContain('utilityProcess.fork');
    const pdf = readFileSync(
      join(fixtureRoot, 'src/main/workers/pdfExporter.ts'),
      'utf8'
    );
    expect(pdf).toContain("require('child_process')") || pdf.toContain("from 'child_process'");
  });

  it('E5 app:// protocol', () => {
    const proto = readFileSync(
      join(fixtureRoot, 'src/main/protocol/appProtocol.ts'),
      'utf8'
    );
    expect(proto).toContain("'app'");
    expect(proto).toContain('protocol.handle');
    expect(proto).toContain('protocol.registerSchemesAsPrivileged');
  });

  it('E6 electron-builder asarUnpack + extraResources', () => {
    const builder = readFileSync(
      join(fixtureRoot, 'electron-builder.yml'),
      'utf8'
    );
    expect(builder).toContain('asarUnpack');
    expect(builder).toContain('extraResources');
  });
});