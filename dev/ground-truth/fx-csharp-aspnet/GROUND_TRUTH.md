# Ground truth de fx-csharp-aspnet (F06o)

API **ASP.NET Core 9** con patron **CQRS** via **MediatR 11**,
persistencia con **EF Core 9** sobre **SQLite**, **minimal APIs**
y un **BackgroundService** para reintentos en segundo plano.
Plantada para que la skill tenga que rastrear las trampas clasicas
del ecosistema C# / .NET.

## Features

1. **pedidos** (FEAT-001): crear, obtener por id, listar.
   7 R-NN (CC-03).
2. **facturacion** (FEAT-002): emitir factura desde pedido,
   marcar pagada, listar. 7 R-NN.
3. **reintentos** (FEAT-003): encolar trabajo, listar pendientes,
   ack. 7 R-NN.

## Trampas del ecosistema (CC-06)

1. `mediator_dispatch_by_type`: handler resuelto por tipo generico
   `IRequestHandler<TRequest, TResponse>` (sin mapeo literal).
2. `efcore_fluent_no_dataannotations`: todo en Fluent API en
   `OnModelCreating` + `IEntityTypeConfiguration<T>`, sin `[Key]`.
3. `source_generators_not_in_repo`: MediatR usa source generators
   que no estan en el repositorio.
4. `partial_class_split`: `PedidoItem`, `CrearPedidoHandler`,
   `ObtenerPedidoHandler` y `EncolarTrabajoHandler` son
   `partial class` repartidas en dos archivos cada una.
5. `middleware_pipeline_order`: `UseExceptionHandler` registrado
   despues de `MapEndpoints`; `UseRequestId()` declarado pero no
   invocado.
6. `extension_method_registration`: `AddOrdersModule()` declarado
   pero no llamado desde `Program.cs`.

## Trampas del paquete (CC-04)

1. `handler_throws_no_handler_mapeado`: solo dos mensajes de error
   del handler se traducen a 400; el resto burbujea a 500.
2. `mediator_silent_no_handler`: `ComandoSinHandler` sin handler
   falla en runtime, no en build.
3. `efcore_no_transaction_envelope`: dos `SaveChangesAsync` sin
   transaccion en `CrearPedidoHandler`.
4. `background_no_update_ultimo_intento`: el BackgroundService
   loguea fallos pero no actualiza `UltimoIntentoEn`.
5. `endpoint_group_route_prefix`: `MapGet("/")` y
   `MapGet("/{id:int}")` conviven en el mismo grupo.
6. `sqlite_inmemory_shared_cache_required`: el factory usa
   `cache=shared` para que WebApplicationFactory reuse la DB.

## Trampas superficiales (CC-05)

1. `dead_validator`: `CrearPedidoValidator.cs` nunca invocado.
2. `dead_logger_field`: `AppDbContext._log` declarado y no usado.
3. `dead_endpoint`: `MapGet("/api/orders/health")` retorna 200 OK
   literal, no usado por tests.

## Archivos clave del fixture

- `FxAspNet.csproj`: `net9.0`, MediatR 11.0.0,
  EF Core Sqlite 9.0.0, EF Core Design 9.0.0.
- `Program.cs`: top-level statements + `public partial class Program { }`
  al final + pipeline de middleware en orden deliberado.
- `appsettings.json`: `ConnectionStrings:Default` con SQLite.
- `src/Domain/Pedidos/`: Pedido.cs, PedidoItem.cs (partial),
  PedidoItem.ParteB.cs (partial), PedidoEstado.cs.
- `src/Domain/Facturacion/`: Factura.cs, FacturaEstado.cs.
- `src/Domain/Reintentos/`: TrabajoPendiente.cs, TrabajoEstado.cs.
- `src/Infrastructure/Persistence/`: AppDbContext.cs + DbInitializer.cs +
  Configurations/{Pedido,PedidoItem,Factura,Trabajo}Configuration.cs
  (toda la configuracion del modelo en Fluent API).
- `src/Infrastructure/Mediator/`: MediatorRegistration.cs
  (`AddOrdersModule()` extension no invocada).
- `src/Infrastructure/Background/`: ReintentosBackgroundService.cs
  (procesa cola cada 5s).
- `src/Features/Pedidos/`: Commands/{CrearPedidoCommand,
  CrearPedidoHandler (partial), CrearPedidoHandler.ParteB,
  CrearPedidoValidator (dead), ComandoSinHandler} +
  Queries/{ObtenerPedidoQuery, ObtenerPedidoHandler (partial),
  ObtenerPedidoHandler.ParteB, ListarPedidosQuery, ListarPedidosHandler}.
- `src/Features/Facturacion/`: Commands/{EmitirFacturaCommand,
  EmitirFacturaHandler, MarcarPagadaCommand, MarcarPagadaHandler} +
  Queries/{ObtenerFacturaQuery, ObtenerFacturaHandler,
  ListarFacturasQuery, ListarFacturasHandler}.
- `src/Features/Reintentos/`: TrabajoCommands.cs +
  EncolarTrabajoHandler.cs (partial) +
  EncolarTrabajoHandler.ParteB.cs (partial) +
  ListarPendientesHandler.cs + AckTrabajoHandler.cs.
- `src/Web/Endpoints/`: OrdersEndpoints.cs,
  BillingEndpoints.cs, RetriesEndpoints.cs (MapGroup minimal API).
- `src/Web/Middleware/`: RequestIdMiddleware.cs +
  RequestIdMiddlewareExtensions.cs (extension `UseRequestId()` no
  invocada).
- `tests/FxAspNet.Tests/`: Fixtures/FxAspNetFactory.cs +
  Features/{Pedidos,Facturacion,Reintentos}Tests.cs +
  Trampas/{TrampasEcosistema,TrampasPaquete,TrampasSuperficiales}Tests.cs.