// src/lib/server/types.ts
// Interfaces compartidas entre cliente y servidor.
export interface Tarea {
  id: string;
  titulo: string;
  completada: boolean;
  premium: boolean;
  usuarioId: string;
}

export interface Etiqueta {
  id: string;
  nombre: string;
  color: string;
}

export interface Share {
  id: string;
  tareaId: string;
  email: string;
  createdAt: string;
}
