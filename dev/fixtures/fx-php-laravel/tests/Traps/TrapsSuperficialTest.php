<?php

namespace Tests\Traps;

use Tests\TestCase;

/**
 * Tests estaticos que verifican la presencia de las 3 trampas
 * superficiales plantadas en el fixture (CC-05).
 */
class TrapsSuperficialTest extends TestCase
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

    public function test_s01_dead_legacy_provider(): void
    {
        $config = $this->read('config/app.php');
        $legacy = $this->read('app/Providers/LegacyServiceProvider.php');

        $this->assertStringContainsString("LegacyServiceProvider::class", $config);
        $this->assertStringContainsString("class LegacyServiceProvider", $legacy);
        $this->assertStringContainsString("// legacy only", $legacy);
    }

    public function test_s02_dead_helper_reference(): void
    {
        $provider = $this->read('app/Providers/InmuebleServiceProvider.php');

        $this->assertStringContainsString("App\\Pricing\\LegacyHelper", $provider);
        // La clase NO existe en app/Pricing/.
        $this->assertFileDoesNotExist($this->root . '/app/Pricing/LegacyHelper.php');
    }

    public function test_s03_dead_route(): void
    {
        $routes = $this->read('routes/web.php');

        $this->assertStringContainsString("Route::get('/legacy'", $routes);
        // Apunta a un controller que no existe.
        $this->assertStringContainsString("App\\Http\\Controllers\\LegacyController", $routes);
        $this->assertFileDoesNotExist($this->root . '/app/Http/Controllers/LegacyController.php');
    }
}
