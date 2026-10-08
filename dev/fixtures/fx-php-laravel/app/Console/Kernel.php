<?php

namespace App\Console;

use App\Console\Commands\ExpireContracts;
use Illuminate\Console\Scheduling\Schedule;
use Illuminate\Foundation\Console\Kernel as ConsoleKernel;

class Kernel extends ConsoleKernel
{
    /**
     * E06: el schedule carga el comando ExpireContracts
     * diariamente a las 00:00 sin solapamiento.
     */
    protected function schedule(Schedule $schedule): void
    {
        $schedule->command(ExpireContracts::class)
            ->dailyAt('00:00')
            ->withoutOverlapping();
    }

    /**
     * Register the commands for the application.
     */
    protected function commands(): void
    {
        $this->load(__DIR__ . '/Commands');

        require base_path('routes/console.php');
    }
}
