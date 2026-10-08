<?php

namespace App\Pricing;

class PricingService
{
    private float $taxRate;

    public function __construct(float $taxRate = 0.21)
    {
        $this->taxRate = $taxRate;
    }

    /**
     * E01: metodo invocado via la facade Pricing::calculate($cents).
     */
    public function calculate(int $cents): float
    {
        return round($cents * (1 + $this->taxRate), 2);
    }

    public function format(float $euros): string
    {
        return number_format($euros, 2, ',', '.') . ' EUR';
    }
}
