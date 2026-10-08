<?php

namespace App\Repositories;

use App\Models\Visit;

interface VisitRepository
{
    public function all(): iterable;

    public function find(int $id): ?Visit;

    public function create(array $data): Visit;
}
