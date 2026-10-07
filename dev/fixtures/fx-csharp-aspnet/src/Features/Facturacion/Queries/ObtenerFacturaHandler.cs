using FxAspNet.Domain.Facturacion;
using FxAspNet.Infrastructure.Persistence;
using MediatR;
using Microsoft.EntityFrameworkCore;

namespace FxAspNet.Features.Facturacion.Queries;

public class ObtenerFacturaHandler : IRequestHandler<ObtenerFacturaQuery, Factura?>
{
    private readonly AppDbContext _db;

    public ObtenerFacturaHandler(AppDbContext db)
    {
        _db = db;
    }

    public async Task<Factura?> Handle(ObtenerFacturaQuery request, CancellationToken cancellationToken)
    {
        return await _db.Facturas
            .FirstOrDefaultAsync(f => f.Id == request.Id, cancellationToken);
    }
}