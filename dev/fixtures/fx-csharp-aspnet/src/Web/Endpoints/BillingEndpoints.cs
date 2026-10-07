using FxAspNet.Features.Facturacion.Commands;
using FxAspNet.Features.Facturacion.Queries;
using MediatR;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Routing;

namespace FxAspNet.Web.Endpoints;

public static class BillingEndpoints
{
    public static IEndpointRouteBuilder MapBillingEndpoints(this IEndpointRouteBuilder endpoints)
    {
        var grupo = endpoints.MapGroup("/api/billing");

        grupo.MapPost("/", async (IMediator mediator, EmitirFacturaCommand cmd, CancellationToken token) =>
        {
            try
            {
                var id = await mediator.Send(cmd, token);
                return Results.Created($"/api/billing/{id}", new { id });
            }
            catch (InvalidOperationException ex) when (ex.Message == "pedido_inexistente")
            {
                return Results.NotFound(new { error = "pedido_inexistente" });
            }
            catch (InvalidOperationException ex) when (ex.Message == "factura_duplicada")
            {
                return Results.Conflict(new { error = "factura_duplicada" });
            }
        });

        grupo.MapPost("/{id:int}/paid", async (IMediator mediator, int id, CancellationToken token) =>
        {
            try
            {
                var estado = await mediator.Send(new MarcarPagadaCommand(id), token);
                return Results.Ok(new { id, estado });
            }
            catch (InvalidOperationException ex) when (ex.Message == "factura_inexistente")
            {
                return Results.NotFound(new { error = "factura_inexistente" });
            }
        });

        grupo.MapGet("/{id:int}", async (IMediator mediator, int id, CancellationToken token) =>
        {
            var factura = await mediator.Send(new ObtenerFacturaQuery(id), token);
            return factura is null ? Results.NotFound() : Results.Ok(factura);
        });

        grupo.MapGet("/", async (IMediator mediator, int? estado, CancellationToken token) =>
        {
            var lista = await mediator.Send(
                new ListarFacturasQuery(estado.HasValue ? (Domain.Facturacion.FacturaEstado?)estado.Value : null),
                token);
            return Results.Ok(lista);
        });

        return endpoints;
    }
}