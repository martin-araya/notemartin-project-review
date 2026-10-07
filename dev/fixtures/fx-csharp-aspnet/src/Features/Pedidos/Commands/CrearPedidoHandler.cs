using FxAspNet.Domain.Pedidos;
using FxAspNet.Infrastructure.Persistence;
using MediatR;
using Microsoft.EntityFrameworkCore;

namespace FxAspNet.Features.Pedidos.Commands;

public partial class CrearPedidoHandler : IRequestHandler<CrearPedidoCommand, int>
{
    private readonly AppDbContext _db;

    public CrearPedidoHandler(AppDbContext db)
    {
        _db = db;
    }

    public async Task<int> Handle(CrearPedidoCommand request, CancellationToken cancellationToken)
    {
        if (string.IsNullOrWhiteSpace(request.Cliente))
        {
            throw new InvalidOperationException("cliente_requerido");
        }
        if (request.Items is null || request.Items.Count == 0)
        {
            throw new InvalidOperationException("items_requeridos");
        }

        var items = request.Items.Select(i => new PedidoItem
        {
            Sku = i.Sku,
            Cantidad = i.Cantidad,
            PrecioUnitario = i.PrecioUnitario
        }).ToList();

        var pedido = new Pedido
        {
            Cliente = request.Cliente,
            CreadoEn = DateTimeOffset.UtcNow,
            Estado = PedidoEstado.Pendiente,
            Total = request.Items.Sum(i => i.Cantidad * i.PrecioUnitario)
        };

        _db.Pedidos.Add(pedido);
        await _db.SaveChangesAsync(cancellationToken);

        foreach (var item in items)
        {
            item.PedidoId = pedido.Id;
            _db.PedidoItems.Add(item);
        }
        await _db.SaveChangesAsync(cancellationToken);

        return pedido.Id;
    }
}