// Hook del panel de pedidos.
// Trampa del paquete #4: pollingInterval de 1 segundo combinado con
// refetchOnFocus dispara fetches encadenados en cuanto el usuario interactua.

import { useGetOrdersQuery } from "../../api/baseApi.js";
import type { Order } from "../../types/index.js";

export function useOrdersPolling(status?: Order["status"], page = 1) {
  return useGetOrdersQuery(
    { status, page },
    {
      pollingInterval: 1000,
      refetchOnFocus: true,
      refetchOnReconnect: true,
    },
  );
}