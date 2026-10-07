using Microsoft.AspNetCore.Builder;

namespace FxAspNet.Web.Middleware;

public static class RequestIdMiddlewareExtensions
{
    public static IApplicationBuilder UseRequestId(this IApplicationBuilder app)
    {
        return app.UseMiddleware<RequestIdMiddleware>();
    }
}