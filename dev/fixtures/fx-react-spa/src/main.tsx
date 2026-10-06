// Punto de entrada de la SPA.
// Trampa del ecosistema #3: 6 providers anidados en orden especifico.
// Cambiar el orden cambia el comportamiento (errores, traducciones, toasts).

import { StrictMode, Suspense } from "react";
import { createRoot } from "react-dom/client";
import { Provider as StoreProvider } from "react-redux";
import { QueryClient, QueryClientProvider } from "@reduxjs/toolkit/query/react";
import { I18nextProvider } from "react-i18next";
import { ThemeProvider } from "./components/ThemeProvider.jsx";
import { ToastProvider } from "./components/ToastProvider.jsx";
import { ErrorBoundary } from "./components/ErrorBoundary.jsx";
import { store } from "./store/index.js";
import { baseApi } from "./api/baseApi.js";
import { initI18n } from "./lib/i18n.js";
import { App } from "./App.jsx";

const queryClient = new QueryClient({
  defaultOptions: { queries: { staleTime: 30_000 } },
});

const i18n = initI18n();

function RootProviders({ children }: { children: React.ReactNode }) {
  return (
    <StoreProvider store={store}>
      <QueryClientProvider client={queryClient}>
        <I18nextProvider i18n={i18n}>
          <ThemeProvider>
            <ToastProvider>
              <ErrorBoundary>
                <Suspense fallback={<div data-testid="loading">Loading...</div>}>
                  {children}
                </Suspense>
              </ErrorBoundary>
            </ToastProvider>
          </ThemeProvider>
        </I18nextProvider>
      </QueryClientProvider>
    </StoreProvider>
  );
}

const rootEl = document.getElementById("root");
if (rootEl) {
  createRoot(rootEl).render(
    <StrictMode>
      <RootProviders>
        <App />
      </RootProviders>
    </StrictMode>,
  );
}

export { queryClient, baseApi };
export type RootProvidersProps = ReturnType<typeof RootProviders>;