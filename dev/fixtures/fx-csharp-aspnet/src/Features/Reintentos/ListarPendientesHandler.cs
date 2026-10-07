using FxAspNet.Domain.Reintentos;
using FxAspNet.Infrastructure.Persistence;
using MediatR;
using Microsoft.EntityFrameworkCore;

namespace FxAspNet.Features.Reintentos;

public class ListarPendientesHandler : IRequestHandler<ListarPendientesQuery, List<TrabajoPendiente>>
{
    private readonly AppDbContext _db;

    public ListarPendientesHandler(AppDbContext db)
    {
        _db = db;
    }

    public async Task<List<TrabajoPendiente>> Handle(ListarPendientesQuery request, CancellationToken cancellationToken)
    {
        var items = await _db.Trabajos
            .Where(t => t.Estado == TrabajoEstado.Pendiente || t.Estado == TrabajoEstado.Fallido)
            .Take(request.Limite)
            .ToListAsync(cancellationToken);
        return items.OrderBy(t => t.CreadoEn).ToList();
    }
}