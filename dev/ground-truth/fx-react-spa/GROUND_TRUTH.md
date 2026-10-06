# Ground truth de fx-react-spa (F06g)

SPA React 19 con TypeScript que combina data routers, RTK Query, React Hook Form,
i18next y HOCs. Plantada para que la skill tenga que rastrear indirecciones:

## Features

1. **autenticacion** (FEAT-001): login, register, session restore. 7 R-NN.
2. **catalogo-y-carrito** (FEAT-002): list, filter, search, add-to-cart. 7 R-NN.
3. **checkout** (FEAT-003): form, validation, action, error propagation. 7 R-NN.
4. **panel-de-pedidos** (FEAT-004): list, filter, polling, refresh. 7 R-NN.

## Trampas del ecosistema (CC-06)

1. `loader`/`action` viven en `routes/router.tsx` + `features/catalog/productsLoader.ts` + `features/checkout/checkoutAction.ts`.
2. Hooks autogenerados por `createApi` (`useGetProductsQuery`, `useGetOrdersQuery`, `useLoginMutation`, `useRegisterMutation`) sin definicion literal.
3. 6 providers anidados en `main.tsx` en orden StoreProvider > QueryClientProvider > I18nextProvider > ThemeProvider > ToastProvider > ErrorBoundary.
4. Cadena de useEffect en `features/catalog/catalog.hooks.ts` con useDebounce.
5. Variables `import.meta.env.VITE_*` resueltas en build (Vite).
6. memo/forwardRef/HOC + Suspense + ErrorBoundary distribuidos.

## Trampas del paquete (CC-04)

1. useEffect con dependencias incorrectas en LoginPage.
2. HOC withAuth que no inyecta user.
3. Asimetria de orden memo/forwardRef entre Button y CartItem.
4. pollingInterval: 1000 + refetchOnFocus en orders.hooks.
5. Cart slice addItem muta via push (fragil fuera de Immer).
6. displayName falso en CartItem ('CartLineItem').

## Trampas superficiales (CC-05)

1. formatPrice en `cart.utils.ts` no usado.
2. Exports default vs named inconsistentes (LoginPage default, RegisterPage named).
3. `lib/msal.ts` existe pero no se importa en ningun modulo.

## Archivos clave del fixture

- `index.html`: entrada HTML
- `src/main.tsx`: bootstrap con 6 providers
- `src/App.tsx`: RootLayout
- `src/routes/router.tsx`: createBrowserRouter con loaders/actions
- `src/api/baseApi.ts`: createApi con 5 endpoints
- `src/store/index.ts`: configureStore
- `src/store/slices/auth.slice.ts`: user, token, isAuthenticated
- `src/store/slices/cart.slice.ts`: items, addItem (push), removeItem
- `src/features/{auth,catalog,cart,checkout,orders}/`: 4 features
- `src/components/{Button,ErrorBoundary,Toast,ThemeProvider,ToastProvider}.tsx`: UI base
- `src/components/HOCs/{withAuth,withLogger}.tsx`: HOCs
- `tests/{setup,handlers}.ts`: MSW + Vitest setup
- `tests/{auth,catalog,cart,checkout,orders,routing,env,providers,traps_ecosystem}.test.tsx`: 9 archivos