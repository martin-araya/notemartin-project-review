// Schema zod compartido por LoginPage y RegisterPage.
// Trampa del paquete: la regex de email es minimal; los tests plantan
// casos en el limite.

import { z } from "zod";

export const loginSchema = z.object({
  email: z.string().email({ message: "invalid_email" }),
  password: z.string().min(8, { message: "password_too_short" }),
});

export const registerSchema = loginSchema
  .extend({
    confirmPassword: z.string().min(8, { message: "password_too_short" }),
  })
  .refine((data) => data.password === data.confirmPassword, {
    path: ["confirmPassword"],
    message: "passwords_mismatch",
  });

export type LoginInput = z.infer<typeof loginSchema>;
export type RegisterInput = z.infer<typeof registerSchema>;