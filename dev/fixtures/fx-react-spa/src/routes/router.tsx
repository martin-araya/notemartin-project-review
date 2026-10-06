// Router principal de la SPA.
// Trampa del ecosistema #1: loaders y actions viven AQUI, no en los componentes.
// Cada ruta define `loader` (carga de datos) y/o `action` (mutaciones) y luego
// `lazy` (componente lazy).

import { createBrowserRouter, Outlet } from "react-router-dom";
import LoginPage from "../features/auth/LoginPage.jsx";
import { RegisterPage } from "../features/auth/RegisterPage.jsx";
import ProductListPage from "../features/catalog/ProductListPage.jsx";
import ProductDetailPage from "../features/catalog/ProductDetailPage.jsx";
import { productsLoader } from "../features/catalog/productsLoader.js";
import CartPage from "../features/cart/CartPage.jsx";
import CheckoutPage from "../features/checkout/CheckoutPage.jsx";
import { checkoutAction } from "../features/checkout/checkoutAction.js";
import OrdersPanelPage from "../features/orders/OrdersPanelPage.jsx";
import { authGuard } from "./AuthGuard.jsx";
import { RouteErrorBoundary } from "./ErrorBoundary.jsx";
import { ErrorBoundary } from "../components/ErrorBoundary.jsx";
import { ToastHost } from "../components/Toast.jsx";

function RootLayout() {
  return (
    <>
      <ErrorBoundary>
        <Outlet />
      </ErrorBoundary>
      <ToastHost />
    </>
  );
}

export const router = createBrowserRouter([
  {
    path: "/",
    Component: RootLayout,
    errorElement: <RouteErrorBoundary />,
    children: [
      { index: true, loader: () => ({ redirect: "/catalog" }) },
      {
        path: "login",
        Component: LoginPage,
      },
      {
        path: "register",
        Component: RegisterPage,
      },
      {
        path: "catalog",
        Component: ProductListPage,
        loader: productsLoader,
      },
      {
        path: "catalog/:id",
        Component: ProductDetailPage,
        loader: authGuard,
      },
      {
        path: "cart",
        Component: CartPage,
        loader: authGuard,
      },
      {
        path: "checkout",
        Component: CheckoutPage,
        action: checkoutAction,
        loader: authGuard,
      },
      {
        path: "orders",
        Component: OrdersPanelPage,
        loader: authGuard,
      },
    ],
  },
]);