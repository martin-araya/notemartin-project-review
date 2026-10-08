<?php

namespace App\Listeners;

use App\Events\VisitScheduled;
use App\Jobs\SendVisitReminder;
use Illuminate\Support\Facades\Log;

class SendVisitConfirmation
{
    public function handle(VisitScheduled $event): void
    {
        Log::info('Visit scheduled', [
            'property_id' => $event->property->id,
            'visitor' => $event->visitorEmail,
        ]);

        SendVisitReminder::dispatch($event->property->id, $event->visitorEmail);
    }
}
