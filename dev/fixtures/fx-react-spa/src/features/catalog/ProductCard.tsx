// ProductCard envuelta en memo (trampa del ecosistema #6: memo + displayName).
// El componente exportado NO es ProductCard; es MemoizedProductCard. La
// busqueda por nombre "ProductCard" falla.

import { memo } from "react";
import type { Product } from "../../types/index.js";
import { Button } from "../../components/Button.jsx";

interface Props {
  product: Product;
  onAddToCart: (id: string) => void;
}

function ProductCardInner({ product, onAddToCart }: Props) {
  return (
    <article
      className="product-card"
      data-testid={`product-${product.id}`}
      data-product-id={product.id}
    >
      <h3>{product.name}</h3>
      <p>{product.description}</p>
      <span className="price">{product.price.toFixed(2)} EUR</span>
      <Button
        variant="primary"
        onClick={() => onAddToCart(product.id)}
        data-testid={`add-${product.id}`}
      >
        Anadir al carrito
      </Button>
    </article>
  );
}

export const MemoizedProductCard = memo(ProductCardInner);
MemoizedProductCard.displayName = "ProductCard";