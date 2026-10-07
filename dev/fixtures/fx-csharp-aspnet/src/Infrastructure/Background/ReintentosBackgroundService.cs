using FxAspNet.Domain.Reintentos;
using FxAspNet.Infrastructure.Persistence;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;

namespace FxAspNet.Infrastructure.Background;

public class ReintentosBackgroundService : BackgroundService
{
    private readonly IServiceScopeFactory _scopeFactory;
    private readonly ILogger<ReintentosBackgroundService> _logger;

    public ReintentosBackgroundService(IServiceScopeFactory scopeFactory, ILogger<ReintentosBackgroundService> logger)
    {
        _scopeFactory = scopeFactory;
        _logger = logger;
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        while (!stoppingToken.IsCancellationRequested)
        {
            try
            {
                await ProcesarUnaVuelta(stoppingToken);
            }
            catch (Exception ex)
            {
                _logger.LogWarning(ex, "Error procesando trabajos pendientes");
            }
            await Task.Delay(TimeSpan.FromSeconds(5), stoppingToken);
        }
    }

    private async Task ProcesarUnaVuelta(CancellationToken token)
    {
        using var scope = _scopeFactory.CreateScope();
        var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
        var pendientes = await db.Trabajos
            .Where(t => t.Estado == TrabajoEstado.Pendiente || t.Estado == TrabajoEstado.Fallido)
            .Take(20)
            .ToListAsync(token);
        pendientes = pendientes.OrderBy(t => t.CreadoEn).ToList();

        foreach (var trabajo in pendientes)
        {
            trabajo.Estado = TrabajoEstado.EnProgreso;
            trabajo.Intentos += 1;
            await db.SaveChangesAsync(token);

            var exito = await IntentarTrabajo(trabajo, token);
            if (exito)
            {
                trabajo.Estado = TrabajoEstado.Completado;
            }
            else
            {
                trabajo.Estado = TrabajoEstado.Fallido;
                _logger.LogWarning("Trabajo {Id} fallo en el intento {Intentos}", trabajo.Id, trabajo.Intentos);
            }
            await db.SaveChangesAsync(token);
        }
    }

    private Task<bool> IntentarTrabajo(TrabajoPendiente trabajo, CancellationToken token)
    {
        return Task.FromResult(!string.IsNullOrWhiteSpace(trabajo.Tipo) && !string.IsNullOrWhiteSpace(trabajo.Payload));
    }
}