using FxAspNet.Domain.Facturacion;
using MediatR;

namespace FxAspNet.Features.Facturacion.Queries;

public record ListarFacturasQuery(FacturaEstado? Estado = null) : IRequest<List<Factura>>;