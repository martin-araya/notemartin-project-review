using FxAspNet.Domain.Pedidos;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace FxAspNet.Infrastructure.Persistence.Configurations;

public class PedidoConfiguration : IEntityTypeConfiguration<Pedido>
{
    public void Configure(EntityTypeBuilder<Pedido> b)
    {
        b.ToTable("pedidos");
        b.HasKey(p => p.Id);
        b.Property(p => p.Cliente).HasMaxLength(200).IsRequired();
        b.Property(p => p.CreadoEn).IsRequired();
        b.Property(p => p.Total).HasColumnType("decimal(18,2)");
        b.Property(p => p.Estado).HasConversion<int>();
        b.HasMany(p => p.Items).WithOne().HasForeignKey(i => i.PedidoId).OnDelete(DeleteBehavior.Cascade);
    }
}