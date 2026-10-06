// Pagina de listings. Trampa de paquete #3: el ``effect()`` se dispara con
// CUALQUIER cambio de signal, no solo ``filters()``.

import type { ListingFilters, PaginatedListings } from '@fx-mono/shared';

export class ListingsPage {
  static readonly name = 'ListingsPage';

  filters: ListingFilters = { page: 1, pageSize: 20 };
  loading = false;
  lastResult: PaginatedListings | null = null;
  error: string | null = null;

  // Trampa de paquete #3: el effect lee ``this`` completo. Cambia CUALQUIER
  // signal (loading, error, lastResult, filters) y vuelve a ejecutar la carga.
  // En produccion el effect deberia depender solo de ``this.filters``.
  effectRef: (() => void) | null = null;

  attachEffect(): void {
    this.effectRef = () => {
      // En produccion: ``this.api.get('/api/listings', { params: this.filters })``
      this.loading = true;
      // eslint-disable-next-line no-console
      console.log('[effect] would GET /api/listings with filters =', this.filters);
      this.lastResult = { items: [], total: 0, page: 1, pageSize: 20 };
      this.loading = false;
    };
    this.effectRef();
  }

  updateFilter(key: keyof ListingFilters, value: unknown): void {
    (this.filters as any)[key] = value;
    // Cada cambio dispara el effect completo (no solo el filtro).
    this.attachEffect();
  }
}
