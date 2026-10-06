// Pagina de checkout. Usa useForm + zodResolver; el submit va al action
// del router, no a una mutacion directa.

import { Form } from "react-router-dom";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Button } from "../../components/Button.jsx";

const checkoutSchema = z.object({
  cardNumber: z.string().regex(/^\d{13,19}$/, { message: "invalid_card_number" }),
  expiry: z.string().regex(/^(0[1-9]|1[0-2])\/\d{2}$/, { message: "invalid_expiry" }),
  cvv: z.string().regex(/^\d{3,4}$/, { message: "invalid_cvv" }),
});

export type CheckoutInput = z.infer<typeof checkoutSchema>;

export default function CheckoutPage() {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<CheckoutInput>({
    resolver: zodResolver(checkoutSchema),
    mode: "onBlur",
  });

  return (
    <main className="checkout-page" data-testid="checkout-page">
      <h1>Finalizar compra</h1>
      <Form method="post" onSubmit={handleSubmit(() => undefined)}>
        <label htmlFor="card">Numero de tarjeta</label>
        <input
          id="card"
          type="text"
          inputMode="numeric"
          {...register("cardNumber")}
          data-testid="card-input"
        />
        {errors.cardNumber && <span role="alert" data-error="cardNumber">{errors.cardNumber.message}</span>}

        <label htmlFor="expiry">Vencimiento (MM/AA)</label>
        <input
          id="expiry"
          type="text"
          {...register("expiry")}
          data-testid="expiry-input"
        />
        {errors.expiry && <span role="alert" data-error="expiry">{errors.expiry.message}</span>}

        <label htmlFor="cvv">CVV</label>
        <input
          id="cvv"
          type="text"
          inputMode="numeric"
          {...register("cvv")}
          data-testid="cvv-input"
        />
        {errors.cvv && <span role="alert" data-error="cvv">{errors.cvv.message}</span>}

        <Button type="submit" data-testid="submit-checkout">Pagar</Button>
      </Form>
    </main>
  );
}