using FxAspNet.Domain.Facturacion;
using FxAspNet.Infrastructure.Persistence;
using MediatR;
using Microsoft.EntityFrameworkCore;

namespace FxAspNet.Features.Facturacion.Commands;

public class MarcarPagadaHandler : IRequestHandler<MarcarPagadaCommand, FacturaEstado>
{
    private readonly AppDbContext _db;

    public MarcarPagadaHandler(AppDbContext db)
    {
        _db = db;
    }

    public async Task<FacturaEstado> Handle(MarcarPagadaCommand request, CancellationToken cancellationToken)
    {
        var factura = await _db.Facturas
            .FirstOrDefaultAsync(f => f.Id == request.FacturaId, cancellationToken);

        if (factura is null)
        {
            throw new InvalidOperationException("factura_inexistente");
        }

        if (factura.Estado == FacturaEstado.Anulada)
        {
            throw new InvalidOperationException("factura_anulada");
        }

        factura.Estado = FacturaEstado.Pagada;
        await _db.SaveChangesAsync(cancellationToken);

        return factura.Estado;
    }
}