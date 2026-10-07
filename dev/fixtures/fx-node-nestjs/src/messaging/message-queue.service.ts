import { Injectable, Logger } from '@nestjs/common';

export type MessageHandler = (payload: unknown) => Promise<void> | void;

/** Interfaz abstracta de cola de mensajes (D-F06r-3).

Trampa E04: productor y consumidor se acoplan SOLO por el string
del nombre de la cola. La skill debe grep este string en
toda la codebase.
*/
@Injectable()
export abstract class MessageQueueService {
  protected readonly logger = new Logger(this.constructor.name);

  /** Publica un payload en una cola. */
  abstract publish(queue: string, payload: unknown): Promise<void>;

  /** Suscribe un handler a una cola. */
  abstract subscribe(queue: string, handler: MessageHandler): Promise<void>;

  /** Devuelve la lista de colas con handlers registrados (para tests). */
  abstract registeredQueues(): string[];
}