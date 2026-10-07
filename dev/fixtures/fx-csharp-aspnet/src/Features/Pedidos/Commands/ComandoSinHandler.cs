using MediatR;

namespace FxAspNet.Features.Pedidos.Commands;

public record ComandoSinHandler(string Texto) : IRequest<string>;