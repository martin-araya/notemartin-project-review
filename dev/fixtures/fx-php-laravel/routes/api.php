<?php

use App\Http\Controllers\ContractController;
use App\Http\Controllers\PropertyController;
use App\Http\Controllers\VisitController;
use Illuminate\Support\Facades\Route;

Route::apiResource('properties', PropertyController::class);
Route::apiResource('visits', VisitController::class);
Route::apiResource('contracts', ContractController::class);
