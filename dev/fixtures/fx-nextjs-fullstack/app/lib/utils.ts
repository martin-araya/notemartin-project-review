// Utilidades varias.
// Trampa superficial #1: formatDate existe pero nadie lo importa.

export function formatDate(value: Date | string | null | undefined): string {
  if (!value) return "";
  const d = value instanceof Date ? value : new Date(value);
  return new Intl.DateTimeFormat("es-ES", { dateStyle: "medium" }).format(d);
}

export function slugify(value: string): string {
  return value
    .toLowerCase()
    .trim()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 64);
}

export function excerpt(body: string, max = 120): string {
  if (body.length <= max) return body;
  return body.slice(0, max - 1).trimEnd() + "...";
}