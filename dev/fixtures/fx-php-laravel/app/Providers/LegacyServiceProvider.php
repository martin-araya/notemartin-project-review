<?php

namespace App\Providers;

use Illuminate\Support\ServiceProvider;

/**
 * S01: provider dead. Registrado en bootstrap/providers.php pero
 * no aporta bindings ni listeners en este fixture. La skill debe
 * detectarlo listando todos los providers y buscando consumidores
 * reales del provider.
 */
class LegacyServiceProvider extends ServiceProvider
{
    public function register(): void
    {
        // legacy only - kept for backward compatibility but no consumer.
    }

    public function boot(): void
    {
        // legacy only - kept for backward compatibility but no consumer.
    }
}
