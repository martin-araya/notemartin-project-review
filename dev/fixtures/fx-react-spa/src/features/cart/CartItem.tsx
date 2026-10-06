// CartItem envuelta en forwardRef + memo + HOC withLogger.
// Trampa del paquete #3: orden `memo(forwardRef(Inner))` (memo afuera) vs el
// `forwardRef(memo(Inner))` de Button.tsx. Ademas, trampa #6: displayName
// falso (`'CartLineItem'`) despista a la skill.

import { forwardRef, memo } from "react";
import { withLogger } from "../../components/HOCs/withLogger.jsx";
import type { CartItem } from "../../types/index.js";
import { Button } from "../../components/Button.jsx";

interface Props {
  item: CartItem;
  onRemove: (productId: string) => void;
}

function CartItemInner({ item, onRemove }: Props, ref: React.Ref<HTMLLIElement>) {
  return (
    <li ref={ref} className="cart-item" data-testid={`cart-item-${item.productId}`}>
      <span className="product-id">{item.productId}</span>
      <span className="quantity">x{item.quantity}</span>
      <span className="unit-price">{(item.unitPrice * item.quantity).toFixed(2)} EUR</span>
      <Button variant="danger" onClick={() => onRemove(item.productId)}>
        Quitar
      </Button>
    </li>
  );
}

const Forwarded = forwardRef<HTMLLIElement, Props>(CartItemInner);
const Memoized = memo(Forwarded);

export const LoggedCartItem = withLogger(Memoized, "CartLineItem");

LoggedCartItem.displayName = "CartLineItem";

export default LoggedCartItem;