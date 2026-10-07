using FxAspNet.Infrastructure.Background;
using FxAspNet.Infrastructure.Persistence;
using FxAspNet.Web.Endpoints;
using MediatR;
using Microsoft.EntityFrameworkCore;

var builder = WebApplication.CreateBuilder(args);

var connectionString = builder.Configuration.GetConnectionString("Default")
                       ?? "DataSource=file:fxaspnet.db?cache=shared";

builder.Services.AddDbContext<AppDbContext>(opt =>
{
    opt.UseSqlite(connectionString);
});

builder.Services.AddMediatR(typeof(Program).Assembly);

builder.Services.AddHostedService<ReintentosBackgroundService>();

var app = builder.Build();

app.MapOrdersEndpoints();
app.MapBillingEndpoints();
app.MapRetriesEndpoints();

app.UseExceptionHandler(eh => eh.Run(async ctx =>
{
    var ex = ctx.Features.Get<Microsoft.AspNetCore.Diagnostics.IExceptionHandlerFeature>()?.Error;
    var logger = ctx.RequestServices.GetRequiredService<ILoggerFactory>().CreateLogger("fxaspnet.exceptions");
    logger.LogError(ex, "Excepcion no controlada");
    ctx.Response.StatusCode = 500;
    await ctx.Response.WriteAsJsonAsync(new { error = "interno" });
}));

await DbInitializer.InicializarAsync(app.Services);

app.Run();

namespace FxAspNet
{
    public partial class Program { }
}