using FxAspNet.Domain.Reintentos;
using FxAspNet.Infrastructure.Persistence;
using MediatR;
using Microsoft.EntityFrameworkCore;

namespace FxAspNet.Features.Reintentos;

public class AckTrabajoHandler : IRequestHandler<AckTrabajoCommand, bool>
{
    private readonly AppDbContext _db;

    public AckTrabajoHandler(AppDbContext db)
    {
        _db = db;
    }

    public async Task<bool> Handle(AckTrabajoCommand request, CancellationToken cancellationToken)
    {
        var trabajo = await _db.Trabajos
            .FirstOrDefaultAsync(t => t.Id == request.TrabajoId, cancellationToken);
        if (trabajo is null)
        {
            return false;
        }
        trabajo.Estado = TrabajoEstado.Completado;
        trabajo.UltimoIntentoEn = DateTimeOffset.UtcNow;
        await _db.SaveChangesAsync(cancellationToken);
        return true;
    }
}