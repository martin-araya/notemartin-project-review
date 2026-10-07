using FxAspNet.Domain.Pedidos;
using FxAspNet.Infrastructure.Persistence;
using MediatR;

namespace FxAspNet.Features.Pedidos.Queries;

public partial class ObtenerPedidoHandler
{
    public string Etiqueta { get; } = "handler_obtener_pedido";
}