<?php

namespace App\Jobs;

use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Queue\SerializesModels;
use Illuminate\Support\Facades\Log;

class SendVisitReminder implements ShouldQueue
{
    use Dispatchable;
    use InteractsWithQueue;
    use Queueable;
    use SerializesModels;

    /**
     * P01: tries y backoff explicitos. El controller responde 202
     * sin esperar al job, y este reintenta hasta 3 veces antes
     * de fallar silenciosamente.
     */
    public int $tries = 3;
    public int $backoff = 10;

    public function __construct(
        public int $propertyId,
        public string $visitorEmail,
    ) {
    }

    public function handle(): void
    {
        if ($this->attempts() >= $this->tries) {
            Log::warning('SendVisitReminder giving up', [
                'property_id' => $this->propertyId,
                'attempts' => $this->attempts(),
            ]);
            $this->fail(new \RuntimeException('giving up'));
            return;
        }

        Log::info('Sending visit reminder', [
            'property_id' => $this->propertyId,
            'visitor' => $this->visitorEmail,
        ]);
    }
}
