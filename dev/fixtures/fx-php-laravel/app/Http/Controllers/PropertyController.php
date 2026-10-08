<?php

namespace App\Http\Controllers;

use App\Models\Property;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;

class PropertyController extends Controller
{
    /**
     * P05: N+1 silencioso. Carga N properties y luego itera
     * ejecutando visits() count por cada una.
     */
    public function index(): JsonResponse
    {
        $properties = Property::query()
            ->orderBy('id', 'desc')
            ->limit(50)
            ->get();

        $payload = $properties->map(function (Property $property) {
            return [
                'id' => $property->id,
                'address' => $property->address,
                'price_cents' => $property->price_cents,
                'price_euros' => $property->price_euros,
                'status' => $property->status,
                'visits_count' => $property->visits()->count(),
            ];
        });

        return response()->json(['data' => $payload]);
    }

    public function store(Request $request): JsonResponse
    {
        $data = $request->validate([
            'address' => ['required', 'string', 'max:255'],
            'price_cents' => ['required', 'integer', 'min:0'],
            'status' => ['nullable', 'string', 'in:available,reserved,sold'],
            'owner_email' => ['required', 'email'],
        ]);

        $property = Property::query()->create($data);

        return response()->json(['data' => $property], 201);
    }

    /**
     * E05: route model binding - Laravel resuelve {property} a
     * App\Models\Property::find($value) antes de ejecutar el handler.
     */
    public function show(Property $property): JsonResponse
    {
        return response()->json(['data' => [
            'id' => $property->id,
            'address' => $property->address,
            'price_cents' => $property->price_cents,
            'price_euros' => $property->price_euros,
            'status' => $property->status,
        ]]);
    }

    public function update(Request $request, Property $property): JsonResponse
    {
        $data = $request->validate([
            'address' => ['nullable', 'string', 'max:255'],
            'price_cents' => ['nullable', 'integer', 'min:0'],
            'status' => ['nullable', 'string', 'in:available,reserved,sold'],
        ]);

        $property->update(array_filter($data, fn ($v) => $v !== null));

        return response()->json(['data' => $property]);
    }

    public function destroy(Property $property): JsonResponse
    {
        $property->delete();

        return response()->json(null, 204);
    }
}
