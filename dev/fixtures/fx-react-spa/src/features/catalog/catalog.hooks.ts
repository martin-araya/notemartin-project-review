// Hooks del catalogo con cadena de useEffect (trampa del ecosistema #4).
// useEffect([query]) -> setDebounced(query) -> useEffect([debounced]) -> fetch.

import { useEffect, useState } from "react";
import { useDebounce } from "../../hooks/useDebounce.js";

export function useCatalogFilters(initialQuery = "") {
  const [query, setQuery] = useState(initialQuery);
  const [category, setCategory] = useState<string | undefined>();
  const debouncedQuery = useDebounce(query, 300);

  // Primer useEffect: reacciona al cambio de `query` y guarda el debounced.
  useEffect(() => {
    if (debouncedQuery.length === 0) return;
    // Solo logging; el fetch lo dispara el useGetProductsQuery al cambiar
    // sus argumentos (vía su subscribe interno).
  }, [debouncedQuery]);

  // Segundo useEffect: reacciona al cambio de `category`.
  useEffect(() => {
    // logging
  }, [category]);

  // Tercer useEffect: cuando ambos cambian a la vez, este effect se dispara
  // dos veces (una por cada cambio). Es el patron de "cadena de useEffect"
  // que dispara efectos encadenados.
  useEffect(() => {
    // logging
  }, [debouncedQuery, category]);

  return { query, setQuery, category, setCategory, debouncedQuery };
}