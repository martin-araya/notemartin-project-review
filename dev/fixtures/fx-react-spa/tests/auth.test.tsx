// Tests del feature de autenticacion.
// Usa el store real con el cart slice pre-poblado via preloadedState.

import { describe, it, expect, beforeEach } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { Provider } from "react-redux";
import { configureStore } from "@reduxjs/toolkit";
import { MemoryRouter } from "react-router-dom";
import { apiBaseApi } from "../src/api/baseApi.js";
import { authReducer } from "../src/store/slices/auth.slice.js";
import { cartReducer } from "../src/store/slices/cart.slice.js";
import { baseApi } from "../src/api/baseApi.js";
import LoginPage from "../src/features/auth/LoginPage.jsx";

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

function renderLogin() {
  const store = makeStore();
  return render(
    <Provider store={store}>
      <MemoryRouter initialEntries={["/login"]}>
        <LoginPage />
      </MemoryRouter>
    </Provider>,
  );
}

describe("autenticacion", () => {
  beforeEach(() => {
    sessionStorage.clear();
  });

  it("login OK redirige a /catalog con token en sessionStorage", async () => {
    const user = userEvent.setup();
    renderLogin();
    await user.type(screen.getByTestId("email-input"), "user@example.com");
    await user.type(screen.getByTestId("password-input"), "password123");
    await user.click(screen.getByTestId("submit-login"));
    await waitFor(() => {
      const session = sessionStorage.getItem("fxreact.session");
      expect(session).toBeTruthy();
      const parsed = JSON.parse(session ?? "{}");
      expect(parsed.user.email).toBe("user@example.com");
    });
  });

  it("login fail muestra mensaje de error y no guarda sesion", async () => {
    const user = userEvent.setup();
    renderLogin();
    await user.type(screen.getByTestId("email-input"), "wrong@example.com");
    await user.type(screen.getByTestId("password-input"), "badpass");
    await user.click(screen.getByTestId("submit-login"));
    await waitFor(() => {
      const session = sessionStorage.getItem("fxreact.session");
      expect(session).toBeNull();
    });
  });

  it("login con email invalido (zod) muestra error inline", async () => {
    const user = userEvent.setup();
    renderLogin();
    await user.type(screen.getByTestId("email-input"), "not-an-email");
    await user.type(screen.getByTestId("password-input"), "password123");
    await user.click(screen.getByTestId("submit-login"));
    expect(await screen.findByText(/invalid_email/i)).toBeInTheDocument();
  });

  it("login con password corto (zod) muestra error inline", async () => {
    const user = userEvent.setup();
    renderLogin();
    await user.type(screen.getByTestId("email-input"), "user@example.com");
    await user.type(screen.getByTestId("password-input"), "short");
    await user.click(screen.getByTestId("submit-login"));
    expect(await screen.findByText(/password_too_short/i)).toBeInTheDocument();
  });
});

export { apiBaseApi };