using FxAspNet.Domain.Facturacion;
using FxAspNet.Infrastructure.Persistence;
using MediatR;
using Microsoft.EntityFrameworkCore;

namespace FxAspNet.Features.Facturacion.Queries;

public class ListarFacturasHandler : IRequestHandler<ListarFacturasQuery, List<Factura>>
{
    private readonly AppDbContext _db;

    public ListarFacturasHandler(AppDbContext db)
    {
        _db = db;
    }

    public async Task<List<Factura>> Handle(ListarFacturasQuery request, CancellationToken cancellationToken)
    {
        var q = _db.Facturas.AsQueryable();
        if (request.Estado.HasValue)
        {
            q = q.Where(f => f.Estado == request.Estado.Value);
        }
        return await q.OrderBy(f => f.Id).ToListAsync(cancellationToken);
    }
}