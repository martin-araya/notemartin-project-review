<?php

namespace App\Observers;

use App\Models\Property;
use Illuminate\Support\Facades\Log;

class PropertyObserver
{
    public function created(Property $property): void
    {
        Log::info('Property created', [
            'id' => $property->id,
            'address' => $property->address,
        ]);
    }

    public function updated(Property $property): void
    {
        Log::info('Property updated', [
            'id' => $property->id,
        ]);
    }
}
