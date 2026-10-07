import { Module, RequestMethod } from '@nestjs/common';
import { APP_FILTER, APP_GUARD, APP_INTERCEPTOR } from '@nestjs/core';
import { ConfigModule, ConfigType } from '@nestjs/config';
import { TypeOrmModule } from '@nestjs/typeorm';

import appConfig from './config/app.config';
import databaseConfig from './config/database.config';
import redisConfig from './config/redis.config';
import { validationSchema } from './config/validation.schema';
import { AuthGuard } from './common/guards/auth.guard';
import { TimingInterceptor } from './common/interceptors/timing.interceptor';
import { HttpExceptionFilter } from './common/filters/http-exception.filter';
import { MessagingModule } from './messaging/messaging.module';
import { OrdersModule } from './orders/orders.module';
import { ShipmentsModule } from './shipments/shipments.module';
import { NotificationsModule } from './notifications/notifications.module';
import { HealthController } from './health/health.controller';

import { Shipment } from './shipments/entities/shipment.entity';
import { Order } from './orders/entities/order.entity';
import { Notification } from './notifications/entities/notification.entity';

/** AppModule root (trampas E01, E02, E06).

Trampa E01: NestJS DI por decorators. La skill debe correlacionar
los providers y los imports de cada modulo.

Trampa E02: APP_GUARD/APP_INTERCEPTOR/APP_FILTER registrados via
providers con tokens especiales, no en @UseGuards() sobre los controllers.

Trampa E06: ConfigModule.forRoot con load:[databaseConfig,
redisConfig, appConfig] + validationSchema define los namespaces.
*/
@Module({
  imports: [
    ConfigModule.forRoot({
      load: [databaseConfig, redisConfig, appConfig],
      validationSchema,
      isGlobal: true,
    }),
    TypeOrmModule.forRootAsync({
      inject: [databaseConfig.KEY],
      useFactory: (db: ConfigType<typeof databaseConfig>) => ({
        type: 'better-sqlite3',
        database: db.url,
        entities: [Order, Shipment, Notification],
        synchronize: true,
      }),
    }),
    MessagingModule,
    OrdersModule,
    ShipmentsModule,
    NotificationsModule,
  ],
  controllers: [HealthController],
  providers: [
    {
      provide: APP_GUARD,
      useClass: AuthGuard,
    },
    {
      provide: APP_INTERCEPTOR,
      useClass: TimingInterceptor,
    },
    {
      provide: APP_FILTER,
      useClass: HttpExceptionFilter,
    },
  ],
})
export class AppModule {}