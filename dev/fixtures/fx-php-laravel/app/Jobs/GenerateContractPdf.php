<?php

namespace App\Jobs;

use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Queue\SerializesModels;
use Illuminate\Support\Facades\Log;

class GenerateContractPdf implements ShouldQueue
{
    use Dispatchable;
    use InteractsWithQueue;
    use Queueable;
    use SerializesModels;

    public int $tries = 1;

    public function __construct(
        public int $contractId,
    ) {
    }

    public function handle(): void
    {
        try {
            Log::info('Generating contract PDF', [
                'contract_id' => $this->contractId,
            ]);
            // Trampa P02: si la generacion falla, el catch se traga el error
            // y el job termina "exitosamente". El contrato queda sin PDF.
            throw new \RuntimeException('PDF generation failed');
        } catch (\Throwable $e) {
            Log::error('GenerateContractPdf failed', [
                'contract_id' => $this->contractId,
                'error' => $e->getMessage(),
            ]);
        }
    }
}
