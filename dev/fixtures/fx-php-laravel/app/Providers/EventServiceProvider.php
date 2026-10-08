<?php

namespace App\Providers;

use App\Events\VisitScheduled;
use App\Listeners\SendVisitConfirmation;
use Illuminate\Foundation\Support\Providers\EventServiceProvider as ServiceProvider;

class EventServiceProvider extends ServiceProvider
{
    /**
     * E04: auto-discovery de listeners mediante el array $listen.
     * Laravel registra SendVisitConfirmation cuando se dispara
     * el evento VisitScheduled.
     *
     * @var array<class-string, array<int, class-string>>
     */
    protected $listen = [
        VisitScheduled::class => [
            SendVisitConfirmation::class,
        ],
    ];

    public function boot(): void
    {
        parent::boot();
    }
}
