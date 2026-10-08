<?php

namespace App\Http\Controllers;

use App\Jobs\GenerateContractPdf;
use App\Models\Contract;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Carbon;

class ContractController extends Controller
{
    public function index(): JsonResponse
    {
        $contracts = Contract::query()->orderBy('id', 'desc')->limit(50)->get();

        return response()->json(['data' => $contracts]);
    }

    /**
     * P02: el job encolado tiene un catch que se traga todos los
     * errores. El controller responde 202 sin verificar que el PDF
     * se haya generado.
     */
    public function store(Request $request): JsonResponse
    {
        $data = $request->validate([
            'property_id' => ['required', 'integer', 'exists:properties,id'],
            'signed_at' => ['required', 'date'],
            'monthly_rent_cents' => ['required', 'integer', 'min:0'],
            'duration_months' => ['required', 'integer', 'min:1'],
        ]);

        $contract = Contract::query()->create([
            'property_id' => $data['property_id'],
            'signed_at' => Carbon::parse($data['signed_at']),
            'monthly_rent_cents' => $data['monthly_rent_cents'],
            'duration_months' => $data['duration_months'],
        ]);

        GenerateContractPdf::dispatch($contract->id);

        return response()->json(['data' => $contract], 202);
    }

    public function show(Contract $contract): JsonResponse
    {
        return response()->json(['data' => [
            'id' => $contract->id,
            'property_id' => $contract->property_id,
            'signed_at' => $contract->signed_at,
            'monthly_rent_cents' => $contract->monthly_rent_cents,
            'monthly_rent_euros' => $contract->monthly_rent_euros,
            'duration_months' => $contract->duration_months,
        ]]);
    }

    public function update(Request $request, Contract $contract): JsonResponse
    {
        $data = $request->validate([
            'monthly_rent_cents' => ['nullable', 'integer', 'min:0'],
            'duration_months' => ['nullable', 'integer', 'min:1'],
        ]);

        $contract->update(array_filter($data, fn ($v) => $v !== null));

        return response()->json(['data' => $contract]);
    }

    public function destroy(Contract $contract): JsonResponse
    {
        $contract->delete();

        return response()->json(null, 204);
    }
}
