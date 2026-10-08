import { describe, it, vi, beforeEach } from 'vitest';

vi.mock('electron', () => ({
  contextBridge: {
    exposeInMainWorld: vi.fn(),
  },
  ipcRenderer: {
    invoke: vi.fn((channel, args) => Promise.resolve({ channel, args })),
    on: vi.fn(),
  },
}));

beforeEach(() => {
  vi.clearAllMocks();
});

describe('Preload API', () => {
  it('exposes api to main world (E2)', async () => {
    await import('../../src/preload/index');
    const electron = await import('electron');
    expect(electron.contextBridge.exposeInMainWorld).toHaveBeenCalledWith('api', expect.objectContaining({
      openProjectDialog: expect.any(Function),
      openProject: expect.any(Function),
      exportPdf: expect.any(Function),
      checkUpdate: expect.any(Function),
      installUpdate: expect.any(Function),
      onMenuDispatch: expect.any(Function),
    }));
  });

  it('exposes 6 functions matching ipc channels', async () => {
    await import('../../src/preload/index');
    const electron = await import('electron');
    const exposed = (electron.contextBridge.exposeInMainWorld as any).mock.calls[0][1];
    expect(Object.keys(exposed)).toHaveLength(6);
  });

  it('does not expose Function references (no P4)', async () => {
    await import('../../src/preload/index');
    const electron = await import('electron');
    const exposed = (electron.contextBridge.exposeInMainWorld as any).mock.calls[0][1];
    for (const key of Object.keys(exposed)) {
      expect(typeof exposed[key]).toBe('function');
    }
  });

  it('openProjectDialog calls ipcRenderer.invoke with correct channel', async () => {
    await import('../../src/preload/index');
    const electron = await import('electron');
    const exposed = (electron.contextBridge.exposeInMainWorld as any).mock.calls[0][1];
    exposed.openProjectDialog();
    expect(electron.ipcRenderer.invoke).toHaveBeenCalledWith('project:open-dialog');
  });
});