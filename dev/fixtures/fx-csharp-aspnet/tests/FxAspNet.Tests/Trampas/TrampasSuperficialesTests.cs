using System.IO;
using Xunit;

namespace FxAspNet.Tests.Trampas;

public class TrampasSuperficialesTests
{
    [Fact]
    public void S01_crear_pedido_validator_dead()
    {
        var src = File.ReadAllText(
            Path.Combine(AppContext.BaseDirectory, "..", "..", "..", "..", "..",
                "src", "Features", "Pedidos", "Commands", "CrearPedidoValidator.cs"));
        Assert.Contains("Validar", src);
    }

    [Fact]
    public void S02_appdbcontext_logger_dead()
    {
        var src = File.ReadAllText(
            Path.Combine(AppContext.BaseDirectory, "..", "..", "..", "..", "..",
                "src", "Infrastructure", "Persistence", "AppDbContext.cs"));
        Assert.Contains("_log", src);
    }

    [Fact]
    public void S03_health_endpoint_existe()
    {
        var src = File.ReadAllText(
            Path.Combine(AppContext.BaseDirectory, "..", "..", "..", "..", "..",
                "src", "Web", "Endpoints", "OrdersEndpoints.cs"));
        Assert.Contains("MapGet(\"/health\"", src);
    }
}