// Hook de debounce usado en busquedas y filtros.
// Trampa del paquete: el parametro `delay` es opt-in; el default (300ms) puede
// disparar fetches encadenados si no se acopla a un useEffect bien armado.

import { useEffect, useState } from "react";

export function useDebounce<T>(value: T, delay = 300): T {
  const [debounced, setDebounced] = useState(value);
  useEffect(() => {
    const id = setTimeout(() => setDebounced(value), delay);
    return () => clearTimeout(id);
  }, [value, delay]);
  return debounced;
}