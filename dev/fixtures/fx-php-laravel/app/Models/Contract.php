<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Contract extends Model
{
    use HasFactory;

    protected $table = 'contracts';

    protected $fillable = [
        'property_id',
        'signed_at',
        'monthly_rent_cents',
        'duration_months',
    ];

    protected $casts = [
        'signed_at' => 'datetime',
        'monthly_rent_cents' => 'integer',
        'duration_months' => 'integer',
    ];

    /**
     * E02: accessor magico que convierte monthly_rent_cents a euros.
     */
    public function getMonthlyRentEurosAttribute(): float
    {
        return round($this->monthly_rent_cents / 100, 2);
    }

    public function property(): BelongsTo
    {
        return $this->belongsTo(Property::class);
    }
}
