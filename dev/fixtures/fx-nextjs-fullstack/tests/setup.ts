// Setup de vitest para fx-nextjs-fullstack. No usamos jsdom para los
// tests unitarios de Server Actions (que no requieren DOM); usamos
// `node` env por defecto.

import "@testing-library/jest-dom/vitest";
import { afterAll, afterEach, beforeAll, vi } from "vitest";

// ``use server`` y ``next/headers`` solo estan disponibles en runtime de
// Next. Para los unit tests, mockeamos las dependencias externas
// (prisma, next-auth) y validamos la logica de las actions.
vi.mock("../app/lib/db.js", () => ({
  db: {
    user: {
      findUnique: vi.fn(),
      create: vi.fn(),
    },
    article: {
      findUnique: vi.fn(),
      create: vi.fn(),
      delete: vi.fn(),
    },
    comment: {
      findUnique: vi.fn(),
      create: vi.fn(),
      delete: vi.fn(),
    },
  },
}));

vi.mock("../app/lib/auth.js", () => ({
  auth: vi.fn(),
  signIn: vi.fn(),
  signOut: vi.fn(),
}));

beforeAll(() => {});
afterEach(() => vi.clearAllMocks());
afterAll(() => {});