// Utilidades del carrito.
// Trampa superficial: formatPrice existe pero no se usa en ningun componente.

export function subtotal(items: { unitPrice: number; quantity: number }[]): number {
  return items.reduce((acc, i) => acc + i.unitPrice * i.quantity, 0);
}

export function taxes(subtotalValue: number, rate = 0.21): number {
  return Math.round(subtotalValue * rate * 100) / 100;
}

export function formatPrice(value: number, locale = "es-ES"): string {
  return new Intl.NumberFormat(locale, { style: "currency", currency: "EUR" }).format(value);
}

export function emptyCart(items: { productId: string }[]): boolean {
  return items.length === 0;
}