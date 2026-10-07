using FxAspNet.Features.Facturacion.Commands;
using FxAspNet.Features.Pedidos.Commands;
using FxAspNet.Tests.Fixtures;
using System.Net;
using System.Net.Http.Json;
using Xunit;

namespace FxAspNet.Tests.Features;

public class FacturacionTests : IClassFixture<FxAspNetFactory>
{
    private readonly FxAspNetFactory _factory;

    public FacturacionTests(FxAspNetFactory factory)
    {
        _factory = factory;
    }

    [Fact]
    public async Task Emitir_factura_de_pedido_existente_returns_201()
    {
        var client = _factory.CreateClient();
        var clienteUnico = $"ana-{Guid.NewGuid():N}";
        var crear = await client.PostAsJsonAsync("/api/orders/", new CrearPedidoCommand(
            clienteUnico,
            new List<PedidoItemDto> { new("sku-1", 1, 10m) }));
        Assert.Equal(HttpStatusCode.Created, crear.StatusCode);

        // Averiguar el id del pedido creado via ListarPedidos.
        var lista = await client.GetAsync("/api/orders/");
        var ids = await lista.Content.ReadFromJsonAsync<List<int>>();
        Assert.NotNull(ids);
        Assert.NotEmpty(ids!);
        var pedidoId = ids![^1];

        var resp = await client.PostAsJsonAsync("/api/billing/", new EmitirFacturaCommand(pedidoId));
        Assert.Equal(HttpStatusCode.Created, resp.StatusCode);
    }

    [Fact]
    public async Task Emitir_factura_de_pedido_inexistente_returns_404()
    {
        var client = _factory.CreateClient();
        var resp = await client.PostAsJsonAsync("/api/billing/", new EmitirFacturaCommand(999999));
        Assert.Equal(HttpStatusCode.NotFound, resp.StatusCode);
    }

    [Fact]
    public async Task Emitir_factura_duplicada_returns_409()
    {
        var client = _factory.CreateClient();
        var clienteUnico = $"ana-{Guid.NewGuid():N}";
        await client.PostAsJsonAsync("/api/orders/", new CrearPedidoCommand(
            clienteUnico,
            new List<PedidoItemDto> { new("sku-1", 1, 10m) }));
        var lista = await client.GetAsync("/api/orders/");
        var ids = await lista.Content.ReadFromJsonAsync<List<int>>();
        var pedidoId = ids![^1];
        await client.PostAsJsonAsync("/api/billing/", new EmitirFacturaCommand(pedidoId));
        var resp = await client.PostAsJsonAsync("/api/billing/", new EmitirFacturaCommand(pedidoId));
        Assert.Equal(HttpStatusCode.Conflict, resp.StatusCode);
    }

    [Fact]
    public async Task Listar_facturas_devuelve_lista()
    {
        var client = _factory.CreateClient();
        var resp = await client.GetAsync("/api/billing/");
        Assert.Equal(HttpStatusCode.OK, resp.StatusCode);
    }
}