# Fixture fx-react-spa (F06g)

SPA React 19 con TypeScript que combina data routers, RTK Query, React Hook Form,
i18next y varios HOCs. Plantada para que la skill tenga que rastrear indirecciones:

- `loader`/`action` viven en `routes/router.tsx`, no en los componentes.
- Hooks autogenerados por `createApi` (`useGetProductsQuery`, etc.) no tienen
  definicion literal: se generan a partir de los endpoints en `api/baseApi.ts`.
- `main.tsx` envuelve la app en 6 providers en un orden especifico.
- Cadenas de `useEffect` en `features/catalog/catalog.hooks.ts`.
- Variables `import.meta.env.VITE_*` resueltas en build.
- Componentes envueltos en `memo`/`forwardRef`/HOC + `Suspense` + `ErrorBoundary`.

## Trampas plantadas

1. loader/action de rutas lazy - `routes/router.tsx` define loaders y actions.
2. Hooks autogenerados - `api/baseApi.ts` con `createApi`; los hooks se importan
   en features pero no estan definidos literalmente.
3. Providers anidados - 6 providers en `main.tsx` en orden especifico.
4. Cadenas de useEffect - `features/catalog/catalog.hooks.ts` con dos efectos
   consecutivos que comparten state.
5. import.meta.env.VITE_* - `lib/env.ts` lee las variables de build.
6. memo/forwardRef/HOC + Suspense + ErrorBoundary - `components/Button.tsx`,
   `features/cart/CartItem.tsx`, `routes/ErrorBoundary.tsx`, `main.tsx`.

## Construir

```bash
make build
```

## Probar

```bash
make test
```

Los tests viven en `tests/*.test.tsx` y se ejecutan con vitest + jsdom + MSW v2
+ Testing Library.