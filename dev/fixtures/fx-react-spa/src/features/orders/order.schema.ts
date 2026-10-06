// Schema zod para Order.
import { z } from "zod";

export const orderSchema = z.object({
  id: z.string(),
  userId: z.string(),
  items: z.array(
    z.object({
      productId: z.string(),
      quantity: z.number().int().positive(),
      unitPrice: z.number().nonnegative(),
    }),
  ),
  total: z.number().nonnegative(),
  status: z.enum(["pending", "paid", "shipped", "delivered"]),
  createdAt: z.string(),
});

export type OrderParsed = z.infer<typeof orderSchema>;