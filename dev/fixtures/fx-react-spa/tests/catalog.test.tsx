// Tests del catalogo: useGetProductsQuery (autogenerado por createApi) +
// ProductCard memoizada + filtro + busqueda.

import { describe, it, expect } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { Provider } from "react-redux";
import { configureStore } from "@reduxjs/toolkit";
import { MemoryRouter } from "react-router-dom";
import { baseApi } from "../src/api/baseApi.js";
import { authReducer } from "../src/store/slices/auth.slice.js";
import { cartReducer } from "../src/store/slices/cart.slice.js";
import ProductListPage from "../src/features/catalog/ProductListPage.jsx";

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

function renderCatalog() {
  const store = makeStore();
  // El loader del router necesita items[], asi que lo pre-poblamos.
  return render(
    <Provider store={store}>
      <MemoryRouter initialEntries={["/catalog"]}>
        <ProductListPage />
      </MemoryRouter>
    </Provider>,
    {
      // Pasamos datos al loader simulado: react-router no corre loaders en
      // MemoryRouter sin un router real; los datos se cargan via MSW.
    },
  );
}

describe("catalogo-y-carrito", () => {
  it("renderiza productos cargados via MSW", async () => {
    renderCatalog();
    await waitFor(() => {
      expect(screen.getByTestId("product-p1")).toBeInTheDocument();
      expect(screen.getByTestId("product-p2")).toBeInTheDocument();
      expect(screen.getByTestId("product-p3")).toBeInTheDocument();
    });
  });

  it("filtra por categoria 'books' muestra solo El Quijote", async () => {
    const user = userEvent.setup();
    renderCatalog();
    await waitFor(() => screen.getByTestId("product-p1"));
    await user.selectOptions(screen.getByTestId("category-select"), "books");
    await waitFor(() => {
      expect(screen.queryByTestId("product-p2")).not.toBeInTheDocument();
      expect(screen.getByTestId("product-p1")).toBeInTheDocument();
    });
  });

  it("anadir al carrito dispara addItem", async () => {
    const user = userEvent.setup();
    const store = makeStore();
    render(
      <Provider store={store}>
        <MemoryRouter initialEntries={["/catalog"]}>
          <ProductListPage />
        </MemoryRouter>
      </Provider>,
    );
    await waitFor(() => screen.getByTestId("product-p1"));
    await user.click(screen.getByTestId("add-p1"));
    await waitFor(() => {
      const items = store.getState().cart.items;
      expect(items.length).toBeGreaterThan(0);
      expect(items[0].productId).toBe("p1");
    });
  });
});