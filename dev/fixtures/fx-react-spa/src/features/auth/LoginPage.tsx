// Pagina de login.
// Trampa del paquete #1: useEffect con dependencias incorrectas - lee
// searchParams sin declararlo en deps.

import { useEffect, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { loginSchema, type LoginInput } from "./auth.schema.js";
import { useAuthActions } from "./auth.hooks.js";
import { Button } from "../../components/Button.jsx";

export default function LoginPage() {
  const navigate = useNavigate();
  const [params] = useSearchParams();
  const [submitting, setSubmitting] = useState(false);
  const { login } = useAuthActions();

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginInput>({
    resolver: zodResolver(loginSchema),
    defaultValues: { email: "", password: "" },
  });

  // Trampa #1: el effect no declara `params` ni `setSubmitting` en deps.
  // En la practica corre una sola vez al montar; en estricto mode correria dos.
  useEffect(() => {
    setSubmitting(false);
  }, []);

  async function onSubmit(values: LoginInput) {
    setSubmitting(true);
    try {
      await login(values.email, values.password);
      const redirectTo = params.get("redirect") ?? "/catalog";
      navigate(redirectTo);
    } catch {
      // el toast ya se mostro en el hook
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <main className="login-page" data-testid="login-page">
      <h1>Iniciar sesion</h1>
      <form onSubmit={handleSubmit(onSubmit)} noValidate>
        <label htmlFor="email">Correo electronico</label>
        <input
          id="email"
          type="email"
          autoComplete="email"
          {...register("email")}
          data-testid="email-input"
        />
        {errors.email && (
          <span role="alert" data-error="email">
            {errors.email.message}
          </span>
        )}

        <label htmlFor="password">Contrasena</label>
        <input
          id="password"
          type="password"
          autoComplete="current-password"
          {...register("password")}
          data-testid="password-input"
        />
        {errors.password && (
          <span role="alert" data-error="password">
            {errors.password.message}
          </span>
        )}

        <Button type="submit" disabled={submitting} data-testid="submit-login">
          {submitting ? "Entrando..." : "Entrar"}
        </Button>
      </form>
    </main>
  );
}