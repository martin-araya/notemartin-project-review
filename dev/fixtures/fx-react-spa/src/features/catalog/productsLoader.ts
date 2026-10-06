// Loader para la ruta /catalog. Vive en el router, no en el componente.
// Trampa del ecosistema #1: la logica de fetch esta AQUI, no en ProductListPage.

import type { LoaderFunctionArgs } from "react-router-dom";
import { API_BASE_URL } from "../../lib/env.js";
import type { Product, Paginated } from "../../types/index.js";

export async function productsLoader({ request }: LoaderFunctionArgs) {
  const url = new URL(request.url);
  const category = url.searchParams.get("category") ?? undefined;
  const query = url.searchParams.get("q") ?? undefined;
  const page = Number(url.searchParams.get("page") ?? "1");
  const params = new URLSearchParams();
  if (category) params.set("category", category);
  if (query) params.set("q", query);
  params.set("page", String(page));
  const res = await fetch(`${API_BASE_URL}/products?${params.toString()}`);
  if (!res.ok) {
    throw new Response(`Error cargando productos: ${res.status}`, {
      status: res.status,
    });
  }
  return (await res.json()) as Paginated<Product>;
}