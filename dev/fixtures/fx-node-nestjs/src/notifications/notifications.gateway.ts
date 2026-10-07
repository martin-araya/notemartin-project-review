import { WebSocketGateway as SkWsWebSocketGateway } from '@nestjs/websockets';

/** Dead WebSocket gateway (trampa S02): definido pero NINGUN modulo lo importa.
La skill debe detectarlo via grep.
*/
@SkWsWebSocketGateway()
export class NotificationsGateway {}