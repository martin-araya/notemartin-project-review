using FxAspNet.Infrastructure.Persistence;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Mvc.Testing;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.DependencyInjection.Extensions;

namespace FxAspNet.Tests.Fixtures;

public class FxAspNetFactory : WebApplicationFactory<Program>
{
    private readonly string _connectionString;

    public FxAspNetFactory()
    {
        _connectionString = $"DataSource=file:test-{Guid.NewGuid():N}?mode=memory&cache=shared";
    }

    protected override void ConfigureWebHost(IWebHostBuilder builder)
    {
        builder.UseSetting("ConnectionStrings:Default", _connectionString);
        builder.ConfigureServices(services =>
        {
            services.RemoveAll<DbContextOptions<AppDbContext>>();
            services.RemoveAll<AppDbContext>();
            services.AddDbContext<AppDbContext>(opt =>
            {
                opt.UseSqlite(_connectionString);
            });
        });
    }
}