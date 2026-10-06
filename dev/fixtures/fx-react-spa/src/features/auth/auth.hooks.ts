// Hooks de sesion: usa useLoginMutation y useRegisterMutation generados
// por createApi en api/baseApi.ts. Trampa del ecosistema #2: las funciones NO
// estan definidas literalmente en este archivo; vienen del baseApi.

import { useAppDispatch } from "../../store/hooks.js";
import { loginSuccess, logout } from "../../store/slices/auth.slice.js";
import { showToast } from "../../components/Toast.jsx";
import { SESSION_STORAGE_KEY } from "../../lib/env.js";
import { useLoginMutation, useRegisterMutation } from "../../api/baseApi.js";

export function useAuthActions() {
  const dispatch = useAppDispatch();
  const [loginTrigger] = useLoginMutation();
  const [registerTrigger] = useRegisterMutation();

  async function login(email: string, password: string) {
    try {
      const res = await loginTrigger({ email, password }).unwrap();
      dispatch(loginSuccess({ user: res.user, token: res.token }));
      sessionStorage.setItem(
        SESSION_STORAGE_KEY,
        JSON.stringify({ user: res.user, token: res.token }),
      );
      showToast("Sesion iniciada", "success");
      return res;
    } catch (err) {
      showToast("Credenciales invalidas", "error");
      throw err;
    }
  }

  async function registerAccount(email: string, password: string, confirmPassword: string) {
    try {
      const user = await registerTrigger({ email, password, confirmPassword }).unwrap();
      showToast("Cuenta creada", "success");
      return user;
    } catch (err) {
      showToast("No se pudo crear la cuenta", "error");
      throw err;
    }
  }

  function logoutAndRedirect() {
    sessionStorage.removeItem(SESSION_STORAGE_KEY);
    dispatch(logout());
  }

  return { login, register: registerAccount, logout: logoutAndRedirect };
}