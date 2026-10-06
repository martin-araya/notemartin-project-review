// Detalle de producto. Usa useGetProductQuery (autogenerado).

import { useParams } from "react-router-dom";
import { useGetProductQuery } from "../../api/baseApi.js";
import { useCart } from "../../hooks/useCart.js";
import { Button } from "../../components/Button.jsx";

export default function ProductDetailPage() {
  const { id = "" } = useParams<{ id: string }>();
  const { data, isLoading, isError } = useGetProductQuery(id);
  const { add } = useCart();

  if (isLoading) return <p data-testid="loading">Cargando...</p>;
  if (isError || !data) return <p role="alert">Producto no encontrado</p>;

  return (
    <article className="product-detail" data-testid={`detail-${id}`}>
      <h1>{data.name}</h1>
      <p>{data.description}</p>
      <p className="price">{data.price.toFixed(2)} EUR</p>
      <p>Stock: {data.stock}</p>
      <Button onClick={() => add(data.id, data.price)}>Anadir al carrito</Button>
    </article>
  );
}