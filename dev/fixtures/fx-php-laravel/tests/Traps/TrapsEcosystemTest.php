<?php

namespace Tests\Traps;

use Tests\TestCase;

/**
 * Tests estaticos que verifican la presencia de las 6 trampas
 * del ecosistema plantadas en el fixture (CC-06). Cada test
 * lee codigo fuente del fixture y comprueba que la trampa
 * esta plantada exactamente como dice el ground truth.
 */
class TrapsEcosystemTest extends TestCase
{
    private string $root;

    protected function setUp(): void
    {
        parent::setUp();
        $this->root = dirname(__DIR__, 2);
    }

    private function read(string $relative): string
    {
        $path = $this->root . '/' . $relative;
        $this->assertFileExists($path, "missing fixture file: {$relative}");

        return file_get_contents($path);
    }

    public function test_e01_facade_alias_in_config_app(): void
    {
        $config = $this->read('config/app.php');
        $facade = $this->read('app/Facades/PricingFacade.php');

        $this->assertStringContainsString("'Pricing' => App\\Facades\\PricingFacade::class", $config);
        $this->assertStringContainsString("getFacadeAccessor", $facade);
        $this->assertStringContainsString("return 'pricing.service';", $facade);
    }

    public function test_e02_eloquent_magic_in_property_model(): void
    {
        $property = $this->read('app/Models/Property.php');

        $this->assertStringContainsString("getPriceEurosAttribute", $property);
        $this->assertStringContainsString("scopeAvailable", $property);
        $this->assertStringContainsString("public function visits()", $property);
        $this->assertStringContainsString("static::observe(PropertyObserver::class)", $property);
    }

    public function test_e03_service_provider_bindings(): void
    {
        $provider = $this->read('app/Providers/InmuebleServiceProvider.php');

        $this->assertStringContainsString("VisitRepository::class, EloquentVisitRepository::class", $provider);
        $this->assertStringContainsString("singleton('pricing.service'", $provider);
    }

    public function test_e04_event_listener_auto_discovery(): void
    {
        $provider = $this->read('app/Providers/EventServiceProvider.php');

        $this->assertStringContainsString('protected $listen = [', $provider);
        $this->assertStringContainsString('VisitScheduled::class', $provider);
        $this->assertStringContainsString('SendVisitConfirmation::class', $provider);
    }

    public function test_e05_middleware_group_and_route_model_binding(): void
    {
        $kernel = $this->read('app/Http/Kernel.php');
        $routes = $this->read('routes/web.php');

        $this->assertStringContainsString("'web' => [", $kernel);
        $this->assertStringContainsString("EnsureTenant::class", $kernel);
        $this->assertStringContainsString("Route::get('/properties/{property}'", $routes);
    }

    public function test_e06_console_schedule(): void
    {
        $kernel = $this->read('app/Console/Kernel.php');

        $this->assertStringContainsString("command(ExpireContracts::class)", $kernel);
        $this->assertStringContainsString("->dailyAt('00:00')", $kernel);
        $this->assertStringContainsString("->withoutOverlapping()", $kernel);
    }
}
