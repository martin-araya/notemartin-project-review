// E2E spec para el panel de admin (trampa middleware).

import { test, expect } from "@playwright/test";

test.describe("panel-admin", () => {
  test("redirige a /login si no hay sesion (middleware)", async ({ page }) => {
    await page.goto("/panel-admin");
    await expect(page).toHaveURL(/\/login/);
    // El param `from` debe estar presente (lo inserta el middleware).
    const url = new URL(page.url());
    expect(url.searchParams.get("from")).toBe("/panel-admin");
  });
});