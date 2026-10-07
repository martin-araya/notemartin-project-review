using FxAspNet.Features.Reintentos;
using FxAspNet.Tests.Fixtures;
using System.Net;
using System.Net.Http.Json;
using Xunit;

namespace FxAspNet.Tests.Features;

public class ReintentosTests : IClassFixture<FxAspNetFactory>
{
    private readonly FxAspNetFactory _factory;

    public ReintentosTests(FxAspNetFactory factory)
    {
        _factory = factory;
    }

    [Fact]
    public async Task Encolar_trabajo_returns_201()
    {
        var client = _factory.CreateClient();
        var resp = await client.PostAsJsonAsync("/api/retries/", new EncolarTrabajoCommand("tipo-a", "payload-1"));
        Assert.Equal(HttpStatusCode.Created, resp.StatusCode);
    }

    [Fact]
    public async Task Listar_pendientes_devuelve_lista()
    {
        var client = _factory.CreateClient();
        await client.PostAsJsonAsync("/api/retries/", new EncolarTrabajoCommand("tipo-a", "payload-1"));
        var resp = await client.GetAsync("/api/retries/pending");
        Assert.Equal(HttpStatusCode.OK, resp.StatusCode);
    }

    [Fact]
    public async Task Ack_de_trabajo_inexistente_returns_404()
    {
        var client = _factory.CreateClient();
        var resp = await client.PostAsync("/api/retries/999999/ack", content: null);
        Assert.Equal(HttpStatusCode.NotFound, resp.StatusCode);
    }
}