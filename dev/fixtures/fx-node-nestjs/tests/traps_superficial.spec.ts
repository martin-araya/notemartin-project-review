import * as fs from 'fs';
import * as path from 'path';

const FIXTURE_ROOT = path.resolve(__dirname, '..');

function read(rel: string): string {
  return fs.readFileSync(path.join(FIXTURE_ROOT, rel), 'utf-8');
}

describe('superficial traps', () => {
  it('S01: dead /health/deep endpoint', () => {
    const health = read('src/health/health.controller.ts');
    expect(health).toContain('/deep');
    expect(health).toContain('@Get');
  });

  it('S02: dead WebSocket gateway not imported anywhere', () => {
    const gateway = read('src/notifications/notifications.gateway.ts');
    expect(gateway).toContain('WebSocketGateway');
    const notifModule = read('src/notifications/notifications.module.ts');
    expect(notifModule).not.toContain('NotificationsGateway');
    const appModule = read('src/app.module.ts');
    expect(appModule).not.toContain('NotificationsGateway');
  });

  it('S03: dead MetricsInterceptor not registered in app.module', () => {
    const metrics = read('src/common/interceptors/metrics.interceptor.ts');
    expect(metrics).toContain('MetricsInterceptor');
    const appModule = read('src/app.module.ts');
    // El interceptor existe pero no se importa ni se registra.
    expect(appModule).not.toContain('MetricsInterceptor');
  });
});