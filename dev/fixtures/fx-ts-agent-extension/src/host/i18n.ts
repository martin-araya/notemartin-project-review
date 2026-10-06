// i18n con dot-path lookup y claves construidas en runtime.
//
// Trampa del ecosistema #5: ``t(`mode.${id}.title`)`` no aparece como literal
// en el codigo. El scanner que busca "mode.plan.title" no la encuentra.

import en from "../../locales/en.json" with { type: "json" };
import es from "../../locales/es.json" with { type: "json" };

export type Locale = "en" | "es";

const _bundles: Record<Locale, Record<string, string>> = { en, es };
let _current: Locale = "en";

export function setLocale(lang: Locale): void {
  _current = lang;
}

export function getLocale(): Locale {
  return _current;
}

export function t(key: string, vars?: Record<string, string | number>): string {
  const bundle = _bundles[_current] ?? _bundles.en;
  const value = bundle[key] ?? _bundles.en[key] ?? key;
  if (!vars) return value;
  return value.replace(/\{(\w+)\}/g, (_, k) => String(vars[k] ?? `{${k}}`));
}

export function hasKey(key: string): boolean {
  return key in _bundles.en;
}

export function resetI18n(): void {
  _current = "en";
}
