<?php

namespace App\Repositories;

use App\Models\Visit;

class EloquentVisitRepository implements VisitRepository
{
    public function all(): iterable
    {
        return Visit::query()->orderBy('id', 'desc')->get();
    }

    public function find(int $id): ?Visit
    {
        return Visit::query()->find($id);
    }

    public function create(array $data): Visit
    {
        return Visit::query()->create($data);
    }
}
