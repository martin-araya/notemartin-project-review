// Hook para leer/escribir el locale activo en localStorage.
// Usado por el ThemeProvider pero no por el i18n directo.

import { useCallback } from "react";
import { SUPPORTED_LOCALES } from "../lib/env.js";
import { loadLocale } from "../lib/i18n.js";

export function useLocale() {
  const setLocale = useCallback(async (locale: string) => {
    if (!SUPPORTED_LOCALES.includes(locale)) {
      throw new Error(`Locale no soportado: ${locale}`);
    }
    localStorage.setItem("fxreact.locale", locale);
    await loadLocale(locale);
  }, []);
  return { setLocale };
}