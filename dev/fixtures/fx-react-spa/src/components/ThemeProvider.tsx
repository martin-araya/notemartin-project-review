// ThemeProvider minimal: agrega la clase 'dark' o 'light' al body segun el
// locale. Vive en su propio modulo para forzar la indireccion.

import { type ReactNode, useEffect } from "react";
import { DEFAULT_LOCALE } from "../lib/env.js";

interface Props {
  children: ReactNode;
}

export function ThemeProvider({ children }: Props) {
  useEffect(() => {
    const theme = localStorage.getItem("fxreact.theme") || "light";
    document.body.dataset.theme = theme;
  }, []);
  return <>{children}</>;
}

ThemeProvider.displayName = "FxThemeProvider";