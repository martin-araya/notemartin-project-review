using Microsoft.AspNetCore.Http;
using System.Threading.Tasks;

namespace FxAspNet.Web.Middleware;

public class RequestIdMiddleware
{
    private readonly RequestDelegate _next;

    public RequestIdMiddleware(RequestDelegate next)
    {
        _next = next;
    }

    public async Task InvokeAsync(HttpContext context)
    {
        var id = context.Request.Headers["X-Request-Id"].ToString();
        if (string.IsNullOrEmpty(id))
        {
            id = Guid.NewGuid().ToString("N");
        }
        context.Items["fx_request_id"] = id;
        await _next(context);
    }
}