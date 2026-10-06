// Panel de pedidos. Usa useOrdersPolling (que envuelve useGetOrdersQuery con
// pollingInterval). Carga los pedidos y los renderiza en una tabla.

import { useState } from "react";
import { useOrdersPolling } from "./orders.hooks.js";
import type { Order } from "../../types/index.js";

const STATUS_LABEL: Record<Order["status"], string> = {
  pending: "Pendiente",
  paid: "Pagado",
  shipped: "Enviado",
  delivered: "Entregado",
};

export default function OrdersPanelPage() {
  const [status, setStatus] = useState<Order["status"] | undefined>();
  const { data, isLoading, isError, refetch } = useOrdersPolling(status);

  return (
    <main className="orders-page" data-testid="orders-page">
      <h1>Mis pedidos</h1>

      <div className="filters">
        <label htmlFor="status-filter">Estado</label>
        <select
          id="status-filter"
          value={status ?? ""}
          onChange={(e) => setStatus((e.target.value || undefined) as Order["status"] | undefined)}
          data-testid="status-filter"
        >
          <option value="">Todos</option>
          <option value="pending">Pendiente</option>
          <option value="paid">Pagado</option>
          <option value="shipped">Enviado</option>
        </select>

        <button type="button" onClick={() => refetch()} data-testid="refresh-orders">
          Refrescar
        </button>
      </div>

      {isLoading && <p data-testid="loading">Cargando...</p>}
      {isError && <p role="alert">Error al cargar pedidos</p>}

      {data && data.items.length === 0 && (
        <p data-testid="no-orders">Aun no tienes pedidos</p>
      )}

      {data && data.items.length > 0 && (
        <table data-testid="orders-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Total</th>
              <th>Estado</th>
              <th>Fecha</th>
            </tr>
          </thead>
          <tbody>
            {data.items.map((o) => (
              <tr key={o.id} data-testid={`order-${o.id}`}>
                <td>{o.id}</td>
                <td>{o.total.toFixed(2)} EUR</td>
                <td data-status={o.status}>{STATUS_LABEL[o.status]}</td>
                <td>{new Date(o.createdAt).toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </main>
  );
}