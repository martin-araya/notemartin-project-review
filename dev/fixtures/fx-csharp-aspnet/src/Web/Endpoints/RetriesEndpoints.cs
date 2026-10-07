using FxAspNet.Features.Reintentos;
using MediatR;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Routing;

namespace FxAspNet.Web.Endpoints;

public static class RetriesEndpoints
{
    public static IEndpointRouteBuilder MapRetriesEndpoints(this IEndpointRouteBuilder endpoints)
    {
        var grupo = endpoints.MapGroup("/api/retries");

        grupo.MapPost("/", async (IMediator mediator, EncolarTrabajoCommand cmd, CancellationToken token) =>
        {
            var id = await mediator.Send(cmd, token);
            return Results.Created($"/api/retries/{id}", new { id });
        });

        grupo.MapGet("/pending", async (IMediator mediator, int? limite, CancellationToken token) =>
        {
            var lista = await mediator.Send(new ListarPendientesQuery(limite ?? 50), token);
            return Results.Ok(lista);
        });

        grupo.MapPost("/{id:int}/ack", async (IMediator mediator, int id, CancellationToken token) =>
        {
            var ok = await mediator.Send(new AckTrabajoCommand(id), token);
            return ok ? Results.NoContent() : Results.NotFound();
        });

        return endpoints;
    }
}