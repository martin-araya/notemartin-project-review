// Route Handler de health check (no protegido por middleware).

import { NextResponse } from "next/server";

export function GET() {
  return NextResponse.json({ status: "ok", ts: Date.now() });
}