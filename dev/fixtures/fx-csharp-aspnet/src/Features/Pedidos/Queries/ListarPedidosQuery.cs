using MediatR;

namespace FxAspNet.Features.Pedidos.Queries;

public record ListarPedidosQuery(int Pagina = 0, int Tamano = 50) : IRequest<List<int>>;