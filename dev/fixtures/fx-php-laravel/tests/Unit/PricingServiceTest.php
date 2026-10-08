<?php

namespace Tests\Unit;

use App\Facades\PricingFacade as Pricing;
use App\Pricing\PricingService;
use Tests\TestCase;

class PricingServiceTest extends TestCase
{
    public function test_pricing_service_calculate(): void
    {
        $service = new PricingService();
        $this->assertEquals(121.0, $service->calculate(100));
    }

    public function test_facade_resolves_to_binding(): void
    {
        $resolved = app('pricing.service');
        $this->assertInstanceOf(PricingService::class, $resolved);
        $this->assertEquals(242.0, $resolved->calculate(200));
    }
}
