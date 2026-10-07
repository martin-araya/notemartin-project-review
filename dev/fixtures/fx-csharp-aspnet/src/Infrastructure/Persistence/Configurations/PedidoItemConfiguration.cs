using FxAspNet.Domain.Pedidos;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace FxAspNet.Infrastructure.Persistence.Configurations;

public class PedidoItemConfiguration : IEntityTypeConfiguration<PedidoItem>
{
    public void Configure(EntityTypeBuilder<PedidoItem> b)
    {
        b.ToTable("pedido_items");
        b.HasKey(i => i.Id);
        b.Property(i => i.Sku).HasMaxLength(64).IsRequired();
        b.Property(i => i.Cantidad).IsRequired();
        b.Property(i => i.PrecioUnitario).HasColumnType("decimal(18,2)");
        b.Ignore(i => i.ReferenciaCircular);
    }
}