using FxAspNet.Domain.Reintentos;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace FxAspNet.Infrastructure.Persistence.Configurations;

public class TrabajoConfiguration : IEntityTypeConfiguration<TrabajoPendiente>
{
    public void Configure(EntityTypeBuilder<TrabajoPendiente> b)
    {
        b.ToTable("trabajos");
        b.HasKey(t => t.Id);
        b.Property(t => t.Tipo).HasMaxLength(64).IsRequired();
        b.Property(t => t.Payload).HasMaxLength(2048).IsRequired();
        b.Property(t => t.Intentos).IsRequired();
        b.Property(t => t.Estado).HasConversion<int>();
    }
}