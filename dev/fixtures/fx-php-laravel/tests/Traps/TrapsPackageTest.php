<?php

namespace Tests\Traps;

use Tests\TestCase;

/**
 * Tests estaticos que verifican la presencia de las 6 trampas
 * del paquete plantadas en el fixture (CC-04). Cada test
 * lee codigo fuente del fixture y comprueba que la trampa
 * del paquete esta plantada.
 */
class TrapsPackageTest extends TestCase
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

    public function test_p01_job_silent_retry(): void
    {
        $job = $this->read('app/Jobs/SendVisitReminder.php');

        $this->assertStringContainsString("public int \$tries = 3;", $job);
        $this->assertStringContainsString("public int \$backoff = 10;", $job);
        $this->assertStringContainsString("if (\$this->attempts() >= \$this->tries)", $job);
    }

    public function test_p02_job_empty_catch(): void
    {
        $job = $this->read('app/Jobs/GenerateContractPdf.php');

        $this->assertStringContainsString("public int \$tries = 1;", $job);
        $this->assertStringContainsString("catch (\\Throwable \$e)", $job);
        $this->assertStringContainsString("Log::error(", $job);
        // Verifica que NO hay un rethrow despues del catch.
        $catchPos = strpos($job, "catch (\\Throwable \$e)");
        $afterCatch = substr($job, $catchPos);
        $this->assertStringNotContainsString("throw \$e;", $afterCatch);
    }

    public function test_p03_facade_alias_typo(): void
    {
        $config = $this->read('config/app.php');
        $facade = $this->read('app/Facades/PricingFacade.php');

        // El alias 'Pricing' debe matchear el namespace de la facade.
        $this->assertStringContainsString("'Pricing' => App\\Facades\\PricingFacade::class", $config);
        // Y la facade debe declarar el accessor.
        $this->assertStringContainsString("getFacadeAccessor", $facade);
    }

    public function test_p04_queue_driver_mismatch(): void
    {
        $phpunit = $this->read('phpunit.xml');
        $queue = $this->read('config/queue.php');

        // phpunit.xml fuerza el driver a 'database' (P04).
        $this->assertStringContainsString("name=\"QUEUE_CONNECTION\" value=\"database\"", $phpunit);
        // Y config/queue.php declara tanto 'database' como 'redis' (driver latente).
        $this->assertStringContainsString("'database'", $queue);
        $this->assertStringContainsString("'redis'", $queue);
    }

    public function test_p05_eloquent_n_plus_one(): void
    {
        $controller = $this->read('app/Http/Controllers/PropertyController.php');

        $this->assertStringContainsString("Property::query()", $controller);
        $this->assertStringContainsString("->limit(50)", $controller);
        // Verifica que NO se usa withCount (N+1 silencioso).
        $this->assertStringNotContainsString("withCount(", $controller);
        $this->assertStringContainsString("\$property->visits()->count()", $controller);
    }

    public function test_p06_unused_middleware(): void
    {
        $kernel = $this->read('app/Http/Kernel.php');
        $middleware = $this->read('app/Http/Middleware/EnsureTenant.php');

        $this->assertStringContainsString("EnsureTenant::class", $kernel);
        $this->assertStringContainsString("class EnsureTenant", $middleware);
    }
}
