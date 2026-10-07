using FxAspNet.Domain.Pedidos;
using FxAspNet.Infrastructure.Persistence;
using MediatR;
using Microsoft.EntityFrameworkCore;

namespace FxAspNet.Features.Pedidos.Commands;

public partial class CrearPedidoHandler
{
    public string Diagnostico { get; } = "handler_crear_pedido";
}