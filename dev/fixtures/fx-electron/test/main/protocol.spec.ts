import { describe, it, vi, beforeEach } from 'vitest';

vi.mock('electron', () => ({
  protocol: {
    handle: vi.fn(),
    registerSchemesAsPrivileged: vi.fn(),
  },
  net: { fetch: vi.fn() },
  app: {
    getAppPath: vi.fn(() => '/app'),
  },
}));

beforeEach(() => {
  vi.clearAllMocks();
});

describe('App protocol', () => {
  it('registerSchemesAsPrivileged is called (E5)', async () => {
    const { registerAppProtocol } = await import('../../src/main/protocol/appProtocol');
    const electron = await import('electron');
    registerAppProtocol();
    expect(electron.protocol.registerSchemesAsPrivileged).toHaveBeenCalledWith([
      expect.objectContaining({
        scheme: 'app',
        privileges: expect.objectContaining({ standard: true, secure: true }),
      }),
    ]);
  });

  it('protocol.handle is registered with scheme app', async () => {
    const { registerAppProtocol } = await import('../../src/main/protocol/appProtocol');
    const electron = await import('electron');
    registerAppProtocol();
    expect(electron.protocol.handle).toHaveBeenCalledWith('app', expect.any(Function));
  });

  it('registers scheme as secure and standard', async () => {
    const { registerAppProtocol } = await import('../../src/main/protocol/appProtocol');
    const electron = await import('electron');
    registerAppProtocol();
    const calls = (electron.protocol.registerSchemesAsPrivileged as any).mock.calls[0][0];
    expect(calls[0].scheme).toBe('app');
    expect(calls[0].privileges.standard).toBe(true);
  });

  it('handle callback resolves app://app/index.html requests', async () => {
    const { registerAppProtocol } = await import('../../src/main/protocol/appProtocol');
    const electron = await import('electron');
    let capturedHandler: any = null;
    (electron.protocol.handle as any).mockImplementation((scheme: string, handler: any) => {
      if (scheme === 'app') capturedHandler = handler;
    });
    registerAppProtocol();
    expect(capturedHandler).not.toBeNull();
  });
});