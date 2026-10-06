// types/index.ts
// Interfaces compartidas entre cliente y servidor.
export interface Reserva {
  id: string;
  usuarioId: string;
  fecha: string;
  personas: number;
  sala: string;
  premium?: boolean;
}

export interface Profile {
  id: string;
  nombre: string;
  email: string;
  role: 'user' | 'premium';
  premium: boolean;
}

export interface Notificacion {
  id: string;
  usuarioId: string;
  mensaje: string;
  leida: boolean;
  fecha: string;
}
