using FxAspNet.Domain.Pedidos;
using MediatR;

namespace FxAspNet.Features.Pedidos.Queries;

public record ObtenerPedidoQuery(int Id) : IRequest<Pedido?>;