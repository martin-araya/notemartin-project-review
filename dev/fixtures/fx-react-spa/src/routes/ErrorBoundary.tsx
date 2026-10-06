// ErrorBoundary para rutas (trampa del ecosistema #6: define una ruta de
// error separada del flujo principal).

import { isRouteErrorResponse, useRouteError } from "react-router-dom";
import { ErrorBoundary } from "../components/ErrorBoundary.jsx";

export function RouteErrorBoundary() {
  const error = useRouteError();
  const message = isRouteErrorResponse(error)
    ? `${error.status} ${error.statusText}`
    : error instanceof Error
      ? error.message
      : "Unknown error";
  return <ErrorBoundary message={message} />;
}