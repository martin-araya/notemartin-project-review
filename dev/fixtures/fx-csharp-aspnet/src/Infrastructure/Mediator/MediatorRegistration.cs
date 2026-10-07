using FxAspNet.Features.Pedidos.Commands;
using FxAspNet.Features.Pedidos.Queries;
using Microsoft.Extensions.DependencyInjection;

namespace FxAspNet.Infrastructure.Mediator;

public static class MediatorRegistration
{
    public static IServiceCollection AddOrdersModule(this IServiceCollection services)
    {
        services.AddScoped<CrearPedidoHandler>();
        services.AddScoped<ObtenerPedidoHandler>();
        services.AddScoped<ListarPedidosHandler>();
        return services;
    }
}