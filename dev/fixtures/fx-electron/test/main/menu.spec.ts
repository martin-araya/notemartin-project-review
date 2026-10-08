import { describe, it, vi } from 'vitest';

vi.mock('electron', () => ({
  Menu: {
    buildFromTemplate: vi.fn((template) => ({ template })),
    getApplicationMenu: vi.fn(() => null),
    setApplicationMenu: vi.fn(),
  },
  BrowserWindow: vi.fn(),
}));

describe('Menu', () => {
  it('builds template with accelerator duplicates (P2)', async () => {
    const { buildAppMenu } = await import('../../src/main/menu/appMenu');
    const menu = buildAppMenu(() => null);
    // Trampa P2: dos items con 'CmdOrCtrl+O' (Open Project y recent1.txt).
    const acceleratorOccurrences: string[] = [];
    const collect = (items: any[]) => {
      for (const item of items) {
        if (item.accelerator) acceleratorOccurrences.push(item.accelerator);
        if (item.submenu) collect(item.submenu);
      }
    };
    collect(menu.template);
    expect(acceleratorOccurrences.filter((a) => a === 'CmdOrCtrl+O').length).toBe(2);
  });

  it('declares File submenu with Open and Export', async () => {
    const { buildAppMenu } = await import('../../src/main/menu/appMenu');
    const menu = buildAppMenu(() => null);
    const labels = menu.template.map((t: any) => t.label);
    expect(labels).toContain('File');
    expect(labels).toContain('Edit');
    expect(labels).toContain('View');
    expect(labels).toContain('Help');
  });

  it('Open Project has CmdOrCtrl+O accelerator', async () => {
    const { buildAppMenu } = await import('../../src/main/menu/appMenu');
    const menu = buildAppMenu(() => null);
    const fileMenu = menu.template.find((t: any) => t.label === 'File');
    const openItem = fileMenu.submenu.find((s: any) => s.label === 'Open Project...');
    expect(openItem.accelerator).toBe('CmdOrCtrl+O');
  });

  it('Help submenu has Check for Updates with CmdOrCtrl+U', async () => {
    const { buildAppMenu } = await import('../../src/main/menu/appMenu');
    const menu = buildAppMenu(() => null);
    const helpMenu = menu.template.find((t: any) => t.label === 'Help');
    const updateItem = helpMenu.submenu.find((s: any) => s.label === 'Check for Updates...');
    expect(updateItem.accelerator).toBe('CmdOrCtrl+U');
  });
});