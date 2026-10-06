# Ground truth de fx-angular-ngrx (F06l)

Aplicacion **Angular 17** empresarial con NgModules + standalone (en
migracion parcial), NgRx (store, effects, entity), RxJS intensivo,
`@angular/material` para UI. Plantada para que la skill tenga
que rastrear indirecciones del ecosistema Angular/NgRx: flujo
`action -> effect -> service -> action`, `createActionGroup`,
operadores RxJS (`switchMap`, `mergeMap`, `exhaustMap`),
`forRoot`/`forChild`, `HTTP_INTERCEPTORS` con `multi: true`,
pipes y directivas personalizados.

## Features

1. **gestion-de-solicitudes** (FEAT-001): list, create, update,
   filter. 7 R-NN.
2. **aprobaciones** (FEAT-002): cola, approve, reject con
   cross-feature effect. 7 R-NN.
3. **reportes** (FEAT-003): load, filter, export CSV. 7 R-NN.

## Trampas del ecosistema (CC-06)

1. **action_effect_service**: load$ -> ApiService.listAll() ->
   loadSuccess/loadFailure. Trampa: listAll() retorna of([]) en
   vez del seed.
2. **create_action_group**: namespace 'Solicitudes' y
   'Aprobaciones' con acciones Load/Load Success generadas
   automaticamente.
3. **rxjs_operators**: switchMap (load), exhaustMapSafe (create),
   mergeMap (update). Cada operador tiene semantica diferente
   que cambia la cancelacion y el reintento.
4. **forRoot_forChild**: CoreModule.forRoot() via
   importProvidersFrom; SolicitudesModule.forChild via
   StoreModule.forFeature.
5. **http_interceptors_multi**: AuthInterceptor y
   LoggingInterceptor con multi: true. El orden de declaracion
   determina el orden de ejecucion.
6. **pipe_directive_custom**: MontoPipe y ContadorDirective. El
   pipe lee una variable global mutable; la directiva tiene un
   setInterval sin cleanup (memory leak).

## Trampas del paquete (CC-04)

1. **empty_observable**: ApiService.listAll retorna of([]). La UI
   nunca ve el seed.
2. **auth_interceptor_ssr**: window.localStorage en
   AuthInterceptor; en SSR el guard devuelve 'ssr-token'.
3. **pipe_not_pure**: MontoPipe lee this._currency mutable.
4. **entity_adapter_no_selectId**: createEntityAdapter sin
   selectId custom; entidades con clave distinta de 'id' no
   funcionan.
5. **provide_store_duplicate**: provideStore global +
   SolicitudesModule importProvidersFrom registran el mismo
   feature key dos veces.
6. **directive_memory_leak**: ContadorDirective implementa
   OnInit pero no OnDestroy; setInterval nunca se limpia.

## Trampas superficiales (CC-05)

1. **dead_export**: API_BASE_URL se exporta pero nadie la usa.
2. **dead_import**: ReportesComponent importa
   SolicitudesActions.
3. **dead_directive_input**: ContadorDirective expone
   fxContador como @Input publico sin uso externo.

## Archivos clave del fixture

- `angular.json`: workspace con proyectos app, solicitudes,
  aprobaciones, reportes, shared.
- `src/main.ts`: bootstrapApplication con appConfig.
- `src/app/app.config.ts`: provideStore + provideEffects +
  HTTP_INTERCEPTORS.
- `src/app/app.routes.ts`: rutas lazy.
- `src/app/core/`: core.module, services/api.service,
  interceptors/{auth,logging}, pipes/monto.pipe,
  directives/contador.directive.
- `src/app/solicitudes/`: module + store ({actions,reducer,
  effects}) + pages ({lista,nueva,detalle}).
- `src/app/aprobaciones/`: module + store + pages/cola.
- `src/app/reportes/`: module + pages/reportes.
- `src/environments/`: environment.ts + environment.prod.ts.
- `tests/`: 6 archivos Vitest estaticos (sin Angular runtime).
