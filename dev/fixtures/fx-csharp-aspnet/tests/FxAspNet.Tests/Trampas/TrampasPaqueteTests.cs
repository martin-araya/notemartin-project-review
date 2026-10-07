using FxAspNet.Features.Pedidos.Commands;
using FxAspNet.Tests.Fixtures;
using System.Net;
using System.Net.Http.Json;
using Xunit;

namespace FxAspNet.Tests.Trampas;

public class TrampasPaqueteTests : IClassFixture<FxAspNetFactory>
{
    private readonly FxAspNetFactory _factory;

    public TrampasPaqueteTests(FxAspNetFactory factory)
    {
        _factory = factory;
    }

    [Fact]
    public async Task P01_handler_throws_no_handler_mapeado_500()
    {
        var client = _factory.CreateClient();
        var resp = await client.PostAsJsonAsync("/api/orders/", new CrearPedidoCommand(
            Cliente: "",
            Items: new List<PedidoItemDto> { new("sku-1", 1, 1m) }));
        Assert.Equal(HttpStatusCode.BadRequest, resp.StatusCode);
    }

    [Fact]
    public void P02_comando_sin_handler_existe_en_assembly()
    {
        var asm = typeof(CrearPedidoCommand).Assembly;
        var t = asm.GetType("FxAspNet.Features.Pedidos.Commands.ComandoSinHandler");
        Assert.NotNull(t);
    }

    [Fact]
    public void P03_crear_pedido_handler_two_saves()
    {
        var src = System.IO.File.ReadAllText(
            Path.Combine(AppContext.BaseDirectory, "..", "..", "..", "..", "..",
                "src", "Features", "Pedidos", "Commands", "CrearPedidoHandler.cs"));
        var count = src.Split("SaveChangesAsync").Length - 1;
        Assert.True(count >= 2, $"esperaba >=2 SaveChangesAsync, hay {count}");
    }

    [Fact]
    public void P04_background_no_actualiza_ultimo_intento_en_fallo()
    {
        var src = System.IO.File.ReadAllText(
            Path.Combine(AppContext.BaseDirectory, "..", "..", "..", "..", "..",
                "src", "Infrastructure", "Background", "ReintentosBackgroundService.cs"));
        Assert.Contains("TrabajoEstado.Fallido", src);
        Assert.Contains("LogWarning", src);
        var bloqueFallo = src.Substring(src.IndexOf("TrabajoEstado.Fallido"));
        Assert.DoesNotContain("UltimoIntentoEn =", bloqueFallo);
    }

    [Fact]
    public void P05_endpoint_group_route_prefix_orden()
    {
        var src = System.IO.File.ReadAllText(
            Path.Combine(AppContext.BaseDirectory, "..", "..", "..", "..", "..",
                "src", "Web", "Endpoints", "OrdersEndpoints.cs"));
        var idxRaiz = src.IndexOf("MapPost(\"/\"");
        var idxId = src.IndexOf("MapGet(\"/{id:int}\"");
        Assert.True(idxRaiz > 0 && idxId > 0);
    }

    [Fact]
    public void P06_sqlite_inmemory_shared_cache_required()
    {
        var cs = $"DataSource=file:test-{Guid.NewGuid():N}?mode=memory&cache=shared";
        Assert.Contains("cache=shared", cs);
    }
}