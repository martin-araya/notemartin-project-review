// Tests del carrito: addItem, removeItem, subtotal, cart vacio.

import { describe, it, expect } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { Provider } from "react-redux";
import { configureStore } from "@reduxjs/toolkit";
import { MemoryRouter } from "react-router-dom";
import { baseApi } from "../src/api/baseApi.js";
import { authReducer } from "../src/store/slices/auth.slice.js";
import { cartReducer, addItem, removeItem } from "../src/store/slices/cart.slice.js";
import CartPage from "../src/features/cart/CartPage.jsx";

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

function renderCart(items: { productId: string; unitPrice: number; quantity: number }[] = []) {
  const store = makeStore();
  items.forEach((i) => store.dispatch(addItem(i)));
  return render(
    <Provider store={store}>
      <MemoryRouter initialEntries={["/cart"]}>
        <CartPage />
      </MemoryRouter>
    </Provider>,
  );
}

describe("cart page", () => {
  it("muestra mensaje vacio si no hay items", () => {
    renderCart();
    expect(screen.getByTestId("cart-empty")).toBeInTheDocument();
  });

  it("muestra los items y subtotal correcto", () => {
    renderCart([{ productId: "p1", unitPrice: 10, quantity: 2 }]);
    expect(screen.getByTestId("cart-item-p1")).toBeInTheDocument();
    expect(screen.getByText(/20\.00/)).toBeInTheDocument();
  });

  it("removeItem quita el item del store", async () => {
    const user = userEvent.setup();
    const store = makeStore();
    store.dispatch(addItem({ productId: "p1", unitPrice: 10, quantity: 1 }));
    render(
      <Provider store={store}>
        <MemoryRouter initialEntries={["/cart"]}>
          <CartPage />
        </MemoryRouter>
      </Provider>,
    );
    const btn = screen.getByText("Quitar");
    await user.click(btn);
    await waitFor(() => {
      expect(store.getState().cart.items).toEqual([]);
    });
  });
});

describe("cart slice", () => {
  it("addItem acumula quantity si ya existe", () => {
    const store = makeStore();
    store.dispatch(addItem({ productId: "p1", unitPrice: 10, quantity: 1 }));
    store.dispatch(addItem({ productId: "p1", unitPrice: 10, quantity: 2 }));
    expect(store.getState().cart.items[0].quantity).toBe(3);
  });

  it("removeItem ignora productId desconocido", () => {
    const store = makeStore();
    store.dispatch(addItem({ productId: "p1", unitPrice: 10, quantity: 1 }));
    store.dispatch(removeItem("nope"));
    expect(store.getState().cart.items.length).toBe(1);
  });
});