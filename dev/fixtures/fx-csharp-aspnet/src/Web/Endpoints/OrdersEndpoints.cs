using FxAspNet.Features.Pedidos.Commands;
using FxAspNet.Features.Pedidos.Queries;
using MediatR;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Routing;

namespace FxAspNet.Web.Endpoints;

public static class OrdersEndpoints
{
    public static IEndpointRouteBuilder MapOrdersEndpoints(this IEndpointRouteBuilder endpoints)
    {
        var grupo = endpoints.MapGroup("/api/orders");

        grupo.MapPost("/", async (IMediator mediator, CrearPedidoCommand cmd, CancellationToken token) =>
        {
            try
            {
                var id = await mediator.Send(cmd, token);
                return Results.Created($"/api/orders/{id}", new { id });
            }
            catch (InvalidOperationException ex) when (ex.Message == "cliente_requerido")
            {
                return Results.BadRequest(new { error = "cliente_requerido" });
            }
            catch (InvalidOperationException ex) when (ex.Message == "items_requeridos")
            {
                return Results.BadRequest(new { error = "items_requeridos" });
            }
        });

        grupo.MapGet("/{id:int}", async (IMediator mediator, int id, CancellationToken token) =>
        {
            var pedido = await mediator.Send(new ObtenerPedidoQuery(id), token);
            return pedido is null ? Results.NotFound() : Results.Ok(pedido);
        });

        grupo.MapGet("/", async (IMediator mediator, int? pagina, int? tamano, CancellationToken token) =>
        {
            var ids = await mediator.Send(new ListarPedidosQuery(pagina ?? 0, tamano ?? 50), token);
            return Results.Ok(ids);
        });

        grupo.MapGet("/health", () => Results.Ok(new { status = "ok" }));

        return endpoints;
    }
}