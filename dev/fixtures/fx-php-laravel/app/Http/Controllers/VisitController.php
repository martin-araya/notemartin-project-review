<?php

namespace App\Http\Controllers;

use App\Events\VisitScheduled;
use App\Facades\PricingFacade as Pricing;
use App\Jobs\SendVisitReminder;
use App\Models\Visit;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Carbon;

class VisitController extends Controller
{
    public function index(): JsonResponse
    {
        $visits = Visit::query()->orderBy('id', 'desc')->limit(50)->get();

        return response()->json(['data' => $visits]);
    }

    /**
     * E04: el handler dispara el evento VisitScheduled, que activa
     * el listener SendVisitConfirmation (auto-discovery).
     * P01: el job encolado se reintenta hasta 3 veces. El controller
     * responde 202 Accepted sin esperar al job.
     */
    public function store(Request $request): JsonResponse
    {
        $data = $request->validate([
            'property_id' => ['required', 'integer', 'exists:properties,id'],
            'scheduled_at' => ['required', 'date'],
            'visitor_email' => ['required', 'email'],
        ]);

        $property = \App\Models\Property::query()->findOrFail($data['property_id']);
        $visit = Visit::query()->create([
            'property_id' => $property->id,
            'scheduled_at' => Carbon::parse($data['scheduled_at']),
            'visitor_email' => $data['visitor_email'],
            'status' => 'scheduled',
        ]);

        // E01: facade resuelta por el contenedor.
        $priceWithTax = Pricing::calculate($property->price_cents);

        // E04: evento auto-discovered.
        event(new VisitScheduled($property, $data['visitor_email']));

        // P01: job encolado con tries=3, backoff=10.
        SendVisitReminder::dispatch($property->id, $data['visitor_email']);

        return response()->json([
            'data' => $visit,
            'price_with_tax' => $priceWithTax,
        ], 202);
    }

    public function show(Visit $visit): JsonResponse
    {
        return response()->json(['data' => $visit]);
    }

    public function update(Request $request, Visit $visit): JsonResponse
    {
        $data = $request->validate([
            'status' => ['nullable', 'string', 'in:scheduled,completed,cancelled'],
        ]);

        $visit->update(array_filter($data, fn ($v) => $v !== null));

        return response()->json(['data' => $visit]);
    }

    public function destroy(Visit $visit): JsonResponse
    {
        $visit->delete();

        return response()->json(null, 204);
    }
}
