using FxAspNet.Domain.Facturacion;
using FxAspNet.Infrastructure.Persistence;
using MediatR;
using Microsoft.EntityFrameworkCore;

namespace FxAspNet.Features.Facturacion.Commands;

public class EmitirFacturaHandler : IRequestHandler<EmitirFacturaCommand, int>
{
    private readonly AppDbContext _db;

    public EmitirFacturaHandler(AppDbContext db)
    {
        _db = db;
    }

    public async Task<int> Handle(EmitirFacturaCommand request, CancellationToken cancellationToken)
    {
        var pedido = await _db.Pedidos
            .Include(p => p.Items)
            .FirstOrDefaultAsync(p => p.Id == request.PedidoId, cancellationToken);

        if (pedido is null)
        {
            throw new InvalidOperationException("pedido_inexistente");
        }

        var existe = await _db.Facturas
            .AnyAsync(f => f.PedidoId == request.PedidoId, cancellationToken);
        if (existe)
        {
            throw new InvalidOperationException("factura_duplicada");
        }

        var factura = new Factura
        {
            PedidoId = pedido.Id,
            Numero = $"F-{pedido.Id}-{DateTimeOffset.UtcNow.ToUnixTimeSeconds()}",
            EmitidaEn = DateTimeOffset.UtcNow,
            Importe = pedido.Total,
            Estado = FacturaEstado.Emitida
        };

        _db.Facturas.Add(factura);
        await _db.SaveChangesAsync(cancellationToken);

        return factura.Id;
    }
}