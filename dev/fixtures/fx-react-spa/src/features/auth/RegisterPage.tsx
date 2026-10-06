// Pagina de registro. Export named (vs default de LoginPage) para que la
// skill note la inconsistencia y mapee imports correctamente.

import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { registerSchema, type RegisterInput } from "./auth.schema.js";
import { useAuthActions } from "./auth.hooks.js";
import { Button } from "../../components/Button.jsx";

export function RegisterPage() {
  const navigate = useNavigate();
  const { register: registerAccount } = useAuthActions();
  const [submitting, setSubmitting] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<RegisterInput>({
    resolver: zodResolver(registerSchema),
  });

  async function onSubmit(values: RegisterInput) {
    setSubmitting(true);
    try {
      await registerAccount(values.email, values.password, values.confirmPassword);
      navigate("/catalog");
    } catch {
      // toast handled in hook
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <main className="register-page" data-testid="register-page">
      <h1>Crear cuenta</h1>
      <form onSubmit={handleSubmit(onSubmit)} noValidate>
        <label htmlFor="reg-email">Correo electronico</label>
        <input id="reg-email" type="email" {...register("email")} />
        {errors.email && <span role="alert">{errors.email.message}</span>}

        <label htmlFor="reg-password">Contrasena</label>
        <input id="reg-password" type="password" {...register("password")} />
        {errors.password && <span role="alert">{errors.password.message}</span>}

        <label htmlFor="reg-confirm">Confirmar contrasena</label>
        <input
          id="reg-confirm"
          type="password"
          {...register("confirmPassword")}
          data-testid="confirm-password-input"
        />
        {errors.confirmPassword && (
          <span role="alert" data-testid="confirm-error">
            {errors.confirmPassword.message}
          </span>
        )}

        <Button type="submit" disabled={submitting} data-testid="submit-register">
          {submitting ? "Creando..." : "Crear cuenta"}
        </Button>
      </form>
    </main>
  );
}