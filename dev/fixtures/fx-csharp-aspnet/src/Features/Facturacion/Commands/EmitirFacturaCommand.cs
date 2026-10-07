using FxAspNet.Domain.Facturacion;
using MediatR;

namespace FxAspNet.Features.Facturacion.Commands;

public record EmitirFacturaCommand(int PedidoId) : IRequest<int>;