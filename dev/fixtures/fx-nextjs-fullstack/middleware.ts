// middleware.ts de Next.js (trampa ecosistema #4).
// Este archivo vive en la RAIZ del proyecto, NO en app/. Es uno de los
// archivos de "magic location" de Next.js (igual que instrumentation.ts).

import { NextRequest, NextResponse } from "next/server";

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  const hasSession = request.cookies.has("fxnext-session");

  // Las rutas bajo /panel-admin requieren sesion. Si no hay cookie,
  // mandamos al usuario a /login con `from` para volver tras autenticarse.
  if (pathname.startsWith("/panel-admin") && !hasSession) {
    const loginUrl = new URL("/login", request.url);
    loginUrl.searchParams.set("from", pathname);
    return NextResponse.redirect(loginUrl);
  }

  // Encabezado de debug para que las trampas del paquete que inspeccionan
  // headers tengan donde mirar.
  const response = NextResponse.next();
  response.headers.set("x-fxnext-middleware", "ran");
  return response;
}

// Matcher: solo se ejecuta en rutas que NO son assets estaticos ni API
// publica. Es la convencion de Next.js para evitar coste en cada request.
export const config = {
  matcher: ["/((?!_next/static|_next/image|favicon.ico|api/health).*)"],
};