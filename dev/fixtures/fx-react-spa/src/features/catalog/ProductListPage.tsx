// Listado de productos. Usa el loader (no fetch directo) y RTK Query como
// cache. ProductCard viene memoizada desde catalog/ProductCard.

import { useLoaderData } from "react-router-dom";
import { useGetProductsQuery } from "../../api/baseApi.js";
import { MemoizedProductCard as ProductCard } from "./ProductCard.jsx";
import { useCart } from "../../hooks/useCart.js";
import { useCatalogFilters } from "./catalog.hooks.js";

export default function ProductListPage() {
  const initial = useLoaderData() as { items: { id: string }[] };
  const { add } = useCart();
  const { query, setQuery, category, setCategory } = useCatalogFilters();

  // RTK Query: usa el hook autogenerado useGetProductsQuery (trampa #2).
  const { data, isLoading, isError } = useGetProductsQuery({ category, query });

  const items = data?.items ?? initial.items;

  return (
    <main className="catalog-page" data-testid="catalog-page">
      <h1>Catalogo</h1>

      <div className="filters">
        <input
          type="search"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Buscar..."
          data-testid="search-input"
        />
        <select
          value={category ?? ""}
          onChange={(e) => setCategory(e.target.value || undefined)}
          data-testid="category-select"
        >
          <option value="">Todas</option>
          <option value="books">Libros</option>
          <option value="electronics">Electronica</option>
          <option value="clothing">Ropa</option>
        </select>
      </div>

      {isLoading && <p data-testid="loading">Cargando...</p>}
      {isError && <p role="alert" data-testid="error">Error al cargar productos</p>}

      <div className="grid">
        {items.length === 0 && !isLoading && <p data-testid="no-results">Sin resultados</p>}
        {items.map((p: { id: string; name: string; price: number; description: string }) => (
          <ProductCard
            key={p.id}
            product={p as never}
            onAddToCart={(id) => add(id, p.price)}
          />
        ))}
      </div>
    </main>
  );
}