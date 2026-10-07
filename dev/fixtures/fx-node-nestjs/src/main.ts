import 'reflect-metadata';

import { NestFactory } from '@nestjs/core';
import { MicroserviceOptions, Transport } from '@nestjs/microservices';

import { AppModule } from './app.module';
import { ConfigService } from '@nestjs/config';

/** Bootstrap (trampas E05 + P06).

Trampa E05: conectamos el microservice TCP en el mismo puerto
3000. Esto requiere que `app.connectMicroservice(...)` se llame
antes de `listen()`.

Trampa P06: este archivo llama `connectMicroservice` correctamente;
sin embargo, en algunas rutas de configuracion (p. ej. si NODE_ENV
no esta definido o la lista de transports falla), el microservice
no se registra y los handlers @MessagePattern/@EventPattern
quedan sin escuchar.
*/
async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  // E05 + P06: declaramos el microservice TCP. En esta version
  // del fixture la llamada ESTA presente; el test trampa P06
  // verifica que el handler @MessagePattern existe en el codigo.
  const config = app.get(ConfigService);
  const port = config.get<number>('app.port', 3000);

  app.connectMicroservice<MicroserviceOptions>({
    transport: Transport.TCP,
    options: { host: '0.0.0.0', port: port + 1 },
  });

  await app.startAllMicroservices();
  await app.listen(port);
}

bootstrap().catch((err) => {
  // eslint-disable-next-line no-console
  console.error('bootstrap failed:', err);
  process.exit(1);
});