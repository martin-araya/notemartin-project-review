<?php

namespace App\Http;

use App\Http\Middleware\EncryptCookies;
use App\Http\Middleware\EnsureTenant;
use App\Http\Middleware\VerifyCsrfToken;
use Illuminate\Foundation\Http\Kernel as HttpKernel;

class Kernel extends HttpKernel
{
    /**
     * E05: el grupo 'web' carga el middleware EnsureTenant
     * (P06: registrado pero con implementacion no-op).
     */
    protected $middlewareGroups = [
        'web' => [
            \App\Http\Middleware\EncryptCookies::class,
            \Illuminate\Cookie\Middleware\AddQueuedCookiesToResponse::class,
            \Illuminate\Session\Middleware\StartSession::class,
            \Illuminate\View\Middleware\ShareErrorsFromSession::class,
            EnsureTenant::class,
            VerifyCsrfToken::class,
        ],
        'api' => [
            EnsureTenant::class,
            \Illuminate\Routing\Middleware\SubstituteBindings::class,
        ],
    ];

    protected $middleware = [
        \Illuminate\Http\Middleware\HandleCors::class,
    ];
}
