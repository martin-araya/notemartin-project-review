using FxAspNet.Domain.Reintentos;
using MediatR;

namespace FxAspNet.Features.Reintentos;

public record EncolarTrabajoCommand(string Tipo, string Payload) : IRequest<int>;

public record ListarPendientesQuery(int Limite = 50) : IRequest<List<TrabajoPendiente>>;

public record AckTrabajoCommand(int TrabajoId) : IRequest<bool>;