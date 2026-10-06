// Pagina del carrito.
import { useAppSelector } from "../../store/hooks.js";
import { subtotal } from "./cart.utils.js";
import LoggedCartItem from "./CartItem.jsx";
import { useCart } from "../../hooks/useCart.js";

export default function CartPage() {
  const items = useAppSelector((s) => s.cart.items);
  const { remove } = useCart();

  if (items.length === 0) {
    return (
      <main className="cart-page" data-testid="cart-page">
        <h1>Carrito</h1>
        <p data-testid="cart-empty">Carrito vacio</p>
      </main>
    );
  }

  return (
    <main className="cart-page" data-testid="cart-page">
      <h1>Carrito</h1>
      <ul data-testid="cart-list">
        {items.map((item) => (
          <LoggedCartItem
            key={item.productId}
            item={item}
            onRemove={(id) => remove(id)}
          />
        ))}
      </ul>
      <footer className="cart-footer">
        <span>Subtotal: {subtotal(items).toFixed(2)} EUR</span>
      </footer>
    </main>
  );
}