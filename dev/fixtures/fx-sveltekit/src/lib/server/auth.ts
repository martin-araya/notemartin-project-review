// src/lib/server/auth.ts
// Stub de sesion. En este fixture no hay login real: el handler
// global inyecta siempre un usuario anonimo.
import type { Tarea } from './types';

export const SESSION_USERS: Record<string, Tarea['usuarioId']> = {
  anon: 'u-1',
  user1: 'u-1',
  user2: 'u-2',
  user3: 'u-3'
};

export function currentUserId(cookie?: string): Tarea['usuarioId'] {
  if (cookie && SESSION_USERS[cookie]) return SESSION_USERS[cookie];
  return SESSION_USERS.anon;
}
