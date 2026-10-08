<?php

namespace Tests\Feature;

use App\Jobs\GenerateContractPdf;
use App\Models\Property;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Support\Facades\Queue;
use Tests\TestCase;

class ContractTest extends TestCase
{
    use RefreshDatabase;

    public function test_create_contract_queues_pdf_job(): void
    {
        Queue::fake();

        $property = Property::query()->create([
            'address' => 'A',
            'price_cents' => 100,
            'owner_email' => 'a@x.com',
        ]);

        $response = $this->postJson('/api/contracts', [
            'property_id' => $property->id,
            'signed_at' => '2026-01-15',
            'monthly_rent_cents' => 50000,
            'duration_months' => 12,
        ]);

        $response->assertStatus(202);
        Queue::assertPushed(GenerateContractPdf::class);
    }

    public function test_list_contracts(): void
    {
        $response = $this->getJson('/api/contracts');
        $response->assertOk();
        $this->assertIsArray($response->json('data'));
    }

    public function test_show_contract_with_accessor(): void
    {
        $property = Property::query()->create([
            'address' => 'A',
            'price_cents' => 100,
            'owner_email' => 'a@x.com',
        ]);

        $create = $this->postJson('/api/contracts', [
            'property_id' => $property->id,
            'signed_at' => '2026-01-15',
            'monthly_rent_cents' => 75000,
            'duration_months' => 6,
        ]);
        $contractId = $create->json('data.id');

        $response = $this->getJson("/api/contracts/{$contractId}");
        $response->assertOk();
        $response->assertJsonPath('data.monthly_rent_euros', 750);
    }

    public function test_create_contract_validation_error(): void
    {
        $response = $this->postJson('/api/contracts', [
            'property_id' => 1,
            'signed_at' => 'not-a-date',
            'monthly_rent_cents' => -1,
            'duration_months' => 0,
        ]);
        $response->assertStatus(422);
    }
}
