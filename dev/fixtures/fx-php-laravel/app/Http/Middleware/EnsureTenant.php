<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class EnsureTenant
{
    /**
     * E05 / P06: middleware registrado en el grupo 'web' via
     * $middleware->appendToGroup('web', EnsureTenant::class).
     * En este fixture, solo se ejecuta si una ruta lo carga
     * explicitamente con Route::middleware(['web']).
     */
    public function handle(Request $request, Closure $next): Response
    {
        return $next($request);
    }
}
