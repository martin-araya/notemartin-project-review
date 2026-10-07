using FxAspNet.Domain.Facturacion;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace FxAspNet.Infrastructure.Persistence.Configurations;

public class FacturaConfiguration : IEntityTypeConfiguration<Factura>
{
    public void Configure(EntityTypeBuilder<Factura> b)
    {
        b.ToTable("facturas");
        b.HasKey(f => f.Id);
        b.Property(f => f.Numero).HasMaxLength(32).IsRequired();
        b.HasIndex(f => f.Numero).IsUnique();
        b.Property(f => f.EmitidaEn).IsRequired();
        b.Property(f => f.Importe).HasColumnType("decimal(18,2)");
        b.Property(f => f.Estado).HasConversion<int>();
    }
}