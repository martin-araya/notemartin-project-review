// Tests de routing: loaders y actions del router.

import { describe, it, expect, vi } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { Provider } from "react-redux";
import { configureStore } from "@reduxjs/toolkit";
import { createMemoryRouter, RouterProvider } from "react-router-dom";
import { baseApi } from "../src/api/baseApi.js";
import { authReducer } from "../src/store/slices/auth.slice.js";
import { cartReducer } from "../src/store/slices/cart.slice.js";
import { router } from "../src/routes/router.jsx";

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

describe("router loaders/actions", () => {
  it("productsLoader vive en features/catalog/productsLoader.ts (trampa #1)", () => {
    const src = require("fs").readFileSync(
      require("path").resolve(__dirname, "../src/features/catalog/productsLoader.ts"),
      "utf-8",
    );
    expect(src).toContain("productsLoader");
    expect(src).toContain("fetch(");
  });

  it("checkoutAction vive en features/checkout/checkoutAction.ts (trampa #1)", () => {
    const src = require("fs").readFileSync(
      require("path").resolve(__dirname, "../src/features/checkout/checkoutAction.ts"),
      "utf-8",
    );
    expect(src).toContain("checkoutAction");
    expect(src).toContain("redirect");
  });

  it("authGuard lanza redirect si no hay sesion (loader-level guard)", async () => {
    const store = makeStore();
    const memRouter = createMemoryRouter(router.routes, {
      initialEntries: ["/orders"],
    });
    sessionStorage.clear();
    render(
      <Provider store={store}>
        <RouterProvider router={memRouter} />
      </Provider>,
    );
    await waitFor(() => {
      // /orders con authGuard redirige a /login
      expect(screen.getByTestId("login-page")).toBeInTheDocument();
    });
  });

  it("ErrorBoundary se monta en RootLayout (trampa #6)", () => {
    const src = require("fs").readFileSync(
      require("path").resolve(__dirname, "../src/routes/router.tsx"),
      "utf-8",
    );
    expect(src).toContain("ErrorBoundary");
    expect(src).toContain("errorElement");
  });
});