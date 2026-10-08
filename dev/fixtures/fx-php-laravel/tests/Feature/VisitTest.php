<?php

namespace Tests\Feature;

use App\Events\VisitScheduled;
use App\Jobs\SendVisitReminder;
use App\Models\Property;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Support\Facades\Event;
use Illuminate\Support\Facades\Queue;
use Tests\TestCase;

class VisitTest extends TestCase
{
    use RefreshDatabase;

    public function test_create_visit_dispatches_event(): void
    {
        Event::fake();
        Queue::fake();

        $property = Property::query()->create([
            'address' => 'A',
            'price_cents' => 100,
            'owner_email' => 'a@x.com',
        ]);

        $response = $this->postJson('/api/visits', [
            'property_id' => $property->id,
            'scheduled_at' => '2026-12-31 10:00:00',
            'visitor_email' => 'visitor@example.com',
        ]);

        $response->assertStatus(202);
        Event::assertDispatched(VisitScheduled::class);
        Queue::assertPushed(SendVisitReminder::class);
    }

    public function test_list_visits(): void
    {
        $response = $this->getJson('/api/visits');
        $response->assertOk();
        $this->assertIsArray($response->json('data'));
    }

    public function test_create_visit_silently_retries(): void
    {
        Queue::fake();

        $property = Property::query()->create([
            'address' => 'B',
            'price_cents' => 200,
            'owner_email' => 'b@x.com',
        ]);

        $this->postJson('/api/visits', [
            'property_id' => $property->id,
            'scheduled_at' => '2026-12-31 11:00:00',
            'visitor_email' => 'visitor2@example.com',
        ])->assertStatus(202);

        Queue::assertPushed(SendVisitReminder::class, function ($job) {
            return $job->tries === 3 && $job->backoff === 10;
        });
    }

    public function test_visit_validation_property_not_found(): void
    {
        $response = $this->postJson('/api/visits', [
            'property_id' => 99999,
            'scheduled_at' => '2026-12-31 10:00:00',
            'visitor_email' => 'visitor@example.com',
        ]);
        $response->assertStatus(422);
    }
}
