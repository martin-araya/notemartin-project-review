// Footer estatico. Trampa superficial #2: este componente existe pero
// el layout.tsx NO lo importa; solo esta disponible para uso manual.

export function Footer() {
  return (
    <footer style={{ borderTop: "1px solid #ddd", padding: "1rem", textAlign: "center" }}>
      <small>fx-nextjs-fullstack · fixture de F06h</small>
    </footer>
  );
}