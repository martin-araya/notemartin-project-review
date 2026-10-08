<?php

namespace App\Console\Commands;

use App\Models\Contract;
use Illuminate\Console\Command;
use Illuminate\Support\Carbon;

class ExpireContracts extends Command
{
    protected $signature = 'contracts:expire';

    protected $description = 'Mark contracts as expired if signed_at + duration_months is in the past.';

    public function handle(): int
    {
        $now = Carbon::now();
        $expired = Contract::query()
            ->whereNotNull('signed_at')
            ->get()
            ->filter(function (Contract $contract) use ($now) {
                $expiration = $contract->signed_at->copy()->addMonths($contract->duration_months);
                return $expiration->isPast();
            });

        $this->info('Found ' . $expired->count() . ' expired contracts.');

        return self::SUCCESS;
    }
}
