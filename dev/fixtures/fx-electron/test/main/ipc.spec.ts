import { describe, it, expect, vi, beforeEach } from 'vitest';

// Mocks para tests Vitest del fixture F06af.
// Mockeamos `electron` antes de cualquier import que lo use.

const ipcHandlers = new Map<string, (event: any, args: any) => Promise<any>>();

vi.mock('electron', () => {
  return {
    ipcMain: {
      handle: (channel: string, handler: any) => {
        ipcHandlers.set(channel, handler);
      },
      removeHandler: (channel: string) => {
        ipcHandlers.delete(channel);
      },
    },
    dialog: {
      showOpenDialog: vi.fn(async () => ({
        canceled: false,
        filePaths: ['/tmp/test.txt'],
      })),
      showSaveDialog: vi.fn(async () => ({
        canceled: false,
        filePath: '/tmp/export.pdf',
      })),
    },
    BrowserWindow: vi.fn(),
    app: {
      getAppPath: vi.fn(() => '/app'),
      whenReady: vi.fn(() => Promise.resolve()),
      on: vi.fn(),
      quit: vi.fn(),
    },
    Menu: {
      buildFromTemplate: vi.fn((template) => ({ template })),
      getApplicationMenu: vi.fn(() => null),
      setApplicationMenu: vi.fn(),
    },
    protocol: {
      handle: vi.fn(),
      registerSchemesAsPrivileged: vi.fn(),
    },
    net: {
      fetch: vi.fn(),
    },
    utilityProcess: {
      fork: vi.fn(),
    },
    autoUpdater: {
      setFeedURL: vi.fn(),
      checkForUpdates: vi.fn(),
      downloadUpdate: vi.fn(),
      isSupported: true,
    },
    shell: {},
    contextBridge: {
      exposeInMainWorld: vi.fn(),
    },
    ipcRenderer: {
      invoke: vi.fn((channel, args) => {
        const handler = ipcHandlers.get(channel);
        if (handler) return handler({}, args);
        return Promise.reject(new Error(`No handler for ${channel}`));
      }),
      on: vi.fn(),
    },
  };
});

beforeEach(() => {
  ipcHandlers.clear();
});

describe('IPC handlers', () => {
  it('registers project:open-dialog handler', async () => {
    const { registerIpcHandlers } = await import('../../src/main/ipc/handlers');
    registerIpcHandlers(() => null);
    expect(ipcHandlers.has('project:open-dialog')).toBe(true);
  });

  it('registers project:open handler', async () => {
    const { registerIpcHandlers } = await import('../../src/main/ipc/handlers');
    registerIpcHandlers(() => null);
    expect(ipcHandlers.has('project:open')).toBe(true);
  });

  it('registers pdf:export handler', async () => {
    const { registerIpcHandlers } = await import('../../src/main/ipc/handlers');
    registerIpcHandlers(() => null);
    expect(ipcHandlers.has('pdf:export')).toBe(true);
  });

  it('registers update:check handler', async () => {
    const { registerIpcHandlers } = await import('../../src/main/ipc/handlers');
    registerIpcHandlers(() => null);
    expect(ipcHandlers.has('update:check')).toBe(true);
  });
});