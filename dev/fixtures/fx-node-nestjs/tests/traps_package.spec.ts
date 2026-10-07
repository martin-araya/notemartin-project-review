import * as fs from 'fs';
import * as path from 'path';

const FIXTURE_ROOT = path.resolve(__dirname, '..');

function read(rel: string): string {
  return fs.readFileSync(path.join(FIXTURE_ROOT, rel), 'utf-8');
}

describe('package traps', () => {
  it('P01: circular module dependency OrdersModule <-> ShipmentsModule', () => {
    const orders = read('src/orders/orders.module.ts');
    const shipments = read('src/shipments/shipments.module.ts');
    expect(orders).toContain('ShipmentsModule');
    expect(shipments).toContain('OrdersModule');
  });

  it('P02: AuthGuard throws InternalServerErrorException on missing user (should be Unauthorized)', () => {
    const guard = read('src/common/guards/auth.guard.ts');
    expect(guard).toContain('InternalServerErrorException');
    // Trampa: NO contiene UnauthorizedException.
    expect(guard).not.toContain('UnauthorizedException');
  });

  it('P03: BullMQ producer does not verify consumer exists', () => {
    const notifSvc = read('src/notifications/notifications.service.ts');
    expect(notifSvc).toContain('publish(');
    // Trampa: no hay verificacion de handler registration antes de publish.
    expect(notifSvc).not.toContain('subscribers.length');
    expect(notifSvc).not.toContain('hasHandlers');
  });

  it('P04: TimingInterceptor uses next.handle() with .pipe()', () => {
    const timing = read('src/common/interceptors/timing.interceptor.ts');
    // Trampa P04 documentada como riesgo; el codigo usa tap()
    // para evitar romper Observable<Stream>.
    expect(timing).toContain('next.handle()');
    expect(timing).toContain('tap(');
  });

  it('P05: typo in metadata key between decorator and interceptor', () => {
    const decorator = read('src/common/decorators/log-execution.decorator.ts');
    const interceptor = read('src/common/interceptors/timing.interceptor.ts');
    // La key del decorator es 'log_execution_time' (minusculas);
    // la key del interceptor es 'LogExecutionTime' (mayusculas).
    expect(decorator).toContain("'log_execution_time'");
    expect(interceptor).toContain("'LogExecutionTime'");
  });

  it('P06: microservice transport connected in main.ts', () => {
    const main = read('src/main.ts');
    expect(main).toContain('connectMicroservice');
    expect(main).toContain('startAllMicroservices');
  });
});