// src/lib/utils/formatDate.ts
// Helper de formato de fecha. Existe pero ninguna pagina ni
// componente lo invoca. El grep en routes/ y components/ confirma
// que es codigo muerto.
export function formatDate(value: string | Date): string {
  const d = value instanceof Date ? value : new Date(value);
  if (Number.isNaN(d.getTime())) return '';
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  return `${y}-${m}-${day}`;
}
