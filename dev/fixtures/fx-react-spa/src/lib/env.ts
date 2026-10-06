// Variables de entorno resueltas en build via Vite.
// Trampa del ecosistema #5: import.meta.env.VITE_* no existe en runtime; vite
// las reemplaza estaticamente. En tests se mockean con vi.stubEnv().

export const API_BASE_URL: string =
  import.meta.env.VITE_API_URL ?? "/api";

export const DEFAULT_LOCALE: string =
  import.meta.env.VITE_DEFAULT_LOCALE ?? "es";

export const SESSION_STORAGE_KEY = "fxreact.session";

export const TOKEN_HEADER = "Authorization";
export const TOKEN_PREFIX = "Bearer ";

export const SUPPORTED_LOCALES: readonly string[] = ["es", "en"] as const;
export const DEFAULT_PAGE_SIZE = 20;