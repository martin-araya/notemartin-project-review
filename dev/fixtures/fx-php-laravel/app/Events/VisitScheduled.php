<?php

namespace App\Events;

use App\Models\Property;
use Illuminate\Foundation\Events\Dispatchable;
use Illuminate\Queue\SerializesModels;

class VisitScheduled
{
    use Dispatchable;
    use SerializesModels;

    public function __construct(
        public Property $property,
        public string $visitorEmail,
    ) {
    }
}
