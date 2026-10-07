using FxAspNet.Domain.Reintentos;
using FxAspNet.Infrastructure.Persistence;
using MediatR;

namespace FxAspNet.Features.Reintentos;

public partial class EncolarTrabajoHandler
{
    public string Etiqueta { get; } = "handler_encolar_trabajo";
}