// Hook que combina el cart slice con RTK Query para mantener stock sincronizado.
// Trampa del ecosistema #3: depende del orden de providers para tener acceso
// al store y al QueryClient.

import { useDispatch, useSelector } from "react-redux";
import type { RootState, AppDispatch } from "../store/index.js";
import { addItem, removeItem } from "../store/slices/cart.slice.js";

export function useCart() {
  const dispatch = useDispatch<AppDispatch>();
  const items = useSelector((state: RootState) => state.cart.items);

  return {
    items,
    add: (productId: string, unitPrice: number, quantity = 1) =>
      dispatch(addItem({ productId, unitPrice, quantity })),
    remove: (productId: string) => dispatch(removeItem(productId)),
  };
}