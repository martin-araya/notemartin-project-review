// ErrorBoundary global para rutas que no capturan su error.
// Trampa del ecosistema #6: se monta como errorElement en el router; la skill
// debe notar que define una ruta de error separada del flujo principal.

import { Component, type ReactNode } from "react";

interface Props {
  children?: ReactNode;
  message?: string;
}

interface State {
  hasError: boolean;
  message: string;
}

export class ErrorBoundary extends Component<Props, State> {
  state: State = { hasError: false, message: "" };

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, message: error.message };
  }

  componentDidCatch(error: Error) {
    console.error("[fx-react-spa] ErrorBoundary capturo:", error);
  }

  render() {
    if (this.state.hasError || this.props.message) {
      const message = this.state.message || this.props.message || "Algo salio mal";
      return (
        <div role="alert" data-testid="error-boundary">
          <h1>Algo salio mal</h1>
          <p>{message}</p>
        </div>
      );
    }
    return this.props.children;
  }
}