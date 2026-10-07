using FxAspNet.Infrastructure.Persistence;
using MediatR;
using Microsoft.EntityFrameworkCore;

namespace FxAspNet.Features.Pedidos.Queries;

public class ListarPedidosHandler : IRequestHandler<ListarPedidosQuery, List<int>>
{
    private readonly AppDbContext _db;

    public ListarPedidosHandler(AppDbContext db)
    {
        _db = db;
    }

    public async Task<List<int>> Handle(ListarPedidosQuery request, CancellationToken cancellationToken)
    {
        return await _db.Pedidos
            .OrderBy(p => p.Id)
            .Skip(request.Pagina * request.Tamano)
            .Take(request.Tamano)
            .Select(p => p.Id)
            .ToListAsync(cancellationToken);
    }
}