using FxAspNet.Domain.Pedidos;
using FxAspNet.Infrastructure.Persistence;
using MediatR;
using Microsoft.EntityFrameworkCore;

namespace FxAspNet.Features.Pedidos.Queries;

public partial class ObtenerPedidoHandler : IRequestHandler<ObtenerPedidoQuery, Pedido?>
{
    private readonly AppDbContext _db;

    public ObtenerPedidoHandler(AppDbContext db)
    {
        _db = db;
    }

    public async Task<Pedido?> Handle(ObtenerPedidoQuery request, CancellationToken cancellationToken)
    {
        return await _db.Pedidos
            .Include(p => p.Items)
            .FirstOrDefaultAsync(p => p.Id == request.Id, cancellationToken);
    }
}