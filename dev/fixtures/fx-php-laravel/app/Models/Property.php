<?php

namespace App\Models;

use App\Observers\PropertyObserver;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Property extends Model
{
    use HasFactory;

    protected $table = 'properties';

    protected $fillable = [
        'address',
        'price_cents',
        'status',
        'owner_email',
    ];

    protected $casts = [
        'price_cents' => 'integer',
    ];

    protected $attributes = [
        'status' => 'available',
    ];

    /**
     * E02: observer registrado via static::observe en boot.
     */
    protected static function boot()
    {
        parent::boot();
        static::observe(PropertyObserver::class);
    }

    /**
     * E02: accessor magico que convierte price_cents a euros.
     */
    public function getPriceEurosAttribute(): float
    {
        return round($this->price_cents / 100, 2);
    }

    /**
     * E02: local scope that filters available properties.
     */
    public function scopeAvailable($query)
    {
        return $query->where('status', 'available');
    }

    /**
     * E02: relacion hasMany con Visit.
     */
    public function visits(): HasMany
    {
        return $this->hasMany(Visit::class);
    }

    public function contracts(): HasMany
    {
        return $this->hasMany(Contract::class);
    }
}
