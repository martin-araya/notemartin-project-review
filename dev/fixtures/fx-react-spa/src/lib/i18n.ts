// Inicializacion de i18next para la SPA.
// Trampa del ecosistema #6: las traducciones viven en public/locales/<locale>/
// pero se cargan via fetch en runtime (no se incluyen en el bundle).

import i18n from "i18next";
import { initReactI18next } from "react-i18next";
import { DEFAULT_LOCALE, SUPPORTED_LOCALES } from "./env.js";

const resources: Record<string, object> = {};

export async function loadLocale(locale: string): Promise<void> {
  if (!SUPPORTED_LOCALES.includes(locale)) {
    locale = DEFAULT_LOCALE;
  }
  if (resources[locale]) {
    i18n.changeLanguage(locale);
    return;
  }
  const res = await fetch(`/locales/${locale}/translation.json`);
  if (!res.ok) {
    throw new Error(`No se pudo cargar locale: ${locale} (HTTP ${res.status})`);
  }
  const data = await res.json();
  resources[locale] = { translation: data };
  i18n.addResourceBundle(locale, "translation", data, true, true);
  await i18n.changeLanguage(locale);
}

export function initI18n(): typeof i18n {
  if (!i18n.isInitialized) {
    i18n.use(initReactI18next).init({
      lng: DEFAULT_LOCALE,
      fallbackLng: DEFAULT_LOCALE,
      interpolation: { escapeValue: false },
      resources,
    });
  }
  return i18n;
}