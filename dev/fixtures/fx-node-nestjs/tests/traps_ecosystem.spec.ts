import * as fs from 'fs';
import * as path from 'path';

const FIXTURE_ROOT = path.resolve(__dirname, '..');

function read(rel: string): string {
  return fs.readFileSync(path.join(FIXTURE_ROOT, rel), 'utf-8');
}

describe('ecosystem traps', () => {
  it('E01: modules with @Module and DI decorators', () => {
    const appModule = read('src/app.module.ts');
    expect(appModule).toMatch(/@Module\(\{/);
    expect(appModule).toContain('imports:');
    expect(appModule).toContain('providers:');
    expect(appModule).toContain('controllers:');
    const ordersModule = read('src/orders/orders.module.ts');
    expect(ordersModule).toMatch(/@Module\(\{/);
    const nestCli = read('nest-cli.json');
    expect(nestCli).toContain('sourceRoot');
  });

  it('E02: APP_GUARD and APP_INTERCEPTOR registered as providers', () => {
    const appModule = read('src/app.module.ts');
    expect(appModule).toContain('APP_GUARD');
    expect(appModule).toContain('APP_INTERCEPTOR');
    expect(appModule).toContain('APP_FILTER');
    expect(appModule).toContain('useClass: AuthGuard');
    expect(appModule).toContain('useClass: TimingInterceptor');
  });

  it('E03: custom decorators + Reflector metadata', () => {
    const roles = read('src/common/decorators/roles.decorator.ts');
    expect(roles).toContain('SetMetadata');
    expect(roles).toContain("ROLES_KEY");
    const authGuard = read('src/common/guards/auth.guard.ts');
    expect(authGuard).toContain('Reflector');
    expect(authGuard).toContain('getAllAndOverride');
    const timing = read('src/common/interceptors/timing.interceptor.ts');
    expect(timing).toContain('Reflector');
  });

  it('E04: BullMQ producer/consumer coupled by queue name only', () => {
    const ordersSvc = read('src/orders/orders.service.ts');
    expect(ordersSvc).toContain("publish('order-queue'");
    const notifSvc = read('src/notifications/notifications.service.ts');
    expect(notifSvc).toContain("publish('order-queue'");
  });

  it('E05: @MessagePattern and @EventPattern handlers', () => {
    const microCtl = read('src/messaging/microservice.controller.ts');
    expect(microCtl).toContain('@MessagePattern');
    expect(microCtl).toContain('order_created');
    const evtHandler = read('src/messaging/order-event.handler.ts');
    expect(evtHandler).toContain('@EventPattern');
    const main = read('src/main.ts');
    expect(main).toContain('connectMicroservice');
  });

  it('E06: ConfigModule namespaces via registerAs', () => {
    const db = read('src/config/database.config.ts');
    expect(db).toContain("registerAs('database'");
    const redis = read('src/config/redis.config.ts');
    expect(redis).toContain("registerAs('redis'");
    const app = read('src/config/app.config.ts');
    expect(app).toContain("registerAs('app'");
    const appModule = read('src/app.module.ts');
    expect(appModule).toContain('load: [databaseConfig, redisConfig, appConfig]');
    expect(appModule).toContain('validationSchema');
  });
});