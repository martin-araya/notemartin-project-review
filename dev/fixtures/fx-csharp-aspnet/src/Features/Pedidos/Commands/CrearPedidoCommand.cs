using MediatR;

namespace FxAspNet.Features.Pedidos.Commands;

public record CrearPedidoCommand(string Cliente, List<PedidoItemDto> Items) : IRequest<int>;

public record PedidoItemDto(string Sku, int Cantidad, decimal PrecioUnitario);