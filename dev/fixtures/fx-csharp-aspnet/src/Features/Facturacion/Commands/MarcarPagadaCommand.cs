using FxAspNet.Domain.Facturacion;
using MediatR;

namespace FxAspNet.Features.Facturacion.Commands;

public record MarcarPagadaCommand(int FacturaId) : IRequest<FacturaEstado>;