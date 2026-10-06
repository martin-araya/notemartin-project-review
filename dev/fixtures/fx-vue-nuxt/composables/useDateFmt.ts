// composables/useDateFmt.ts
// Composable con un helper de formato de fecha. Existe pero ninguna
// pagina ni componente lo invoca. El grep en pages/ y components/
// confirma que es codigo muerto del paquete.
export function useDateFmt() {
  function formatDate(value: string | Date): string {
    const d = value instanceof Date ? value : new Date(value);
    if (Number.isNaN(d.getTime())) return '';
    const y = d.getFullYear();
    const m = String(d.getMonth() + 1).padStart(2, '0');
    const day = String(d.getDate()).padStart(2, '0');
    return `${y}-${m}-${day}`;
  }
  return { formatDate };
}
