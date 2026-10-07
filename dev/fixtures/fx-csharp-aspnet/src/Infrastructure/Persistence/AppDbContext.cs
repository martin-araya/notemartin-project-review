using FxAspNet.Domain.Facturacion;
using FxAspNet.Domain.Pedidos;
using FxAspNet.Domain.Reintentos;
using Microsoft.EntityFrameworkCore;

namespace FxAspNet.Infrastructure.Persistence;

public class AppDbContext : DbContext
{
    private static readonly ILogger<AppDbContext> _log = LoggerFactory.Create(b => b.AddConsole()).CreateLogger<AppDbContext>();

    public AppDbContext(DbContextOptions<AppDbContext> options) : base(options)
    {
    }

    public DbSet<Pedido> Pedidos => Set<Pedido>();
    public DbSet<PedidoItem> PedidoItems => Set<PedidoItem>();
    public DbSet<Factura> Facturas => Set<Factura>();
    public DbSet<TrabajoPendiente> Trabajos => Set<TrabajoPendiente>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.ApplyConfigurationsFromAssembly(typeof(AppDbContext).Assembly);
        base.OnModelCreating(modelBuilder);
    }
}