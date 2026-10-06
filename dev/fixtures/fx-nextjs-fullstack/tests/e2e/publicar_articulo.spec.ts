// E2E spec para el flujo de publicacion.

import { test, expect } from "@playwright/test";

test.describe("publicar-articulo", () => {
  test("la pagina publica redirige a /login si no hay sesion", async ({ page }) => {
    await page.goto("/publicar-articulo");
    await expect(page).toHaveURL(/\/login/);
  });

  test("el formulario se monta correctamente", async ({ page }) => {
    await page.goto("/publicar-articulo");
    // Tras redirect a /login, vemos el formulario de login.
    await expect(page.getByTestId("login-form")).toBeVisible();
  });
});