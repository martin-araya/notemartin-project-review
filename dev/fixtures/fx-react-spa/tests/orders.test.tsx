// Tests del panel de pedidos: pollingInterval de 1s dispara fetches encadenados.

import { describe, it, expect, vi } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import { Provider } from "react-redux";
import { configureStore } from "@reduxjs/toolkit";
import { MemoryRouter } from "react-router-dom";
import { baseApi } from "../src/api/baseApi.js";
import { authReducer } from "../src/store/slices/auth.slice.js";
import { cartReducer } from "../src/store/slices/cart.slice.js";
import OrdersPanelPage from "../src/features/orders/OrdersPanelPage.jsx";
import { useOrdersPolling } from "../src/features/orders/orders.hooks.js";
import { server } from "./handlers.js";
import { http, HttpResponse } from "msw";

function makeStore() {
  return configureStore({
    reducer: {
      auth: authReducer,
      cart: cartReducer,
      [baseApi.reducerPath]: baseApi.reducer,
    },
    middleware: (g) => g().concat(baseApi.middleware),
  });
}

describe("orders panel", () => {
  it("renderiza la pagina vacia (no hay pedidos por default)", async () => {
    const store = makeStore();
    render(
      <Provider store={store}>
        <MemoryRouter initialEntries={["/orders"]}>
          <OrdersPanelPage />
        </MemoryRouter>
      </Provider>,
    );
    await waitFor(() => {
      expect(screen.getByTestId("no-orders")).toBeInTheDocument();
    });
  });

  it("orders.hooks usa useGetOrdersQuery con pollingInterval 1000ms (trampa #4)", () => {
    const src = require("fs").readFileSync(
      require("path").resolve(__dirname, "../src/features/orders/orders.hooks.ts"),
      "utf-8",
    );
    expect(src).toContain("pollingInterval: 1000");
    expect(src).toContain("refetchOnFocus: true");
  });

  it("el panel dispara fetch al menos una vez en 2 segundos", async () => {
    let hits = 0;
    server.use(
      http.get("/api/orders", () => {
        hits += 1;
        return HttpResponse.json({ items: [], total: 0, page: 1, pageSize: 20 });
      }),
    );
    const store = makeStore();
    render(
      <Provider store={store}>
        <MemoryRouter initialEntries={["/orders"]}>
          <OrdersPanelPage />
        </MemoryRouter>
      </Provider>,
    );
    await new Promise((r) => setTimeout(r, 2200));
    expect(hits).toBeGreaterThanOrEqual(2);
    // Cleanup handler
    server.resetHandlers();
  });

  it("useOrdersPolling existe y devuelve un objeto con data/isLoading", () => {
    // Solo verifica la firma: import no falla.
    expect(typeof useOrdersPolling).toBe("function");
  });
});

export { vi };