// AuthGuard: redirect a /login si no hay sesion.
// Trampa del ecosistema #1: usado como `loader` en el router.

import { redirect, type LoaderFunctionArgs } from "react-router-dom";
import { SESSION_STORAGE_KEY } from "../lib/env.js";

export async function authGuard({ request }: LoaderFunctionArgs) {
  if (typeof window === "undefined") return null;
  const raw = sessionStorage.getItem(SESSION_STORAGE_KEY);
  if (raw) return null;
  const url = new URL(request.url);
  const redirectTo = encodeURIComponent(url.pathname + url.search);
  throw redirect(`/login?redirect=${redirectTo}`);
}