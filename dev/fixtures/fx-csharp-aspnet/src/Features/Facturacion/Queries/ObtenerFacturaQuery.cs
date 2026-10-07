using FxAspNet.Domain.Facturacion;
using MediatR;

namespace FxAspNet.Features.Facturacion.Queries;

public record ObtenerFacturaQuery(int Id) : IRequest<Factura?>;