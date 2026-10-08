<?php

namespace App\Providers;

use App\Pricing\PricingService;
use App\Repositories\EloquentVisitRepository;
use App\Repositories\VisitRepository;
use Illuminate\Support\ServiceProvider;

class InmuebleServiceProvider extends ServiceProvider
{
    /**
     * E02: bindings de interfaces a implementaciones concretas.
     * E03: singleton para el servicio de pricing (resuelve la facade).
     */
    public function register(): void
    {
        $this->app->bind(VisitRepository::class, EloquentVisitRepository::class);
        $this->app->singleton('pricing.service', function ($app) {
            return new PricingService();
        });
        // P02: referencia a una clase que no existe (trampa de superficie).
        $this->app->bind('legacy.helper', function ($app) {
            return new \App\Pricing\LegacyHelper();
        });
    }

    public function boot(): void
    {
        // No-op
    }
}
