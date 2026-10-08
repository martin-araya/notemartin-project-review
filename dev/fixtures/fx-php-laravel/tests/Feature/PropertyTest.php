<?php

namespace Tests\Feature;

use App\Models\Property;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class PropertyTest extends TestCase
{
    use RefreshDatabase;

    public function test_create_property(): void
    {
        $response = $this->postJson('/api/properties', [
            'address' => '123 Main St',
            'price_cents' => 150000,
            'owner_email' => 'owner@example.com',
        ]);

        $response->assertStatus(201);
        $response->assertJsonPath('data.address', '123 Main St');
        $response->assertJsonPath('data.price_cents', 150000);
        $this->assertDatabaseHas('properties', ['address' => '123 Main St']);
    }

    public function test_list_properties(): void
    {
        Property::query()->create([
            'address' => 'A',
            'price_cents' => 100,
            'owner_email' => 'a@x.com',
        ]);
        Property::query()->create([
            'address' => 'B',
            'price_cents' => 200,
            'owner_email' => 'b@x.com',
        ]);

        $response = $this->getJson('/api/properties');

        $response->assertOk();
        $this->assertCount(2, $response->json('data'));
    }

    public function test_show_property_with_route_binding(): void
    {
        $property = Property::query()->create([
            'address' => 'Bound',
            'price_cents' => 99900,
            'owner_email' => 'b@x.com',
        ]);

        $response = $this->getJson("/api/properties/{$property->id}");

        $response->assertOk();
        $response->assertJsonPath('data.id', $property->id);
        $response->assertJsonPath('data.address', 'Bound');
        $response->assertJsonPath('data.price_euros', 999);
    }

    public function test_show_property_404(): void
    {
        $response = $this->getJson('/api/properties/99999');
        $response->assertStatus(404);
    }

    public function test_update_property(): void
    {
        $property = Property::query()->create([
            'address' => 'Old',
            'price_cents' => 100,
            'owner_email' => 'a@x.com',
        ]);

        $response = $this->patchJson("/api/properties/{$property->id}", [
            'status' => 'reserved',
        ]);

        $response->assertOk();
        $this->assertDatabaseHas('properties', [
            'id' => $property->id,
            'status' => 'reserved',
        ]);
    }

    public function test_create_property_validation_error(): void
    {
        $response = $this->postJson('/api/properties', [
            'address' => '',
            'price_cents' => -1,
        ]);
        $response->assertStatus(422);
    }
}
