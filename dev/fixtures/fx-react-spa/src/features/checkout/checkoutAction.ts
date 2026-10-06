// Action para la ruta /checkout (trampa del ecosistema #1: vive en el router).
import { redirect as routerRedirect } from "react-router-dom";
import { API_BASE_URL, TOKEN_HEADER, TOKEN_PREFIX } from "../../lib/env.js";
import { getStore } from "../../store/index.js";
import { showToast } from "../../components/Toast.jsx";

export interface CheckoutFormData {
  cardNumber: string;
  expiry: string;
  cvv: string;
}

export async function checkoutAction({ request }: { request: Request }) {
  const form = await request.formData();
  const data: CheckoutFormData = {
    cardNumber: String(form.get("cardNumber") ?? ""),
    expiry: String(form.get("expiry") ?? ""),
    cvv: String(form.get("cvv") ?? ""),
  };

  if (data.cardNumber.replace(/\D/g, "").length < 13) {
    showToast("Numero de tarjeta invalido", "error");
    return { ok: false, error: "invalid_card" };
  }

  const state = getStore().getState();
  if (!state.cart.items.length) {
    return routerRedirect("/cart");
  }

  const res = await fetch(`${API_BASE_URL}/orders`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...(state.auth.token
        ? { [TOKEN_HEADER]: `${TOKEN_PREFIX}${state.auth.token}` }
        : {}),
    },
    body: JSON.stringify({ items: state.cart.items }),
  });

  if (!res.ok) {
    showToast("Error al procesar el pago", "error");
    return { ok: false, error: `http_${res.status}` };
  }

  showToast("Pedido creado", "success");
  return routerRedirect("/orders");
}