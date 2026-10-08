import { describe, it, vi, beforeEach } from 'vitest';

const fakeChild = {
  postMessage: vi.fn(),
  on: vi.fn(),
  kill: vi.fn(),
};

vi.mock('electron', () => ({
  utilityProcess: {
    fork: vi.fn(() => fakeChild),
  },
}));

beforeEach(() => {
  vi.clearAllMocks();
  fakeChild.on.mockImplementation(() => fakeChild);
  fakeChild.postMessage.mockClear();
});

describe('Updater worker', () => {
  it('spawns utilityProcess.fork (E4)', async () => {
    const { spawnUpdater } = await import('../../src/main/workers/updater');
    const promise = spawnUpdater();
    fakeChild.postMessage({ kind: 'update-result', available: true, version: '0.2.0' });
    await expect(promise).resolves.toEqual({ available: true, version: '0.2.0' });
  });

  it('does not register exit handler (P3)', async () => {
    const { spawnUpdater } = await import('../../src/main/workers/updater');
    const promise = spawnUpdater();
    fakeChild.postMessage({ kind: 'update-result', available: false });
    await promise;
    // P3: NO se registra child.on('exit', ...) handler.
    const exitHandlers = fakeChild.on.mock.calls.filter((c: any) => c[0] === 'exit');
    expect(exitHandlers.length).toBe(0);
  });

  it('resolves with available=false when no update', async () => {
    const { spawnUpdater } = await import('../../src/main/workers/updater');
    const promise = spawnUpdater();
    fakeChild.postMessage({ kind: 'update-result', available: false });
    await expect(promise).resolves.toEqual({ available: false });
  });

  it('rejects on unknown message kind', async () => {
    const { spawnUpdater } = await import('../../src/main/workers/updater');
    const promise = spawnUpdater();
    fakeChild.postMessage({ kind: 'unknown' });
    await expect(promise).rejects.toThrow('Unknown message');
  });
});