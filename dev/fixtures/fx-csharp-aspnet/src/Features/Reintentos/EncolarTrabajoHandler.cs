using FxAspNet.Domain.Reintentos;
using FxAspNet.Infrastructure.Persistence;
using MediatR;

namespace FxAspNet.Features.Reintentos;

public partial class EncolarTrabajoHandler : IRequestHandler<EncolarTrabajoCommand, int>
{
    private readonly AppDbContext _db;

    public EncolarTrabajoHandler(AppDbContext db)
    {
        _db = db;
    }

    public async Task<int> Handle(EncolarTrabajoCommand request, CancellationToken cancellationToken)
    {
        var trabajo = new TrabajoPendiente
        {
            Tipo = request.Tipo,
            Payload = request.Payload,
            Intentos = 0,
            Estado = TrabajoEstado.Pendiente,
            CreadoEn = DateTimeOffset.UtcNow
        };
        _db.Trabajos.Add(trabajo);
        await _db.SaveChangesAsync(cancellationToken);
        return trabajo.Id;
    }
}