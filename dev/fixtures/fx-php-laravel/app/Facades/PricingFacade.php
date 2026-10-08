<?php

namespace App\Facades;

use Illuminate\Support\Facades\Facade;

/**
 * E01: facade de Laravel. Las llamadas estaticas se resuelven
 * via el contenedor, apuntando a la clave 'pricing.service'.
 *
 * @method static float calculate(int $cents)
 * @method static string format(float $euros)
 *
 * @see \App\Pricing\PricingService
 */
class PricingFacade extends Facade
{
    protected static function getFacadeAccessor(): string
    {
        return 'pricing.service';
    }
}
