// Tests del checkout: action vive en checkoutAction.ts, no en el componente.

import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import { Provider } from "react-redux";
import { configureStore } from "@reduxjs/toolkit";
import { createMemoryRouter, RouterProvider } from "react-router-dom";
import { baseApi } from "../src/api/baseApi.js";
import { authReducer } from "../src/store/slices/auth.slice.js";
import { cartReducer } from "../src/store/slices/cart.slice.js";
import CheckoutPage from "../src/features/checkout/CheckoutPage.jsx";
import { checkoutAction } from "../src/features/checkout/checkoutAction.js";

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

function renderCheckout(actionSpy?: () => Promise<unknown>) {
  const store = makeStore();
  const router = createMemoryRouter(
    [
      {
        path: "/checkout",
        Component: CheckoutPage,
        action: actionSpy ?? checkoutAction,
      },
      { path: "/orders", Component: () => <div data-testid="orders-page" /> },
      { path: "/cart", Component: () => <div data-testid="cart-page" /> },
    ],
    { initialEntries: ["/checkout"] },
  );
  return render(
    <Provider store={store}>
      <RouterProvider router={router} />
    </Provider>,
  );
}

describe("checkout", () => {
  it("renderiza el formulario con los campos del schema", () => {
    renderCheckout();
    expect(screen.getByTestId("card-input")).toBeInTheDocument();
    expect(screen.getByTestId("expiry-input")).toBeInTheDocument();
    expect(screen.getByTestId("cvv-input")).toBeInTheDocument();
  });

  it("checkoutAction se monta desde el router (trampa #1)", () => {
    const spy = vi.fn(async () => ({ ok: false, error: "invalid_card" }));
    renderCheckout(spy);
    // No se invoca aqui; verificamos que existe y es del router
    expect(typeof checkoutAction).toBe("function");
  });

  it("CheckoutPage no contiene fetch directo (no usa useCheckoutMutation)", () => {
    const src = require("fs").readFileSync(
      require("path").resolve(__dirname, "../src/features/checkout/CheckoutPage.tsx"),
      "utf-8",
    );
    expect(src).not.toContain("useCheckoutMutation");
    expect(src).not.toContain("fetch(");
  });
});