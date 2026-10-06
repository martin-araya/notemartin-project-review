# Fixture F06l — fx-angular-ngrx

Aplicacion **Angular 17** empresarial con NgModules + standalone
(en migracion parcial), NgRx (store, effects, entity), RxJS
intensivo, `@angular/material` para UI. Plantada para que la skill
tenga que rastrear indirecciones del ecosistema Angular/NgRx:
flujo `action -> effect -> service -> action`,
`createActionGroup`, operadores RxJS (`switchMap`, `mergeMap`,
`exhaustMap`), `forRoot`/`forChild`, `HTTP_INTERCEPTORS` con
`multi: true`, pipes y directivas personalizados.

## Stack

- **Frontend:** Angular 17 + `@angular/material` 17.
- **Estado:** NgRx 17 (store, effects, entity, devtools).
- **RxJS:** 7.8 con operadores reactivos.
- **Forms:** Reactive Forms Module.
- **Tests:** Jest 29 + `jest-preset-angular` 14 + `jasmine-marbles`
  0.9 para tests de effects.

## Como se ejecutan los tests

```bash
make test           # npx jest --runInBand
make build          # ng build (opcional)
make history        # regenera la historia git (8 commits)
```

En contenedor (con Chrome headless):

```bash
python dev/tools/run_fixture_tests.py --fixture fx-angular-ngrx --container
```

## Estructura

- `angular.json`: workspace con proyectos `app`, `solicitudes`,
  `aprobaciones`, `reportes`, `shared`.
- `tsconfig.json` + `tsconfig.app.json` + `tsconfig.spec.json`.
- `src/main.ts`: `bootstrapApplication` con `importProvidersFrom`.
- `src/app/app.{component,config,routes}.ts`: providers,
  router-outlet, rutas lazy.
- `src/app/core/`: `core.module.ts` (forRoot con HTTP_INTERCEPTORS),
  `interceptors/{auth,logging}.interceptor.ts`,
  `services/api.service.ts`, `pipes/monto.pipe.ts`,
  `directives/contador.directive.ts`.
- `src/app/solicitudes/`: `solicitudes.module.ts` (forChild del
  feature state), `store/{actions,reducer,effects,selectors,state}.ts`,
  `pages/{lista,detalle,nueva}.component.ts`.
- `src/app/aprobaciones/`: `aprobaciones.module.ts`, store con
  cross-feature effect a `solicitudes`.
- `src/app/reportes/`: `reportes.module.ts`, `reportes.component.ts`
  con selector computado + MontoPipe.
- `tests/`: 8 archivos Jest.

## Features

1. **gestion-de-solicitudes** (FEAT-001): list, create, update,
   filter. 7 R-NN.
2. **aprobaciones** (FEAT-002): cola, approve, reject con
   cross-feature effect. 7 R-NN.
3. **reportes** (FEAT-003): load, filter, export CSV. 7 R-NN.

## Trampas plantadas

- 6 del ecosistema (CC-06): flujo action->effect->service, 
  createActionGroup, operadores RxJS, forRoot/forChild,
  HTTP_INTERCEPTORS multi, pipes/directivas custom.
- 6 del paquete (CC-04): observable vacio, switchMap+mergeMap
  combinados, AuthInterceptor SSR-incompatible, pipe no pure,
  entity adapter sin selectId custom, provideStore duplicado.
- 3 superficiales (CC-05): apiBase inutil, imports muertos, export
  publico no usado.