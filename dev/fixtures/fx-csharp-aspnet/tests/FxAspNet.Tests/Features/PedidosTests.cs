using FxAspNet.Features.Pedidos.Commands;
using FxAspNet.Features.Pedidos.Queries;
using FxAspNet.Tests.Fixtures;
using System.Net;
using System.Net.Http.Json;
using Xunit;

namespace FxAspNet.Tests.Features;

public class PedidosTests : IClassFixture<FxAspNetFactory>
{
    private readonly FxAspNetFactory _factory;

    public PedidosTests(FxAspNetFactory factory)
    {
        _factory = factory;
    }

    [Fact]
    public async Task Crear_pedido_valido_returns_201_con_id()
    {
        var client = _factory.CreateClient();
        var cmd = new CrearPedidoCommand(
            Cliente: $"ana-{Guid.NewGuid():N}",
            Items: new List<PedidoItemDto>
            {
                new("sku-1", 2, 9.99m),
                new("sku-2", 1, 4.50m)
            });

        var resp = await client.PostAsJsonAsync("/api/orders/", cmd);
        Assert.Equal(HttpStatusCode.Created, resp.StatusCode);
    }

    [Fact]
    public async Task Crear_pedido_con_cliente_vacio_returns_400()
    {
        var client = _factory.CreateClient();
        var cmd = new CrearPedidoCommand(
            Cliente: "",
            Items: new List<PedidoItemDto> { new("sku-1", 1, 1m) });

        var resp = await client.PostAsJsonAsync("/api/orders/", cmd);
        Assert.Equal(HttpStatusCode.BadRequest, resp.StatusCode);
    }

    [Fact]
    public async Task Obtener_pedido_inexistente_returns_404()
    {
        var client = _factory.CreateClient();
        var resp = await client.GetAsync("/api/orders/999999");
        Assert.Equal(HttpStatusCode.NotFound, resp.StatusCode);
    }

    [Fact]
    public async Task Listar_pedidos_devuelve_lista()
    {
        var client = _factory.CreateClient();
        var resp = await client.GetAsync("/api/orders/");
        Assert.Equal(HttpStatusCode.OK, resp.StatusCode);
    }
}