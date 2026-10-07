# Fixture F06o — fx-csharp-aspnet

API **ASP.NET Core 9** con patron **CQRS** via **MediatR 11**,
persistencia con **EF Core 9** sobre **SQLite**, **minimal APIs**
y un **BackgroundService** para reintentos en segundo plano.
Plantada para que la skill tenga que rastrear las trampas clasicas
del ecosistema C# / .NET.

## Stack

- **Lenguaje:** C# 13 sobre `.NET 9`.
- **Framework:** ASP.NET Core 9 (minimal APIs + MapGroup).
- **CQRS / Mediator:** MediatR 11.0.0 (ultima version MIT).
- **Persistencia:** EF Core 9 (Microsoft.EntityFrameworkCore.Sqlite) +
  Microsoft.EntityFrameworkCore.Design.
- **Background:** Microsoft.Extensions.Hosting (BackgroundService).
- **Tests:** xUnit 2.9 + Microsoft.AspNetCore.Mvc.Testing 9
  (WebApplicationFactory<Program>) + SQLite in-memory compartido.

## Como se ejecutan los tests

```bash
make test           # dotnet test --nologo
make build          # dotnet build --nologo
make history        # regenera la historia git (8 commits)
```

En contenedor (con .NET 9 SDK):

```bash
python dev/tools/run_fixture_tests.py --fixture fx-csharp-aspnet --container
```

## Estructura

- `FxAspNet.csproj`: `net9.0`, MediatR 11.0.0, EF Core Sqlite 9.0.0,
  EF Core Design 9.0.0.
- `Program.cs`: top-level statements + `public partial class Program { }`
  al final + pipeline de middleware en orden deliberado.
- `appsettings.json` / `appsettings.Development.json`: cadena de conexion
  SQLite y configuracion de logging.
- `src/Domain/Pedidos/`: Pedido.cs, PedidoItem.cs (partial), PedidoEstado.cs.
- `src/Domain/Facturacion/`: Factura.cs, FacturaEstado.cs.
- `src/Domain/Reintentos/`: TrabajoPendiente.cs, TrabajoEstado.cs.
- `src/Infrastructure/Persistence/`: AppDbContext.cs + Configurations/*.
- `src/Infrastructure/Mediator/`: MediatorRegistration.cs (extension no
  invocada, trampa E06).
- `src/Infrastructure/Background/`: ReintentosBackgroundService.cs.
- `src/Features/{Pedidos,Facturacion,Reintentos}/`: Commands/, Queries/
  con handlers `partial class` repartidos en varios archivos.
- `src/Web/Endpoints/`: OrdersEndpoints.cs, BillingEndpoints.cs,
  RetriesEndpoints.cs (MapGroup minimal API).
- `src/Web/Middleware/`: RequestIdMiddleware.cs +
  RequestIdMiddlewareExtensions.cs (extension no invocada, trampa E05).
- `tests/FxAspNet.Tests/`: Fixtures/FxAspNetFactory.cs +
  Features/ + Trampas/.

## Features

1. **pedidos** (FEAT-001): crear, obtener por id, listar.
   7 R-NN (CC-03).
2. **facturacion** (FEAT-002): emitir factura desde pedido,
   marcar pagada, listar. 7 R-NN.
3. **reintentos** (FEAT-003): encolar trabajo, listar pendientes,
   ack. 7 R-NN.

## Trampas plantadas

- 6 del ecosistema (CC-06):
  1. `mediator_dispatch_by_type` — handler resuelto por tipo generico
     `IRequestHandler<TRequest, TResponse>` (sin mapeo literal).
  2. `efcore_fluent_no_dataannotations` — todo en Fluent API en
     `OnModelCreating` + `IEntityTypeConfiguration<T>`, sin `[Key]`.
  3. `source_generators_not_in_repo` — MediatR usa source generators
     que no estan en el repositorio.
  4. `partial_class_split` — `PedidoItem`, `CrearPedidoHandler`,
     `ObtenerPedidoHandler` son `partial class` repartidas.
  5. `middleware_pipeline_order` — `UseExceptionHandler` registrado
     despues de `MapEndpoints`; `UseRequestId()` declarado pero no
     invocado.
  6. `extension_method_registration` — `AddOrdersModule()` declarado
     pero no llamado desde `Program.cs`.
- 6 del paquete (CC-04):
  1. `handler_throws_no_handler` — InvalidOperationException no se mapea a
     400 por la trampa E05.
  2. `mediator_silent_no_handler` — un command sin handler falla en
     runtime, no en build.
  3. `efcore_no_transaction_envelope` — `CrearPedidoHandler` hace dos
     `SaveChangesAsync` sin transaccion.
  4. `background_no_update_ultimo_intento` — el BackgroundService
     loguea fallos pero no actualiza la BD.
  5. `endpoint_group_route_prefix_conflict` — `MapGroup("/api/orders")
     .MapGet("/")` y `MapGet("/{id:int}")` — la skill debe verificar
     el orden.
  6. `sqlite_inmemory_shared_cache_required` — el factory configura
     `cache=shared`; sin el, cada conexion ve una DB distinta.
- 3 superficiales (CC-05):
  1. `dead_validator` — `CrearPedidoValidator.cs` nunca invocado.
  2. `dead_logger_field` — `AppDbContext._log` declarado y no inyectado.
  3. `dead_endpoint` — `MapGet("/api/orders/health")` retorna `200 OK`
     literal, no usado por tests.