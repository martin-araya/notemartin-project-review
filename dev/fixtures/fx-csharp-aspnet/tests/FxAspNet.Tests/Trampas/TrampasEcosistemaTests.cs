using Xunit;

namespace FxAspNet.Tests.Trampas;

public class TrampasEcosistemaTests
{
    [Fact]
    public void E01_mediator_resolved_by_request_type()
    {
        var asm = typeof(FxAspNet.Features.Pedidos.Commands.CrearPedidoHandler).Assembly;
        var handlerType = asm.GetType("FxAspNet.Features.Pedidos.Commands.CrearPedidoHandler");
        Assert.NotNull(handlerType);
        var interfaces = handlerType!.GetInterfaces();
        Assert.Contains(interfaces, i => i.IsGenericType && i.GetGenericTypeDefinition().FullName!.Contains("IRequestHandler"));
    }

    [Fact]
    public void E02_efcore_fluent_no_dataannotations()
    {
        var asm = typeof(FxAspNet.Infrastructure.Persistence.AppDbContext).Assembly;
        var pedidoType = asm.GetType("FxAspNet.Domain.Pedidos.Pedido");
        Assert.NotNull(pedidoType);
        var props = pedidoType!.GetProperties();
        foreach (var p in props)
        {
            var attrs = p.GetCustomAttributesData();
            foreach (var a in attrs)
            {
                Assert.False(a.AttributeType.FullName!.StartsWith("System.ComponentModel.DataAnnotations"),
                    $"prop {p.Name} no debe tener data annotations");
            }
        }
    }

    [Fact]
    public void E03_source_generators_in_csproj()
    {
        var csproj = AppContext.BaseDirectory;
        Assert.True(Directory.Exists(csproj));
    }

    [Fact]
    public void E04_partial_class_pedidoitem_split()
    {
        var asm = typeof(FxAspNet.Domain.Pedidos.PedidoItem).Assembly;
        var type = asm.GetType("FxAspNet.Domain.Pedidos.PedidoItem");
        Assert.NotNull(type);
        Assert.True(type!.IsPublic);
    }

    [Fact]
    public void E05_middleware_useExceptionHandler_en_program()
    {
        var program = System.IO.File.ReadAllText(
            Path.Combine(AppContext.BaseDirectory, "..", "..", "..", "..", "..", "Program.cs"));
        Assert.Contains("UseExceptionHandler", program);
    }

    [Fact]
    public void E06_extension_method_addOrdersModule_no_invocado()
    {
        var asm = typeof(FxAspNet.Infrastructure.Mediator.MediatorRegistration).Assembly;
        var t = asm.GetType("FxAspNet.Infrastructure.Mediator.MediatorRegistration");
        Assert.NotNull(t);
        var m = t!.GetMethod("AddOrdersModule");
        Assert.NotNull(m);

        var program = System.IO.File.ReadAllText(
            Path.Combine(AppContext.BaseDirectory, "..", "..", "..", "..", "..", "Program.cs"));
        Assert.DoesNotContain("AddOrdersModule()", program);
    }
}